import pandas as pd
import re
from .constaints import *
from django.conf import settings

def read_files(file, index_col=None):
    table = pd.read_csv(f"{settings.BASE_DIR}/data/{file}.csv", index_col=index_col)
    return table

def get_Ke(d, value):
    for k, v in d.items():
        if v == value:
            return k
        elif k == value:
            return v
        
def get_cart(birthday):
    u_sin = read_files("У-син", index_col="Орган")
    season_qi = read_files("season_qi", index_col="Орган")
    stvoly = read_files("stvoly", index_col="year")
    vetvi = read_files("vetvi", index_col="year")
    sloy = read_files("sloy", index_col="year")
    polugodie = read_files("Полугодия", index_col="year")

    year = int(birthday[:4])
    if birthday in polugodie.loc[year, "I полугодие"]:
        polugodie_true = "I полугодие"
        polugodie_false = "II полугодие"
    elif birthday in polugodie.loc[year, "II полугодие"]:
        polugodie_true = "II полугодие"
        polugodie_false = "I полугодие"
    else:
        polugodie_true = "II полугодие"
        polugodie_false = "I полугодие"
        year = year-1
        
    cart = pd.DataFrame(
        {"Ствол":[stvoly.loc[year, 'Орган'], get_Ke(stvoly_Ke, stvoly.loc[year, 'Орган'])],
        "Ветвь":[vetvi.loc[year, 'Орган'], get_Ke(vetvi_Ke, vetvi.loc[year, 'Орган'])],
        "Слой":[sloy.loc[year, polugodie_true], sloy.loc[year, polugodie_false]],
        "Zang Fu Xu":[" ", None]}
    )
    cart = cart.T
    cart = cart.rename(columns={
        0:"Не используем",
        1:"Используем"
    })

    home_full = {stvoly.loc[year, 'Стихия'], 
                u_sin.loc[stvoly.loc[year, 'Орган'], "Стихия"],
                u_sin.loc[vetvi.loc[year, 'Орган'], "Стихия"],
                u_sin.loc[sloy.loc[year, polugodie_true].split("+")[0], "Стихия"],
                u_sin.loc[sloy.loc[year, polugodie_true].split("+")[1], "Стихия"]}

    season_qi_full = { 
                season_qi.loc[stvoly.loc[year, 'Орган'], "Стихия"],
                season_qi.loc[vetvi.loc[year, 'Орган'], "Стихия"],
                season_qi.loc[sloy.loc[year, polugodie_true].split("+")[0], "Стихия"],
                season_qi.loc[sloy.loc[year, polugodie_true].split("+")[1], "Стихия"]}

    home_empty = list(set(stihiya.keys()) - home_full)
    season_qi_empty = list(set(stihiya.keys()) - season_qi_full)

    a = set(u_sin[u_sin["Стихия"].isin(home_empty)].index.to_list())
    b = set(season_qi[season_qi["Стихия"].isin(season_qi_empty)].index.to_list())

    print(f"Пустой дом по У-СИН: {a} \t ({home_empty})")
    print(f"Пустая сезонная ЦИ: {b} \t ({season_qi_empty})")

    cart.loc["Zang Fu Xu", "Используем"] = a & b 
    if not cart.loc["Zang Fu Xu", "Используем"]:
        cart.loc["Zang Fu Xu", "Используем"] = " "
    return cart


def get_chan(string):
    canals_p = re.sub('[:,/.;#$%^&]', ' ', string).split()
    canals = []
    for c in canals_p:
        if c.capitalize() in u_sin_pitanie.keys():
            canals.append(c.capitalize())
        else:
            print(f"""*Название канала '{c.capitalize()}' введено неверно. Попробуйте снова!*""")
            break
    return canals


def get_list_of_channels(lst, table, srez):
    a = []
    for i in lst:
        a += table[i][:srez].to_list()
        
    a = " ".join(a).replace(",", '')
    a = a.replace(",", '')
    a = re.sub("\d", "", a)   
    return a.split()