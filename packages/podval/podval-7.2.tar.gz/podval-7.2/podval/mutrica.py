from PIL import Image
import requests

#     im = Image.open(requests.get('', stream=True).raw)
# def v_2():
#     im1 = Image.open(requests.get('', stream=True).raw)
#     im2 = Image.open(requests.get('', stream=True).raw)
#     return im1, im2
def library():
    print('''
Диск: https://drive.google.com/drive/folders/1HDofK5q6VmdBjRN5TL-TPSpAYqi8tgYN
Лист 1 (кривые роста, Хольта-Уинтерса, Брауна, Четверикова)
https://colab.research.google.com/drive/1dgglyYI0NdRQ6A7YXOHswUEvPFb1M2Ei?usp=sharing  
Лист 2 (Стьюдента, Ирвина, критерия на медиане, разности средних уровней, Фостера-Стьюарта, средневзвешенной скользящей средней, экспоненциальное сглаживание)
https://colab.research.google.com/drive/1LIh8VYTdiheMyZkuFeL5Q520nAWjAkpj?usp=sharing
Лист 3 (системы)
https://drive.google.com/file/d/13u9ZJ8RGhW9ZPOSSUjl-h4LbgYxEQWD8/view?usp=sharing 
Лист 4 (панельки, Фишера, Хаусмана, Бреуша-Пагана)
https://colab.research.google.com/drive/1CCjPyduT-vBX45vyFjeN-urDIahmmqbH?usp=sharing 
Лист 5 (логит, пробит)
https://colab.research.google.com/drive/1HD51t_bi0bfayRW5OfXxhzPbGnmtIw65?usp=sharing 
Лист 6.1 (arima, arma)
https://colab.research.google.com/drive/1mZy8xV_7if_7Xi7P4KF8IeT7MzlTJVyx?usp=sharing 
Лист 6.2 (ar(), ma(3))
https://drive.google.com/file/d/1Eu3nlA5jC1J4p-R__TP9cvYYM2QPuoE7/view?usp=sharing
Лист 6.3 (ar(1), ma(2), arma(2,3))
https://colab.research.google.com/drive/1qk3Ad-k9TVzT0ySAWXRfOPOZTs5Ao4Jz?usp=sharing   
    ''')

def help_():
    print('''
1. Линейная модель множественной регрессии. Основные предпосылки метода наименьших квадратов.
2. Нелинейные модели регрессии. Подходы к оцениванию. Примеры
3. Тестирование правильности выбора спецификации: типичные ошибки спецификации модели, Тест Рамсея (тест RESET), условия применения теста.
4. Тестирование правильности выбора спецификации: типичные ошибки спецификации модели, Критерий Акаике, Критерий Шварца. условия применения критериев.
5. Гетероскедастичность: определение, причины, последствия. Тест Голдфеда-Квандта и особенности его применения.
6. Гетероскедастичность: определение, причины, последствия. Тест ранговой корреляции Спирмена и особенности его применения.
7. Гетероскедастичность: определение, причины, последствия. Тест Бреуша-Пагана и особенности его применения.
8. Гетероскедастичность: определение, причины, последствия. Тест Глейзера и особенности его применения.
9. Способы корректировки гетероскедастичности: взвешенный метод наименьших квадратов (ВМНК) и особенности его применения.
10. Автокорреляция: определение, причины, последствия. Тест Дарбина-Уотсона и особенности его применения.
11. Автокорреляция: определение, причины, последствия. Тест Бройша – Годфри и особенности его применения.
12.   Автокорреляция: определение, причины, последствия. H – тест и особенности его применения.
13. Автокорреляция: определение, причины, последствия. Метод рядов Сведа-Эйзенхарта и особенности его применения.
14. Модель с автокорреляцией случайного возмущения. Оценка моделей с авторегрессией.
15. Процедура Кохрейна-Оркатта.
16. Процедура Хилдрета – Лу.
17. Оценка влияния факторов, включенных в модель. Коэффициент эластичности, Бета-коэффициент, Дельта – коэффициент.
18. Мультиколлинеарность: понятие, причины и последствия.
19. Алгоритм пошаговой регрессии.
20. Метод главных компонент (PCA) как радикальный метод борьбы с мультиколлинеарностью
21. Выявление мультиколлинеарности: коэффициент увеличения дисперсии (VIF –тест).
22. Выявление мультиколлинеарности: Алгоритм Фаррара-Глобера.
23. Построение гребневой регрессии. Суть регуляризации.
24. Фиктивная переменная и правило её использования.
25. Модель дисперсионного анализа.
26. Модель ковариационного анализа.
27. Фиктивные переменные в сезонном анализе.
28.  Фиктивная переменная сдвига: спецификация регрессионной модели с фиктивной переменной сдвига; экономический смысл параметра при фиктивной переменной; смысл названия.
29. Фиктивная переменная наклона: спецификация регрессионной модели с фиктивной переменной наклона; экономический смысл параметра при фиктивной переменной; смысл названия.
30. Определение структурных изменений в экономике: использование фиктивных переменных, тест Чоу.
31. ​​Модели бинарного выбора. Недостатки линейной модели.
32. Модели множественного выбора: модели с неупорядоченными альтернативными вариантами.
33. Модели усеченных выборок.
34. Модели цензурированных выборок (tobit-модель).
35.   Модели множественного выбора: гнездовые logit-модели.
36.    Модели счетных данных (отрицательная биномиальная модель, hurdle-model)
37. Модели множественного выбора: модели с упорядоченными альтернативными вариантами.
38. Модели случайно усеченных выборок (selection model).
39. Логит-модель. Этапы оценки. Области применения.
40. Пробит-модель. Этапы оценки. Области применения.
41. Метод максимального правдоподобия
42. Свойства оценок метода максимального правдоподобия.
43. Информационная матрица и оценки стандартных ошибок для оценок параметров logit и probit моделей. Интерпретация коэффициентов в моделях бинарного выбора.
44. Мера качества аппроксимации и качества прогноза logit и probit моделей.
45. Временные ряды: определение, классификация, цель и задача моделирования временного ряда.
46.    Исследование структуры одномерного временного ряда.
47.   Процедура выявления аномальных наблюдений на основе метода Ирвина. Особенности применения метода. Анализ аномальных наблюдений.
48. Проверка наличия тренда. Критерий серий, основанный на медиане. Особенности применения метода.
49. Процедура выявления аномальных наблюдений. Причины аномальных значений. Блочные диаграммы по типу «ящика с усами».
50. Проверка наличия тренда. Метод проверки разности средних уровней. Особенности применения метода.
51. Проверка наличия тренда. Метод Фостера-Стьюарта. Особенности применения метода.
52.   Сглаживание временных рядов. Простая (среднеарифметическая) скользящая средняя. Взвешенная (средневзвешенная) скользящая средняя. Среднехронологическая. Экспоненциальное сглаживание.
53. Функциональные зависимости временного ряда. Предварительный анализ временных рядов.
54. Трендовые модели. Без предела роста. Примеры функций. Содержательная интерпретация параметров.
55. Процедура выявления аномальных наблюдений на основе распределения Стьюдента. Особенности применения метода. Анализ аномальных наблюдений.
56. Трендовые модели. С пределом роста без точки перегиба. Примеры функций. Содержательная интерпретация параметров.
57. Трендовые модели. С пределом роста и точкой перегиба или кривые насыщения. Примеры функций. Содержательная интерпретация параметров.
58.  Выбор кривой роста.
59. Прогнозирование с помощью кривой роста.
60.    Прогнозирование временного ряда на основе трендовой модели.
61. Модель Тейла-Вейджа (мультипликативная модель).
62. Метод Четверикова.
63. Моделирование тренд-сезонных процессов. Типы функциональных зависимостей.
64.Мультипликативная (аддитивная) модель ряда динамики при наличии тенденции: этапы построения.
65. Моделирование периодических колебаний (гармоники Фурье).
66. Прогнозирование одномерного временного ряда случайной компоненты (распределение Пуассона).
67. Функциональные преобразования переменных в линейной регрессионной модели. Метод Зарембки. Особенности применения.
68. Функциональные преобразования переменных в линейной регрессионной модели. Тест Бокса-Кокса. Особенности применения.
69. Адаптивная модель прогнозирования Брауна.
70. Функциональные преобразования переменных в линейной регрессионной модели. Критерий Акаике  и Шварца. Особенности применения.
71. Модель Хольта-Уинтерса (адаптивная модель).
72. Функциональные преобразования переменных в линейной регрессионной модели. Тест Бера. Особенности применения.
73. Функциональные преобразования переменных в линейной регрессионной модели. Тест МакАлера. Особенности применения.
74. Функциональные преобразования переменных в линейной регрессионной модели. Тест МакКиннона. Особенности применения.
75. Функциональные преобразования переменных в линейной регрессионной модели. Тест Уайта. Особенности применения.
76. Функциональные преобразования переменных в линейной регрессионной модели. Тест Дэвидсона. Особенности применения.
77. Модели с распределенными лаговыми переменными.
78. Оценка моделей с лагами в независимых переменных. Преобразование Койка
79. ​​Полиномиально распределенные лаги Алмон
80. Авторегрессионные модели.
81. Авторегрессионные модели с распределенными лагами.
82. Стационарные временные ряды. Определения стационарности, лаговой переменной, автоковариационной функции временного ряда, автокоррляционной функции, коррелограммы,  коэффициенты корреляции между разными элементами стационарного временного ряда с временным лагом.
83. Стационарные временные ряды. Определения частной автокорреляционной функции, белого шума, автоковариационная функция для белого шума, ACF для белого шума, частная автокорреляционная функция для белого шума.
84. Модели стационарных временных рядов: модель ARMA(p,q) (классический вид и через лаговый оператор). Авторегрессионный многочлен, авторегрессионная часть и часть скользящего среднего.
85. Модели стационарных временных рядов: модель ARMA(1, q). Доказательство утверждения: Модель ARMA(1, q) стационарна тогда и только тогда, когда |a|<1.
86. Модели стационарных временных рядов: Модель MA(q), Среднее, дисперсия и ACF для MA(q). Модель MA(∞).
87.  Модели стационарных временных рядов: Модель AR(p). Доказательство утверждения: Модель AR(p) определяет стационарный ряд ⇐⇒ выполнено условие стационарности: все корни многочлена a(z) по модулю больше единицы. Модель AR(1).
88. Прогнозирование для модели ARMA. Условия прогнозирования. Периоды прогнозирования. Информативность прогнозов.
89. Оценка и тестирование модели: Предварительное тестирование на белый шум.
90.  Оценка модели и тестирование гипотез временного ряда.
91. Информационные критерии для сравнения моделей и выбора порядка временного ряда: Акаике, Шварца, Хеннана-Куина. Условия их применения.
92. Проверка адекватности модели: тесты на автокорреляцию временного ряда Дарбина-Уотсона, Льюинга-Бокса.
93.    Линейная регрессия для стационарных рядов: Модель FDL.
94. Линейная регрессия для стационарных рядов. Модель ADL.
95. Понятие TS-ряда. Модель линейного тренда. Модель экспоненциального тренда.
96. Нестационарные временные ряды: случайное блуждание, стохастический тренд, случайное блуждание со сносом.
97. Дифференцирование ряда: определение, DS-ряды.
98. Подход Бокса-Дженкинса.
99. Модель ARIMA.
100. Тест ADF на единичный корень.
101. Модель ARCH.
102. Модель GARCH.
103.  Область применения панельных данных. Преимущества использования панельных данных.
104. Модели панельных данных и основные обозначения.
105. Модель пула (Pool model).
106.  Модель регрессии с фиксированным эффектом (fixed effect model)
107. Модель регрессии со случайным эффектом (random effect model).
108. Тест Бройша-Пагана для панельных данных
109. Тест Хаусмана для панельных данных.
110. Тест Лагранжа для панельных данных.
111. Вычисление значения оценок параметров β и а в модели с фиксированным эффектом.
112. Отражение пространственных эффектов. Бинарная матрица граничных соседей. Приведите пример.
113. Отражение пространственных эффектов. Бинарная матрица ближайших соседей. Приведите пример.
114. Отражение пространственных эффектов. Матрица расстояний. Приведите пример.
115. Отражение пространственных эффектов. Матрица расстояний с учетом размера объекта. Приведите пример.
116. Алгоритм построения матрицы пространственных весов. Приведите пример.
117. Пространственная автокорреляция по методологии А. Гетиса и Дж. Орда. Недостатки методологии.
118. Пространственная автокорреляция по методологии Роберта Джири.
119.     Пространственная автокорреляция по методологии Морана П.
120. Пространственная кластеризация территорий. Локальный индекс автокорреляции П. Морана (Ili)
121. Матрица взаимовлияния Л. Анселина (LISA).   
    ''')
    im1 = Image.open(requests.get('https://sun9-30.userapi.com/impg/QKMEZ71IcaN0FplOjPCDZtCYtVBYbePhqoFQJQ/WbZmnjq8SsM.jpg?size=411x639&quality=96&sign=1600978b5cd33db774a78f5eb09a2751&type=album', stream=True).raw)
    im2 = Image.open(requests.get('https://sun9-55.userapi.com/impg/CRe3YBaHZ_J_u8aQGtLoEffZHNxOeApmjcIfgg/ql9212zhWfo.jpg?size=409x668&quality=96&sign=95a620b977a68f1134f83e4c18074164&type=album', stream=True).raw)
    im3 = Image.open(requests.get('https://sun9-20.userapi.com/impg/dXNHlU9uzq3xn1_34bHga9c0EKntKilmnbwJww/dMXO3JYdpUQ.jpg?size=411x674&quality=96&sign=c288c1a4a9404f612206aed21aba825e&type=album', stream=True).raw)
    im4 = Image.open(requests.get('https://sun9-47.userapi.com/impg/54j8zRQjHVVjW1bQaP0EoEOPjeOW5Tl9y8MNfw/3paKG2ox_rA.jpg?size=409x351&quality=96&sign=265b324f2f9a6216fcb8d1752f7357ff&type=album', stream=True).raw)
    return im1, im2, im3, im4

def v_1():
    im = Image.open(requests.get('https://sun9-80.userapi.com/impg/QjG48hxYwFgxepQuonh6mSaVUqmFfw-B2_pPOg/pogJGAbBktU.jpg?size=983x521&quality=96&sign=55c64f49118b6024824cfc0684a4fe6b&type=album', stream=True).raw)
    im2 = Image.open(requests.get('https://sun1-94.userapi.com/impg/4PavD_m2xyBplKZUiyzmAwU5BykUjXR5dCDj1g/9qPgUTFfeAE.jpg?size=989x453&quality=96&sign=9a847674666d5d4ffb8e25007408d26e&type=album', stream=True).raw)
    return im, im2

def v_2():
    im1 = Image.open(requests.get('https://sun9-68.userapi.com/impg/CkjgYz_vtjek7MsLlULqST0Aeo0JVCMC5QTUEg/JiSy3ShxG6g.jpg?size=696x731&quality=96&sign=47aacbe579131c9ce447cbfae3e11aa9&type=album', stream=True).raw)
    im2 = Image.open(requests.get('https://sun9-59.userapi.com/impg/zv_JpX7wjYgtwN5ZyxyKWfPW0r8MTVBnA6_jaA/0EknoQxUDIE.jpg?size=687x289&quality=96&sign=edc32c4d9d5cfacdf9b51d68c7ca3e0a&type=album', stream=True).raw)
    return im1, im2
    
def v_3():
    im = Image.open(requests.get('https://sun1-15.userapi.com/impg/h9RurjKBkCcMeP3DiSXW-PK08tkzErjYeuEoNA/S4RFU0HF-9s.jpg?size=799x462&quality=96&sign=eba23c9dbb2822d9d659040077d3a2d0&type=album', stream=True).raw)
    im2 = Image.open(requests.get('https://sun9-25.userapi.com/impg/TK-SoOz9Pe5v5hQtvr_mooalk_YzssUJzfEtyg/NZC8YmOZ7hI.jpg?size=788x494&quality=96&sign=83d07438854a77846f24947e03c2d6de&type=album', stream=True).raw)
    return im, im2

def v_4():
    im = Image.open(requests.get('https://sun9-73.userapi.com/impg/9D2WJIpvkozfdOw3KMac8_hBS6GsxYdlFCqRrA/cTa62sGPg-Q.jpg?size=1580x1072&quality=96&sign=f49c4505330e37effbd69f0406e5e4b9&type=album', stream = True).raw)
    im2 = Image.open(requests.get('https://sun9-64.userapi.com/impg/N0xnxJPDCTO6Q24Vo9rawSDwNeZ18Zhpg5muSA/XWgT54ZWtMo.jpg?size=1566x1282&quality=96&sign=89d3901e0a6b8a74e7b731a82fa0d14b&type=album', stream = True).raw)
    return im, im2

def v_5():
    im = Image.open(requests.get('https://sun9-26.userapi.com/impg/5fjeykqeZrlITxCHoQRCh1Y6nw3KmqdzMdMgRA/RiIL0hp3wpU.jpg?size=1154x666&quality=96&sign=62fea3f6bab90b2252dda6f8fff77b55&type=album', stream=True).raw)
    im2 = Image.open(requests.get('https://sun1-26.userapi.com/impg/5CUfWQ_pPVYoW-1scLNv5Oj5zG1CsUz0t_hl7g/LBubkn4sPf8.jpg?size=994x1080&quality=96&sign=cb5d39d05fdd23ff0932497b70d87f99&type=album', stream=True).raw)
    return im, im2

def v_6():
    im = Image.open(requests.get('https://sun9-24.userapi.com/impg/kNKOedgI4AxA9NeN5zF4ivMxKHeYCCh0XHThyw/w-UrONj5ZTw.jpg?size=899x564&quality=96&sign=3c67915980ee73ffb49b535e04e3905a&type=album', stream=True).raw)
    im2 = Image.open(requests.get('https://sun9-59.userapi.com/impg/ySQo5YmztAdJ0ftlGe4BAZVRm9Gih55MTUZJqA/-1lRh7ajDVU.jpg?size=885x744&quality=96&sign=c5eada1e6216a85a41358b3d1a7843c6&type=album', stream=True).raw)
    return im, im2

def v_7():
    im = Image.open(requests.get('https://sun9-31.userapi.com/impg/56-aGcPigunxFj1QV2Svhp4JB7WVoBy5wz7afA/Jgj3h4kr_Tg.jpg?size=1798x918&quality=96&sign=c8c4780fac65f06f0c43ab7456dfa677&type=album', stream = True).raw)
    im2 = Image.open(requests.get('https://sun9-16.userapi.com/impg/wLh6en-AfWxENvj1iGD7F8a58FW3-eQnJgt0GA/l0PbyzJHtgo.jpg?size=1947x989&quality=96&sign=921a28cf78b7be6bcfd622f7813557bb&type=album', stream = True).raw)
    return im, im2

def v_8():
    im = Image.open(requests.get('https://sun9-75.userapi.com/impg/IsRN5KomBFg-SeKA_LIeC_6ZMDa1TcqEKJtW0w/Zxb2TG0QejA.jpg?size=796x631&quality=96&sign=2d097fbc1772fd515973bc7039f68253&type=album', stream=True).raw)
    im2 = Image.open(requests.get('https://sun9-37.userapi.com/impg/EYNTO3a7pvzQmAwkkNGgZlMVvnp43ZNiP0ajCA/aynCo9Yh5wg.jpg?size=667x444&quality=96&sign=177b7c8c460f58c28e7d0b4dcb5efbcb&type=album', stream=True).raw)
    return im, im2

def v_9():
    im = Image.open(requests.get('https://sun1-95.userapi.com/impg/14ADRZvOBuWjhYjhv0_uSN1D-07O3Bodr0s5Tw/LdSyhBLD0WI.jpg?size=710x667&quality=96&sign=cd93a4559300e3a96d203442f6b6434f&type=album', stream = True).raw)
    im2 = Image.open(requests.get('https://sun9-49.userapi.com/impg/iebUtAUcYSNcv67U1BtR6hUjsnNyEX5BvbHlVg/kp6bPpuUgiY.jpg?size=1060x192&quality=96&sign=1bbb0abce427a9b0a70b2efea0dff81e&type=album', stream = True).raw)
    return im, im2


def v_10():
    im = Image.open(requests.get('https://sun9-80.userapi.com/impg/AVJ00yqQGe9-bOMNcAkkN7MGA3gBliz_sPgFYQ/xQRLi0hfivY.jpg?size=860x761&quality=96&sign=6bc2c2ad8559b0ba76e81dcec653b41c&type=album', stream = True).raw)
    im2 = Image.open(requests.get('https://sun9-43.userapi.com/impg/bxjk4Yu9rPP2f6vOExA_5OKwBvt9VobmVDV9sg/cZ4UKKbe4fA.jpg?size=781x418&quality=96&sign=f00de74ec1f63ed30e11ffdee1f5f36c&type=album', stream = True).raw)
    return im, im2
    
def v_11():
    im = Image.open(requests.get('https://sun9-21.userapi.com/impg/4FPQag6pdGJZ6Prf3zZ5YzxTxstVs73nA5wOfw/d0z88l0WdHc.jpg?size=900x735&quality=95&sign=87ca7f0981a2df0e097f5f222fefad49&type=album', stream=True).raw)
    return im

def v_12():
    im = Image.open(requests.get('https://sun9-72.userapi.com/impg/Nl_Qa0n56K_XzQWNTWpga3L-cteg1ML7Jo_Vdg/J--bFRcAe1Q.jpg?size=800x361&quality=96&sign=a794c840c9c991aacf803b272800301e&type=album', stream=True).raw)
    
    im2 = Image.open(requests.get('https://sun9-5.userapi.com/impg/1EjxBo1YHROx6wiaqtn4_lFcvgsJwejzLfb3Yg/OZ43HFTiSrQ.jpg?size=801x520&quality=96&sign=129699f505b246256a03043ca27dfd33&type=album', stream=True).raw)
    
    return im, im2

def v_13():
    im = Image.open(requests.get('https://sun9-50.userapi.com/impg/NazQ-nTzY-NPM_DJNqcGsJ_sszl_mIsAb2jj6Q/VtRS2A_gk8A.jpg?size=914x660&quality=96&sign=a439784a8cd8554c6ca384ef7a0feb07&type=album', stream=True).raw)
    im2 = Image.open(requests.get('https://sun9-39.userapi.com/impg/q976Lo36RGL9Itq1OPpphKuJj3G7qrxKo6xSHw/dBicZhRz66I.jpg?size=879x280&quality=96&sign=5db0d456b309b0fd5e6c86602a4ebd6b&type=album', stream=True).raw)
    return im, im2

def v_14():
    im = Image.open(requests.get('https://sun9-6.userapi.com/impg/ULX9-hQIOCeOMXEFS1pjFyTnf3RgFpodog5NiQ/hLOMRtboa0Y.jpg?size=1237x834&quality=96&sign=74bad49691418adc22a48dfa44887003&type=album', stream=True).raw)
    return im

def v_15():
    im = Image.open(requests.get('https://sun9-39.userapi.com/impg/cPkoq1aFm8Hfq2gu5trt-9tBIBlHsOq6a2h2IA/bPoVDpsU4sQ.jpg?size=1432x928&quality=96&sign=92df1682f2c12d3ae3a3d27c80c9ca68&type=album', stream=True).raw)
    return im
    
def v_16():
    im = Image.open(requests.get('https://sun9-17.userapi.com/impg/H7hcTaZjL7U1TNlRaQwB3eeU8yzrFj4YxdLSGA/i-Nkx-q8jZw.jpg?size=779x686&quality=96&sign=1e4329baa80942f61cae733453c6ca18&type=album', stream=True).raw)
    return im

def v_17():
    im = Image.open(requests.get('https://sun9-66.userapi.com/impg/7cTNccvqCepa7vrVNiHVxH2vO7Fkaz0o6ep9ug/phX9ifDlMko.jpg?size=949x629&quality=96&sign=8dfb4398c89b90f86076cdd7caf97e68&type=album', stream=True).raw)
    im2 = Image.open(requests.get('https://sun9-43.userapi.com/impg/2BM74Ji3iLMVDHPhkTe9sAudF3kIfm0d4wvCDA/PkhyXiV6GuQ.jpg?size=984x389&quality=96&sign=7d2f744104686d8d28872c47150fd9ae&type=album', stream=True).raw)
    return im, im2

def v_18():
    im1 = Image.open(requests.get('https://sun9-13.userapi.com/impg/z3b8zL6_Y60YfX0sRlkMIR1oDcREnbAI6ieu6g/LSN-muY_RLU.jpg?size=707x585&quality=96&sign=42690db14c90bd73543f7430ab2de30d&type=album', stream=True).raw)
    return im1

def v_19():
    im = Image.open(requests.get('https://sun9-11.userapi.com/impg/JIFKDlYIyKlci4ZW_mJtTSv7t5CkHpAhgnKQSw/WSrnQrdef7E.jpg?size=782x658&quality=96&sign=7d61322869aff7d07b3678776cb8de47&type=album', stream=True).raw)
    im2 = Image.open(requests.get('https://sun1-57.userapi.com/impg/NECSbbwzv9AZWc0RLEV4BLXRcpb-J6NipIPJrA/-rGsR_WU2bA.jpg?size=777x237&quality=96&sign=c0ef10881a8243fecac5098a1275ee2c&type=album', stream=True).raw)
    return im, im2

def v_20():
    im = Image.open(requests.get('https://sun9-63.userapi.com/impg/Mr7cz-seEj61TmY1ApKckogtMzO8k_u6RyHevQ/TBSC3OQZ9vk.jpg?size=1522x720&quality=96&sign=5cc95a37615104ad33cbaf9202c5eb92&type=album', stream = True).raw)
    im2 = Image.open(requests.get('https://sun9-8.userapi.com/impg/W1SZiOkKu1QdtoLkgZh3DwkB1WClGQGGO5gLGg/BkJAvVP3RwQ.jpg?size=1570x866&quality=96&sign=7dbd8517ceb47e3ed18fd4ea9cdac56a&type=album', stream = True).raw)
    im3 = Image.open(requests.get('https://sun9-7.userapi.com/impg/mhAtaUQYP-s4X5aZmmbUH3Y5IFIBGkD7widXww/3TBoYBUqN1U.jpg?size=1500x624&quality=96&sign=9ef535a41c59b852fe658ea52634db27&type=album', stream = True).raw)
    return im, im2, im3
    
def v_21():
    im = Image.open(requests.get('https://sun9-29.userapi.com/impg/Yv9j-vjxfPLFflnf39UhvybQi9r_lYaR57X-Cg/Gi_2bECHJoU.jpg?size=1280x877&quality=96&sign=93ae964e75517dbc6eaf05a078083a23&type=album', stream=True).raw)
    return im

def v_22():
    im = Image.open(requests.get('https://sun9-31.userapi.com/impg/-WcvaKEGlYgZBr8jJNz5IFYKRKXPraYAkY18XQ/gZe-sLhtTZk.jpg?size=891x332&quality=96&sign=22b09a7cb3eb661d25de359974ccaf5f&type=album', stream=True).raw)
    im2 = Image.open(requests.get('https://sun9-64.userapi.com/impg/vbvMg_IJOuibixJ83cmuuIfbW14JhrrZYutevw/KMq4GavKkiY.jpg?size=808x532&quality=96&sign=4a2109fff1d437ae2f27a673d9db812b&type=album', stream=True).raw)
    im3 = Image.open(requests.get('https://sun9-76.userapi.com/impg/gORsSVmbXGncldwh3rujqaPInP4lsRSD4yIH6g/5v5eBcPkwN8.jpg?size=868x455&quality=96&sign=164cec9424be191abd3d43cb53b2c9ed&type=album', stream=True).raw)
    im4 = Image.open(requests.get('https://sun9-72.userapi.com/impg/56-nplgce8EnRHr9gMBL0oOgd4ywwbk-IEq2Eg/W8Z1CusAgCU.jpg?size=747x500&quality=96&sign=a0ca42e9ed2936edbc71afe539b6313f&type=album', stream=True).raw)
    return im, im2, im3, im4

def v_23():
    im = Image.open(requests.get('https://sun9-72.userapi.com/impg/9j4bLWhgFQ8-Ke7oVgWUu39lOZAHQF7VpY5sJg/nJEXBAueNww.jpg?size=1607x455&quality=96&sign=7c389f0dc71aa480a040f879bbcd297e&type=album', stream = True).raw)
    im2 = Image.open(requests.get('https://sun9-55.userapi.com/impg/kcliC2kUx9M_8Els-_EWXTMi3lfD8S3OTAlBgw/9vhD6vWPT7Q.jpg?size=1442x1203&quality=96&sign=fb1f919afddc1a959134970f58879e64&type=album', stream = True).raw)
    im3 = Image.open(requests.get('https://sun9-56.userapi.com/impg/em3bGaNvOOHCRfFpW_O2XQXJsuqnbFP6dvBamg/LR9xhYj3z8U.jpg?size=1593x552&quality=96&sign=3312a3635df200cf36d861562ebe3f2c&type=album', stream = True).raw)
    return im, im2, im3

def v_24():
    im = Image.open(requests.get('https://sun9-32.userapi.com/impg/ZSEfqtbaGZ0_cU5lzfcqmDw3BpK4hhPZJRFaPg/KQbM4-tC_IQ.jpg?size=685x130&quality=96&sign=a980a15d4345433cab49b1bb619a3d4c&type=album', stream=True).raw)
    im2 = Image.open(requests.get('https://sun9-54.userapi.com/impg/3IC_5P6ZPQI_mG-MnCCXwME06GHWRuGdKUjuOg/v4w36gqI9qc.jpg?size=678x424&quality=96&sign=7d24b10847ad99da51dce0baf36509eb&type=album', stream=True).raw)
    im3 = Image.open(requests.get('https://sun9-29.userapi.com/impg/sbNZ3UEADcnmJAsvTTWM31pPZgB4gfpX9t233Q/b31EAzEnD_A.jpg?size=752x440&quality=96&sign=0c2f76c1a97678c1b1a9dd7f1471b2be&type=album', stream=True).raw)
    return im, im2, im3

def v_25():
    im = Image.open(requests.get('https://sun9-50.userapi.com/impg/2KPPiQJJVDBZRrdh-BVVRAEt76DsCpurpNavbg/EUa0IvPwTRg.jpg?size=900x746&quality=96&sign=818b36a93a0f3ec513ba352a3c4ac3e8&type=album', stream = True).raw)
    return im

def v_26():
    im = Image.open(requests.get('https://sun9-27.userapi.com/impg/dOvviPbr0ciHh51k82_CgYYEV3y3-KimDXsEVA/9MGfJZvvl_I.jpg?size=772x301&quality=96&sign=31cf62639b988b45a92c4e3c1934842f&type=album', stream = True).raw)
    return im

def v_27():
    im = Image.open(requests.get('https://sun9-56.userapi.com/impg/GLJN546HIKVgr5QmY1IXs82ACJ8iY5Mmqjdk5w/J1NeSCE_DbY.jpg?size=886x224&quality=95&sign=968424a940bee6d3152aa3305923931a&type=album', stream=True).raw)
    return im

def v_28():

    im = Image.open(requests.get('https://sun9-43.userapi.com/impg/THOrImzC97SaJ-MyMbaSvK45Ub-XzeZVNS9QXw/nQivPnXeBBE.jpg?size=803x217&quality=96&sign=d0f8f34d5946b38edaee6d2e5edb8c62&type=album', stream=True).raw)
    
    return im

def v_29():
    im = Image.open(requests.get('https://sun9-50.userapi.com/impg/HIlZQXxItx_Ig3wm8vpEA6Q2jS95xHUWWHJjIw/w1Yzqlge0a0.jpg?size=900x359&quality=96&sign=1bc2ffccfcc0cbf00aa1e85f2f0a3580&type=album', stream=True).raw)
    return im

def v_30():
    im = Image.open(requests.get('https://sun9-40.userapi.com/impg/Z1Yak-dvOwLbvjp93UglqU-esg2wsRalyANBDQ/RyQA7KnmQh8.jpg?size=892x378&quality=96&sign=067dce9b90672a3036804ca4cd45e39d&type=album', stream=True).raw)
    im2 = Image.open(requests.get('https://sun1-23.userapi.com/impg/QUJ8qiwLNRBc1y_6QfxJG9q5_Se1u4KsGq9E5w/amtQ4fs_3Jc.jpg?size=913x661&quality=96&sign=8271e6c7e589b1973542552e1f705624&type=album', stream=True).raw)
    return im, im2

def v_31():
    im = Image.open(requests.get('https://sun9-12.userapi.com/impg/AMI2qYuWwp0xYd4UY_rQncvGfxGLvp42_QfnpA/1e6qEC9Hkd0.jpg?size=1432x928&quality=96&sign=3e70ecc9217bfcbeb4e385baadabc902&type=album', stream=True).raw)
    im2 = Image.open(requests.get('https://sun9-43.userapi.com/impg/ZsREs3OF7K75gS5tXV6qgJonA3iPwdQnmQyKqw/gVYB5oEs5PY.jpg?size=1432x1266&quality=96&sign=200a606468b49016a114283e20257196&type=album', stream=True).raw)
    return im, im2
    
def v_32():
    im = Image.open(requests.get('https://sun9-9.userapi.com/impg/0BJ7QH3fVB3x4yUqdv_r6g-KppyuGEvoHZWI3Q/HsAyeg3K4Mw.jpg?size=644x723&quality=96&sign=ae44ce1719dd711b0584914531627c14&type=album', stream=True).raw)
    im2 = Image.open(requests.get('https://sun9-9.userapi.com/impg/IhKvrIFIdnnGj5AxgazFDW2CalLBpDc6uo2ooA/FOFWE7Jc3ok.jpg?size=774x596&quality=96&sign=87b2a4e4f5bb3207b297a82a30aac11b&type=album', stream=True).raw)
    return im, im2

def v_33():
    im = Image.open(requests.get('https://sun9-33.userapi.com/impg/fTWMXVz9ADIJydDB7KSbSZGlpuqFfV03AS-dJQ/yGRa8l4rE0k.jpg?size=984x644&quality=96&sign=ce522f13e2072d05c897750d6a4b1bad&type=album', stream=True).raw)
    return im

def v_34():
    im1 = Image.open(requests.get('https://sun1-26.userapi.com/impg/Nw6WapjqiPKU3kPGAvKAB8vDVC1F1QjR2PPePw/MO63DPsY0gU.jpg?size=712x488&quality=96&sign=c5bff57e100981e39154592f543b58c1&type=album', stream=True).raw)
    im2 = Image.open(requests.get('https://sun9-40.userapi.com/impg/hEoiM2YKZoAVbP-FhQ1nz15bMlvA7pEJaVT5tA/DaQcr4u7yH8.jpg?size=705x496&quality=96&sign=5cbee58972354a9436938d5dff724968&type=album', stream=True).raw)
    return im1, im2

def v_35():
    im = Image.open(requests.get('https://sun9-44.userapi.com/impg/3OB76mwq3BxFcUNFySEV9wkQJkOPw56HwYli5w/eYMDN7Kk3Sg.jpg?size=801x522&quality=96&sign=24d9b27339cb9fb0b8e0e4b380b47ac8&type=album', stream=True).raw)
    im2 = Image.open(requests.get('https://sun9-3.userapi.com/impg/rgW_5cVGhvUOp51VnZVmTrxaWoGvllxmf9K3gQ/HgwBO7Qf5ms.jpg?size=779x469&quality=96&sign=9af8804ae320b42ca2eac681cfdecf11&type=album', stream=True).raw)
    return im, im2

def v_36():
    im = Image.open(requests.get('https://sun9-28.userapi.com/impg/tS1_N5GYgHw6tbF3SOCQ_QiMTpw3fwE_z9E2sQ/0DHkFiR2WqU.jpg?size=1514x1158&quality=96&sign=890802ae940eba033b5a49416e028ccb&type=album', stream = True).raw)
    im2 = Image.open(requests.get('https://sun9-32.userapi.com/impg/8h7HTPcKY0iZfKDKakKCd2RA2PdC7ijNO3SqmQ/bOOSPxZXhew.jpg?size=1508x1052&quality=96&sign=15dfd5f5e090bc8f19c4a4bc3e58aa0d&type=album', stream = True).raw)
    return im, im2
    
def v_37():
    im = Image.open(requests.get('https://sun9-69.userapi.com/impg/5pkN_eejL7JPo8NvAN2epCGOluIikEh0vbMFDw/_qkVd9w3Peo.jpg?size=1280x715&quality=96&sign=9cb4b4c37be0419c35f899acb7171482&type=album', stream=True).raw)
    im2 = Image.open(requests.get('https://sun9-72.userapi.com/impg/h7T7QSJs7mDHMkivZ5TylE9y1gEt_Fg0xLJU-g/uXpGjiQgeJs.jpg?size=1280x1022&quality=96&sign=461d9bad098bee74f69cc8d2278ba269&type=album', stream=True).raw)
    im3 = Image.open(requests.get('https://sun1-19.userapi.com/impg/69JnaudMJNQx54IDIkeDitTZoOGOCNFC8dE8eQ/fkpdBanyNtY.jpg?size=1280x461&quality=96&sign=8783ca747b7361bd854919ab9859a466&type=album', stream=True).raw)
    im4 = Image.open(requests.get('https://sun9-23.userapi.com/impg/Uzg87nQIgYQvk7V2qAm7AiCEaIqSLJmQ0hL1NQ/4xYancWIQTs.jpg?size=1168x836&quality=96&sign=b4ff333ef9ed469d60d38ca9bc1c21d1&type=album', stream=True).raw)
    return im, im2, im3, im4

def v_38():
    im = Image.open(requests.get('https://sun1-47.userapi.com/impg/SzfoL0C-pR3VY7daTsZQUiWyy2yb1FfGUjXZfg/7YoJmTWoJLY.jpg?size=643x714&quality=96&sign=bb8d4f016d48c3f76b8bb43ee87cf9a1&type=album', stream=True).raw)
    return im

def v_39():
    im = Image.open(requests.get('https://sun9-56.userapi.com/impg/UOF3TMh9pm0XrC6ZcFyhUdzf937VMos1MrL73g/JBbxDs7e8SE.jpg?size=1616x730&quality=96&sign=765be4d3878a5aab57a7512e4e7a57af&type=album', stream = True).raw)
    im2 = Image.open(requests.get('https://sun9-5.userapi.com/impg/rm2vkjmZpFgv8Chlk_RJTB1WvkWiueuQgtA_OA/v9mfUVg1lHg.jpg?size=1004x686&quality=96&sign=d91875febfea21d973f40eebc307a77c&type=album', stream = True).raw)
    im3 = Image.open(requests.get('https://sun9-5.userapi.com/impg/s2gNamFvrD_qwrNfObTZH39gHN-t94E38YVB5w/I58B63BhHsg.jpg?size=1607x744&quality=96&sign=ba8ddeba340cc82412257573b4bbf60b&type=album', stream = True).raw)
    return im, im2, im3

def v_40():
    im = Image.open(requests.get('https://sun9-77.userapi.com/impg/Id_4dYIDwLYhgw8pgVG63CDWNR5v_NS2OSjiHw/o8q0peTRFzs.jpg?size=817x451&quality=96&sign=8980be28c7d9e2938d43725d8e4b38f7&type=album', stream=True).raw)
    im2 = Image.open(requests.get('https://sun9-46.userapi.com/impg/6JkadHOIPZI1u4KBhWvO23mQ8xbK0cYHY1_AjQ/usTWNl_uYIg.jpg?size=800x449&quality=96&sign=b076b0c07065f056486fc4b0aec29d0a&type=album', stream=True).raw)    
    im3 = Image.open(requests.get('https://sun9-77.userapi.com/impg/ixXn55zCrLcYsRNT91lDe_IxA6M1sRE1uI7QBw/6NLmSmimy50.jpg?size=864x487&quality=96&sign=163ea291fd60a4ab16024a8f4e58d7af&type=album', stream=True).raw)
    im4 = Image.open(requests.get('https://sun1-47.userapi.com/impg/vbt6BXs2bplTiNHS1oW9Zf_cSFUFKE0N8CCi2A/OcSbyRk4hUo.jpg?size=1026x722&quality=96&sign=c6ff86ef99a0274f77f9c7e9cecfc03b&type=album', stream=True).raw)
    return im, im2, im3, im4

def v_41():
    im = Image.open(requests.get('https://sun9-10.userapi.com/impg/fab_YS_PQvGhPMN69dSQDG-LD8Qh4t45tcGw_g/UNX9ZUIzTJg.jpg?size=903x455&quality=96&sign=c8ff2ad35073d5d59e1ec9af91e39faa&type=album', stream = True).raw)
    return im

def v_42():
    im = Image.open(requests.get('https://sun1-91.userapi.com/impg/WFCC0waKGs86vKqApIBN83ZBOAYFGUhWweNsbA/vh6Nu_Sxi9w.jpg?size=884x352&quality=96&sign=43a06d81cff93a13495ee1566337e131&type=album', stream = True).raw)
    return im

def v_43():
    im = Image.open(requests.get('https://sun9-15.userapi.com/impg/9pLw6bNHIfHMdwZ_JcxPDObE3bMviAhkGwpf0A/q2TStGvz0Y8.jpg?size=879x563&quality=95&sign=5fc0224a8ee1284d5e154f2c399908f5&type=album', stream=True).raw)
    return im

def v_44():
    im = Image.open(requests.get('https://sun9-41.userapi.com/impg/R-AeeG4w0Q9fnW-y5mGZTTWge4T1NYVqGJEnSQ/z2Cjx1jkFq0.jpg?size=810x538&quality=96&sign=7269d1cc5d8195881be5fb68a510d859&type=album', stream=True).raw)

    im2 = Image.open(requests.get('https://sun9-4.userapi.com/impg/fT-HmZLGU2G0ig-ynIlmIlwCmbZx90bphb2MkA/aBBT_qcvK0w.jpg?size=811x330&quality=96&sign=4f884c3c79427b441ed283ad6231736c&type=album', stream=True).raw)
    
    return im, im2

def v_45():
    im = Image.open(requests.get('https://sun9-77.userapi.com/impg/ysnMocBm7AMFftHnJg5hyRCklyGCD7gPhjwSYQ/nWqSDVjbF_0.jpg?size=900x482&quality=96&sign=dc7ff6ad6e881476bf51de44ea6abec5&type=album', stream=True).raw)
    return im

def v_46():
    im = Image.open(requests.get('https://sun9-14.userapi.com/impg/ypAjw1glIlXWU0Owddmoc90aK-8iU-IBC4-atw/RTksBGBQUvc.jpg?size=883x600&quality=96&sign=01b0a4d1d6c5177958a7de8bcb2d7e35&type=album', stream=True).raw)
    im2 = Image.open(requests.get('https://sun9-16.userapi.com/impg/c7q79DFxBKDYOMp35Pw1Noob_OFW5EQyY1udjg/KP_Za0vhmgw.jpg?size=879x507&quality=96&sign=8711f29b52c047b6422a6536aca2f74b&type=album', stream=True).raw)
    return im, im2

def v_47():
    im = Image.open(requests.get('https://sun9-72.userapi.com/impg/C1MGuGvaxF2mPgf-ycJyRHYAajBpa4b_TDVzYg/tYDRjRWjxI8.jpg?size=1432x1354&quality=96&sign=060206dc757b7b1608a5eb8a98f2ae07&type=album', stream=True).raw)
    return im

def v_48():
    im = Image.open(requests.get('https://sun9-42.userapi.com/impg/7DDYm5lQ5HUvyGe4sE45vpNcmXRD59K9EjiYng/D7mN9n3sYiw.jpg?size=781x769&quality=96&sign=d294d3564129fa3e74b8b9e08c296dae&type=album', stream=True).raw)
    im2 = Image.open(requests.get('https://sun9-34.userapi.com/impg/_gUruRTCiEhBiHsJLy_mRGYDGePS4zee3JTnkw/bz8XMPyjwMU.jpg?size=774x404&quality=96&sign=6d94315550e27581822f8e4f92e22b13&type=album', stream=True).raw)
    return im, im2

def v_49():
    im = Image.open(requests.get('https://sun9-78.userapi.com/impg/n72L1BLYCFQzG7-UA7EmWL-eC0IJDtoZFTmi-Q/Wb0lip78lyw.jpg?size=980x637&quality=96&sign=8a180521b4aca9bfd95eb1133e6363d4&type=album', stream=True).raw)
    im2 = Image.open(requests.get('https://sun9-41.userapi.com/impg/soPyp0nhy6YmWoGKofY86qwe97Zc2msW3eaakA/mYIPgE7ergw.jpg?size=984x472&quality=96&sign=d27f9a4452bd5ae8ec21ca1cb498f144&type=album', stream=True).raw)
    return im, im2

def v_50():
    im1 = Image.open(requests.get('https://sun9-65.userapi.com/impg/MotZdiwYUKS3-nxcIMkQy-kwPp1mm-wT381tuA/AgkzxHfTFLk.jpg?size=699x96&quality=96&sign=76c6033799ce7d7cb0d4238cf6ca1f7c&type=album', stream=True).raw)
    im2 = Image.open(requests.get('https://sun9-29.userapi.com/impg/8PRHkXZCYKB3fNjgRydDN5vmuZuNfe2gBFfEKQ/WFSzumP0nbI.jpg?size=561x640&quality=96&sign=ba07527e9900f29f0124acfc1c340a47&type=album', stream=True).raw)
    im3 = Image.open(requests.get('https://sun9-7.userapi.com/impg/yARYgZzUw_NxFxZTzlKlSvjQ_aHcsmX5PtbtKA/VcA5hqQJ9a4.jpg?size=690x500&quality=96&sign=120f8096e3e7237a7c6c9b32420fe116&type=album', stream=True).raw)
    im4 = Image.open(requests.get('https://sun9-46.userapi.com/impg/P6vcX7MNrHe9UE8eZMIwkwIokvrskC3kU-6SuA/0sU0KI22bcc.jpg?size=860x90&quality=96&sign=8064802d24742d6f3b7ee00baa4f6213&type=album', stream=True).raw)
    return im1, im2, im3, im4

def v_51():
    im = Image.open(requests.get('https://sun9-12.userapi.com/impg/Kp2C0CSSd3xOymtDrJAbG5OQYFLsQGtQR-G3Qw/CD1rdd17eLw.jpg?size=797x847&quality=96&sign=a1a832295ea690f52da917a68bbddf14&type=album', stream=True).raw)
    return im

def v_52():
    im = Image.open(requests.get('https://sun9-75.userapi.com/impg/dmosIR7FApl8HZeD4fNy6fyg-EwayQxNFCrfzg/K_Pa1J6YmQo.jpg?size=1540x948&quality=96&sign=7256fb8c4d8c71d71fe8a82f81dd6c9a&type=album', stream = True).raw)
    im2 = Image.open(requests.get('https://sun9-40.userapi.com/impg/XhBPEf_fIk7VsygoOub9Z1GfR2Jq_iB5KeoicA/VaVcuvEtfAQ.jpg?size=1520x828&quality=96&sign=82a40619dfb8d9cc8403873d32341dfb&type=album', stream = True).raw)
    im3 = Image.open(requests.get('https://sun9-29.userapi.com/impg/KjkF-1Y6YrFVvXItpnNENksc5mmBRGO8L_14lw/529hLgCz20U.jpg?size=1522x958&quality=96&sign=0bcce3d403a07566d456806bf946f210&type=album', stream = True).raw)
    im4 = Image.open(requests.get('https://sun9-4.userapi.com/impg/uAhzCPcKXcxuKjE-7sSt3que2K5_1OdcTy30Ew/qdokH2GW51o.jpg?size=1492x596&quality=96&sign=b05950b953f84f89bab4de95fb892e63&type=album', stream = True).raw)
    return im, im2, im3, im4

def v_53():
    im = Image.open(requests.get('https://sun9-7.userapi.com/impg/UuolK-48Qdt_OeUorgQidWA4X6S-gPuyWtoM2Q/CpC1dz0TUDA.jpg?size=1280x751&quality=96&sign=d3bd7fae6929a6ff297832560f2b3d70&type=album', stream=True).raw)
    im2 = Image.open(requests.get('https://sun9-31.userapi.com/impg/4lLI5eJw-BUZQWeeWBplOgkbkvcDr3ZOVo2DPA/NqQLARDTTtg.jpg?size=1280x979&quality=96&sign=a77a143902564ca0d7b53b605b53e1d3&type=album', stream=True).raw)
    return im, im2

def v_54():
    im = Image.open(requests.get('https://sun1-93.userapi.com/impg/eFQLoU_b26eRsjME-jhTSzyr8ryZrPHxXHjwxg/uFnvv7lSKGY.jpg?size=898x459&quality=96&sign=48884a4aa592215f89c45dc6230938d1&type=album', stream=True).raw)
    im2 = Image.open(requests.get('https://sun9-40.userapi.com/impg/tccm0ta7gUe5R13i0OfgPasnIaGGr__Y6swLGw/lSRrIiOdZSg.jpg?size=882x400&quality=96&sign=2ca3fb727216c4bdfbc42b83e8b2a3c7&type=album', stream=True).raw)
    im3 = Image.open(requests.get('https://sun1-27.userapi.com/impg/bYitQUEihKHozOYcVaaZ767j13paco4_nJi3aA/z6ZmzWeLj90.jpg?size=868x310&quality=96&sign=76b56d530357b2d220c4198621cf3e86&type=album', stream=True).raw)
    return im, im2, im3

def v_55():
    im = Image.open(requests.get('https://sun9-25.userapi.com/impg/kUK6xLI9R328V3yDJIwYc3Rq-yNnQkly1D-Dkg/aQBMIXhcexo.jpg?size=1650x967&quality=96&sign=d0b2de9d546c38bf25918df32d05b304&type=album', stream = True).raw)
    im2 = Image.open(requests.get('https://sun9-12.userapi.com/impg/Fr2GuDZNwT35XGxVTVv-VS2Ye9GYmktamxN6Yg/ZC3y_m5G5Zc.jpg?size=1622x462&quality=96&sign=8485d89ec8264b7d12c411f45749b06d&type=album', stream = True).raw)
    return im, im2

def v_56():
    im = Image.open(requests.get('https://sun9-16.userapi.com/impg/5j2HnkDA73LNcnJBTnX2drfciqqcoqfr3J-tzw/_fJ1wA8uP8M.jpg?size=1003x636&quality=96&sign=5efd14f75928bcc4ae46c66136af6b3e&type=album', stream=True).raw)
    im2 = Image.open(requests.get('https://sun9-60.userapi.com/impg/7X6t-7om9KzUvzq4q39a1JlaxjgDfsoSzsJn7A/gBy11mvVfZI.jpg?size=1009x586&quality=96&sign=e0a1cfb0dc67e1bf1ae416503269b163&type=album', stream=True).raw)
    im3 = Image.open(requests.get('https://sun9-21.userapi.com/impg/ecHYjNxvWIbXmH56KcmOxWLN0sfGyjb60IcGJA/a3UJ3UOk9r4.jpg?size=962x398&quality=96&sign=a04bc1b567eb527194c611fcb3cba35d&type=album', stream=True).raw)
    return im, im2, im3

def v_57():
    im = Image.open(requests.get('https://sun9-59.userapi.com/impg/r6FWj26P4jkIIuj6SxuyAPljnj4XkVMIJOkF3g/K6lX5RR8FTI.jpg?size=898x370&quality=96&sign=2b874079c9a8cc2f4633b4a5d15075d9&type=album', stream = True).raw)
    im2 = Image.open(requests.get('https://sun9-38.userapi.com/impg/rgvPvmIrS7vZ5-k8Tr3FBi1FMbe4WghGMO4ddg/ApRHDxfFu0s.jpg?size=583x705&quality=96&sign=c813c0f1e0585bdc98a43b92e97160e1&type=album', stream = True).raw)
    return im, im2

def v_58():
    im = Image.open(requests.get('https://sun9-44.userapi.com/impg/-XUQx_SGzi3WCZEl1XVHldAty8HqEKiU9n618w/_L9rHFqF9Yk.jpg?size=787x718&quality=96&sign=1851628b5b33f165a54df712cd75a16b&type=album', stream = True).raw)
    return im

def v_59():
    im = Image.open(requests.get('https://sun9-76.userapi.com/impg/erW574lpJaX9x8NCK3314myqjZsGkkS4f3_4UQ/DWw6Wkc_GbY.jpg?size=876x646&quality=95&sign=280d5fb06abcafbff67d2bb9eb658c62&type=album', stream=True).raw)
    return im

def v_60():
    im = Image.open(requests.get('https://sun9-35.userapi.com/impg/FrUhTqEXsjU67gq25sDCmomw9HImFXFLmZsNGw/UIYWuxwHAKo.jpg?size=812x382&quality=96&sign=768b621840045ee14f7294b2a69f8d0f&type=album', stream=True).raw)

    im2 = Image.open(requests.get('https://sun9-9.userapi.com/impg/HF2reIbSAqFuOUTjGzfZE6gCti_pQGXFvzHd6g/1zQ8tOc3Sy0.jpg?size=812x578&quality=96&sign=59ad61ad0612d5524b1000ccdb41b1d8&type=album', stream=True).raw)

    return im, im2

def v_61():
    im = Image.open(requests.get('https://sun9-51.userapi.com/impg/6w6QNDvkkCk9U6PF2WG3UFAWsxTK_RAYDPCsrQ/RDFjL3eybo4.jpg?size=917x615&quality=96&sign=4dc32ab4470c8e16e2f79e0101cf3aac&type=album', stream=True).raw)
    return im

def v_62():
    im = Image.open(requests.get('https://sun9-15.userapi.com/impg/rIrvO_GaT9R4LCtl0wRw5AN20Vh-TdO3ArVVJw/7R0ydHFLRqo.jpg?size=882x748&quality=96&sign=97a7d0dbe554d84fb3bd012c695db0b9&type=album', stream=True).raw)
    im2 = Image.open(requests.get('https://sun9-80.userapi.com/impg/XJ8gz2EpXxKBFSJsfwV10pTA-xcxmYHA1MMQpg/YfVvusnOx_A.jpg?size=788x771&quality=96&sign=43d702876c65b668cc43cc2550911c22&type=album', stream=True).raw)
    return im, im2

def v_63():
    im = Image.open(requests.get('https://sun9-37.userapi.com/impg/JFRjrod_Y6XOkm6_C1cFqyiUuXgrOsdDO3HfTQ/B6nXE6B6HMg.jpg?size=1432x1204&quality=96&sign=a9e5515b1698c6ac8b2410b69774d95f&type=album', stream=True).raw)
    im2 = Image.open(requests.get('https://sun9-20.userapi.com/impg/XGcxK5uVKcf9wURJPV-htWdp8u-tIhVOYtlIqw/sfnoy4RacaQ.jpg?size=1432x1070&quality=96&sign=5b23931a4b61e5905ce2ab136fb7b41e&type=album', stream=True).raw)
    im3 = Image.open(requests.get('https://sun9-27.userapi.com/impg/YNMw7mIWA91kT1xMFlJsGiQe0y4A9R6f1-bjvQ/LS3msxf9zMM.jpg?size=1432x1040&quality=96&sign=87ba22d7d0008ba91c17fe1bc74ce39d&type=album', stream=True).raw)
    im4 = Image.open(requests.get('https://sun9-29.userapi.com/impg/bshwyQaueywv2db87u-qT20geyU_RwGL_qQ15Q/fH9BZTQp0zg.jpg?size=1432x632&quality=96&sign=d94d163443e50c546b8acab3cd6e3e2a&type=album', stream=True).raw)
    return im, im2, im3, im4

def v_64():
    im = Image.open(requests.get('https://sun9-34.userapi.com/impg/xBgAHYszqTIXTz2fy-GoZn9sKVyDUUxne3pGFA/HHhmt1maMDM.jpg?size=774x652&quality=96&sign=c4f9119d0cd7e12b67f93d7fe9569e58&type=album', stream=True).raw)
    im2 = Image.open(requests.get('https://sun9-59.userapi.com/impg/EIGiCxJPR_gNXkBgdGNk8i39TIH3LPGdPHPh8g/tQc-SmaL_Cw.jpg?size=775x512&quality=96&sign=d8383cfb566af3f2615370e459170892&type=album', stream=True).raw)
    return im, im2

def v_65():
    im = Image.open(requests.get('https://sun9-43.userapi.com/impg/F_4YP45XIbGDtEFjYesikFZU6sw9H0DZK5_6AA/2NuNCQbS-QA.jpg?size=992x707&quality=96&sign=47c22e7de74d09ffb9338419c39ce833&type=album', stream=True).raw)
    return im

def v_66():
    im1 = Image.open(requests.get('https://sun9-61.userapi.com/impg/PdgvwqvmkN_qyfLw2m0TWVyRR3RJsnC4uegFhA/3ga07Pf74Ck.jpg?size=615x636&quality=96&sign=e50dfbebe2ed488f7da3625838238e02&type=album', stream=True).raw)
    im2 = Image.open(requests.get('https://sun9-17.userapi.com/impg/VrOop-N9nHHq09rroMhMgYFViDtW2Kankk0GuQ/89JWzEwLIqw.jpg?size=894x108&quality=96&sign=208865b1212e8f32791c50250b6e0c69&type=album', stream=True).raw)
    return im1, im2

def v_67():
    im = Image.open(requests.get('https://sun9-43.userapi.com/impg/L6wGdGk_RZGG3nhAu6ek-AqwuGQgGvuRIqCPmA/HxsyHqY2tas.jpg?size=770x316&quality=96&sign=d99edc28143a9fa533689a69c8a6e04f&type=album', stream=True).raw)
    im2 = Image.open(requests.get('https://sun9-27.userapi.com/impg/b4HH-Y_0JC22_n4ObgZ8sQwqq23pQxeq8qHmlw/-IHyKjGl3DY.jpg?size=576x720&quality=96&sign=9ea3fc55edd2ef82e67c14eb1f7445fe&type=album', stream=True).raw)
    return im, im2

def v_68():
    im = Image.open(requests.get('https://sun9-43.userapi.com/impg/fMt2oIGLzJJC-rISLK3f-8iR6qazi9FvdY1K9A/bIKS7XmUzsM.jpg?size=2126x1000&quality=96&sign=b973d80eed71f721c270cb42eb27d287&type=album', stream = True).raw)
    im2 = Image.open(requests.get('https://sun9-61.userapi.com/impg/62rsarCV0RXAp0VWOY2aPImgD6Qw2t_Xv7yu7g/OfACJQ0oOtg.jpg?size=1516x1246&quality=96&sign=c453f67e2a99de6c11d71f21eaca697a&type=album', stream = True).raw)
    return im, im2

def v_69():
    im = Image.open(requests.get('https://sun9-77.userapi.com/impg/wwsHmBk7m731_oUyT4-4ZLKx_uHhNQq8S3D0rQ/nAkpV7p_1bY.jpg?size=1280x371&quality=96&sign=053b1a5908e468df2ebceb7d62766079&type=album', stream=True).raw)
    im2 = Image.open(requests.get('https://sun9-41.userapi.com/impg/hhQ3ghD55pl8BJ2r3sob_dorWtjKN8G_913aAg/I0aXPnFWW14.jpg?size=1200x710&quality=96&sign=0988431fb416b4f836f0c41a300ee191&type=album', stream=True).raw)
    im3 = Image.open(requests.get('https://sun9-79.userapi.com/impg/2tYpoT1Zzowrbn18S_HA7giKElp2dkXLtSOTPA/LVZh7sqFQC0.jpg?size=1023x1080&quality=96&sign=5132f03f0567905f5ea02725e4693eff&type=album', stream=True).raw)
    return im, im2, im3

def v_70():
    im = Image.open(requests.get('https://sun9-22.userapi.com/impg/rtxvnJWNrWvPOWvjTE-4JStW0_xXxConNmvuuQ/Gm-MpzRUa3I.jpg?size=892x582&quality=96&sign=f0bf3328a61b03540ac83eca257cf849&type=album', stream=True).raw)
    im2 = Image.open(requests.get('https://sun9-24.userapi.com/impg/VnPAtAavaE6O8GCMCQdFDRmMbBA5uyFrpCA9MA/nqMXHFVjUrQ.jpg?size=582x596&quality=96&sign=a7054d968c3e6a7ed5267ddae668a416&type=album', stream=True).raw)
    im3 = Image.open(requests.get('https://sun1-14.userapi.com/impg/qBMAnAEnn1PrUp53kDPfdTTchHGCKVUVFu0MHA/c3QabqvZGY8.jpg?size=881x804&quality=96&sign=c169800d8191e6b4ae33f4c8c4de999d&type=album', stream=True).raw)
    return im, im2, im3

def v_71():
    im = Image.open(requests.get('https://sun9-56.userapi.com/impg/CvFZ4AfDOEfHzr3D2C5Tgy3KXHPx3leIuaOAlw/mDtO0s4ZBb8.jpg?size=1667x825&quality=96&sign=445ea2da705d8dce63ee10af0fb0df66&type=album', stream = True).raw)
    im2 = Image.open(requests.get('https://sun9-7.userapi.com/impg/lHwE9ShT0YojhXoRGO-1ldef_7blU1-Dvn04Vw/3CDSPEn7d9c.jpg?size=2120x894&quality=96&sign=1eda2dc5506219755efe355df5f1eee0&type=album', stream = True).raw)
    return im, im2

def v_72():
    im = Image.open(requests.get('https://sun9-70.userapi.com/impg/8Pe7A1UgZVNEynxCDJY9Azasw2HGSyb5PCtT_g/7e2Z9wyL6qs.jpg?size=975x601&quality=96&sign=808e53c5fc69ee2d2dda3a6a073d495f&type=album', stream=True).raw)
    im2 = Image.open(requests.get('https://sun9-35.userapi.com/impg/qEgdcPy-Vm3N95uRymUiAMeAf4DlHSD-rwjDcg/AcoTvHxOoU4.jpg?size=598x427&quality=96&sign=33da780022d9053ab36b4834c03eaf4b&type=album', stream=True).raw)
    return im, im2

def v_73():
    im = Image.open(requests.get('https://sun9-12.userapi.com/impg/15_XN5bR0e1F_VcSyxNF7nhA6X6DPSsaO7fHqA/zOQJHVLLQ3s.jpg?size=801x684&quality=96&sign=d0eb80c4b2c199e03083b8835e877482&type=album', stream = True).raw)
    im2 = Image.open(requests.get('https://sun9-30.userapi.com/impg/oSG-iekDb-dBNxxfqhUkHO0i0cwRI6yTxftO3A/yyxrGboE5h8.jpg?size=573x436&quality=96&sign=813dd9bd68a7f54a8c847dadb6c02194&type=album', stream = True).raw)
    return im, im2

def v_74():
    im = Image.open(requests.get('https://sun9-70.userapi.com/impg/Rs-lrw2N2e-M9EZGPK4pUTznrQP-T3-VtEXL0Q/PZCPBP4bydo.jpg?size=799x376&quality=96&sign=07551bc6352fd04d6cbb7d67868ca09a&type=album', stream = True).raw)
    im2 = Image.open(requests.get('https://sun9-18.userapi.com/impg/2z8qkodhIHc9gRld92zSUQAcOOidR4T6M-d8hA/4xOqGCc27TI.jpg?size=888x546&quality=96&sign=8dd0272be434fcaedb7f969af8042948&type=album', stream = True).raw)
    return im, im2

def v_75():
    im = Image.open(requests.get('https://sun9-41.userapi.com/impg/VFSVmyZXyVeHkNVqWohvxPHUOZ1ny3pq9EH-fw/4EkcjkX0LoE.jpg?size=890x439&quality=95&sign=6bb6ca22eb57ab5cbf5e37156f28838d&type=album', stream=True).raw)
    im2 = Image.open(requests.get('https://sun9-35.userapi.com/impg/m6yHMWwQEUv1E2ijbJ3K7M0xYTfh8M4DYuX0Rg/R7-3XC5Nrjs.jpg?size=883x441&quality=95&sign=0f12162d4a365c8aa3720ad329ed4ec6&type=album', stream=True).raw)
    return im, im2

def v_76():
    im = Image.open(requests.get('https://sun9-11.userapi.com/impg/oCBmwJcBTDoq0qcM8Sct1-IasrP7j1doCMUKJw/WFIK_LX7LmM.jpg?size=810x551&quality=96&sign=b6ba75a81e6a2183bffaf442fc87a7d2&type=album', stream=True).raw)

    im2 = Image.open(requests.get('https://sun9-73.userapi.com/impg/BdByV3D-6Wqo_0UroY9cLMOXbXDje8_XTs8jYA/Xm3do3-5H3Q.jpg?size=810x485&quality=96&sign=76fcb7de4606d5a0f27794d744802397&type=album', stream=True).raw)

    return im, im2

def v_77():
    im2 = Image.open(requests.get('https://sun9-16.userapi.com/impg/e_ydSqKKVXG9uXtVB-BPob_VRv1zox41vf_aLA/VtKGwL-X8C8.jpg?size=881x440&quality=96&sign=ef1d6d41f068cc42859306d820109ed0&type=album', stream=True).raw)
    im3 = Image.open(requests.get('https://sun9-75.userapi.com/impg/cOACoCWluneWFzGuinNnSp0DXAOHsjYOTlcO6Q/WxavqfUv-RM.jpg?size=891x586&quality=96&sign=496e3482da06237a9cd9c403e99fe1ad&type=album', stream=True).raw)
    im = Image.open(requests.get('https://sun9-11.userapi.com/impg/of39FQpto1FBK3sHOjom8NsuLar8rvI-uf0n-w/j_Ul-6f11u0.jpg?size=675x684&quality=96&sign=3c649ba894e061448bc52d631de8c9bd&type=album', stream=True).raw)
    return im, im2, im3

def v_78():
    im = Image.open(requests.get('https://sun9-78.userapi.com/impg/oJ9aUWc-B74uj4CYUuQYD00Yo7Q2HAgmL8RG9g/OCJFqo8QWf4.jpg?size=826x793&quality=96&sign=496743cb33c769f16cefd9d8a50c9e72&type=album', stream=True).raw)
    im2 = Image.open(requests.get('https://sun9-69.userapi.com/impg/_6B7SHQ6YJJDw5gymAuAxkKWZ8SXOWSjuNzSwA/xhaia48XCjg.jpg?size=903x470&quality=96&sign=9186e1e8cfa6d5219712d441a8a6af8a&type=album', stream=True).raw)
    return im, im2

def v_79():
    im = Image.open(requests.get('https://sun9-42.userapi.com/impg/BZjqiipVHkhb6vLDa6qS9j5j-PBQuZmeKmcMzw/k8LOiiMAD6w.jpg?size=1432x866&quality=96&sign=16f80e62281e50a3af5774fbe8151a09&type=album', stream=True).raw)
    return im

def v_80():
    im = Image.open(requests.get('https://sun9-62.userapi.com/impg/k1MVDGQXury9D9v5bIhBND4l4NdbMT34GwI4Jw/0frJypH7724.jpg?size=635x797&quality=96&sign=e19379f13b74f2605593c6148ee62af3&type=album', stream=True).raw)
    return im

def v_81():
    im = Image.open(requests.get('https://sun9-3.userapi.com/impg/Ln73up__WYLowf-4GZFLlHiyrZBFpLipR8l5Yg/zeOsFOqlqtk.jpg?size=963x526&quality=96&sign=9ad2298994f0867cce39b91f3263fd6b&type=album', stream=True).raw)
    return im

def v_82():
    im1 = Image.open(requests.get('https://sun9-50.userapi.com/impg/qmdxcBvLvccuqfCdG5pEdb78_lvMJoEj3KWBBA/UV-XvozrZ84.jpg?size=549x629&quality=96&sign=25b0c76689f7b615729dddaf6e4b8b2f&type=album', stream=True).raw)
    im2 = Image.open(requests.get('https://sun9-43.userapi.com/impg/BpY7-ca-sUoJ4-F3JU5qrqnVcHP5cQOQemE1Tg/MHyoM2PuCp0.jpg?size=547x357&quality=96&sign=bd4b46ed802da1af000fd4d194f54212&type=album', stream=True).raw)
    return im1, im2

def v_83():
    im = Image.open(requests.get('https://sun9-35.userapi.com/impg/TJqLluXjJYHo3AXyN5fyOsCM1mxBdSzyWPZAWw/MQf1FdCEpI4.jpg?size=491x918&quality=96&sign=f1bf329b16c4ce4c0ff9a0cff14ed5c3&type=album', stream=True).raw)
    im2 = Image.open(requests.get('https://sun1-56.userapi.com/impg/J_F8JieFJ4pA40s54vM7iCnYVYYMC1cXfYUQBQ/M15Zop6IfN4.jpg?size=702x685&quality=96&sign=b4bb20b5a6d3d0dbb6277cf40a08ab75&type=album', stream=True).raw)
    im3 = Image.open(requests.get('https://sun1-87.userapi.com/impg/6Ucso4lnN-hEXrLt8wiG1cSKVkd2J6rtFh_dPQ/OvLZeTtdK7Q.jpg?size=716x822&quality=96&sign=806d92246f58be6d9d4e07e29a891408&type=album', stream=True).raw)
    return im, im2, im3

def v_84():
    im = Image.open(requests.get('https://sun9-34.userapi.com/impg/2r2QN18mfvilPwNtR81K97q9mFumDMd8_tddnQ/4FuUqasgDlo.jpg?size=2114x518&quality=96&sign=754273fd946a9be8bb773e3f07bb0585&type=album', stream = True).raw)
    im2 = Image.open(requests.get('https://sun9-39.userapi.com/impg/zeeBaK-ArU5YqLLedkFwxYmBB7__GEBHQWsymA/YNRynfAuY0c.jpg?size=1500x1332&quality=96&sign=063799ec3e9635a9cc840ae799a91406&type=album', stream = True).raw)
    return im, im2
    
def v_85():
    im = Image.open(requests.get('https://sun9-27.userapi.com/impg/XuQxkCu8LUBYitnk92ORbjEwmF7M_tdZ9jjI7Q/qXuVuemDAY4.jpg?size=1280x1106&quality=96&sign=a6ac29e2047f89415308903cb404f411&type=album', stream=True).raw)
    return im

def v_86():
    im = Image.open(requests.get('https://sun9-22.userapi.com/impg/gtfQZqwwtFAFOn8rxx--y_U-DlE5znCnK9j8ZA/-Lp6sgWWEro.jpg?size=894x745&quality=96&sign=f110527125b38e544d66ff954ae9e160&type=album', stream=True).raw)
    im2 = Image.open(requests.get('https://sun9-40.userapi.com/impg/zywihhYT9Y97MUl7MYt8_A2YRmg4m_qQY5x8rA/BRTWljXdF-s.jpg?size=871x684&quality=96&sign=af1dc6e130cbb0d69f94c5a687b5dedb&type=album', stream=True).raw)
    return im, im2

def v_87():
    im = Image.open(requests.get('https://sun9-67.userapi.com/impg/PFBqqMN3juyNIJjETOtKokpcQXRG0gQO5yqktg/33sAphM9Cvs.jpg?size=1637x734&quality=96&sign=6dd98cd3bf9b182e7a95ed4e001f4042&type=album', stream = True).raw)
    im2 = Image.open(requests.get('https://sun9-52.userapi.com/impg/f_0uyeLEwEFdPfizb4cqm8boAjzU32yfHc2P5Q/cPVG5viIeyo.jpg?size=1615x843&quality=96&sign=d62542eaf39fc021370f65d40a678d63&type=album', stream = True).raw)
    im3 = Image.open(requests.get('https://sun9-78.userapi.com/impg/NaE1smtyUtuDWBwdRfMhTxrjQQLpZx8SvjoZag/VEzlx6tjAF4.jpg?size=1628x539&quality=96&sign=8a435f0218bdb68982c14b781d1568d2&type=album', stream = True).raw)
    im4 = Image.open(requests.get('https://sun9-9.userapi.com/impg/6QRIqMxnARL8xHhA2fdBrX9Gej6a3GxSNjYDzg/bBo9l30y6Bs.jpg?size=1622x755&quality=96&sign=0e9e2ce9832874d53e88f1a8f776a87e&type=album', stream = True).raw)
    return im, im2, im3, im4

def v_88():
    im = Image.open(requests.get('https://sun9-57.userapi.com/impg/rIPrVO2HMb015tZdNN5VV5PaQMDVSOQiwDks0g/6nQBreVXU-g.jpg?size=986x462&quality=96&sign=44960c34174f671c66551a579a4dc449&type=album', stream=True).raw)
    im2 = Image.open(requests.get('https://sun9-1.userapi.com/impg/B0KwGsiNFIn3ZHL_qP_PZpqLb47GRqemQx10Qg/OpZ24q1Wl5k.jpg?size=691x250&quality=96&sign=ca8355d0295629f4d85ee5252c3c3b4f&type=album', stream=True).raw)
    im3 = Image.open(requests.get('https://sun9-39.userapi.com/impg/U_tDe3OLRZ5Uv1YInO_bfPt8FRDGcusWES4XeQ/oVm5_8R67_k.jpg?size=704x494&quality=96&sign=1e6d2f30a95bc2976aaa46a833e5c400&type=album', stream=True).raw)
    return im, im2, im3

def v_89():
    im = Image.open(requests.get('https://sun9-78.userapi.com/impg/R7WGkzzCLBcgG7lyK9p62MAkO1sn600-yOisbQ/RJCSu4t9x64.jpg?size=675x680&quality=96&sign=1f70f254007d4b21416e1b419b7eef71&type=album', stream = True).raw)
    im2 = Image.open(requests.get('https://sun9-3.userapi.com/impg/ASVGKUpIZMS5P3e4UJYKnbQ5BRhNUUKwahLzsQ/rrxk8DWvH08.jpg?size=662x424&quality=96&sign=feb10eda9f4a7d560c0e311665141437&type=album', stream = True).raw)
    return im, im2

def v_90():
    im = Image.open(requests.get('https://sun9-14.userapi.com/impg/9fVhH-_-BHeIIX2uav53YsRKEYV125CWork6zQ/Qn7MLBi68W4.jpg?size=904x502&quality=96&sign=bd027a29118f15ebcd42f133569477b4&type=album', stream = True).raw)
    im2 = Image.open(requests.get('https://sun9-57.userapi.com/impg/ZbnsV5vDLnzkylTTI9JY0_DOZBm-j4kb2SXg-A/EMQN4jsO7rQ.jpg?size=889x579&quality=96&sign=1b0b0e924bd50cbe7bc8a073e0b5dce4&type=album', stream = True).raw)
    return im, im2

def v_91():
    im = Image.open(requests.get('https://sun9-30.userapi.com/impg/blf4wQ4mXeT7iPU9P1zeJ2DyPNGguIHGBILOJQ/BUFKU7Y4KxQ.jpg?size=877x608&quality=95&sign=848bb82e0af15b0ac8d82225d5696e61&type=album', stream=True).raw)
    return im

def v_92():
    im = Image.open(requests.get('https://sun9-18.userapi.com/impg/59gRuaNRJRT8AE58zIdQKb9JW18iDuuyDWkv_Q/VIb8vH5YzFc.jpg?size=803x680&quality=96&sign=33342e836a51f7a1ddab1d39e83cf449&type=album', stream=True).raw)

    im2 = Image.open(requests.get('https://sun9-32.userapi.com/impg/n_OY-cSo2HO-YKbzYn7CoreEFU1KqLOBkvqOBw/_erR7apQBs8.jpg?size=786x519&quality=96&sign=00aeddfff6d9bd12b9d83f96f32c5b09&type=album', stream=True).raw)

    return im, im2

def v_93():
    im = Image.open(requests.get('https://sun9-7.userapi.com/impg/49fQnTKf7XRNGPfdKBFihUKSnGUU8W46Ew005Q/ogZZPdAYRbM.jpg?size=670x747&quality=96&sign=7d5bb9c42f37e2420f77f77c1d254632&type=album', stream=True).raw)
    return im

def v_94():
    im = Image.open(requests.get('https://sun9-46.userapi.com/impg/bMCPcIq9wk0pnOJwixKW7GLAcPQV94PZiA2TqQ/5j9gNRhsXKw.jpg?size=898x376&quality=96&sign=3743b371c7d1be11ae488845b72bedfd&type=album', stream=True).raw)
    return im

def v_95():
    im = Image.open(requests.get('https://sun9-75.userapi.com/impg/zEXdeuXhpte6ZcYnLxV3ACGhvtBvSfyi069sTA/aOIGlmIXdP4.jpg?size=1432x1056&quality=96&sign=f7d34987db959fe8c8298eff698a9e45&type=album', stream=True).raw)
    im2 = Image.open(requests.get('https://sun9-19.userapi.com/impg/9W_PQEuDxG6GJGYGeGIbrXypZz3ex8QGcjrWQw/akBcGTnXf4I.jpg?size=1432x428&quality=96&sign=8a42a04425dccfea4b69b3e268f24d66&type=album', stream=True).raw)
    return im, im2
    
def v_96():
    im = Image.open(requests.get('https://sun9-5.userapi.com/impg/dZLdZLWkviY6FBgz_SdtqqlRvkPxkKJcHmdqdQ/XMKYuBCL_xo.jpg?size=635x551&quality=96&sign=7b46a276cc49dfc67291836a5e48d000&type=album', stream=True).raw)
    im2 = Image.open(requests.get('https://sun9-33.userapi.com/impg/xXmiVRcJWJIDK8jX06guS3BCahJCeuhHy9Grgw/6gR3jOIQ0jU.jpg?size=635x650&quality=96&sign=9cbeee85a81c6b0416156f640ef91cd9&type=album', stream=True).raw)
    return im, im2

def v_98():
    im = Image.open(requests.get('https://sun9-5.userapi.com/impg/RQ_-N_D5zDLk2fLtRYXsXIDYKnr_OstiCn8LOQ/UU7e3o9K1LM.jpg?size=1280x1186&quality=96&sign=e34585e1213763c873d006b36cc5dd7c&type=album', stream=True).raw)
    im2 = Image.open(requests.get('https://sun9-45.userapi.com/impg/rg9JMostGoICFohFg3Ag5wpLzUS7hZkULzdv7w/sdY09YXcxI4.jpg?size=1280x737&quality=96&sign=243b2fc5e713d8f8aeb803cadfb0db74&type=album', stream=True).raw)
    return im, im2

def v_97():
    im = Image.open(requests.get('https://sun9-45.userapi.com/impg/W69jFsDG6cTM3EmJWrZ1veGdVk_ut_xrczAYdg/sFGgeANsY68.jpg?size=958x736&quality=96&sign=406f566a167c2b430fa0a8c2c0008e79&type=album', stream=True).raw)
    im2 = Image.open(requests.get('https://sun9-66.userapi.com/impg/5c1NhlvnfgfEWjmsVVhnjudfu9hjXb-kTXrSFw/WvMdBmt7Nv0.jpg?size=949x164&quality=96&sign=0154f8353d50b4500dc633b6d1f92a08&type=album', stream=True).raw)
    return im, im2

def v_99():
    im = Image.open(requests.get('https://sun9-1.userapi.com/impg/kdNAQFHo1ZiTCK_x95pMoZ7vBvxvoOSJ7u2tQw/Hru8eO3dcAs.jpg?size=450x869&quality=96&sign=e630e6d9e114d5498798116a13ccddb7&type=album', stream=True).raw)
    im2 = Image.open(requests.get('https://sun9-55.userapi.com/impg/ILto8RZe2KQNnlGLMoix8on9nblhjzIZzND53g/rcmZ28jMh6I.jpg?size=564x645&quality=96&sign=9ff45da0d9f5492fbcb1c3adbbcdce0d&type=album', stream=True).raw)
    return im, im2

def v_100():
    im = Image.open(requests.get('https://sun9-79.userapi.com/impg/JenUTS5_nMsRWA_rX2CaDRZbSa1D0mktprKBjg/iyBHLhwds_E.jpg?size=1354x1024&quality=96&sign=69ad72387d5b5f81b67dc976c9031060&type=album', stream = True).raw)
    return im
    
def v_101():
    im = Image.open(requests.get('https://sun1-23.userapi.com/impg/sfj_tw5xD6aJ7L5nXutMDUJveRQZV2fc93ld-w/frFnoaMuGc0.jpg?size=1280x1018&quality=96&sign=e3fa46df027c39ba0d97015e03878b16&type=album', stream=True).raw)
    return im

def v_102():
    im = Image.open(requests.get('https://sun9-66.userapi.com/impg/ozbPag7fC12InXbygkO39xQAz7NYcIZGH8ts1w/CTnhzNiOP0E.jpg?size=897x628&quality=96&sign=f31ce81ce60296e78f128e2a5bc328f8&type=album', stream=True).raw)
    return im

def v_103():
    im = Image.open(requests.get('https://sun9-60.userapi.com/impg/LQUYVl_EKoH7VmyP8Zlw4oXwrYGmaDLBItH62g/DWhqm7hUIxA.jpg?size=1621x743&quality=96&sign=ccd408c497a9b06bcf167ece2d523e4e&type=album', stream = True).raw)
    im2 = Image.open(requests.get('https://sun9-47.userapi.com/impg/VH25J3AXkkGygxkxed6VxQ5j4biWlrWKtElVdA/DEwrJ6PEU_Y.jpg?size=1642x822&quality=96&sign=eb70e51b387bca13b2d6a23031437ddd&type=album', stream = True).raw)
    return im, im2

def v_104():
    im = Image.open(requests.get('https://sun9-77.userapi.com/impg/rg-J2Og2TUq00RZE-_iGyXLyZmEuA4H0D0V2eA/S5pu8h8bxTE.jpg?size=825x676&quality=96&sign=8d6f928886424e5236cd20e0f3ea4c2a&type=album', stream=True).raw)
    im2 = Image.open(requests.get('https://sun9-31.userapi.com/impg/uzVAFMgVqX3Grb7TxC7rXea0wgLeQegV78CxpA/udd-LVCXT-8.jpg?size=828x461&quality=96&sign=c3cde3ea14c0fa9145853e2d35fdf645&type=album', stream=True).raw)    
    im3 = Image.open(requests.get('https://sun9-45.userapi.com/impg/lbPZK3L1eDr7Lh_UL764oQiqJDGK0KEqOe1bRg/NPssGQDbvO0.jpg?size=823x684&quality=96&sign=c0db449e8991359d4f3d7b211d6eef4f&type=album', stream=True).raw)    
    im4 = Image.open(requests.get('https://sun1-89.userapi.com/impg/2GqkUr_LREBotENqi39cXsvn85bsg--VXd5UkQ/a1rR_33ioL4.jpg?size=811x337&quality=96&sign=99ad74c0e505461803c85e7300cb1e39&type=album', stream=True).raw)    
    return im, im2, im3, im4

def v_105():
    im = Image.open(requests.get('https://sun9-67.userapi.com/impg/ulltuBe46cV9Mo9oOnwGVXcYG8ZffFikzVPtFg/T-EAG6AJQNo.jpg?size=664x630&quality=96&sign=55bb9ec02c08171e6c6c5bac0580f1be&type=album', stream = True).raw)
    im2 = Image.open(requests.get('https://sun9-61.userapi.com/impg/xsHrI-t3yb6-rJSH5F0HpRD9xO3TMThD7Es2uw/PhWPCil9cAw.jpg?size=666x448&quality=96&sign=bd40d2cb6ced86821914d0d4a817618c&type=album', stream = True).raw)
    return im, im2

def v_106():
    im = Image.open(requests.get('https://sun9-15.userapi.com/impg/xPcDhqGoJ6ps4oxlzzbWKEZpXh4IES0_5BMN6w/v0bgk_MblIA.jpg?size=874x423&quality=96&sign=5f33d152c049c74a5c91cd7220ea6038&type=album', stream = True).raw)
    im2 = Image.open(requests.get('https://sun9-48.userapi.com/impg/WWm6C5Citg0SbDTFaa_Zi35im3CVFiEnxP0hTQ/EK5IgoNrKyU.jpg?size=831x409&quality=96&sign=d62e7dac1f318401cc803ed0b372ae44&type=album', stream = True).raw)
    return im, im2

def v_107():
    im = Image.open(requests.get('https://sun9-53.userapi.com/impg/crCweaQrn97W55vDKRFn_nLGis3mOHu242FwsQ/p_15ATQ2oAY.jpg?size=875x451&quality=95&sign=bcfbf5095033588ac8a6b5591bf7e340&type=album', stream=True).raw)
    return im

def v_108():
    im = Image.open(requests.get('https://sun9-9.userapi.com/impg/yqYkfZuLbZ3O5CGVysx5-X_NBmiY6xkZUDbR8g/wAFyegYRCco.jpg?size=800x286&quality=96&sign=a1966c0348aeedf776b931adfbe2d094&type=album', stream=True).raw)
    return im

def v_109():
    im = Image.open(requests.get('https://sun9-4.userapi.com/impg/WjqOoXBLKJOiNd37Jvm777HlUj6XorVqjrFYeQ/QKQ3sXFG6T0.jpg?size=874x490&quality=96&sign=22afa6ba0f32e76cca97da6272ad1af4&type=album', stream=True).raw)
    im2 = Image.open(requests.get('https://sun9-23.userapi.com/impg/1FBqlMemFmqdAVa2yK5FZtvjwK6aOdjX70eBKQ/rQHeGtOkS0U.jpg?size=894x687&quality=96&sign=a96a1e9a33cb953272edaea219116db6&type=album', stream=True).raw)    
    return im, im2

def v_110():
    im = Image.open(requests.get('https://sun9-29.userapi.com/impg/yvJ7iZrviQQCX53o3Oa-YmhMOEYhTHOXCelhoQ/v1vjMBUHBn8.jpg?size=875x672&quality=96&sign=2d3a71ab0fefcf38d788cc43109bdd24&type=album', stream=True).raw)
    return im

def v_111():
    im = Image.open(requests.get('https://sun9-41.userapi.com/impg/3kkXNWyEPzvZIdwNW0_KjVu8fHvV39poyd3l7Q/rSmRGwc8McE.jpg?size=1432x972&quality=96&sign=1af2acdcf0ce057ab57f309a3cd09d09&type=album', stream=True).raw)
    im2 = Image.open(requests.get('https://sun9-76.userapi.com/impg/-cptxYCoqRhzTzo4z7_hL90OvJHj6S8iSgKqbQ/_7VtEDwQr5Y.jpg?size=1432x326&quality=96&sign=597e8df7fabaa75a080873a0780b56de&type=album', stream=True).raw)
    return im, im2

def v_112():
    im = Image.open(requests.get('https://sun9-23.userapi.com/impg/1At8XPpR5G-4hFrP507cR5yeF6j0yv_3Rwu2wg/cWhQGKst6q8.jpg?size=634x762&quality=96&sign=0934d3e3629adeb6923793f19739d124&type=album', stream=True).raw)
    im2 = Image.open(requests.get('https://sun9-65.userapi.com/impg/6nn4C8oVny6XyIbZThU5hIJLZ7O89K44tGHgtQ/UYCIDJFFUNI.jpg?size=579x266&quality=96&sign=11e558e15cc3845cd7125efaeddfafc2&type=album', stream=True).raw)
    return im, im2

def v_113():
    im = Image.open(requests.get('https://sun9-13.userapi.com/impg/tTenkN0lcAs9hYmnLYGI0pjFr7VvJ3GZmUz9tw/C-b0qZeQt3g.jpg?size=968x661&quality=96&sign=fc9589d50084a75c9fa768622cd527fe&type=album', stream=True).raw)
    im2 = Image.open(requests.get('https://sun9-14.userapi.com/impg/sswhBcgdUFPa0r8WVck_BaUJ51DDW64J-53_ng/XBVhv3Y6cz0.jpg?size=968x445&quality=96&sign=b08f1c08cb6545ee4de1e508bd44dda4&type=album', stream=True).raw)
    return im, im2

def v_114():
    im = Image.open(requests.get('https://sun9-10.userapi.com/impg/IR0Ydj0x_iVgYGTot60LZv2HaiP0y1Im97TiHg/Wwt4fkE334E.jpg?size=1280x748&quality=96&sign=fa84e3e31e74e8594ad51a8b17138dc4&type=album', stream=True).raw)
    im2 = Image.open(requests.get('https://sun9-12.userapi.com/impg/Wu3N_C7hBjFqgagNxNTLvEN_tZXsCzwTPQi7Xw/jzHiDWRnjVY.jpg?size=964x1080&quality=96&sign=7ccf1116e6d49577831e73f75cd32a3f&type=album', stream=True).raw)
    im3 = Image.open(requests.get('https://sun9-48.userapi.com/impg/NY1gDksc6i5HRBdl8KUJFUVCfBOogFhe3NzhHQ/sht8Mjb2ByE.jpg?size=552x370&quality=96&sign=3a224aea858ebfa70657db2aa0c850cf&type=album', stream=True).raw)
    return im, im2, im3

def v_115():
    im = Image.open(requests.get('https://sun9-78.userapi.com/impg/k11MT2doYlWCrFgBjyHrn5sIkQbF-8OLkYw1Kg/9wf_vuK5rUs.jpg?size=530x609&quality=96&sign=806244cafa4634de368e38a96187bcca&type=album', stream=True).raw)
    im2 = Image.open(requests.get('https://sun1-56.userapi.com/impg/_aOPj3QLOeB-kRV1duryio-EnSV8JEBMIb_50g/OP0WnCSxmQU.jpg?size=564x841&quality=96&sign=0918148e73757b270d3a9e2ed278a888&type=album', stream=True).raw)
    return im, im2

def v_116():
    im = Image.open(requests.get('https://sun9-53.userapi.com/impg/q2IYaberLHD0Ho7kMr0-PAnnwot9BH76oOyoMA/bxHhwOqsZ5s.jpg?size=1868x1384&quality=96&sign=2d17165587a6c564352d9b8cc2961c6e&type=album', stream = True).raw)
    return im

def v_117():
    im = Image.open(requests.get('https://sun9-29.userapi.com/impg/F5H4LBL9K5s1yYI5KMvDHa5lJ53hVtarVkdLKQ/04dwrrEYNg8.jpg?size=1280x1223&quality=96&sign=525073ba171a013c70735136c21e9ee1&type=album', stream=True).raw)
    return im

def v_118():
    im = Image.open(requests.get('https://sun1-86.userapi.com/impg/dG_xMTfoiIwJ8lsGR-w8X2XjSDROfhh5BUJIRw/aNMK2m7S4d4.jpg?size=897x487&quality=96&sign=00391e297df758fcb03ed863d992a2c6&type=album', stream=True).raw)
    im2 = Image.open(requests.get('https://sun1-20.userapi.com/impg/pURB71rTB3xvgg8fIF_QOOKaEOu8tNQafTiOoA/Jv_cFmdTiOw.jpg?size=890x453&quality=96&sign=797f7e218b009fa7979a3cd18a402108&type=album', stream=True).raw)
    return im, im2

def v_119():
    im = Image.open(requests.get('https://sun9-55.userapi.com/impg/NncHMNzqT_Mfm28bcUZMLLeYi8gs4pp_DkmO1w/vs93LXHBeyk.jpg?size=1363x736&quality=96&sign=917fde450cc1985ea3dbb1c7f580b0cc&type=album', stream = True).raw)
    im2 = Image.open(requests.get('https://sun9-40.userapi.com/impg/Eso729xyZao00wFr6zw_1foIAuUyEppsyax6jg/9Mb9d6fNuTQ.jpg?size=2222x1051&quality=96&sign=f086af65519d756b2150ce92237dddfa&type=album', stream = True).raw)
    return im, im2

def v_120():
    im = Image.open(requests.get('https://sun9-61.userapi.com/impg/bDnxB75DQBcykV4lGC_asHadYPWvWJb7JqwjlQ/75_b526CIXc.jpg?size=866x716&quality=96&sign=84229852b0057609a3759bbb1ca387d5&type=album', stream = True).raw)
    im2 = Image.open(requests.get('https://sun9-27.userapi.com/impg/qKgzSMZGmmEvJ5IaCbf_b7fT-emTkn-J81bdFQ/qJvaIpIC-RY.jpg?size=925x753&quality=96&sign=27dc747b63c98e7e435f55e2a8d6681d&type=album', stream = True).raw)
    im3 = Image.open(requests.get('https://sun9-57.userapi.com/impg/isxCq2QKZjA8EQXVk7gm4o6J4fvH-epcfst6kw/sNeD7lWY_gI.jpg?size=885x740&quality=96&sign=d029c9785d2b321a1cbd493396db31c2&type=album', stream = True).raw)
    return im, im2, im3


def v_121():
    im = Image.open(requests.get('https://sun9-15.userapi.com/impg/262PTJH_8Zg9zCFm1Eb81XywrEw39MsXscdgZw/F1CV6EOu8vA.jpg?size=673x726&quality=96&sign=663ef618edbf365c119541c4040007e0&type=album', stream = True).raw)
    return im
