import streamlit as st
import pandas as pd
from datetime import datetime
import re

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
                'Sp': 'Hg',
                'St': 'Th',
                'Lu': 'Sp',
                'Co': 'St',
                'Kid': 'Lu',
                'Bl': 'Co',
                'Liv': 'Kid',
                'Gb': 'Bl'}
u_sin_Ke = {'Hg': 'Bl',
            'Ht': 'Bl',
            'St': 'Liv',
            'Lu': ['Th','Si'],
            'Co': ['Hg', 'Ht'],
            'Kid': 'St',
            'Bl': 'Sp',
            'Liv': 'Co',
            'Gb': 'Lu',
            'Th': 'Kid',
            'Si': 'Kid',
            'Sp':'Gb'}
home_Ke = {'Liv': 'Gb',
            'Gb': 'Liv',
            'Ht': ['Si', 'Th'],
            'Si': ['Ht', 'Hg'],
            'Hg': ['Si', 'Th'],
            'Th': ['Ht', 'Hg'],
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

    ################################### Вводим канал в застое:
    plus = st.text_input('Введите канал в застое', '')
    canals_p = re.sub('[:,/.;#$%^&]', ' ', plus).split()
    canals_plus = []
    for c in canals_p:
        canals_plus.append(c.capitalize())
                
    if canals_plus:
        y = []
        for elem in canals_plus:
            st.markdown(f"""### Возможные каналы в недостатке при застое в {elem}:""")
            st.markdown(f"""по стволам: {get_Ke(stvoly_Ke, elem)}""")    
            st.markdown(f"""по ветвям: {get_Ke(vetvi_Ke, elem)}""")        
            st.markdown(f"""по y-син: {u_sin_Ke[elem]}""")        
            st.markdown(f"""внутри дома: {home_Ke[elem]}""")        
            y.append(get_Ke(stvoly_Ke, elem))
            y.append(get_Ke(vetvi_Ke, elem))
            
            if type(u_sin_Ke[elem]) == type(list()):
                y.append(u_sin_Ke[elem][0])
                y.append(u_sin_Ke[elem][1])
            else:
                y.append(u_sin_Ke[elem])
                
            if type(home_Ke[elem]) == type(list()):    
                y.append(home_Ke[elem][0])
                y.append(home_Ke[elem][1])
            else:
                y.append(home_Ke[elem])
        y = [x for x in y if x is not None]

        st.markdown(f"""##### **Каналы $Ке$ для {canals_plus}**: {set(y)}""")
        
        st.markdown("""### Выбор точек питания (перечисление по мере снижения эффективности):""")
        canals = []

        df_2 = pd.DataFrame(
            columns=list(set(y)),
            index=["Точка трансформации", "Точка качества дома", "Точка сезонной ци", "Точки трансформации сезонной ци"]
        )

        for el in y:
            canals.append(u_sin_pitanie[el])
            try:
                df_2.loc[df_2.index[0], el] = f'{u_sin_pitanie[el]}{qi.loc[u_sin.loc[u_sin_Ke[el], "Стихия"].mode()[0], u_sin_pitanie[el]]}'
            except:
                df_2.loc[df_2.index[0], el] = f'{u_sin_pitanie[el]}{qi.loc[u_sin.loc[u_sin_Ke[el], "Стихия"], u_sin_pitanie[el]]}'
            
            try:
                df_2.loc[df_2.index[1], el] = f'{u_sin_pitanie[el]}{qi.loc[u_sin.loc[u_sin_pitanie[el], "Стихия"].mode()[0], u_sin_pitanie[el]]}'
            except:
                df_2.loc[df_2.index[1], el] = f'{u_sin_pitanie[el]}{qi.loc[u_sin.loc[u_sin_pitanie[el], "Стихия"], u_sin_pitanie[el]]}'

            celll = " "
            cell = " "
            for c in season_qi[season_qi["Стихия"] == stihiya[season_qi.loc[el, "Стихия"]]].index.to_list():
                cell+=(f'{c}{qi.loc[stihiya[season_qi.loc[el, "Стихия"]], c]}, ')
                celll+=(f'{c}{qi.loc[stihiya[stihiya[season_qi.loc[el, "Стихия"]]], c]}, ')  
                canals.append(c)
            df_2.loc[df_2.index[2], el] = cell
            df_2.loc[df_2.index[3], el] = celll 

        #Выводим DataFrame в интерфейсе
        st.dataframe(df_2)    
        
        st.markdown(f"""Возможные каналы для питания: {canals}""")  
        st.markdown(f"""Из них конфликтуют с запрещёнными: {set(canals) & set(df["Не используем"])}""")
        st.markdown(f"""Предпочтительно использовать: {set(canals) & df.loc["Zang Fu Xu", "Используем"]}""")  


    ###################### Для канала в недостатке:
    minus = st.text_input('Введите канал в недостатке', '')
    canals_p = re.sub('[:,/.;#$%^&]', ' ', minus).split()
    canals_minus = []
    for c in canals_p:
        canals_minus.append(c.capitalize())

    if canals_minus:
        st.markdown("""### Выбор точек питания (перечисление по мере снижения эффективности):""")
        
        df_3 = pd.DataFrame(
            columns=canals_minus,
            index=["Точка трансформации", "Точка качества дома", "Точка сезонной ци", "Точки трансформации сезонной ци"]
        )
        
        canals = []
        for minus in canals_minus:
            canals.append(u_sin_pitanie[minus])
            try:
                df_3.loc[df_3.index[0], minus] = f'{u_sin_pitanie[minus]}{qi.loc[u_sin.loc[u_sin_Ke[minus], "Стихия"].mode()[0], u_sin_pitanie[minus]]}'
            except:
                df_3.loc[df_3.index[0], minus] = f'{u_sin_pitanie[minus]}{qi.loc[u_sin.loc[u_sin_Ke[minus], "Стихия"], u_sin_pitanie[minus]]}'
            
            try:
                df_3.loc[df_3.index[1], minus] = f'{u_sin_pitanie[minus]}{qi.loc[u_sin.loc[u_sin_pitanie[minus], "Стихия"].mode()[0], u_sin_pitanie[minus]]}'
            except:
                df_3.loc[df_3.index[1], minus] = f'{u_sin_pitanie[minus]}{qi.loc[u_sin.loc[u_sin_pitanie[minus], "Стихия"], u_sin_pitanie[minus]]}'

            
            cell = " "
            for c in season_qi[season_qi["Стихия"] == stihiya[season_qi.loc[minus, "Стихия"]]].index.to_list():
                cell+=(f'{c}{qi.loc[stihiya[season_qi.loc[minus, "Стихия"]], c]}, ')
                canals.append(c)
            df_3.loc[df_3.index[2], minus] = cell

            celll = " "
            for c in season_qi[season_qi["Стихия"] == stihiya[season_qi.loc[minus, "Стихия"]]].index.to_list():
                celll+=(f'{c}{qi.loc[stihiya[stihiya[season_qi.loc[minus, "Стихия"]]], c]}, ')  
            df_3.loc[df_3.index[3], minus] = celll 

        #Выводим DataFrame в интерфейсе
        st.dataframe(df_3)    

        st.markdown(f"""##### **Возможные каналы для питания:** {canals}""")  
        
        st.markdown(f"""Из них конфликтуют с запрещёнными: {set(canals) & set(df["Не используем"])}""")
        st.markdown(f"""Предпочтительно использовать: {set(df.loc[['Ствол', 'Ветвь', 'Слой'], "Используем"].to_list()) | (df.loc['Zang Fu Xu', 'Используем'])}""")  

        
        st.markdown("""--------------------------------------------------""")
        
        use = set([df.loc['Ствол', 'Используем'], df.loc['Ветвь', 'Используем'], df.loc['Слой', 'Используем']]) | (df.loc['Zang Fu Xu', 'Используем'])
        
        dnt_use = set([df.loc['Ствол', 'Не используем'], df.loc['Ветвь', 'Не используем'], df.loc['Слой', 'Не используем']]) 
        
        joined = (set(canals) | set(y)) - dnt_use

        # st.markdown(f"""Каналы питания и $Ке$ без конфликтов: {(set(canals) | set(y)) - dnt_use}""")

        if (df.loc['Слой', 'Используем'].split('+')[0] in joined) & (df.loc['Слой', 'Используем'].split('+')[1] in joined):
            st.markdown(f"""##### **Можем использовать слой:** {df.loc['Слой', 'Используем']}""")
            tochki = []
            ttt = []
            for i in df_2.index:
                ttt.append(list(set(tochki)))
                tochki = []
                for c in df_2.columns:
                    tochki.extend(re.findall(f"({df.loc['Слой', 'Используем'].split('+')[0]}\d*|{df.loc['Слой', 'Используем'].split('+')[1]}\d*)", df_2.loc[i, c]))
                st.markdown(f"""{i}: {set(tochki)}""")

            ttt = [x for x in ttt if len(x) > 0]

            st.markdown(f"""#### **Наиболее эффективная пара точек: {ttt[0]}**""")
        else:
            ttt = []
            for i in df_2.index:
                tt = (re.sub(f'({df.loc[df.index[0], "Не используем"]}\d*|{df.loc[df.index[1], "Не используем"]}\d*)', '', df_3.loc[i, df_3.columns[0]]))
                tt = tt.replace(',', '').strip()
                ttt.append(tt)
                print(f"""{i}: {tt}""")

            ttt = [x for x in ttt if len(x) > 0]
            
            if ttt:
                st.markdown(f"""#### **Наиболее эффективная точка для питания: {ttt[0]}**""")
            else:
                st.markdown(f"""#### **Подходящих точек не найдено!**""")