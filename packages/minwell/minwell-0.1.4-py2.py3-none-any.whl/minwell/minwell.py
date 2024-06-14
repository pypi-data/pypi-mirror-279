from importlib.resources import contents, path
from PIL import ImageGrab
from IPython.display import display, Image
from fuzzywuzzy import process
import warnings
import os

warnings.filterwarnings('ignore')

l = ['63.jpg',
 '77.jpg',
 '91_2.jpg',
 '51_2.png',
 '51_3.png',
 '8_1.png',
 '88_2.jpg',
 '75_2.jpg',
 '30_2.png',
 '53_1.png',
 '48_2.png',
 '91_3.jpg',
 '89.jpg',
 '76.jpg',
 '62.jpg',
 '91_1.jpg',
 '8_3.png',
 '51_1.png',
 '8_2.png',
 '88_1.jpg',
 '75_1.jpg',
 '95_4.jpg',
 '53_2.png',
 '30_1.png',
 '49.png',
 '48_1.png',
 '57_2.png',
 '71_1.jpg',
 '36_3.png',
 '95_1.jpg',
 '36_2.png',
 '58.png',
 '55_1.png',
 '10_1.png',
 '64.jpg',
 '107_1.jpg',
 '72.jpg',
 '99.jpg',
 '57_1.png',
 '71_2.jpg',
 '10_3.png',
 '95_3.jpg',
 '95_2.jpg',
 '9.png',
 '10_2.png',
 '55_2.png',
 '36_1.png',
 '98.jpg',
 '107_2.jpg',
 '73.jpg',
 '101.jpg',
 '15_1.png',
 '14.png',
 '28.png',
 '90_1.jpg',
 '92_2.jpg',
 '52_2.png',
 '31_1.png',
 '29.png',
 '100.jpg',
 '74_1.jpg',
 '116.jpg',
 '15_2.png',
 '102.jpg',
 '17.png',
 '90_2.jpg',
 '92_1.jpg',
 '31_2.png',
 '52_1.png',
 '16.png',
 '103.jpg',
 '117.jpg',
 '74_2.jpg',
 '113.jpg',
 '96_1.jpg',
 '12.png',
 '70_2.jpg',
 '104_1.jpg',
 '54_3.png',
 '13_1.png',
 '106_2.jpg',
 '120_1.jpg',
 '54_2.png',
 '37_1.png',
 '112.jpg',
 '110.jpg',
 '96_2.jpg',
 '11.png',
 '70_1.jpg',
 '104_2.jpg',
 '13_2.png',
 '120_2.jpg',
 '106_1.jpg',
 '37_2.png',
 '54_1.png',
 '38.png',
 '105.jpg',
 '67_3.jpg',
 '20_1.png',
 '108.jpg',
 '65_1.jpg',
 '111_2.jpg',
 '35.png',
 '21.png',
 '83_2.jpg',
 '3_1.png',
 '1_2.png',
 '39_1.png',
 '34.png',
 '22_2.png',
 '121.jpg',
 '109.jpg',
 '67_2.jpg',
 '20_2.png',
 '65_2.jpg',
 '111_1.jpg',
 '83_1.jpg',
 '3_2.png',
 '1_1.png',
 '39_2.png',
 '22_1.png',
 '23.png',
 '67_1.jpg',
 '7_3.png',
 '5_1.png',
 '78_2.jpg',
 '27.png',
 '33.png',
 '24_3.png',
 '61_2.jpg',
 '115_1.jpg',
 '47_1.png',
 '24_2.png',
 '32.png',
 '78_3.jpg',
 '26.png',
 '7_2.png',
 '119.jpg',
 '5_2.png',
 '18.png',
 '78_1.jpg',
 '61_1.jpg',
 '115_2.jpg',
 '24_1.png',
 '47_2.png',
 '19.png',
 '5_3.png',
 '118.jpg',
 '7_1.png',
 '59_2.png',
 '81.jpg',
 '56.png',
 '42.png',
 '66_1.jpg',
 '40_2.png',
 '43.png',
 '94.jpg',
 '80_2.jpg',
 '59_1.png',
 '69.jpg',
 '82.jpg',
 '41.png',
 '6_4.png',
 '66_2.jpg',
 '40_1.png',
 '97.jpg',
 '80_1.jpg',
 '68.jpg',
 '93.jpg',
 '87.jpg',
 '44.png',
 '2.png',
 '50.png',
 '4_2.png',
 '79_1.jpg',
 '6_1.png',
 '25_1.png',
 '60_1.png',
 '45.png',
 '46_2.png',
 '86.jpg',
 '114_2.jpg',
 '84.jpg',
 '4_1.png',
 '79_2.jpg',
 '6_3.png',
 '6_2.png',
 '79_3.jpg',
 '46_1.png',
 '60_2.png',
 '25_2.png',
 '85.jpg',
 '114_1.jpg']

teor = {'Линейная модель множественной регрессии. Основные предпосылки метода наименьших квадратов.': 1,
 'Нелинейные модели регрессии. Походы к оцениванию. Примеры': 2,
 'Тестирование правильности выбора спецификации: типичные ошибки спецификации модели, Тест Рамсея (тест RESET), условия применения теста.': 3,
 'Тестирование правильности выбора спецификации: типичные ошибки спецификации модели, Критерий Акаике, Критерий Шварца. условия применения критериев.': 4,
 'Гетероскедастичность: определение, причины, последствия. Тест Голдфеда-Квандта и особенности его применения.': 5,
 'Гетероскедастичность: определение, причины, последствия. Тест ранговой корреляции Спирмена и особенности его применения.': 6,
 'Гетероскедастичность: определение, причины, последствия. Тест Тест Бреуша-Пагана и особенности его применения.': 7,
 'Гетероскедастичность: определение, причины, последствия. Тест Тест Глейзера и особенности его применения.': 8,
 'Способы корректировки гетероскедастичности: взвешенный метод наименьших квадратов (ВМНК) и особенности его применения.': 9,
 'Автокорреляция: определение, причины, последствия. Тест Дарбина-Уотсона и особенности его применения.': 10,
 'Автокорреляция: определение, причины, последствия. Тест Бройша – Годфри и особенности его применения.': 11,
 'Автокорреляция: определение, причины, последствия. H – тест и особенности его применения.': 12,
 'Автокорреляция: определение, причины, последствия. Метод рядов Сведа-Эйзенхарта и особенности его применения.': 13,
 'Модель с автокорреляцией случайного возмущения. Оценка моделей с авторегрессией.': 14,
 'Процедура Кохрейна-Оркатта.': 15,
 'Процедура Хилдрета – Лу.': 16,
 'Оценка влияния факторов, включенных в модель. Коэффициент эластичности, Бета-коэффициент, Дельта – коэффициент.': 17,
 'Мультиколлинеарность: понятие, причины и последствия': 18,
 'Выявление мультиколлинеарности: коэффициент увеличения дисперсии (VIF –тест)': 19,
 'Выявление мультиколлинеарности: Алгоритм Фаррара-Глобера': 20,
 'Построение гребневой регрессии. Суть регуляризации.': 21,
 ' Алгоритм пошаговой регрессии': 22,
 'Метод главных компонент (PCA) как радикальный метод борьбы с мультколлинеарностью': 23,
 'Фиктивная переменная и правило её использования': 24,
 'Модель дисперсионного анализа': 25,
 'Модель ковариационного анализа': 26,
 'Фиктивные переменные в сезонном анализе': 27,
 'Фиктивная переменная сдвига: спецификация регрессионной модели с фиктивной переменной сдвига; экономический смысл параметра при фиктивной переменной; смысл названия': 28,
 ' Фиктивная переменная наклона: спецификация регрессионной модели с фиктивной переменной наклона; экономический смысл параметра при фиктивной переменной; смысл названия': 29,
 'Определение структурных изменений в экономике: использование фиктивных переменных, тест Чоу ': 30,
 'Модели бинарного выбора. Недостатки линейной модели. ': 31,
 'Модели множественного выбора: модели с неупорядоченными альтернативными вариантами': 32,
 'Модели множественного выбора: модели с упорядоченными альтернативными вариантами': 33,
 'Модели множественного выбора: гнездовые logit-модели ': 34,
 'Модели счетных данных (отрицательная биномиальная модель, hurdle-model)': 35,
 'Модели усеченных выборок': 36,
 ' Модели цензурированных выборок (tobit-модель)': 37,
 'Модели случайно усеченных выборок (selection model)': 38,
 'Логит-модель. Этапы оценки. Области применения.': 39,
 'Пробит-модель. Этапы оценки. Области применения.': 40,
 'Метод максимального правдоподобия.': 41,
 'Свойства оценок метода максимального правдоподобия': 42,
 'Информационная матрица и оценки стандартных ошибок для оценок параметров logit и probit моделей. Интерпретация коэффициентов в моделях бинарного выбора.': 43,
 'Мера качества аппроксимации и качества прогноза logit и probit моделей/': 44,
 ' Временные ряды: определение, классификация, цель и задача моделирования временного ряда. ': 45,
 'Исследование структуры одномерного временного ряда.': 46,
 'Функциональные зависимости временного ряда. Предварительный анализ временных рядов.': 47,
 ' Процедура выявления аномальных наблюдений. Причины аномальных значений. Блочные диаграммы по типу «ящика с усами».': 48,
 'Процедура выявления аномальных наблюдений на основе распределения Стьюдента. Особенности применения метода. Анализ аномальных наблюдений.': 49,
 'Процедура выявления аномальных наблюдений на основе метода Ирвина. Особенности применения метода. Анализ аномальных наблюдений.': 50,
 'Проверка наличия тренда. Критерий серий, основанный на медиане. Особенности применения метода.': 51,
 'Проверка наличия тренда. Метод проверки разности средних уровней. Особенности применения метода.': 52,
 'Проверка наличия тренда. Метод Фостера-Стьюарта. Особенности применения метода.': 53,
 'Сглаживание временных рядов. Простая (среднеарифметическая) скользящая средняя. Взвешенная (средневзвешенная) скользящая средняя. Среднехронологическая. Экспоненциальное сглаживание': 54,
 'Трендовые модели. Без предела роста. Примеры функций. Содержательная интерпретация параметров.': 55,
 'Трендовые модели. С пределом роста без точки перегиба. Примеры функций. Содержательная интерпретация параметров.': 56,
 'Трендовые модели. С пределом роста и точкой перегиба или кривые насыщения. Примеры функций. Содержательная интерпретация параметров.': 57,
 'Выбор кривой роста.': 58,
 'Прогнозирование с помощью кривой роста.': 59,
 'Прогнозирование временного ряда на основе трендовой модели.': 60,
 'Адаптивная модель прогнозирования Брауна.': 61,
 'Моделирование тренд-сезонных процессов. Типы функциональных зависимостей.': 62,
 'Модель Хольта-Уинтерса (адаптивная модель).': 63,
 'Модель Тейла-Вейджа (мультипликативная модель).': 64,
 'Метод Четверикова.': 65,
 'Мультипликативная (аддитивная) модель ряда динамики при наличии тенденции: этапы построения.': 66,
 'Моделирование периодических колебаний (гармоники Фурье).': 67,
 'Прогнозирование одномерного временного ряда случайной компоненты (распределение Пуассона).': 68,
 'Функциональные преобразования переменных в линейной регрессионной модели. Метод Зарембки. Особенности применения.': 69,
 'Функциональные преобразования переменных в линейной регрессионной модели. Тест Бокса-Кокса. Особенности применения.': 70,
 'Функциональные преобразования переменных в линейной регрессионной модели. Критерий Акаике  и Шварца. Особенности применения.': 71,
 'Функциональные преобразования переменных в линейной регрессионной модели. Тест Бера. Особенности применения.': 72,
 'Функциональные преобразования переменных в линейной регрессионной модели. Тест МакАлера. Особенности применения.': 73,
 'Функциональные преобразования переменных в линейной регрессионной модели. Тест МакКиннона. Особенности применения.': 74,
 'Функциональные преобразования переменных в линейной регрессионной модели. Тест Уайта. Особенности применения.': 75,
 'Функциональные преобразования переменных в линейной регрессионной модели. Тест Дэвидсона. Особенности применения.': 76,
 ' Модели с распределенными лаговыми переменными.': 77,
 ' Оценка моделей с лагами в независимых переменных. Преобразование Койка.': 78,
 ' Полиномиально распределенные лаги Алмон': 79,
 ' Авторегрессионные модели': 80,
 ' Авторегрессионные модели с распределенными лагами.': 81,
 ' Стационарные временные ряды. Определения стационарности, лаговой переменной, автоковариационной функции временного ряда, автокоррляционной функции, коррелограммы,  коэффициенты корреляции между разными элементами стационарного временного ряда с временным лагом h.': 82,
 ' Стационарные временные ряды. Определения частной автокорреляционной функции, белого шума, автоковариационная функция для белого шума, ACF для белого шума, частная автокорреляционная функция для белого шума.': 83,
 ' Модели стационарных временных рядов: модель ARMA(p,q) (классический вид и через лаговый оператор). Авторегрессионный многочлен, авторегрессионная часть и часть скользящего среднего. ': 84,
 'Модели стационарных временных рядов: модель ARMA(1,q). Доказательство утверждения: Модель ARMA(1, q) стационарна тогда и только тогда, когда|a| < 1.': 85,
 'Модели стационарных временных рядов: Модель MA(q), Среднее, дисперсия и ACF для MA(q). Модель MA(∞).': 86,
 ' Модели стационарных временных рядов: Модель AR(p). Доказательство утверждения: Модель AR(p) определяет стационарный ряд ⇐⇒ выполнено условие стационарности: все корни многочлена a(z) по модулю больше единицы. Модель AR(1).': 87,
 'Прогнозирование для модели ARMA. Условия прогнозирования. Периоды прогнозирования. Информативность прогнозов. ': 88,
 'Оценка и тестирование модели: Предварительное тестирование на белый шум. ': 89,
 'Оценка модели и тестирование гипотез временного ряда.': 90,
 'Информационные критерии для сравнения моделей и выбора порядка временного ряда: Акаике, Шварца, Хеннана-Куина. Условия их применения.': 91,
 'Проверка адекватности модели: тесты на автокорреляцию временного ряда Дарбина-Уотсона, Льюинга-Бокса.': 92,
 'Линейная регрессия для стационарных рядов: Модель FDL.': 93,
 'Линейная регрессия для стационарных рядов. Модель ADL.': 94,
 'Понятие TS-ряда. Модель линейного тренда. Модель экспоненциального тренда.': 95,
 ' Нестационарные временные ряды: случайное блуждание, стохастический тренд, случайное блуждание со сносом.': 96,
 'Дифференцирование ряда: определение, DS-ряды.': 97,
 ' Подход Бокса-Дженкинса.': 98,
 'Модель ARIMA.': 99,
 'Тест ADF на единичный корень. ': 100,
 'Модель ARCH.': 101,
 'Модель GARCH.': 102,
 'Область применения панельных данных. Преимущества использования панельных данных.': 103,
 'Модели панельных данных и основные обозначения.': 104,
 'Модель пула (Pool model).': 105,
 ' Модель регрессии с фиксированным эффектом (fixed effect model)': 106,
 ' Модель регрессии со случайным эффектом (random effect model).': 107,
 'Тест Бройша-Пагана для панельных данных.': 108,
 'Тест Хаусмана для панельных данных.': 109,
 'Тест Лагранжа для панельных данных.': 110,
 'Вычисление значения оценок параметров β и а в модели с фиксированным эффектом.': 111,
 ' Отражение пространственных эффектов. Бинарная матрица граничных соседей. Приведите пример.': 112,
 'Отражение пространственных эффектов. Бинарная матрица ближайших соседей. Приведите пример.': 113,
 'Отражение пространственных эффектов. Матрица расстояний. Приведите пример.': 114,
 'Отражение пространственных эффектов. Матрица расстояний с учетом размера объекта. Приведите пример.': 115,
 'Алгоритм построения матрицы пространственных весов. Приведите пример.': 116,
 'Пространственная автокорреляция по методологии А. Гетиса и Дж. Орда. Недостатки методологии.': 117,
 'Пространственная автокорреляция по методологии Роберта Джири.': 118,
 'Пространственная автокорреляция по методологии Морана П.': 119,
 'Пространственная кластеризация территорий. Локальный индекс автокорреляции П. Морана (Ili) ': 120,
 'Матрица взаимовлияния Л. Анселина (LISA).': 121}

def cdf(s=''):
    if type(s) != str:
        return 0.8686886 * (s / 56543)
        
    if s == '':
        return -1
        
    key = process.extractOne(s, teor.keys())[0]
    num = teor[key]

    pics = []
    for v in l:
        if str(num) in v:
            pics.append(v)
    
    pics = pics[::-1]

    for elem in pics:
        with path('minwell.theory', elem) as pt:
            img = Image(filename=pt)
            display(img)

def zarembka():
    return('''
    class Zarembka():
        def __init__(self, X, y):
            self.X = pd.DataFrame(X)
            self.y = y
    
            self.X_log = pd.DataFrame(X)
            self.y_log = np.log(y)
    
        def test(self):
            self.summa = np.sum(self.y_log)
    
            self.y_geom = np.exp(1/len(self.X_log)*self.summa)
    
            self.y = self.y / self.y_geom
            self.y_log = np.log(self.y/ self.y_geom)
    
            assert 'const' not in self.X.columns
            self.X['const'] = 1
            self.X_log['const'] = 1
    
            self.result = sm.OLS(self.y, self.X).fit()
            self.result_log = sm.OLS(self.y_log, self.X_log).fit()
    
            self.ess1 = np.sum(self.result.resid ** 2)
            self.ess2 = np.sum(self.result_log.resid ** 2)
    
            self.z = abs(len(self.X) / 2 * np.log(self.ess1 / self.ess2))
            self.z_table = stats.chi2.ppf(0.95,1)
    
            if self.z > self.z_table:
                print('Полулогарифмическая модель лучше')
    
            else:
                print('Линейная модель лучше')
    ''')

def box_cox():
    return('''
    class Box_Cox():
        def __init__(self, X, y):
            self.X = pd.DataFrame(X)
            self.y = y
    
            self.y_log = np.log(y)
    
        def test(self):
            self.lambda_ = np.arange(0.001,1,0.01)
            self.ess_list = []
            
            assert 'const' not in self.X.columns
    
            self.summa = np.sum(self.y_log)
            self.y_geom = np.exp(1/len(self.X)*self.summa)
            
            self.y = self.y / self.y_geom
            
            for i in self.lambda_:
                self.X_help = self.X**i/i
                self.y_help = self.y**i/i
                self.X_help['const'] = 1
                self.ess_list.append(np.sum(sm.OLS(self.y_help, self.X_help).fit().resid**2))
                del self.X_help, self.y_help 
    
            plt.plot(self.lambda_, self.ess_list);
            
            if min(self.ess_list) == self.ess_list[0]:
                print('Полулогарифмическая модель лучше')
    
            else:
                print('Линейная модель лучше')
    ''')

def akaike():
    return('''
    class Akaike():
        def __init__(self, X, y):
            self.X = pd.DataFrame(X)
            self.y = y
    
            self.X_log = pd.DataFrame(X)
            self.y_log = np.log(y)
        
        def test(self):
    
            assert 'const' not in self.X.columns
            self.X['const'] = 1
            self.X_log['const'] = 1
            
            self.ess1 = np.sum(sm.OLS(self.y, self.X).fit().resid**2)
            self.ess2 = np.sum(sm.OLS(self.y_log, self.X_log).fit().resid**2)
    
            self.AIC1 = np.log(self.ess1 / len(self.X)) + 2 / len(self.X) + 1 + np.log(2 * np.pi)
            self.AIC2 = np.log(self.ess2 / len(self.X_log)) + 2 / len(self.X_log) + 1 + np.log(2 * np.pi)
    
            if self.AIC2 < self.AIC1:
                print('Полулогарифмическая модель лучше')
    
            else:
                print('Линейная модель лучше')
    ''')

def shwartz():
    return('''
    class Shvartz():
        def __init__(self, X, y):
            self.X = pd.DataFrame(X)
            self.y = y
    
            self.X_log = pd.DataFrame(X)
            self.y_log = np.log(y)
        
        def test(self):
            assert 'const' not in self.X.columns
            self.X['const'] = 1
            self.X_log['const'] = 1
            
            self.ess1 = np.sum(sm.OLS(self.y, self.X).fit().resid**2)
            self.ess2 = np.sum(sm.OLS(self.y_log, self.X_log).fit().resid**2)
    
            self.BIC1 = np.log(self.ess1 / len(self.X)) + 2 * np.log(len(self.X)) / len(self.X) + 1 + np.log(2*np.pi)
            self.BIC2 = np.log(self.ess2 / len(self.X_log)) + 2 * np.log(len(self.X_log)) / len(self.X_log) + 1 + np.log(2*np.pi)
    
            if self.BIC2 < self.BIC1:
                print('Полулогарифмическая модель лучше')
    
            else:
                print('Линейная модель лучше')
    ''')

def bera():
    return('''
    class Bera():
        def __init__(self, X, y):
            self.X = pd.DataFrame(X)
            self.y = y
    
            self.X_log = pd.DataFrame(X)
            self.y_log = np.log(y)
            
        def test(self):
            assert 'const' not in self.X.columns
            self.X['const'] = 1
            self.X_log['const'] = 1

            self.predict1 = sm.OLS(self.y, self.X).fit().predict()
            self.predict2 = sm.OLS(self.y_log, self.X_log).fit().predict()

            self.upsilon_1 = sm.OLS(np.log(self.predict1), self.X).fit().resid
            self.upsilon_2 = sm.OLS(np.exp(self.predict2), self.X_log).fit().resid

            self.X['upsilon'] = self.upsilon_1
            self.X_log['upsilon'] = self.upsilon_2

            self.predict1_2 = sm.OLS(self.y, self.X).fit().tvalues 
            self.predict2_2 = sm.OLS(self.y_log, self.X_log).fit().tvalues 

            p = 1
            ttable = stats.t.ppf(0.95, len(self.X) - p - 1)
            
            self.t_value_1 = abs(self.predict1_2['upsilon'])
            self.t_value_2 = abs(self.predict2_2['upsilon'])
            
    
            if (self.t_value_1 < ttable and self.t_value_2 < ttable) or (self.t_value_1 > ttable and self.t_value_2 > ttable):
                print("Невозможно сказать какая модель лучше")
            elif self.t_value_2 > ttable:
                print('Полулогарифмическая модель лучше')
            else:
                print('Линейная модель лучше')
    ''')

def mackinon():
    return('''
    class MacKinon():
        def __init__(self, X, y):
            self.X = pd.DataFrame(X)
            self.y = y
    
            self.X_log = pd.DataFrame(X)
            self.y_log = np.log(y)
    
        def test(self):
            self.predict1 = sm.OLS(self.y, self.X).fit().predict()
            self.predict2 = sm.OLS(self.y_log, self.X_log).fit().predict()

            self.X_log['temp'] =  self.predict2 - np.exp(self.predict1)
            self.X['temp'] = np.log(self.predict2) - self.predict1

            self.predict1_2 = sm.OLS(self.y, self.X).fit().tvalues
            self.predict2_2 = sm.OLS(self.y_log, self.X_log).fit().tvalues

            p = 1
            ttable = stats.t.ppf(0.95, len(self.X) - p - 1)
            
            self.t_value_1 = abs(self.predict1_2['temp'])
            self.t_value_2 = abs(self.predict2_2['temp'])

            if (self.t_value_1 < ttable and self.t_value_2 < ttable) or (self.t_value_1 > ttable and self.t_value_2 > ttable):
                print("Невозможно сказать какая модель лучше")
            elif self.t_value_2 > ttable:
                print('Полулогарифмическая модель лучше')
            else:
                print('Линейная модель лучше')
    ''')

def anomaliesStudent():
    return('''
    class anomaliesStudent():
        def __init__(self, y):
            self.y = y
    
        def test(self):
            self.S_y = np.sqrt(np.sum((self.y - np.mean(self.y))**2) / (n-1))
            self.y_anomalies = ...# подозрение на аномалии
            tau = []
            
            for y_anomaly in self.y_anomalies:
                tau.append(np.abs(y_anomaly - np.mean(self.y))/self.S_y)
            
            alpha1 = 0.05
            ttable1 = t.ppf(1-alpha1/2, n-2)
            tau_table1 = (ttable1 * np.sqrt(n-1))/(np.sqrt(n-2+ttable1**2)) 
    
            alpha2 = 0.001
            ttable2 = t.ppf(1-alpha2/2, n-2) 
            tau_table2 = (ttable2 * np.sqrt(n-1))/(np.sqrt(n-2+ttable2**2))
    
            for i in range(len(tau)):
                if tau[i] <= tau_table1:
                    print(f'Наблюдение {i} нельзя считать аномальным')
    
                if (tau[i] > tau_table1) and (tau[i] <= tau_table2):
                    print(f'Наблюдение {i} можно признать аномальным, если в пользу этого имеются другие поводы')
    
                else:
                    print(f'Наблюдение {i} признается аномальным')
    ''')

def Irvin():
    return('''
    class Irvin():
        def __init__(self, y):
            self.y = y
    
        def test(self):
            self.S_y = np.sqrt(np.sum((self.y - np.mean(self.y))**2) / (n-1))
            self.y_anomalies = ...# подозрение на аномалии
            self.y_previous = ... # предыдущие игреки для каждого аномального
    
            lmbd_t = []
            for i in range(len(self.y_anomalies)):
                lmbd_t.append(np.abs(self.y_anomalies[i] - self.y_previous[i])/self.S_y)
    
            lmbd_crit = 0.95
    
            for i in range(len(lmbd_t)):
                if lmbd_t[i] > lmbd_crit:
                    print(f'Наблюдение {i} признается аномальным')
                else:
                    print(f'Наблюдение {i} нельзя считать аномальным')
    ''')

def MedianaTrend():
    return('''
    class medianaTrend():
        def __init__(self, y):
            self.y = y
            self.y_sorted = sorted(y)
    
        def test():
            median = np.median(self.y_sorted)
            ls = ['+' if i > median else '-' for i in self.y]
    
            num_series = 0
            for i in range(len(ls)):
                if i == 0 or ls[i] != ls[i - 1]:
                    num_series += 1
    
            max_length = 0
            current_length = 0
            
            for i in range(len(ls)):
                if i == 0 or ls[i] == ls[i - 1]:
                    current_length += 1
                else:
                    max_length = max(max_length, current_length)
                    current_length = 1
    
            max_length = max(max_length, current_length)
    
            if (max_length < 3.3 * np.log(len(self.y)+1)) and (num_series > (1/2*(len(self.y) + 1 - 1.96*np.sqrt(len(self.y)-1)))):
                print('Гипотеза об отсутствии тренда принимается')
    
            else:
                print('Гипотеза об отсутствии тренда отвергается')
    ''')

def line():
    return('''
    # предварительное сглаживание ряда
    class smoothing():
        def __init__(self, y):
            self.y = y
    
        def smooth():
            m = 3
            y_smoothing = []
            y_0 = (5 * self.y[0] + 2 * self.y[1] - self.y[2]) / 6
            y_n = (-self.y[n - 3] + 2 * self.y[n - 2] + 5 * self.y[n - 1]) / 6
            y_smoothing.append(y_0)
            
            for i in range(1, len(y)-1):
                y_temp = (self.y[i - 1] + self.y[i] + self.y[i + 1]) / 3
                y_smoothing.append(y_temp)
            
            y_smoothing.append(y_n)
    
    class modelPrirosta():
        def __init__(self):
            self.y = y
        def model():
            y_smoothing = np.convolve(self.y, np.ones(window_size)/window_size, mode='same')
    
            # первые средние приросты
            u_t = [(y_smoothing[i+1]+y_smoothing[i-1])/2 for i in range(1, len(y_smoothing)-1)]
            u_t_2 = [(u_t[i+1]+u_t[i-1])/2 for i in range(1, len(u_t)-1)]
    
            ut_y_fraq = [u_t[i-1]/y_smoothing[i] for i in range(1, len(y_smoothing)-1)]
            log_u = np.log(u_t)
            log_ut_y = np.log(ut_y_fraq)
            log_ut_y2 = np.log([u_t[i-1]/y_smoothing[i]**2 for i in range(1, len(y_smoothing)-1)])
    
            # Показатель--Характер изменения--Кривая роста
            # u_t--Примерно постоянный--Полином первого порядка
            # u_t--Примерно линейный--Полином второго порядка
            # u_t_2--Примерно линейный--Полином третьего порядка
            # ut_y_fraq--Примерно постоянный--Экспонента( exp(a_0 + a_1 * t) )
            # log_u--Примерно линейный--Модифицированная экспонента( f(t) = k + a * b ^ t )
            # log_ut_y--Примерно линейный--Кривая Гомпертца ( f(t) = k * (a ^ (b ^ t)) )
            # log_ut_y2--Примерно линейный--Логистическая кривая ( f(t) = 1 / (k + a * b ^ t) )
    
    class Prognoz():
        def predict():
            # далее идет пример для экспоненты
            from scipy.optimize import minimize
    
            y = df['BBR_EA_M_I'].values
            t = df['date'].values
            t = np.arange(0, len(t), 1)
            
            # Определение функции для вычисления суммы квадратов разностей
            def objective(params):
                a, b = params
                predicted_y = a * np.exp(b * t)
                return np.sum((y - predicted_y) ** 2)
            
            # Начальное приближение для параметров a и b
            initial_guess = [0, 0]  # Пример начального приближения
            
            # Минимизация суммы квадратов разностей с помощью МНК
            result = minimize(objective, initial_guess)
            optimal_params = result.x
            
            print("Оптимальные параметры a и b:", optimal_params)
    
            from scipy.stats import t as t_test
    
            a_optimal, b_optimal = optimal_params
            
            # Прогнозирование на 4 периода вперед
            future_t = np.arange(len(df), len(df)+4,1)  # Пример периодов для прогноза
            t = np.arange(0, len(df), 1)
            future_y_point_forecast = a * np.exp(b * future_t)
            
            # Стандартное отклонение прогноза
            residuals = y - (a * np.exp(b * t))
            std_dev = np.sqrt(np.sum(residuals ** 2) / (len(t) - 2))
            
            # Коэффициент для доверительного интервала
            t_value = t_test.ppf(0.975, len(t) - 2)
            
            # Интервальный прогноз на 4 периода вперед
            u = t_value * std_dev * np.sqrt(1 + 1/n + 3*(n+2*1-1)**2/(n*(n**2-1)))
            future_y_upper_bound = future_y_point_forecast + u
            future_y_lower_bound = future_y_point_forecast - u
            
            print("Точечный прогноз на 4 периода вперед:", future_y_point_forecast)
            print("Верхняя граница интервального прогноза:", future_y_upper_bound)
            print("Нижняя граница интервального прогноза:", future_y_lower_bound)
    
    
             # для полиномов
            t_k = ...# время прогноза
            u = t_value * std_dev * np.sqrt(1 + 1/n + (t_k ** 2) / np.sum(t ** 2) + (np.sum(t ** 4) - 2 * (t_k ** 2) * np.sum(t ** 2) + n * (t_k ** 4)) / (n * np.sum(t ** 4) - np.sum(t ** 2) ** 2))
    ''')

def Braun():
    return('''
    class Braun():
        def __init__(self, y):
            self.y = y
    
        def model(self):
            t = np.arange(0, len(self.y), 1)
            
            t0 = t[:50]
            y0 = self.y[:50]
    
            X = sm.add_constant(t0)
            linear_model = sm.OLS(y0, X)
            linear_results = linear_model.fit()
            
           
            a0, a1 = linear_results.params
            forecasts = []
            beta = 0.89  # Коэффициент дисконтирования данных
            
            for i in range(50, len(df)-1):
                forecast = a0 + a1 * (t[i] + 1)
                forecasts.append(forecast)
                
                error = y[i + 1] - forecast
            
                A0_new = a0 + a1 + (1 - beta)**2 * error
                A1_new = a1 + (1 - beta)**2 * error
                a0 = A0_new
                a1 = A1_new
            
            print(a0, a1)
    
        def predict(self):
            t = np.arange(0, len(df), 1)
            y_func = a0 + a1*t
    
        def interval_predict():
            #пример
            from scipy.stats import t as t_test
            n = len(y)
            y = ...
            t = np.arange(0, len(df), 1)
            y_pred = a0 + a1*t
            S_y = np.sqrt(np.sum((y - y_pred)**2)/n)
            
            t_test = t_test.ppf(0.95, n-2)
            S_y = np.sqrt(np.sum((y - np.mean(y))**2) / (n-1))
            u = S_y * t_test * np.sqrt(1 + 1/n + 3*(n+2*1-1)**2/(n*(n**2-1)))
    
            t_future = np.arange(n, n+4, 1)  # Пример значений от 100 до 103 (4 шага вперед) с шагом 1
            y_future = a0 + a1 * t_future
            
            # Создаем интервальный прогноз
            y_lower = y_future - u  # Нижняя граница интервального прогноза
            y_upper = y_future + u 
    ''')

def Holta():
    return('''
    class Holt():
        def __init__(self, y):
            self.y = y
    
        def model(self):
            index = pd.date_range(start='1/1/1993', periods=len(y), freq='M')
            ts = pd.Series(y, index=index)
            
            hw_model = sm.tsa.ExponentialSmoothing(ts, trend='add', seasonal='add', seasonal_periods=12).fit()
            
            forecast = hw_model.forecast(steps=4)
    ''')

def Chetverikov():
    return('''
    class Chetverikov():
        def Chetverikov(t, y, L):
            y_reshaped = np.array(y).reshape(-1, L)
            chrono_mean = (
            0.5 * y_reshaped[:, 0]
            + np.sum(y_reshaped[:, 1:-1], axis=1)
            + 0.5 * y_reshaped[:, -1]
            ) / L
            l1 = y_reshaped - chrono_mean[[[i] * 4 for i in range(len(chrono_mean))]]
            l1_2 = l1**2
            sigma1 = np.sqrt((np.sum(l1_2, axis=1) - np.sum(l1, axis=1) ** 2 / L) / (L - 1))
            l1_norm = l1 / sigma1[[[i] * 4 for i in range(len(chrono_mean))]]
            s1 = np.mean(l1_norm, axis=0)
            
            f1 = (
            y_reshaped
            - s1[[list(range(0, L)) for i in range(len(y_reshaped))]]
            * sigma1[[[i] * 4 for i in range(len(chrono_mean))]]
            )
            
            f2 = [np.nan] * (int(0.5 * L) - 1)
            
            for i in range(int(0.5 * L), len(f1.reshape(-1)) + 1):
            f2.append(np.mean(f1.reshape(-1)[i - int(0.5 * L) : i]))
            
            f2[0] = f1[0, 0]
            
            f2 = np.array(f2).reshape(-1, L)
            
            l2 = y_reshaped - f2
            
            l2_2 = l2**2
            
            sigma2 = np.sqrt((np.sum(l2_2, axis=1) - np.sum(l2, axis=1) ** 2 / L) / (L - 1))
            l2_norm = l2 / sigma2[[[i] * 4 for i in range(len(chrono_mean))]]
            
            s2 = np.mean(l2_norm, axis=0)
            
            eps = (
            l2
            - s2[[list(range(0, L)) for i in range(len(y_reshaped))]]
            * sigma2[[[i] * 4 for i in range(len(chrono_mean))]]
            )
            
            k = np.sum(l2_2 * eps, axis=1) / np.sum(eps**2, axis=1)
            
            return {
            "chrono_mean": chrono_mean[[[i] * 4 for i in range(len(chrono_mean))]].reshape(
            -1
            ),
            "f1": f1.reshape(-1),
            "f2": f2.reshape(-1),
            "s1": s1,
            "s2": s2,
            "eps": eps.reshape(-1),
            }
    ''')

def KLags():
    return('''
    # пример
    class KLags():
        def model_1(df, k, inplace=False):
            assert k > 0, 'k <= 0'
            if not inplace:
                df = df.copy()
            
            df['USD CLOSE t'] = df['USD CLOSE']
            df = df.drop(columns=['USD CLOSE'])
            for i in range(1, k):
                df['USD CLOSE t' + ' - ' + str(i)] = df['USD CLOSE t'].shift(i)
        
            df = df.iloc[k - 1:].reset_index(drop=True)
        
            X = sms.add_constant(df.drop(columns=['GAZP CLOSE']))
            Y = df['GAZP CLOSE']
        
            model = sms.OLS(Y,X)
            results = model.fit()
            
            return results
    ''')

def InfinityLags():
    return('''
    # пример
    class InfinityLags():
        # Для "удобного" моделирования будем использовать преобразование Койка, которое позволит спецификацию модели с бесконечным числом членов свести к спецификации с конечным числом членов.
        def model_2(df, inplace=False):
            if not inplace:
                df = df.copy()
        
            df['GAZP CLOSE t'] =  df['GAZP CLOSE'] 
            df['USD CLOSE t'] =  df['USD CLOSE']
        
            df = df.drop(columns=['USD CLOSE', 'GAZP CLOSE'])
            df['GAZP CLOSE t - 1'] = df['GAZP CLOSE t'].shift(1)
        
            df = df.iloc[1:].reset_index(drop=True)
            X = sms.add_constant(df.drop(columns=['GAZP CLOSE t']))
            Y = df['GAZP CLOSE t']
        
            model = sms.OLS(Y,X)
            results = model.fit()
        
            return results

            results = model_2(wd_df)

            print(results.summary())

            b0 = ... #коэф перед USD CLOSE t
            lambda_ = ... #коэф перед GAZP CLOSE t - 1 
            a_0 = const / (1 - lambda_)

            for i in range(1, 10):
                print(f'bo * lambda ^ {i} = {b0 * (lambda_ ** i)}')
    ''')

def avtoregression():
    return('''
    # пример
    class avtoregression():
        def model_3(df, k, inplace=False):
            assert k > 0, 'k <= 0'
            if not inplace:
                df = df.copy()
            
            df['USD CLOSE t'] = df['USD CLOSE']
            df['GAZP CLOSE t'] =  df['GAZP CLOSE'] 
            df = df.drop(columns=['USD CLOSE', 'GAZP CLOSE'])
            
            for i in range(1, k):
                df['GAZP CLOSE t' + ' - ' + str(i)] = df['GAZP CLOSE t'].shift(i)
        
            df = df.iloc[k - 1:].reset_index(drop=True)
        
            X = sms.add_constant(df.drop(columns=['GAZP CLOSE t']))
            Y = df['GAZP CLOSE t']
        
            model = sms.OLS(Y,X)
            results = model.fit()
            
            return results
    ''')

def h_test():
    return('''
    class InfinityLags():
        # Для "удобного" моделирования будем использовать преобразование Койка, которое позволит спецификацию модели с бесконечным числом членов свести к спецификации с конечным числом членов.
        def model_2(df, inplace=False):
            if not inplace:
                df = df.copy()
        
            df['GAZP CLOSE t'] =  df['GAZP CLOSE'] 
            df['USD CLOSE t'] =  df['USD CLOSE']
        
            df = df.drop(columns=['USD CLOSE', 'GAZP CLOSE'])
            df['GAZP CLOSE t - 1'] = df['GAZP CLOSE t'].shift(1)
        
            df = df.iloc[1:].reset_index(drop=True)
            X = sms.add_constant(df.drop(columns=['GAZP CLOSE t']))
            Y = df['GAZP CLOSE t']
        
            model = sms.OLS(Y,X)
            results = model.fit()
        
            return results

            results = model_2(wd_df)

            print(results.summary())

            b0 = ... #коэф перед USD CLOSE t
            lambda_ = ... #коэф перед GAZP CLOSE t - 1 
            a_0 = const / (1 - lambda_)

            for i in range(1, 10):
                print(f'bo * lambda ^ {i} = {b0 * (lambda_ ** i)}')
                
    class hTest():
        def h_test(df):
            results = model_2(df)
            
            ESS = np.sum(results.resid ** 2)
            EDS = np.sum(results.resid.diff().iloc[1:] ** 2)
            DW = EDS / ESS
        
            ro = 1 - DW / 2
            n = df.shape[0]
            D = pd.read_html(results.summary().tables[1].as_html(), header = 0, index_col = 0)[0].loc['const', 'std err'] ** 2
        
            if n * D > 1:
                print('h-статистика не может быть вычислена')
                return
                
            h = ro * np.sqrt(n / (1 - n * D))
        
            if h > 1.96:
                print('H0 отклоняется. Имеет место автокорреляция')
        
            else:
                print('H0 принимается. Автокорреляция отсутсвует')
    ''')

def stationary():
    return('''
    class Stationary():
        def check_stationary():
            from statsmodels.tsa.stattools import adfuller
            # Проведем тест Дики-Фуллера на стационарность
            result = adfuller(df['gazp'])
            print('ADF Statistic: %f' % result[0])
            print('p-value: %f' % result[1])
            print('Critical Values:')
            for key, value in result[4].items():
                print('\t%s: %.3f' % (key, value))
            
            if result[1] < 0.05:
                print(f'H0 отклоняется. Единиччных корней нет, ряд gazp стационарный')
            else:
                print(f'H0 принимается. Ряд gazp нестационарный')

        def if_not_stationary():
            # введем новый столбец арифметической доходности акций
            df['gazp_arifm'] = (df['gazp']-df['gazp'].shift(1))/df['gazp']
            df['gazp_geom'] = np.log(df['gazp']/df['gazp'].shift(1)) # логарифм темпа роста
            df.dropna(inplace=True)
    ''')

def acf():
    return('''
    class ACF():
        def ACF():
            from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
            df['gazp_arifm'] = (df['gazp']-df['gazp'].shift(1))/df['gazp']
            # Визуализация ACF (p)
            plot_acf(df['gazp_arifm'], lags=12)
            plt.title('Автокорреляционная функция ACF')
            plt.xlabel('Лаги')
            plt.ylabel('Корреляция')
            plt.show()
    ''')

def pacf():
    return('''
    class PACF():
        def PACF():
            from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
            df['gazp_arifm'] = (df['gazp']-df['gazp'].shift(1))/df['gazp']
            plot_pacf(df['gazp_arifm'], lags=12, method='ols')
            plt.title('Частичная автокорреляционная функция (PACF)')
            plt.xlabel('Лаги')
            plt.ylabel('Корреляция')
            plt.show()
    ''')


d = {
        'zarembka' : zarembka(),
        'зарембка' : zarembka(),
        'метод зарембки' : zarembka(),
        'box cox' : box_cox(),
        'бокс кокс' : box_cox(),
        'метод бокса-кокса' : box_cox(),
        'бокс-кокс' : box_cox(),
        'акаике' : akaike(),
        'aic' : akaike(),
        'критерий акаике' : akaike(),
        'akaike' : akaike(),
        'шварц' : shwartz(),
        'sc' : shwartz(),
        'критерий шварца' : shwartz(),
        'тест бера' : bera(),
        'бера' : bera(),
        'bera' : bera(),
        'test bera' : bera(),
        'макалер' : bera(),
        'macaler' : bera(),
        'тест макалера' : bera(),
        'test macaler' : bera(),
        'macaler' : bera(),
        'маккиннон' : mackinon(),
        'тест маккиннона' : mackinon(),
        'test mackinnon' : mackinon(),
        'mackinnon' : mackinon(),
        'процедура выявления аномальных наблюдений на основе распределения стьюдента' : anomaliesStudent(),
        'аномальные наблюдения стьюдент' : anomaliesStudent(),
        'аномалии стьюдент' : anomaliesStudent(),
        'стьюдент' : anomaliesStudent(),
        'тест стьюдента' : anomaliesStudent(),
        'метод ирвина' : Irvin(),
        'irvin' : Irvin(),
        'method irvin' :  Irvin(),
        'ирвин' : Irvin(),
        'критерий серий, основанный на медиане' : MedianaTrend(),
        'медиана' : MedianaTrend(),
        'тренд медиана' : MedianaTrend(),
        'медиана тренд' : MedianaTrend(),
        'кривая роста' : line(),
        'модель брауна' : Braun(),
        'модель прогнозирования брауна' : Braun(),
        'браун' : Braun(),
        'адаптивная модель прогнозирования брауна' : Braun(),
        'модель хольта-уинтереса' : Holta(),
        'модель хольта уинтереса' : Holta(),
        'метод четверикова' : Chetverikov(),
        'четвериков' : Chetverikov(),
        'модель с конечным числом лагов' : KLags(),
        'модель с бесконечным числом лагов' : InfinityLags(),
        'авторегрессия' : avtoregression(),
        'авторегрессионная модель' : avtoregression(),
        'h-тест' : h_test(),
        'h тест' : h_test(),
        'h-test' : h_test(),
        'h test' : h_test(),
        'стационарность' : stationary(),
        'тест дики-фуллера' : stationary(),
        'тест дики фуллера' : stationary(),
        'тест дики фулера' : stationary(),
        'тест дики-фулера' : stationary(),
        'acf' : acf(),
        'pacf' : pacf()
}
def ppf(s):
    if type(s) != str:
        return 0.437698979 * (s / 3232)
        
    s = s.lower()
    print(d.get(process.extractOne(s, d.keys())[0], 0))

def help_ppf():
    print(list(sorted(d.keys())))

def help_cdf():
    print(list(sorted(teor.keys())))
