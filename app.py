import streamlit as st
import pandas as pd
from datetime import datetime
from PIL import Image
import re

@st.cache_data
def get_Ke(d, value):
    for k, v in d.items():
        if v == value:
            return k
        elif k == value:
            return v

def read_files():       
    polugodie = pd.read_csv("Полугодия.csv", index_col="year")
    u_sin = pd.read_csv("У-син.csv", index_col="Орган")
    season_qi = pd.read_csv("season_qi.csv", index_col="Орган")
    qi = pd.read_csv("qi.csv", index_col="Стихия")
    stvoly = pd.read_csv("stvoly.csv", index_col="year")
    vetvi = pd.read_csv("vetvi.csv", index_col="year")
    sloy = pd.read_csv("sloy.csv", index_col="year")
    table = pd.read_csv("table.csv", index_col='Орган')
    # tochki_pitanie = pd.read_csv("tochki_pitanie.csv", index_col='Орган').drop('Unnamed: 0', axis=1)
    # channels_Ke = pd.read_csv("channels_Ke.csv", index_col=0)
    # points = pd.read_csv("points.csv", index_col=0)
    return polugodie, u_sin, season_qi, qi, stvoly, vetvi, sloy, table

polugodie, u_sin, season_qi, qi, stvoly, vetvi, sloy, table = read_files()



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

vis_yaer = [1920, 1924, 1928, 1932, 1936, 1940, 1944, 1948, 1952, 1956, 1960, 1964, 1968, 
            1972, 1976, 1980, 1984, 1988, 1992, 1996, 2000, 2004, 2008, 2012, 2016, 2020, 
            2024, 2028, 2032, 2036, 2040, 2044, 2048, 2052]

moon_palace = dict({1: [1920, 1942, 0, 1987, 2009, 2032], 2: [0, 1943, 1965, 1988, 2010, 0], 
    3: [1921, 1944, 1966, 0, 2011, 2033], 4: [1922, 0, 1967, 1989, 2012, 2034], 
    5: [1923, 1945, 1968, 1990, 0, 2035], 6: [1924, 1946, 0, 1991, 2013, 2036], 
    7: [0, 1947, 1969, 1992, 2014, 0], 8: [1925, 1948, 1970, 0, 2015, 2037], 
    9: [1926, 0, 1971, 1993, 2016, 2038], 10: [1927, 1949, 1972, 1994, 0, 2039], 
    11: [1928, 1950, 0, 1995, 2017, 2040], 12: [0, 1951, 1973, 1996, 2018, 0], 
    13: [1929, 1952, 1974, 0, 2019, 2041], 14: [1930, 0, 1975, 1997, 2020, 2042], 
    15: [1931, 1953, 1976, 1998, 0, 2043], 16: [1932, 1954, 0, 1999, 2021, 2044], 
    17: [0, 1955, 1977, 2000, 2022, 0], 18: [1933, 1956, 1978, 0, 2023, 2045], 
    19: [1934, 0, 1979, 2001, 2024, 2046], 20: [1935, 1957, 1980, 2002, 0, 2047], 
    21: [1936, 1958, 0, 2003, 2025, 2048], 22: [0, 1959, 1981, 2004, 2026, 0], 
    23: [1937, 1960, 1982, 0, 2027, 2049], 24: [1938, 0, 1983, 2005, 2028, 2050], 
    25: [1939, 1961, 1984, 2006, 0, 2051], 26: [1940, 1962, 0, 2007, 2029, 2052], 
    27: [0, 1963, 1985, 2008, 2030, 0], 28: [1941, 1964, 1986, 0, 2031, 2053]})

sec_step = {1: 27,
            2: 2,
            3: 2,
            4: 5,
            5: 7,
            6: 10,
            7: 12,
            8: 15,
            9: 18,
            10: 20,
            11: 23,
            12: 25}


man = ["Liv1", "Liv4", "Liv3", "Liv3, Gb37", "Liv5, Gb40", "Liv2", "Liv8", 
       "Kid1", "Kid7", "Kid3", "Kid3, Bl58", "Kid4, Bl64", "Kid2", "Kid10", 
       "Lu11", "Lu8", "Lu9", "Lu9, Co6", "Lu7, Co4", "Lu10", "Lu5", 
       "Hg9, Ht9", "Hg5, Ht4", "Hg7, Ht7", "Hg7, Ht7, Si7", "Hg6, Ht5, Si4", "Hg8, Ht8", "Hg3, Ht3"]

woman = ["Gb41", "Gb44", "Gb34", "Gb37, Liv3", "Gb40, Liv5", "Gb38", "Gb43", 
       "Bl65", "Bl67", "Bl40", "Kid3, Bl58", "Kid4, Bl64", "Bl60", "Bl66", 
       "Co3", "Co1", "Co11", "Lu9, Co6", "Lu7, Co4", "Co5", "Co2", 
       "Si3", "Si1", "Si8", "Hg7, Ht7, Si7", "Ht5, Si4", "Si5", "Si2"]

######################################  Составление карты пациента  ##########################################



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
    if not cart.loc["Zang Fu Xu", "Используем"]:
        cart.loc["Zang Fu Xu", "Используем"] = None
    return cart




########################################  Создаём приложение ######################################




st.title("Карта пациента")
st.markdown(
    """Добро пожаловать в приложение для построения карты пациента с точки зрения классической китайской медицины.
    Для получения карты необходимо всего лишь ввести пол пациента и его дату рождения в соответствующие поля ниже:
"""
)

# Вводим пол пациента
sex = st.selectbox(
    "Выберете пол пациента",
    ("", "Мужчина", "Женщина"),
)

# Вводим дату рождения
date = st.text_input('Введите дату рождения пациента', '')
if date:
    try:
        birthday = str(pd.to_datetime(date, dayfirst=True)).split()[0] #input("Введите дату рождения")
        st.markdown(f'Дата рождения: {birthday}')
    except:
        st.error("Некорректная дата. Попробуйте снова")

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
    
    if df.loc["Zang Fu Xu", "Используем"] == None:
        Zang_Fu_Xu = set()
    else:
        Zang_Fu_Xu = set(df.loc["Zang Fu Xu", "Используем"])
        
        
    # Выводим DataFrame в интерфейсе
    st.dataframe(df)

    use = set([df.loc['Ствол', 'Используем'], df.loc['Ветвь', 'Используем']]) | (Zang_Fu_Xu)
        
    dnt_use = set([df.loc['Ствол', 'Не используем'], df.loc['Ветвь', 'Не используем']]) 

    neutral = set(u_sin_pitanie.keys()) ^ (set([df.loc['Ствол', 'Не используем'], 
                                            df.loc['Ветвь', 'Не используем']]) |  
                                        set([df.loc['Ствол', 'Используем'], 
                                            df.loc['Ветвь', 'Используем']]) |
                                            Zang_Fu_Xu)
                                            
    st.markdown(f"""Нейтральные каналы: {', '.join(list(neutral))}:""")
    st.markdown("""--------------------------------------------------""")

    
    
    ###################################   Выбираем метод лечения:   ##########################################


    method = st.selectbox(
    "Выберете метод лечения",
    (" ", "Питание и Ке", "Лунные дворцы", "Травма"))
    

    ###################################   Вводим канал в застое:    ###########################################
        
        
        
    if method=="Питание и Ке":    
        plus = st.text_input('Введите канал в застое', '')
        canals_p = re.sub('[:,/.;#$%^&]', ' ', plus).split()
        canals_plus = []
        for c in canals_p:
            if c.capitalize() in u_sin_pitanie.keys():
                canals_plus.append(c.capitalize())
            else:
                st.error(f"""*Название канала '{c.capitalize()}' введено неверно. Попробуйте снова!*""")
                break
                    
        if canals_plus:
            y = []
            for elem in canals_plus:
                st.markdown(f"""### Возможные каналы в недостатке при застое в {elem}:""")
            
                df_n = pd.DataFrame(
                    {"Канал":[get_Ke(stvoly_Ke, elem), 
                            get_Ke(vetvi_Ke, elem),
                            u_sin_Ke[elem],
                            home_Ke[elem]]}, 
                    index=["по стволам", "по ветвям", "по у-син", "внутри дома"]
                )
                
                st.dataframe(df_n)
                
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

            ke_channels = set(y)
            st.markdown(f"""Каналы *$Ке$* для {', '.join(list(canals_plus))} : **{', '.join(list(ke_channels))}**""")



        ###################################   Для канала в недостатке:  ########################################
        
        
        
        
        minus = st.text_input('Введите канал в недостатке', '')
        canals_p = re.sub('[:,/.;#$%^&]', ' ', minus).split()
        canals_minus = []
        for c in canals_p:
            if c.capitalize() in u_sin_pitanie.keys():
                canals_minus.append(c.capitalize())
            else:
                st.error(f"""*Название канала '{c.capitalize()}' введено неверно. Попробуйте снова!*""")
                break

        if canals_minus:
            st.markdown("""### Выбор точек питания (перечисление по мере снижения эффективности):""")
            
            df_3 = pd.DataFrame(
                columns=canals_minus,
                index=["Точка трансформации", "Точка качества дома", "Точка сезонной ци", "Точки трансформации \nсезонной ци", "Luo точка"]
            )
            
            channels = []
            for minus in canals_minus:
                channels.append(u_sin_pitanie[minus])
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
                    channels.append(c)
                df_3.loc[df_3.index[2], minus] = cell

                celll = " "
                for c in season_qi[season_qi["Стихия"] == stihiya[season_qi.loc[minus, "Стихия"]]].index.to_list():
                    celll+=(f'{c}{qi.loc[stihiya[stihiya[season_qi.loc[minus, "Стихия"]]], c]}, ')  
                df_3.loc[df_3.index[3], minus] = celll 

                df_3.loc[df_3.index[4], minus] = table.loc[home_Ke['Lu'], 'Luo']

            #Выводим DataFrame в интерфейсе
            st.dataframe(df_3)    

            st.markdown(f"""Возможные каналы для питания: **{', '.join(list(set(channels)))}**""")  
            
            
            dnt_use = set([df.loc['Ствол', 'Не используем'], df.loc['Ветвь', 'Не используем']]) | set(canals_minus) | set(canals_plus)

            if (set(channels) & dnt_use):
                st.warning(f"""!!!  Конфликт с запрещёнными каналами: **{', '.join(list(set(channels) & dnt_use))}** !!!""")
            else:
                st.markdown("""Конфликт с запрещёнными каналами: *Конфликта нет*""")

            
            one_spine = []
            for n in list((set(channels) & ke_channels)):
                if (n not in dnt_use):
                    one_spine.append(n)

            if one_spine:
                st.markdown(f"""Одновременно питание недостатка и Ке на застой: **{', '.join(one_spine)}**""")  
                st.markdown(f"""Подходящие точки в порядке снижения эффективности:""")
                points = []
                for i in df_3.columns:
                    point = ", ".join(df_3[i].to_list())
                    needed_points = re.findall(list(one_spine)[0]+"\d+", point)
                    try:
                        from PIL import Image
                        image = Image.open(f"data\{needed_points[0]}.jpg")
                        st.image(image, width=300)
                    except: 
                        print("")                   
                    st.markdown(f"""**{', '.join(list(needed_points))}**""")
            else:
                st.markdown(f"""*Одной иглой питание недостатка и Ке на застой не получится, - нет пересекающихся каналов*""")  
            
                second_spine = []
                for n in list(set(channels)):
                    if (n in use) & (n not in dnt_use):
                        second_spine.append(n)

                if second_spine:
                    # st.markdown(f"""Точки питания, рекомендованные по карте: **{', '.join(second_spine)}**""")  
                    st.markdown(f"""Подходящие точки рекомендованных каналов для питания в порядке снижения эффективности:""")
                    points = []
                    for i in df_3.columns:
                        point = ", ".join(df_3[i].to_list())
                        needed_points = re.findall(second_spine[0]+"\d+", point)
                        
                        st.markdown(f"""**{', '.join(list(needed_points))}**""")
                        
                else:
                    st.markdown(f"""*Подходящих точек не найдено :(*""") 

                for channal in canals_plus:
                    st.markdown(f"""Застой в канале {channal} корректируем техникой 'тяни-толкай', точка:""")
                    st.markdown(f"""**{table.loc[channal, 'Jing_Jin']}**""")
            
                    image_path = f"data/{table.loc[channal, 'Jing_Jin']}.jpg"
                    image = Image.open(image_path)
                    st.image(image, width=300)

                    # pp = st.text_input("Введите выбранные точки через запятую", "")
                    # if pp:
                    #     pp = pp.split(",")
                    #     for p in pp:
                    #         image_path = f"data/{p}.jpg"
                    #         image = Image.open(image_path)
                    #         st.image(image, width=300)


            st.markdown("""--------------------------------------------------""")



####################################   Лунные дворцы    ############################################



    if method=="Лунные дворцы":
        image_path = "data/Лунные дворцы.jpg"
        image = Image.open(image_path)
        st.image(image, width=600)
        
        date = st.text_input('Введите дату события', '')
        if date:
            try:
                date = str(pd.to_datetime(date, dayfirst=True)).split()[0] #input("Введите дату рождения")
                year = int(date[:4])
                month = int(date[5:7])
                day = int(date[8:])
                st.markdown(f'Дата события: **{date}**')
            except:
                st.error("*Некорректная дата. Попробуйте снова*")

            for k, v in moon_palace.items():
                if year in v:
                    first_step = k

            if (year in vis_yaer) & (pd.to_datetime(date) > pd.to_datetime(f"{year}-02-28")):
                first_step = first_step+1

            lunar_day = first_step + sec_step[month]+ day

            while lunar_day > 28:
                lunar_day+=-28
            st.markdown(f"Лунный день по дате события: **{lunar_day}**")
            st.markdown(f"Янские точки дня: \t**{woman[lunar_day-1]}**")
            st.markdown(f"Иньские точки дня: \t**{man[lunar_day-1]}**")
            
            
            if lunar_day in range(1, 15):
                lunar_day = lunar_day+14
            else:
                lunar_day = lunar_day-14
            
            
            text_ld = ""
            
            if sex == "Мужчина":
                points = man[lunar_day-1]
                st.markdown(f"##### Точки по лунным дворцам: \t{points}")
            
            else:
                points = woman[lunar_day-1]
                st.markdown(f"##### Точки по лунным дворцам: \t{points}")

            
            
            points = points.split(', ')
            for el in points:
                elem = re.match("\D*", el)[0]
                if elem in dnt_use:
                    st.warning(f"Точку **{el}** использовать нельзя!!!")

            
    pp = st.text_input("Введите выбранные точки через запятую", "")
    if pp:
        pp = pp.split(",")
        for p in pp:
            p = p.strip().capitalize()
            image_path = f"data/{p}.jpg"
            image = Image.open(image_path)
            st.image(image, width=300)

            