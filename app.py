import streamlit as st
import pandas as pd
from datetime import datetime

@st.cache_data
def get_Ke(d, value):
    for k, v in d.items():
        if v == value:
            return k
        elif k == value:
            return v

def read_files():       
    polugodie = pd.read_excel("Полугодия.xlsx", index_col="year")
    u_sin = pd.read_excel("У-син.xlsx", index_col="Орган")
    season_qi = pd.read_excel("season_qi.xlsx", index_col="Орган")
    qi = pd.read_excel("qi.xlsx", index_col="Стихия")
    stvoly = pd.read_excel("stvoly.xlsx", index_col="year")
    vetvi = pd.read_excel("vetvi.xlsx", index_col="year")
    sloy = pd.read_excel("sloy.xlsx", index_col="year")
    return polugodie, u_sin, season_qi, qi, stvoly, vetvi, sloy

polugodie, u_sin, season_qi, qi, stvoly, vetvi, sloy = read_files()



stihiya = {"вода":"металл", "дерево":"вода", "огонь":"дерево", "земля":"огонь", "металл":"земля"}
stvoly_Ke = {"Lu":"Si", "Co":"Liv", "Sp":"Gb", "St":"Kid", "Ht":"Bl"}
vetvi_Ke = {"Lu":"Bl", "Co":"Kid", "Sp":"Th", "St":"Hg", "Ht":"Gb", "Si":"Liv"}        
u_sin_pitanie = {'Ht': 'Liv',
                'Si': 'Gb',
                'Hg': 'Liv',
                'Th': 'Gb',
                'Sp': ['Ht', 'Hg'],
                'St': ['Si', 'Th'],
                'Lu': 'Sp',
                'Co': 'St',
                'Kid': 'Lu',
                'Bl': 'Co',
                'Liv': 'Kid',
                'Gb': 'Bl'}
u_sin_Ke = {'Hg': 'Gb',
            'Th': 'Liv',
            'Sp': 'Si',
            'St': 'Ht',
            'Lu': ['Si', 'Th'],
            'Co': ['Ht', 'Hg'],
            'Kid': 'St',
            'Bl': 'Sp',
            'Liv': 'Co',
            'Gb': 'Lu',
            'Ht': 'Bl',
            'Si': 'Kid'}
home_Ke = {'Liv': 'Gb',
            'Gb': 'Liv',
            'Ht': 'Si',
            'Si': 'Ht',
            'Hg': 'Th',
            'Th': 'Hg',
            'Sp': 'St',
            'St': 'Sp',
            'Lu': 'Co',
            'Co': 'Lu',
            'Kid': 'Bl',
            'Bl': 'Kid'}


# Составление карты пациента
def get_cart(year):
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
    return cart

########################################  Создаём приложение ######################################

st.title("Карта пациента")
st.markdown(
    """Добро пожаловать в приложение для построения карты пациента с точки зрения классической китайской медицины.
    Для получения карты необходимо всего лишь ввести дату рождения в поле ниже:
"""
)
# Вводим дату рождения
date = st.text_input('Введите дату рождения пациента', '')
if date:
    try:
        birthday = str(pd.to_datetime(date, dayfirst=True)).split()[0] #input("Введите дату рождения")
        st.markdown(f'Дата рождения: {birthday}')
    except:
        st.markdown("Некорректная дата. Попробуйте снова")

    # Получаем год и полугодие по китайскому календарю
    year = int(birthday[:4])
    if birthday in polugodie.loc[year, "I полугодие"]:
        st.markdown(f"I полугодие {year} года")
        polugodie_true = "I полугодие"
        polugodie_false = "II полугодие"
    elif birthday in polugodie.loc[year, "II полугодие"]:
        st.markdown(f"II полугодие {year} года")
        polugodie_true = "II полугодие"
        polugodie_false = "I полугодие"
    else:
        st.markdown(f"II полугодие {year-1} года")
        polugodie_true = "II полугодие"
        polugodie_false = "I полугодие"
        year = year-1

    df = get_cart(year=year)
    
    #Выводим DataFrame в интерфейсе
    st.dataframe(df)

    # Вводим канал в застое:
    plus = st.text_input('Введите канал в застое', '')
    if plus:
        st.markdown("""Возможные каналы в недостатке:""")
        st.markdown(f"""по стволам: {get_Ke(stvoly_Ke, plus)}""")    
        st.markdown(f"""по ветвям: {get_Ke(vetvi_Ke, plus)}""")        
        st.markdown(f"""по y-син: {u_sin_Ke[plus]}""")        
        st.markdown(f"""внутри дома: {home_Ke[plus]}""")        
        
        y = [get_Ke(stvoly_Ke, plus), get_Ke(vetvi_Ke, plus), u_sin_Ke[plus], home_Ke[plus]]
    

    # Для канала в недостатке:
    minus = st.text_input('Или введите канал в недостатке', '')
    if minus:
        st.markdown("""Выбор точек питания по У-СИН по снижению эффективности:""")
        st.markdown(f"""Точка трансформации:""")
        try:
            st.markdown(f'{u_sin_pitanie[minus]}{qi.loc[u_sin.loc[u_sin_Ke[minus], "Стихия"].mode()[0], u_sin_pitanie[minus]]}')
        except:
            st.markdown(f'{u_sin_pitanie[minus]}{qi.loc[u_sin.loc[u_sin_Ke[minus], "Стихия"], u_sin_pitanie[minus]]}')
        
        st.markdown(f"""Точка качества дома:""")
        try:
            st.markdown(f'{u_sin_pitanie[minus]}{qi.loc[u_sin.loc[u_sin_pitanie[minus], "Стихия"].mode()[0], u_sin_pitanie[minus]]}')
        except:
            st.markdown(f'{u_sin_pitanie[minus]}{qi.loc[u_sin.loc[u_sin_pitanie[minus], "Стихия"], u_sin_pitanie[minus]]}')
        
        st.markdown(f"""Точка сезонной ци:""")
        for c in season_qi[season_qi["Стихия"] == stihiya[season_qi.loc[minus, "Стихия"]]].index.to_list():
            st.markdown(f'{c}{qi.loc[stihiya[season_qi.loc[minus, "Стихия"]], c]}')
        
        st.markdown(f"""Точки трансформации сезонной ци:""")
        for c in season_qi[season_qi["Стихия"] == stihiya[season_qi.loc[minus, "Стихия"]]].index.to_list():
            st.markdown(f'{c}{qi.loc[stihiya[stihiya[season_qi.loc[minus, "Стихия"]]], c]}')