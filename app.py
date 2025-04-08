import streamlit as st
import pandas as pd
from datetime import datetime
from PIL import Image
import re
import matplotlib.pyplot as plt
import numpy as np
import csv

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
    # qi = pd.read_csv("qi.csv", index_col="Стихия")
    stvoly = pd.read_csv("stvoly.csv", index_col="year")
    vetvi = pd.read_csv("vetvi.csv", index_col="year")
    sloy = pd.read_csv("sloy.csv", index_col="year")
    table = pd.read_csv("table.csv", index_col='Орган')
    points = pd.read_csv("points.csv", index_col=0)
    pitanie = pd.read_csv("pitanie.csv", index_col='Unnamed: 0')
    ke = pd.read_csv("ke.csv", index_col='Unnamed: 0')
    return polugodie, u_sin, season_qi, stvoly, vetvi, sloy, table, points, pitanie, ke

polugodie, u_sin, season_qi, stvoly, vetvi, sloy, table, points, pitanie, ke = read_files()




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

technika = {"gui":"Используется техника выведения:\
                \nПарные иглы ставятся билатерально в дистперсии под углом 90\*\
                \nПоследовательность постановки - по полу: с сильной стороны на слабую. \
                \nОдиночные иглы ставятся в дисперсии под углом 90\*",
            "xue":"Иглы ставятся билатерально в технике <<тяни-толкай>>:\
                \nПод углом 90\* на здоровой стороне в тонизации, на больной - в дисперсии.\
                \nСнимаются в обратном порядке. \
                \nПри двусторонней или срединной травме иглы ставятся по полу:\
                \nна сильной стороне в тонизации, на слабой - в дисперсии.",
            "pit":"Иглы ставятся в тонизации, по полу, на слабой стороне:\
                \nдля мужчин - слева, для женщин - справа",
            "JJ":"Иглы ставятся билатерально под углом 45\* на здоровой стороне в тонизации, на больной - в дисперсии.\
                \nСнимаются в обратном порядке.", 
            "ld":"Если на сеансе используем только точки <<лунных дворцов>>, то иглы ставятся билатерально в тонизации под углом 90\*.\
                \nЕсли <<лунные дворцы>> используются как дополнение к лечению, то иглы ставятся в тонизации с одной стороны по полу, на слабой стороне:\
                \nдля мужчин - слева, для женщин - справа"}

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


man = ["Liv1", "Liv4", "Liv3", "Liv3", "Liv5", "Liv2", "Liv8", 
       "Kid1", "Kid7", "Kid3", "Kid3", "Kid4", "Kid2", "Kid10", 
       "Lu11", "Lu8", "Lu9", "Lu9", "Lu7", "Lu10", "Lu5", 
       "Hg9, Ht9", "Hg5, Ht4", "Hg7, Ht7", "Hg7, Ht7", "Hg6, Ht5", "Hg8, Ht8", "Hg3, Ht3"]

woman = ["Gb41", "Gb44", "Gb34", "Gb37", "Gb40", "Gb38", "Gb43", 
       "Bl65", "Bl67", "Bl40", "Bl58", "Kid4, Bl64", "Bl60", "Bl66", 
       "Co3", "Co1", "Co11", "Co6", "Co4", "Co5", "Co2", 
       "Si3", "Si1", "Si8", "Si7", "Si4", "Si5", "Si2"]

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


def get_chan(string):
    canals_p = re.sub('[:,/.;#$%^&]', ' ', string).split()
    canals = []
    for c in canals_p:
        if c.capitalize() in u_sin_pitanie.keys():
            canals.append(c.capitalize())
        else:
            st.error(f"""*Название канала '{c.capitalize()}' введено неверно. Попробуйте снова!*""")
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
 

# Функция для рисования секторов графа
def draw_sector(ax, center, radius, theta_start, theta_end, sign):
    # Угол в радианах
    theta = np.linspace(np.radians(theta_start), np.radians(theta_end), 100)
    x = np.append(center[0], center[0] + radius * np.cos(theta))
    y = np.append(center[1], center[1] + radius * np.sin(theta))

    # Заполняем сектор цветом
    ax.fill(x, y, color='lightgrey', alpha=0.5)
    count = 0
    cnt = 0
    for s in sign:
        # Добавляем маленькие кружочки
        if s in ['жар', 'холод', 'сырость', 'сухость', 'tree']:
            circle_x = center[0] + count + radius * np.cos(np.radians((theta_start + theta_end) / 2)) * (0.5)
            circle_y = center[1] + radius * np.sin(np.radians((theta_start + theta_end) / 2)) * (0.5)
            ax.add_patch(plt.Circle((circle_x, circle_y), circle_radius, color=colors[s]))
        # Добавляем знак в центр сектора
        else:
            circle_x = center[0] + radius * np.cos(np.radians((theta_start + theta_end) / 2)) * (0.5)
            circle_y = center[1] - cnt + radius * np.sin(np.radians((theta_start + theta_end) / 2)) * (0.5)
            ax.text(circle_x, circle_y, s, ha='center', va='center', fontsize=20, fontweight='semibold', color=colors[s])
        count += 0.15   
        cnt += 0.45             


########################################  Создаём приложение ######################################

st.title("Карта пациента")
st.markdown(f'Дата: **{datetime.now().strftime("%d.%m.%Y")}**')
# ddate = st.sidebar.text_input('Введите дату приёма', '')
# Вводим имя пациента
patient = st.sidebar.text_input('Введите Ф.И.О. пациента', '')

st.header(patient)


# Вводим дату рождения
born = st.sidebar.text_input('Введите дату рождения', '')
if born:
    try:
        born = pd.to_datetime(born, dayfirst=True).strftime("%d.%m.%Y")
        birthday = str(pd.to_datetime(born, dayfirst=True)).split()[0] #input("Введите дату рождения")
        st.markdown(f'Дата рождения: **{pd.to_datetime(born, dayfirst=True).strftime("%d.%m.%Y")}**')
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
    st.dataframe(df, use_container_width=True)

    use = set([df.loc['Ствол', 'Используем'], df.loc['Ветвь', 'Используем']]) | (Zang_Fu_Xu)
        
    dnt_use = set([df.loc['Ствол', 'Не используем'], df.loc['Ветвь', 'Не используем']]) 

    neutral = set(u_sin_pitanie.keys()) ^ (set([df.loc['Ствол', 'Не используем'], 
                                            df.loc['Ветвь', 'Не используем']]) |  
                                        set([df.loc['Ствол', 'Используем'], 
                                            df.loc['Ветвь', 'Используем']]) |
                                            Zang_Fu_Xu)
                                            
    st.markdown(f"""Нейтральные каналы: **{', '.join(list(neutral))}**""")

    if st.checkbox("Показать предыдущую запись"):
        try:
            patients = pd.read_csv("patients/patients.csv", index_col='Дата')
            patients = patients[patients['ФИО']==patient][-1:].dropna(axis=1)
            if patients['метод лечения'].values[0] == "Питание и Ке":
                st.markdown("""====================================================================================""")
                try:
                    st.markdown(f"##### :blue[Жалобы на {patients.index[0]}:]")
                    st.markdown(f"{patients['жалобы'].values[0]}")
                except:
                    st.markdown("")

                id = patients[patients['ФИО']==patient][-1:].dropna(axis=1).index[0]
                canals_plus = re.sub("\[|\]|'", "", patients.loc[id, "застой"]).split(", ")   
                canals_minus = re.sub("\[|\]|'", "", patients.loc[id, "недостаток"]).split(", ")   
                block = re.sub("\[|\]|'", "", patients.loc[id, "блок"]).split(", ") 
                wind = re.sub("\[|\]|'", "", patients.loc[id, "Gui"]).split(", ") 
                protivotok = re.sub("\[|\]|'", "", patients.loc[id, "противоток"]).split(", ") 
                xue = re.sub("\[|\]|'", "", patients.loc[id, "xue"]).split(", ") 
                tree = re.sub("\[|\]|'", "", patients.loc[id, "пат.рост"]).split(", ") 
                fire = re.sub("\[|\]|'", "", patients.loc[id, "жар"]).split(", ") 
                water = re.sub("\[|\]|'", "", patients.loc[id, "холод"]).split(", ") 
                earth = re.sub("\[|\]|'", "", patients.loc[id, "сырость"]).split(", ") 
                metall = re.sub("\[|\]|'", "", patients.loc[id, "сухость"]).split(", ") 

                di = {'+':canals_plus,
                '__':canals_minus,
                '>>>':protivotok,
                '+/-':block,
                'Gui':wind,
                'tree':tree,
                'Xue':xue,
                'жар':fire,
                'холод':water,
                'сырость':earth,
                'сухость':metall
                }

                ander = dict()

                for k in di.keys():
                    for v in di[k]:
                        v=v.lower()
                        if v in ander.keys():
                            ander[v].append(k)
                        else:
                            ander[v] = [k]

                ###################################### Рисуем карту патогенов ###################################


                # Генерируем случайные знаки и цвета
                def random_sign(channel, table=ander):
                    if channel in table.keys():
                        return table[channel]
                    else:
                        return ''

                # Устанавливаем базовые параметры
                num_vertices = 5
                radius = 1
                circle_radius = 0.08  # Радиус небольших кружков
                colors = {'жар':'red', 'сырость':'orange', 'сухость':'grey', 'холод':'blue', 'tree':'green', 
                    "+":"#800080", "__":"#800080", "Gui":"dimgrey", "Xue":"#800000", "+/-":"#800080", ">>>":"#000000"}  # Цвета для символов


                # Создание графика
                fig, ax = plt.subplots(figsize=(15,8), )
                ax.axis('equal')  # Одинаковые масштабы по осям
                ax.axis('off')  # Отключаем оси

                # Открывающие углы для каждой вершины
                angles = np.linspace(0, 360, num_vertices+1)

                # Рисуем вершины: одна с 4 секторами, остальные с 2
                draw_sector(ax, (np.sin(np.radians(angles[0])) * 2, np.cos(np.radians(angles[0])) * 2), radius, 0, 90, random_sign('th'))
                draw_sector(ax, (np.sin(np.radians(angles[0])) * 2, np.cos(np.radians(angles[0])) * 2), radius, 90, 180, random_sign('si'))
                draw_sector(ax, (np.sin(np.radians(angles[0])) * 2, np.cos(np.radians(angles[0])) * 2), radius, 180, 270, random_sign('ht'))
                draw_sector(ax, (np.sin(np.radians(angles[0])) * 2, np.cos(np.radians(angles[0])) * 2), radius, 270, 360, random_sign('hg'))  # 4 сектора для первой вершины

                draw_sector(ax, (np.sin(np.radians(angles[1])) * 2, np.cos(np.radians(angles[1])) * 2), radius, angles[1] + 0 * 180, angles[1] + (0 + 1) * 180, random_sign('sp'))
                draw_sector(ax, (np.sin(np.radians(angles[1])) * 2, np.cos(np.radians(angles[1])) * 2), radius, angles[1] + 1 * 180, angles[1] + (1 + 1) * 180, random_sign('st'))

                draw_sector(ax, (np.sin(np.radians(angles[2])) * 2, np.cos(np.radians(angles[2])) * 2), radius, angles[1] + 0 * 180, angles[1] + (0 + 1) * 180, random_sign('lu'))
                draw_sector(ax, (np.sin(np.radians(angles[2])) * 2, np.cos(np.radians(angles[2])) * 2), radius, angles[1] + 1 * 180, angles[1] + (1 + 1) * 180, random_sign('co'))

                draw_sector(ax, (np.sin(np.radians(angles[3])) * 2, np.cos(np.radians(angles[3])) * 2), radius, angles[4] + 0 * 180, angles[4] + (0 + 1) * 180, random_sign('kid'))
                draw_sector(ax, (np.sin(np.radians(angles[3])) * 2, np.cos(np.radians(angles[3])) * 2), radius, angles[4] + 1 * 180, angles[4] + (1 + 1) * 180, random_sign('bl'))

                draw_sector(ax, (np.sin(np.radians(angles[4])) * 2, np.cos(np.radians(angles[4])) * 2), radius, angles[4] + 0 * 180, angles[4] + (0 + 1) * 180, random_sign('liv'))
                draw_sector(ax, (np.sin(np.radians(angles[4])) * 2, np.cos(np.radians(angles[4])) * 2), radius, angles[4] + 1 * 180, angles[4] + (1 + 1) * 180, random_sign('gb'))

                # Отображаем график
                # plt.title(f"{patients.index[0]}", loc='left', fontdict={'fontsize':20})

                st.write(fig)
                st.markdown(""":blue[Проведённое лечение: ]""")
                st.markdown(f"""{patients['лечение'].values[0]}""")
                st.markdown("""====================================================================================""")

            else:
                st.dataframe(patients.T, use_container_width=True)
        except:
            st.markdown(f':red[Пациент **{patient}** отсутствует в базе данных]')


    if st.checkbox("Показать все записи"):
        try:
            df_save = pd.read_csv(f"patients/patients.csv", index_col='Дата')
            df_save_2 = df_save[df_save['ФИО']==patient]
            st.dataframe(df_save_2, use_container_width=True)
        except:
            st.markdown(f':red[Пациент **{patient}** отсутствует в базе данных]')        

    st.markdown("""--------------------------------------------------""")


    complaints = st.sidebar.text_area("Жалобы", "")


    
    
    ###################################   Выбираем метод лечения:   ##########################################


    method = st.sidebar.selectbox(
    "Выберете метод лечения",
    (" ", "Питание и Ке", "Лунные дворцы"))
    

    ###################################   Вводим канал в застое:    ###########################################
        
    if method=="Питание и Ке":
        
        plus = st.sidebar.text_input('Введите основной канал в застое', '')
        canals_plus = get_chan(plus)
                    
        if canals_plus:
            # st.dataframe(ke[canals_plus][:4]) 
            
            a = get_list_of_channels(canals_plus, ke, 4)

            st.sidebar.markdown(f"""Возможные каналы в недостатке:""")
            st.sidebar.markdown(f""":blue[**{', '.join(list(set(a)))}**]""")
            


    ###################################   Для канала в недостатке:  ########################################
        
        minus = st.sidebar.text_input('Введите канал в недостатке', '')
        canals_minus = get_chan(minus)
 
        if canals_minus:
            zastoi = get_list_of_channels(canals_minus, ke, 4)
            st.sidebar.markdown(f"""Возможные каналы в застое:""")
            st.sidebar.markdown(f""":blue[**{', '.join(list(set(zastoi)))}**]""")

        block = get_chan(st.sidebar.text_input('Введите каналы в блоке', ''))
        wind = get_chan(st.sidebar.text_input('Введите каналы с ветром', ''))
        protivotok = get_chan(st.sidebar.text_input('Введите каналы с противотоком', ''))
        xue = get_chan(st.sidebar.text_input('Xue', ''))
        if st.sidebar.checkbox("Работа с качеством"):
            tree = get_chan(st.sidebar.text_input('Патологический рост', ''))
            fire = get_chan(st.sidebar.text_input('Жар', ''))
            water = get_chan(st.sidebar.text_input('Холод', ''))
            earth = get_chan(st.sidebar.text_input('Сырость', ''))
            metall = get_chan(st.sidebar.text_input('Сухость', ''))
        else:
            tree, fire, water, earth, metall = [], [], [], [], []

        di = {'+':canals_plus,
            '__':canals_minus,
            '>>>':protivotok,
            '+/-':block,
            'Gui':wind,
            'tree':tree,
            'Xue':xue,
            'жар':fire,
            'холод':water,
            'сырость':earth,
            'сухость':metall
            }

        ander = dict()

        for k in di.keys():
            for v in di[k]:
                v=v.lower()
                if v in ander.keys():
                    ander[v].append(k)
                else:
                    ander[v] = [k]

        ###################################### Рисуем карту патогенов ###################################

        # Генерируем случайные знаки и цвета
        def random_sign(channel, table=ander):
            if channel in table.keys():
                return table[channel]
            else:
                return ''
            
        # Устанавливаем базовые параметры
        num_vertices = 5
        radius = 1
        circle_radius = 0.08  # Радиус небольших кружков
        colors = {'жар':'red', 'сырость':'orange', 'сухость':'grey', 'холод':'blue', 'tree':'green', 
                  "+":"#800080", "__":"#800080", "Gui":"dimgrey", "Xue":"#800000", "+/-":"#800080", ">>>":"#000000"}  # Цвета для символов


        # Создание графика
        fig, ax = plt.subplots(figsize=(15, 8))
        ax.axis('equal')  # Одинаковые масштабы по осям
        ax.axis('off')  # Отключаем оси

        # Открывающие углы для каждой вершины
        angles = np.linspace(0, 360, num_vertices+1)

        # Рисуем вершины: одна с 4 секторами, остальные с 2
        draw_sector(ax, (np.sin(np.radians(angles[0])) * 2, np.cos(np.radians(angles[0])) * 2), radius, 0, 90, random_sign('th'))
        draw_sector(ax, (np.sin(np.radians(angles[0])) * 2, np.cos(np.radians(angles[0])) * 2), radius, 90, 180, random_sign('si'))
        draw_sector(ax, (np.sin(np.radians(angles[0])) * 2, np.cos(np.radians(angles[0])) * 2), radius, 180, 270, random_sign('ht'))
        draw_sector(ax, (np.sin(np.radians(angles[0])) * 2, np.cos(np.radians(angles[0])) * 2), radius, 270, 360, random_sign('hg'))  # 4 сектора для первой вершины

        draw_sector(ax, (np.sin(np.radians(angles[1])) * 2, np.cos(np.radians(angles[1])) * 2), radius, angles[1] + 0 * 180, angles[1] + (0 + 1) * 180, random_sign('sp'))
        draw_sector(ax, (np.sin(np.radians(angles[1])) * 2, np.cos(np.radians(angles[1])) * 2), radius, angles[1] + 1 * 180, angles[1] + (1 + 1) * 180, random_sign('st'))

        draw_sector(ax, (np.sin(np.radians(angles[2])) * 2, np.cos(np.radians(angles[2])) * 2), radius, angles[1] + 0 * 180, angles[1] + (0 + 1) * 180, random_sign('lu'))
        draw_sector(ax, (np.sin(np.radians(angles[2])) * 2, np.cos(np.radians(angles[2])) * 2), radius, angles[1] + 1 * 180, angles[1] + (1 + 1) * 180, random_sign('co'))

        draw_sector(ax, (np.sin(np.radians(angles[3])) * 2, np.cos(np.radians(angles[3])) * 2), radius, angles[4] + 0 * 180, angles[4] + (0 + 1) * 180, random_sign('kid'))
        draw_sector(ax, (np.sin(np.radians(angles[3])) * 2, np.cos(np.radians(angles[3])) * 2), radius, angles[4] + 1 * 180, angles[4] + (1 + 1) * 180, random_sign('bl'))

        draw_sector(ax, (np.sin(np.radians(angles[4])) * 2, np.cos(np.radians(angles[4])) * 2), radius, angles[4] + 0 * 180, angles[4] + (0 + 1) * 180, random_sign('liv'))
        draw_sector(ax, (np.sin(np.radians(angles[4])) * 2, np.cos(np.radians(angles[4])) * 2), radius, angles[4] + 1 * 180, angles[4] + (1 + 1) * 180, random_sign('gb'))

        # Отображаем график
        # plt.title(patient)
        st.write(fig)

        st.markdown("""--------------------------------------------------""")

        ##### Питание #####

        if canals_minus:            
            st.markdown(f"""#### Основной недостаток выявлен в канале {canals_minus[0]}:""")
            
            # Выводим DataFrame в интерфейсе:
            st.dataframe(pitanie[canals_minus], use_container_width=True)  
                
            m = get_list_of_channels(canals_minus, pitanie, 5)  

            st.markdown("""#### Возможные каналы для питания:""")
            st.markdown(f"""**:blue[{', '.join(list(set(m)))}]**""") 
            
            dnt_use = set([df.loc['Ствол', 'Не используем'], df.loc['Ветвь', 'Не используем']]) | set(canals_minus) | set(canals_plus)
            
            if (set(m) & dnt_use):
                st.warning(f""":red[!!!  Конфликт с запрещёнными каналами: **{', '.join(list(set(m) & dnt_use))}** !!!]""")
            else:
                st.markdown("""Конфликт с запрещёнными каналами: :green[*Конфликта нет*]""")

            
            one_spine = []
            for i in list((set(m) & set(a))):
                if (i not in dnt_use):
                    one_spine.append(i)

            if one_spine:
                chan_pit = ' '.join(one_spine)
                st.markdown(f"""Одновременно питание недостатка и Ке на застой: :green[**{chan_pit}**]""")  
                point_pit = []
                for i in canals_minus:
                    pp = pitanie[i][:5].to_list() 
                    point_pit+=pp

                point_pit = " ".join(point_pit).replace(",", '')
                point_pit = point_pit.replace(",", '')
                try:
                    point_pit = re.search(f"{chan_pit}\d+", point_pit)[0]
                    st.markdown(f"""#### Подходящие точки для питания в этом случае:""")
                    st.markdown(f"""#### :green[{point_pit}]""")
                    st.markdown(f"""*{points.loc[point_pit, "Локализация"]}*""")
                    st.markdown(f"""*{technika['pit']}*""")
                except:
                    chan_pit = chan_pit.split()
                    st.markdown("""#### Подходящие точки для питания в этом случае:""")
                    for c in chan_pit:
                        pp = re.search(f"{c}\d+", point_pit)[0]
                        st.markdown(f"""#### :green[***{pp}***]""")
                        try:
                            st.markdown(f"""*{points.loc[pp, "Локализация"]}*""")
                        except:
                            st.markdown(f"""*Точки нет в базе данных*""")
                    st.markdown(f"""*{technika['pit']}*""")                        

            else:
                st.markdown(f"""*Одной иглой питание недостатка и Ке на застой не получится, - нет пересекающихся каналов*""")  
            
                for channal in canals_plus:
                    st.markdown(f"""Застой в канале {channal} корректируем техникой 'тяни-толкай', точка:""")
                    st.markdown(f"""**{table.loc[channal, 'Jing_Jin']}**""")
                    st.markdown(f"""*{technika['JJ']}*""")

            st.markdown("""--------------------------------------------------""")

        ##### Gui #####
        if wind:
            t_gui = []
            for i in di['Gui']:
                t_gui.append(table.loc[i, 'Gui'])
            tt_gui = ', '.join(t_gui)
            st.markdown(f"""#### Работа с Gui: :green[{tt_gui}]""")
            for t in t_gui:
                st.markdown(f"""#### :green[***{t}***]""")            
                try:
                    st.markdown(f"""*{points.loc[t, "Локализация"]}*""")
                except:
                    st.markdown(f"""*Точки нет в базе данных*""")
            st.markdown(f"""*{technika['gui']}*""") 


        ##### Xue #####
        if xue:
            t_xue = []
            for i in di['Xue']:
                t_xue.append(table.loc[i, 'Xue'])
            tt_xue = ', '.join(t_xue)
            st.markdown(f"""#### Работа с Xue: :green[{tt_xue}]""")
            for t in t_xue:
                st.markdown(f"""#### :green[***{t}***]""")            
                try:
                    st.markdown(f"""*{points.loc[t, "Локализация"]}*""")
                except:
                    st.markdown(f"""*Точки нет в базе данных*""")
            st.markdown(f"""*{technika['xue']}*""") 

        pp = st.sidebar.text_input("Введите выбранные точки через запятую", "")
        if pp:
            st.markdown(f"""#### ***В этом сеансе поставлены точки:***""")
            st.markdown(f"""#### **:blue[{pp}]**""")
            # pp = pp.split(",")
            # show_img = st.radio(
            #     "Показать точки", ["нет", "да"]
            # )
            # if show_img=="да":
            #     for p in pp:
            #         p = p.strip().capitalize()
            #         image_path = f"data/{p}.jpg"
            #         image = Image.open(image_path)
            #         st.image(image, width=300)

            comments = st.text_area("Ваши комментарии", "")

            
            ##########################        Сохраняем пациента         ##########################

            if st.sidebar.button("Save",type="primary"):
                doh = None
                new_save = [datetime.now().date(), patient, born, complaints, method, canals_plus, canals_minus, block, wind,
                        protivotok, xue, tree, fire, water, earth, metall, pp, comments, doh]

                with open('patients/patients.csv', 'a', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(new_save) 
                file.close()
                st.sidebar.markdown(""":green[***Файл успешно сохранён!***]""")
                
            

####################################   Лунные дворцы    ############################################


    if method=="Лунные дворцы":
        image_path = "data/Лунные дворцы.jpg"
        image = Image.open(image_path)
        st.image(image, width=600)
        
        # Вводим пол пациента
        sex = st.sidebar.selectbox(
            "Выберете пол пациента",
            ("", "Мужчина", "Женщина"),
        )

        doh = st.sidebar.text_input('Введите дату события', '')
        if doh:
            try:
                date = str(pd.to_datetime(doh, dayfirst=True)).split()[0] #input("Введите дату рождения")
                year = int(date[:4])
                month = int(date[5:7])
                day = int(date[8:])
                st.markdown(f'Дата события: **{pd.to_datetime(doh, dayfirst=True).strftime("%d.%m.%Y")}**')
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
                points_ld = man[lunar_day-1]
                st.markdown(f"#### Точки по лунным дворцам: \t:green[{points_ld}]")
            
            else:
                points_ld = woman[lunar_day-1]
                st.markdown(f"#### Точки по лунным дворцам: \t:green[{points_ld}]")

            
            for p in points_ld.split(', '):
                st.markdown(f"#### :green[{p}]")
                try:
                    st.markdown(f"""*{points.loc[p, "Локализация"]}*""")
                except:
                    st.markdown(f"""*Точки нет в базе данных*""")
            st.markdown(f"""*{technika['ld']}*""")

        #################################################       Выбранные точки      ##################################################
        
        pp = st.sidebar.text_input("Введите выбранные точки через запятую", "")
        if pp:
            st.markdown(f"""#### ***В этом сеансе поставлены точки:***""")
            st.markdown(f"""#### **:blue[{pp}]**""")
            # pp = pp.split(",")
            # show_img = st.radio(
            #     "Показать точки", ["нет", "да"]
            # )
            # if show_img=="да":
            #     for p in pp:
            #         p = p.strip().capitalize()
            #         image_path = f"data/{p}.jpg"
            #         image = Image.open(image_path)
            #         st.image(image, width=300)

            comments = st.text_area("Ваши комментарии", "")

            
            ################################        Сохраняем пациента         ####################################

            if st.sidebar.button("Save",type="primary"):
                canals_plus, canals_minus, block, wind, protivotok, xue, tree, fire, water, earth, metall = None, None, None, None, None, None, None, None, None, None, None
                new_save = [datetime.now().date(), patient, born, complaints, method, canals_plus, canals_minus, block, wind,
                        protivotok, xue, tree, fire, water, earth, metall, pp, comments, doh]
                with open('patients/patients.csv', 'a', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(new_save) 
                file.close()
                st.sidebar.markdown(""":green[***Файл успешно сохранён!***]""")
               