"""
Podmienky pre tvorbu siete sú:
- geografická dostupnosť ústavnej starostlivosti,
- počet poistencov v spádovom území nemocnice,
- minimálny počet lôžok.

Pre vyhodnotenie podmienok geografickej dostupnosti a počtu poistencov v spádovom území sa prihliada iba na všeobecné nemocnice úrovne II. a vyššej úrovne. Partnerské nemocnice, špecializované nemocnice a nemocnice I. úrovne sa nezohľadňujú, pričom sa prihliada len na poistencov s pobytom na území Slovenskej republiky.
"""

import numpy as np
from OSN_common.nacitanie_dat import (
    nacitaj_zoznam_nemocnic,
    nacitaj_zoznam_obci,
    nacitaj_zoznam_poistencov,
)

import pandas as pd

NEMOCNICE = nacitaj_zoznam_nemocnic()
OBCE = nacitaj_zoznam_obci()


def _nacitaj_dojazdovu_maticu():
    """Načítaj dojazdovú maticu v správnom formáte.

    Na analýzu dojazdových časov je použitá matica dojazdov medzi sídlami, pričom sú vypočítané dojazdové vzdialenosti medzi všetkými 2926 ZUJ kódmi sídiel poistencov a 64 vybranými sídlami nemocníc.

    Oblasť Bratislavy sa pre potreby výpočtu dojazdu považuje za 1 sídlo. Rovnako to platí aj pre Košice.
    """

    dojazdova_matica = pd.read_csv("dojazdova_matica/dojazdova_matica.csv", index_col=0)
    dojazdova_matica.index = dojazdova_matica.index.astype("str")
    return dojazdova_matica


DOJAZDOVA_MATICA = _nacitaj_dojazdovu_maticu()


def priprav_poistencov(rok):
    """
    Príprava dát o poistencoch, aby bolo možné vykonať analýzu počtu poistencov v spádových územiach jednotlivých nemocníc.

    Spojenie dát od poisťovní a základné predspracovanie dát sa deje v preprocessingu.

    Vráti počet poistencov, ktoré majú platný slovenský ZUJ kód bydliska podľa jednotlivých obcí.
    """
    _poistenci_all = nacitaj_zoznam_poistencov(rok)

    print(f"Celkový počet poistencov: {len(_poistenci_all):,}")

    # Vyber iba poistencov, ktorí majú platný slovenský ZUJ kód bydliska
    poistenci = _poistenci_all[_poistenci_all["kod_pobytu"].isin(OBCE["ZUJ"])]

    print(f"Počet poistencov s pobytom na Slovensku: {len(poistenci):,}")

    poistenci_na_ZUJ = poistenci.groupby("kod_pobytu")["id_poistenca"].count()
    poistenci_na_okres = (
        poistenci.merge(OBCE[["ZUJ", "Okres"]], left_on="kod_pobytu", right_on="ZUJ")
        .groupby("Okres")["id_poistenca"]
        .count()
    )

    return poistenci_na_ZUJ.reindex(DOJAZDOVA_MATICA.index), poistenci_na_okres


def priprav_urovne_siete(siet_nemocnic):
    siet_vseobecnych_nemocnic = siet_nemocnic[
        (siet_nemocnic.index.get_level_values("typ_nemocnice") == "Všeobecná nemocnica")
        & (siet_nemocnic.index.get_level_values("uroven_nemocnice") > 1)
    ]
    vseobecne_nemocnice = (
        NEMOCNICE.set_index("pzs_6")
        .loc[siet_vseobecnych_nemocnic.index.get_level_values("pzs_6")]
        .reset_index()
        .set_index("ZUJ")
    )
    vseobecne_nemocnice["uroven_nemocnice"] = (
        siet_vseobecnych_nemocnic.index.get_level_values("uroven_nemocnice")
    )

    return {
        uroven: vseobecne_nemocnice[vseobecne_nemocnice["uroven_nemocnice"] >= uroven]
        for uroven in range(2, 6)
    }


def priprav_matice(urovne_siete, poistenci_na_ZUJ):
    najblizsie_ZUJ = {
        uroven: DOJAZDOVA_MATICA.filter(
            urovne_siete[uroven].index, axis="columns"
        ).idxmin(axis=1)
        for uroven in range(2, 6)
    }
    matice_spadov = {
        uroven: pd.DataFrame(
            0, index=DOJAZDOVA_MATICA.index, columns=urovne_siete[uroven].index
        )
        for uroven in range(2, 6)
    }
    for uroven in range(2, 6):
        for obec, nemocnica in najblizsie_ZUJ[uroven].items():
            matice_spadov[uroven].loc[obec, [nemocnica]] = 1

    # Výpočet počtu poistencov v spádových oblastiach
    matice_poistencov = {}
    for uroven in range(2, 6):
        matice_poistencov[uroven] = pd.concat(
            [poistenci_na_ZUJ] * len(urovne_siete[uroven]), axis=1
        )
        matice_poistencov[uroven].columns = urovne_siete[uroven].index

    for uroven in range(2, 6):
        urovne_siete[uroven]["pocet_v_ZUJ"] = (
            urovne_siete[uroven]
            .index.value_counts()
            .reindex(urovne_siete[uroven].index)
        )
        urovne_siete[uroven]["spad_pocet_poistencov"] = (
            matice_poistencov[uroven] * matice_spadov[uroven]
        ).sum() / urovne_siete[uroven]["pocet_v_ZUJ"]

    # Výpočet priemerného času dojazdu
    matice_dojazdov = {
        uroven: pd.DataFrame(
            index=DOJAZDOVA_MATICA.index, columns=urovne_siete[uroven].index
        )
        for uroven in range(2, 6)
    }
    for uroven in range(2, 6):
        for column in matice_dojazdov[uroven].columns:
            matice_dojazdov[uroven][column] = DOJAZDOVA_MATICA[column]

    for uroven in range(2, 6):
        urovne_siete[uroven]["priemerny_cas_dojazdu"] = (
            (matice_dojazdov[uroven] * matice_spadov[uroven]).replace(0, pd.NA).mean()
        )

    return matice_spadov, matice_poistencov, matice_dojazdov


LIMITY_DOSTUPNOSTI = {5: [300, 350], 4: [90, 120], 3: [60, 90], 2: [30, 45]}
PERCENTO_SPODNY_LIMIT = 0.9
PERCENTO_HORNY_LIMIT = 0.15


def vyhodnot_geograficku_dostupnost(urovne_siete, poistenci_na_ZUJ):
    matice_spadov, matice_poistencov, matice_dojazdov = priprav_matice(
        urovne_siete, poistenci_na_ZUJ
    )

    splnane_podmienky_horny_limit = 0
    splnane_podmienky_spodny_limit = 0

    celkovy_pocet_poistencov = matice_poistencov[5].sum().sum()

    for uroven in range(2, 6):
        plnenie_spodny_limit = (
            (matice_dojazdov[uroven] <= LIMITY_DOSTUPNOSTI[uroven][0]).astype("Int8")
            * matice_spadov[uroven]
            * matice_poistencov[uroven]
        ).sum().sum() / celkovy_pocet_poistencov
        plnenie_horny_limit = (
            (matice_dojazdov[uroven] > LIMITY_DOSTUPNOSTI[uroven][1]).astype("Int8")
            * matice_spadov[uroven]
            * matice_poistencov[uroven]
        ).sum().sum() / celkovy_pocet_poistencov
        print(
            f"Sieť na úrovni {uroven} {'SPĹŇA' if plnenie_spodny_limit >= PERCENTO_SPODNY_LIMIT else 'NESPĹŇA'} podmienku spodného limitu geografickej dostupnosti"
        )
        print(
            f"Sieť na úrovni {uroven} {'SPĹŇA' if plnenie_horny_limit <= PERCENTO_HORNY_LIMIT else 'NESPĹŇA'} podmienku horného limitu geografickej dostupnosti"
        )
        splnane_podmienky_spodny_limit += plnenie_spodny_limit >= PERCENTO_SPODNY_LIMIT
        splnane_podmienky_horny_limit += plnenie_horny_limit <= PERCENTO_HORNY_LIMIT

    celkove_plnenie_geografickej_dostupnosti = (
        splnane_podmienky_spodny_limit + splnane_podmienky_horny_limit
    ) / 8

    print(
        f"Celkové hodnotenie plnenia podmienok geografickej dostupnosti siete: {celkove_plnenie_geografickej_dostupnosti}"
    )

    # Informatívne plnenie limitov na nemocnicu
    for uroven in range(2, 6):
        urovne_siete[uroven]["percento_pod_spodny_limit"] = (
            (matice_dojazdov[uroven] <= LIMITY_DOSTUPNOSTI[uroven][0]).astype("Int8")
            * matice_spadov[uroven]
            * matice_poistencov[uroven]
        ).sum() / (
            urovne_siete[uroven]["spad_pocet_poistencov"]
            * urovne_siete[uroven]["pocet_v_ZUJ"]
        )
        urovne_siete[uroven]["percento_nad_horny_limit"] = (
            (matice_dojazdov[uroven] > LIMITY_DOSTUPNOSTI[uroven][1]).astype("Int8")
            * matice_spadov[uroven]
            * matice_poistencov[uroven]
        ).sum() / (
            urovne_siete[uroven]["spad_pocet_poistencov"]
            * urovne_siete[uroven]["pocet_v_ZUJ"]
        )

    return celkove_plnenie_geografickej_dostupnosti


LIMITY_SPADU = {
    5: [5000000, np.inf],
    4: [1400000, 2000000],
    3: [450000, 900000],
    2: [100000, 220000],
}


def priemerny_dojazd_na_okres(
    matica_spadov, matica_poistencov, matica_dojazdov, poistenci_na_okres
):
    matica_poistencov_na_okres = (
        matica_poistencov.merge(OBCE[["ZUJ", "Okres"]], left_index=True, right_on="ZUJ")
        .merge(poistenci_na_okres, left_on="Okres", right_index=True)
        .set_index("ZUJ")
    )
    matica_poistencov_na_okres = matica_poistencov_na_okres.iloc[:, :-2].div(
        matica_poistencov_na_okres["id_poistenca"], axis=0
    )
    return (
        (matica_dojazdov * matica_spadov * matica_poistencov_na_okres)
        .apply("max", axis=1)
        .to_frame()
        .merge(OBCE[["ZUJ", "Okres"]], left_index=True, right_on="ZUJ")
        .set_index("ZUJ")
        .groupby("Okres")
        .apply("sum")
        .rename({0: "dojazd"}, axis=1)
    )


def vyhodnot_spady(siet_nemocnic, urovne_siete, poistenci_na_ZUJ, poistenci_na_okres):

    matice_spadov, matice_poistencov, matice_dojazdov = priprav_matice(
        urovne_siete, poistenci_na_ZUJ
    )

    celkove_hodnotenie_spadu = 0

    for uroven in range(2, 6):
        urovne_siete[uroven]["splna_spad"] = (
            LIMITY_SPADU[uroven][0] <= urovne_siete[uroven]["spad_pocet_poistencov"]
        ) & (urovne_siete[uroven]["spad_pocet_poistencov"] <= LIMITY_SPADU[uroven][1])
        if uroven == 2:
            # každá nemocnica III. úrovne alebo vyššej úrovne spĺňa podmienku počtu poistencov na II. úrovni aj pokiaľ je počet poistencov v jej spádovom území na II. úrovni vyšší, ako horný limit definovaný v zákone pre II. úroveň.
            urovne_siete[uroven].loc[
                (urovne_siete[uroven]["uroven_nemocnice"] >= 3)
                & (
                    urovne_siete[uroven]["spad_pocet_poistencov"]
                    > LIMITY_SPADU[uroven][1]
                ),
                "splna_spad",
            ] = True
            # každá nemocnica, ktorej počet poistencov v jej spádovom území na II. úrovni je menej ako 100 000 poistencov ale najmenej 75 000 poistencov, spĺňa podmienku počtu poistencov na II. úrovni, pokiaľ existuje alternatívna kandidátska sieť nemocníc neobsahujúca danú nemocnicu a zároveň, v ktorej existuje okres, pre ktorý by čas dojazdu presiahol 35 minút, pričom vo vyhodnocovanej kandidátskej sieti je čas dojazdu v tomto okrese pod 35 minút.
            povodne_dojazdy = priemerny_dojazd_na_okres(
                matice_poistencov[2],
                matice_dojazdov[2],
                matice_spadov[2],
                poistenci_na_okres,
            )
            kandidatske_nemocnice = urovne_siete[2][
                (urovne_siete[2]["spad_pocet_poistencov"] < 100000)
                & (urovne_siete[2]["spad_pocet_poistencov"] >= 75000)
            ]
            for _, kandidatska_nemocnica in kandidatske_nemocnice.iterrows():
                alternativna_siet = siet_nemocnic.drop(
                    kandidatska_nemocnica["pzs_6"], level=0
                )
                alternativne_dojazdy = priemerny_dojazd_na_okres(
                    *[
                        m[2]
                        for m in priprav_matice(
                            priprav_urovne_siete(alternativna_siet), poistenci_na_ZUJ
                        )
                    ],
                    poistenci_na_okres,
                )
                porovnanie = povodne_dojazdy.merge(
                    alternativne_dojazdy,
                    left_index=True,
                    right_index=True,
                    suffixes=["_povodny", "_alternativny"],
                )
                zlepsene_okresy = porovnanie[
                    (porovnanie["dojazd_alternativny"] > 35)
                    & (porovnanie["dojazd_povodny"] < 35)
                ]
                if len(zlepsene_okresy):
                    print(
                        f'Nemocnica {kandidatska_nemocnica["nazov_nemocnice"]} splna spad podla podmienky 1 pre okresy {", ".join(zlepsene_okresy.index)}'
                    )
                    urovne_siete[2].loc[
                        urovne_siete[2]["pzs_6"] == kandidatska_nemocnica["pzs_6"],
                        "splna_spad",
                    ] = True
            # každá nemocnica, ktorej počet poistencov v jej spádovom území na II. úrovni je menej ako 75 000 poistencov, spĺňa podmienku počtu poistencov na II. úrovni, pokiaľ existuje alternatívna kandidátska sieť nemocníc neobsahujúca danú nemocnicu a zároveň, v ktorej existuje okres, pre ktorý by čas dojazdu presiahol 45 minút, pričom vo vyhodnocovanej kandidátskej sieti je čas dojazdu v tomto okrese pod 45 minút.
            kandidatske_nemocnice = urovne_siete[2][
                urovne_siete[2]["spad_pocet_poistencov"] < 75000
            ]
            for _, kandidatska_nemocnica in kandidatske_nemocnice.iterrows():
                alternativna_siet = siet_nemocnic.drop(
                    kandidatska_nemocnica["pzs_6"], level=0
                )
                alternativne_dojazdy = priemerny_dojazd_na_okres(
                    *[
                        m[2]
                        for m in priprav_matice(
                            priprav_urovne_siete(alternativna_siet), poistenci_na_ZUJ
                        )
                    ],
                    poistenci_na_okres,
                )
                porovnanie = povodne_dojazdy.merge(
                    alternativne_dojazdy,
                    left_index=True,
                    right_index=True,
                    suffixes=["_povodny", "_alternativny"],
                )
                zlepsene_okresy = porovnanie[
                    (porovnanie["dojazd_alternativny"] > 45)
                    & (porovnanie["dojazd_povodny"] < 45)
                ]
                if len(zlepsene_okresy):
                    print(
                        f'Nemocnica {kandidatska_nemocnica["nazov_nemocnice"]} spĺňa spád podľa podmienky 2 pre okresy {", ".join(zlepsene_okresy.index)}'
                    )
                    urovne_siete[2].loc[
                        urovne_siete[2]["pzs_6"] == kandidatska_nemocnica["pzs_6"],
                        "splna_spad",
                    ] = True

        podiel_nemocnic = urovne_siete[uroven]["splna_spad"].sum() / len(
            urovne_siete[uroven]
        )
        print(f"Sieť spĺňa podmienky spádu na úrovni {uroven} na {podiel_nemocnic:.2%}")
        celkove_hodnotenie_spadu += podiel_nemocnic

    celkove_hodnotenie_spadu /= 4
    print(
        f"Celkové hodnotenie plnenia počtu poistencov v spádovom území: {celkove_hodnotenie_spadu:.4}"
    )
    return celkove_hodnotenie_spadu


# Zabezpečenie minimálneho počtu lôžok

MIN_POCTY_LOZOK_TYP = pd.read_excel(
    "lozka/minimálny počet lôžok.xlsx", sheet_name="Typ"
)
# minimalne_pocty_lozok_oddelenie = pd.read_excel('minimálny počet lôžok.xlsx', sheet_name='Oddelenie', index_col=1)


def vyhodnot_lozka(rok):
    pocty_lozok = pd.read_excel(
        f"lozka/pocty_lozok_{rok}.xlsx",
        usecols="V,Y,Z,AK",
        dtype={"CISR_ODB": "str"},
    )
    pocty_lozok["pzs_6"] = pocty_lozok["IDENTIFZAR"].str[:6]
    pocty_lozok = pocty_lozok.merge(NEMOCNICE[["pzs_6", "kraj"]], how="left")

    plnenie_lozok_SR = pocty_lozok["POS_SLED"].sum() >= MIN_POCTY_LOZOK_TYP["SR"].sum()
    print(
        f"Sieť {'SPĹŇA' if plnenie_lozok_SR else 'NESPĹŇA'} podmienky plnenia minimálneho počtu lôžok pre SR."
    )

    celkove_plnenie_lozok = 0

    for kraj in pocty_lozok["kraj"].dropna().unique():
        plnenie_lozok = (
            pocty_lozok.loc[pocty_lozok["kraj"] == kraj, "POS_SLED"].sum()
            >= MIN_POCTY_LOZOK_TYP[kraj].sum()
        )
        print(
            f"Sieť {'SPĹŇA' if plnenie_lozok else 'NESPĹŇA'} podmienky plnenia minimálneho počtu lôžok pre {kraj} kraj."
        )
        celkove_plnenie_lozok += plnenie_lozok

    celkove_plnenie_lozok /= 8
    celkove_plnenie_lozok = 0.5 * plnenie_lozok_SR + 0.5 * celkove_plnenie_lozok
    print(
        f"Celkové hodnotenie plnenia minimálneho počtu lôžok: {celkove_plnenie_lozok}"
    )

    return celkove_plnenie_lozok


# Celkové hodnotenie plnenia podmienok tvorby siete


def vyhodnot_podmienky_tvorby_siete(siet_nemocnic, rok):
    poistenci_na_ZUJ, poistenci_na_okres = priprav_poistencov(rok)
    urovne_siete = priprav_urovne_siete(siet_nemocnic)
    hodnotenie_tvorby_siete = (
        vyhodnot_geograficku_dostupnost(urovne_siete, poistenci_na_ZUJ)
        + vyhodnot_spady(
            siet_nemocnic, urovne_siete, poistenci_na_ZUJ, poistenci_na_okres
        )
        + vyhodnot_lozka(rok)
    ) / 3
    print(f"Celkové hodnotenie podmienok tvorby siete: {hodnotenie_tvorby_siete:.4}")
    return urovne_siete
