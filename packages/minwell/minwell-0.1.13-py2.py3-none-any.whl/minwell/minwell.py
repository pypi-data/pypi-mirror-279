from importlib.resources import contents, path
from PIL import ImageGrab
from IPython.display import display, Image
from fuzzywuzzy import process
import warnings
import os

warnings.filterwarnings('ignore')

l = sorted([
 '100_1.jpg',
 '101_1.jpg',
 '102_1.jpg',
 '103_1.jpg',
 '104_1.jpg',
 '104_2.jpg',
 '105_1.jpg',
 '106_1.jpg',
 '106_2.jpg',
 '107_1.jpg',
 '107_2.jpg',
 '108_1.jpg',
 '109_1.jpg',
 '10_1.png',
 '10_2.png',
 '10_3.png',
 '110_1.jpg',
 '111_1.jpg',
 '111_2.jpg',
 '112_1.jpg',
 '113_1.jpg',
 '114_1.jpg',
 '114_2.jpg',
 '115_1.jpg',
 '115_2.jpg',
 '116_1.jpg',
 '117_1.jpg',
 '118_1.jpg',
 '119_1.jpg',
 '11_1.png',
 '120_1.jpg',
 '120_2.jpg',
 '121_1.jpg',
 '12_1.png',
 '13_1.png',
 '13_2.png',
 '14_1.png',
 '15_1.png',
 '15_2.png',
 '16_1.png',
 '17_1.png',
 '18_1.png',
 '19_1.png',
 '1_1.png',
 '1_2.png',
 '20_1.png',
 '20_2.png',
 '21_1.png',
 '22_1.png',
 '22_2.png',
 '23_1.png',
 '24_1.png',
 '24_2.png',
 '24_3.png',
 '25_1.png',
 '25_2.png',
 '26_1.png',
 '27_1.png',
 '28_1.png',
 '29_1.png',
 '2_1.png',
 '30_1.png',
 '30_2.png',
 '31_1.png',
 '31_2.png',
 '32_1.png',
 '33_1.png',
 '34_1.png',
 '35_1.png',
 '36_1.png',
 '36_2.png',
 '36_3.png',
 '37_1.png',
 '37_2.png',
 '38_1.png',
 '39_1.png',
 '39_2.png',
 '3_1.png',
 '3_2.png',
 '40_1.png',
 '40_2.png',
 '41_1.png',
 '42_1.png',
 '43_1.png',
 '44_1.png',
 '45_1.png',
 '46_1.png',
 '46_2.png',
 '47_1.png',
 '47_2.png',
 '48_1.png',
 '48_2.png',
 '49_1.png',
 '4_1.png',
 '4_2.png',
 '50_1.png',
 '51_1.png',
 '51_2.png',
 '51_3.png',
 '52_1.png',
 '52_2.png',
 '53_1.png',
 '53_2.png',
 '54_1.png',
 '54_2.png',
 '54_3.png',
 '55_1.png',
 '55_2.png',
 '56_1.png',
 '57_1.png',
 '57_2.png',
 '58_1.png',
 '59_1.png',
 '59_2.png',
 '5_1.png',
 '5_2.png',
 '5_3.png',
 '60_1.png',
 '60_2.png',
 '61_1.jpg',
 '61_2.jpg',
 '62_1.jpg',
 '63_1.jpg',
 '64_1.jpg',
 '65_1.jpg',
 '65_2.jpg',
 '66_1.jpg',
 '66_2.jpg',
 '67_1.jpg',
 '67_2.jpg',
 '67_3.jpg',
 '68_1.jpg',
 '69_1.jpg',
 '6_1.png',
 '6_2.png',
 '6_3.png',
 '6_4.png',
 '70_1.jpg',
 '70_2.jpg',
 '71_1.jpg',
 '71_2.jpg',
 '72_1.jpg',
 '73_1.jpg',
 '74_1.jpg',
 '74_2.jpg',
 '75_1.jpg',
 '75_2.jpg',
 '76_1.jpg',
 '77_1.jpg',
 '78_1.jpg',
 '78_2.jpg',
 '78_3.jpg',
 '79_1.jpg',
 '79_2.jpg',
 '79_3.jpg',
 '7_1.png',
 '7_2.png',
 '7_3.png',
 '80_1.jpg',
 '80_2.jpg',
 '81_1.jpg',
 '82_1.jpg',
 '83_1.jpg',
 '83_2.jpg',
 '84_1.jpg',
 '85_1.jpg',
 '86_1.jpg',
 '87_1.jpg',
 '88_1.jpg',
 '88_2.jpg',
 '89_1.jpg',
 '8_1.png',
 '8_2.png',
 '8_3.png',
 '90_1.jpg',
 '90_2.jpg',
 '91_1.jpg',
 '91_2.jpg',
 '91_3.jpg',
 '92_1.jpg',
 '92_2.jpg',
 '93_1.jpg',
 '94_1.jpg',
 '95_1.jpg',
 '95_2.jpg',
 '95_3.jpg',
 '95_4.jpg',
 '96_1.jpg',
 '96_2.jpg',
 '97_1.jpg',
 '98_1.jpg',
 '99_1.jpg',
 '9_1.png'], key  = lambda x : int(x.split('_')[0]))

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
        if str(num) == v.split('_')[0]:
            pics.append(v)

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


        # Визуализация
        
        import numpy as np
        import matplotlib.pyplot as plt

        # Известные данные
        t_known = np.arange(0, 160, 1)  # Пример значений от 0 до 160 с шагом 1
        # y_known = 147.9846921065483 + 0.023249539030893225 * t_known  # Пример функции y = 147.9846921065483 + 0.023249539030893225*t

        y_known = df['BBR_EA_M_I'].values

        n = 160  # Начальное значение t для прогноза
        t_future = np.arange(n, n + 4, 1)  # Пример значений от 160 до 163 (4 шага вперед) с шагом 1
        y_future = 147.9846921065483 + 0.023249539030893225 * t_future

        random_component = np.random.normal(0, 5, len(t_future))  # Пример: нормальный шум с средним 0 и стандартным отклонением 5

        # Создаем интервальный прогноз
        y_lower = y_future - u  # Нижняя граница интервального прогноза
        y_upper = y_future + u  # Верхняя граница интервального прогноза

        # Строим график
        plt.figure(figsize=(10, 6))

        # График известных данных
        plt.plot(t_known, y_known, label='Известные данные (y от t)', color='red')

        # График прогноза
        plt.plot(t_future, y_future, label='Средний прогноз', color='blue')

        # Интервал прогноза
        plt.fill_between(t_future, y_lower, y_upper, color='gray', alpha=0.3, label='Интервал прогноза')

        # Настройки графика
        plt.xlabel('t')
        plt.ylabel('y')
        plt.title('Интервальный прогноз на 4 шага вперед')
        plt.legend()
        plt.grid(True)
        plt.show()
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
            
            forecast = hw_model.forecast(steps=4

    # Визуализация
    index = pd.date_range(start='1/1/1993', periods=len(y), freq='M')
    ts = pd.Series(y, index=index)

    hw_model = sm.tsa.ExponentialSmoothing(ts, trend='add', seasonal='add', seasonal_periods=12).fit()

    forecast = hw_model.forecast(steps=4)

    plt.figure(figsize=(10, 6))
    plt.plot(ts, label='Исходные данные')
    plt.plot(hw_model.fittedvalues, color='red', label='Модель Хольта-Уинтерса')
    plt.plot(forecast, color='green', linestyle='--', label='Прогноз')
    plt.xlabel('Дата')
    plt.ylabel('Значение')
    plt.title('Модель Хольта-Уинтерса и прогноз')
    plt.legend()
    plt.grid(True)
    plt.show()
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

def tobit():
    return('''
    import math
    import warnings
    
    import numpy as np
    import pandas as pd
    from scipy.optimize import minimize
    import scipy.stats
    from scipy.special import log_ndtr
    from sklearn.linear_model import LinearRegression
    from sklearn.metrics import mean_squared_error, mean_absolute_error
    
    
    def split_left_right_censored(x, y, cens):
        counts = cens.value_counts()
        if -1 not in counts and 1 not in counts:
            warnings.warn("No censored observations; use regression methods for uncensored data")
        xs = []
        ys = []
    
        for value in [-1, 0, 1]:
            if value in counts:
                split = cens == value
                y_split = np.squeeze(y[split].values)
                x_split = x[split].values
    
            else:
                y_split, x_split = None, None
            xs.append(x_split)
            ys.append(y_split)
        return xs, ys
    
    
    def tobit_neg_log_likelihood(xs, ys, params):
        x_left, x_mid, x_right = xs
        y_left, y_mid, y_right = ys
    
        b = params[:-1]
        # s = math.exp(params[-1])
        s = params[-1]
    
        to_cat = []
    
        cens = False
        if y_left is not None:
            cens = True
            left = (y_left - np.dot(x_left, b))
            to_cat.append(left)
        if y_right is not None:
            cens = True
            right = (np.dot(x_right, b) - y_right)
            to_cat.append(right)
        if cens:
            concat_stats = np.concatenate(to_cat, axis=0) / s
            log_cum_norm = scipy.stats.norm.logcdf(concat_stats)  # log_ndtr(concat_stats)
            cens_sum = log_cum_norm.sum()
        else:
            cens_sum = 0
    
        if y_mid is not None:
            mid_stats = (y_mid - np.dot(x_mid, b)) / s
            mid = scipy.stats.norm.logpdf(mid_stats) - math.log(max(np.finfo('float').resolution, s))
            mid_sum = mid.sum()
        else:
            mid_sum = 0
    
        loglik = cens_sum + mid_sum
    
        return - loglik
    
    
    def tobit_neg_log_likelihood_der(xs, ys, params):
        x_left, x_mid, x_right = xs
        y_left, y_mid, y_right = ys
    
        b = params[:-1]
        # s = math.exp(params[-1]) # in censReg, not using chain rule as below; they optimize in terms of log(s)
        s = params[-1]
    
        beta_jac = np.zeros(len(b))
        sigma_jac = 0
    
        if y_left is not None:
            left_stats = (y_left - np.dot(x_left, b)) / s
            l_pdf = scipy.stats.norm.logpdf(left_stats)
            l_cdf = log_ndtr(left_stats)
            left_frac = np.exp(l_pdf - l_cdf)
            beta_left = np.dot(left_frac, x_left / s)
            beta_jac -= beta_left
    
            left_sigma = np.dot(left_frac, left_stats)
            sigma_jac -= left_sigma
    
        if y_right is not None:
            right_stats = (np.dot(x_right, b) - y_right) / s
            r_pdf = scipy.stats.norm.logpdf(right_stats)
            r_cdf = log_ndtr(right_stats)
            right_frac = np.exp(r_pdf - r_cdf)
            beta_right = np.dot(right_frac, x_right / s)
            beta_jac += beta_right
    
            right_sigma = np.dot(right_frac, right_stats)
            sigma_jac -= right_sigma
    
        if y_mid is not None:
            mid_stats = (y_mid - np.dot(x_mid, b)) / s
            beta_mid = np.dot(mid_stats, x_mid / s)
            beta_jac += beta_mid
    
            mid_sigma = (np.square(mid_stats) - 1).sum()
            sigma_jac += mid_sigma
    
        combo_jac = np.append(beta_jac, sigma_jac / s)  # by chain rule, since the expression above is dloglik/dlogsigma
    
        return -combo_jac
    
    
    class TobitModel:
        def __init__(self, fit_intercept=True):
            self.fit_intercept = fit_intercept
            self.ols_coef_ = None
            self.ols_intercept = None
            self.coef_ = None
            self.intercept_ = None
            self.sigma_ = None
    

        def fit(self, x, y, cens, verbose=False):
            """
            Fit a maximum-likelihood Tobit regression
            :param x: Pandas DataFrame (n_samples, n_features): Data
            :param y: Pandas Series (n_samples,): Target
            :param cens: Pandas Series (n_samples,): -1 indicates left-censored samples, 0 for uncensored, 1 for right-censored
            :param verbose: boolean, show info from minimization
            :return:
            """
            x_copy = x.copy()
            if self.fit_intercept:
                x_copy.insert(0, 'intercept', 1.0)
            else:
                x_copy.scale(with_mean=True, with_std=False, copy=False)
            init_reg = LinearRegression(fit_intercept=False).fit(x_copy, y)
            b0 = init_reg.coef_
            y_pred = init_reg.predict(x_copy)
            resid = y - y_pred
            resid_var = np.var(resid)
            s0 = np.sqrt(resid_var)
            params0 = np.append(b0, s0)
            xs, ys = split_left_right_censored(x_copy, y, cens)
    
            result = minimize(lambda params: tobit_neg_log_likelihood(xs, ys, params), params0, method='BFGS',
                              jac=lambda params: tobit_neg_log_likelihood_der(xs, ys, params), options={'disp': verbose})
            if verbose:
                print(result)
            self.ols_coef_ = b0[1:]
            self.ols_intercept = b0[0]
            if self.fit_intercept:
                self.intercept_ = result.x[1]
                self.coef_ = result.x[1:-1]
            else:
                self.coef_ = result.x[:-1]
                self.intercept_ = 0
            self.sigma_ = result.x[-1]
            return self
    
        def predict(self, x):
            return self.intercept_ + np.dot(x, self.coef_)
    
        def score(self, x, y, scoring_function=mean_absolute_error):
            y_pred = np.dot(x, self.coef_)
            return scoring_function(y, y_pred)
    ''')

def ma():
    return('''
    import statsmodels.tsa.arima.model as smt
    MA_1 = smt.ARIMA(df['SBER_arifm_profit'], order=(0, 0, q)) # q из MA(q) 
    MA_1_res = MA_1.fit()
    print(MA_1_res.summary())
    ''')

def ar():
    return('''
    from statsmodels.tsa.ar_model import AutoReg
    from statsmodels.graphics.tsaplots import plot_acf
    from statsmodels.tsa.api import AutoReg
    from sklearn.metrics import mean_absolute_error, mean_squared_error

    AR_1 = smt.ARIMA(df['SBER_arifm_profit'], order=(q, 0, 0)) # q из AR(q) 
    AR_1_res = AR_1.fit()
    print(AR_1_res.summary())
    ''')

def arma():
    return('''
    from statsmodels.tsa.arima.model import ARIMA
    #ARMA(1,1)
    ARMA_model11 = ARIMA(df['SBER_arifm_profit'], order=(1, 0, 1))
    ARMA_res11 = ARMA_model11.fit()
    print(ARMA_res11.summary())
    ''')

def arima():
    return('''
    mod = sm.tsa.arima.ARIMA(endog, order=(1, 0, 0))
    res = mod.fit()
    print(res.summary())
    ''')

def kmnk():
  return('''
  #отделяем все y
  y1 = data[название y1]
  y2 = data[название y2]
  X = data.drop([название y1, название y2], axis = 1) # удаляем все y из X
  model1 = sm.OLS(y1, X).fit()
  print(model1.summary())
  model2 = sm.OLS(y2, X).fit()
  print(model2.summary())
  # находим коэффициенты для каждой модели и с помощью формулы приведенной модели находим коэффициенты для a1, a2, b1, b2(те для изначальных моделей)
  #пример:
  # у нас получается приведенная форма с такими же регрессорами, как и в наших моделях, после чего мы
  # приравниваем коэффициенты из привиденной формы к найденным коэффициентам из оцененных уравнений
  Solve = sp.solve(((a2*b1/(-a2*b2 + 1) - 0.2534), (a1/(-a2*b2 + 1) - 3.2257),
             (b1/(-a2*b2 + 1) - 0.000003),(a1*b2/(-a2*b2 + 1) - 0.0003)),
             (a1, a2, b1, b2), dict = True)[0]
  # где численные значения это найденные значения коэффициентов
  ''')

def dmnk():
  return('''
  #отделяем все y
  y1 = data[название y1]
  y2 = data[название y2]
  X = data.drop([название y1, название y2], axis = 1) # удаляем все y из X
  model1 = sm.OLS(y1, X).fit()
  print(model1.summary())
  model2 = sm.OLS(y2, X).fit()
  print(model2.summary())
  # находим коэффициенты для каждой модели
  # далее находим значения y1_heat и y2_heat, подставляя найденные коэффициенты
  #пример
  data['sber_new'] = 0.2534 * df_1['time'] + 3.2257 * df_1['usd']
  data['vtb_new'] = 0.000003 * df_1['time'] + 0.0003 * df_1['usd']
  # теперь мы оцениваем изначальную систему уравнению, но вместо y в левой части подстовляем новые y с шапочкой
  # пример:
  model3 = sm.OLS(y1, data.drop(['vtb', 'sber', 'time', 'sber_new'], axis = 1)).fit()
  print(model3.summary())
  model4 = sm.OLS(y2, df_1.drop(['vtb', 'sber', 'usd', 'vtb_new'], axis = 1)).fit()
  print(model4.summary())
  # ну и найденные коэффициенты уже будут искомыми
  ''')

def tmnk():
  return('''
  from statsmodels.regression.linear_model import GLS
  #далее все шаги, как в 2мнк
  #отделяем все y
  y1 = data[название y1]
  y2 = data[название y2]
  X = data.drop([название y1, название y2], axis = 1) # удаляем все y из X
  model1 = sm.OLS(y1, X).fit()
  print(model1.summary())
  model2 = sm.OLS(y2, X).fit()
  print(model2.summary())
  # находим коэффициенты для каждой модели
  # далее находим значения y1_heat и y2_heat, подставляя найденные коэффициенты
  #пример
  data['sber_new'] = 0.2534 * df_1['time'] + 3.2257 * df_1['usd']
  data['vtb_new'] = 0.000003 * df_1['time'] + 0.0003 * df_1['usd']
  # ВОТ ТЕПЕРЬ НАЧИНАЕТСЯ ОТЛИЧИЕ ОТ 2МНК
  # все отличие в том, что мы используем GLS модель с коэффициентом ковариации
  model5 = GLS(y1, df_1.drop(['vtb', 'sber', 'time', 'sber_new'], axis = 1), sigma=(model3.resid.cov(model4.resid))).fit()
  print(model5.summary())
  model6 =  GLS(y2, df_1.drop(['vtb', 'sber', 'usd', 'vtb_new'], axis = 1), sigma=(model3.resid.cov(model4.resid))).fit()
  print(model6.summary())
  # ну и найденные коэффициенты уже будут искомыми
  ''')

def sur():
  return('''
  # библиотека
  from linearmodels.system import SUR
  model_sur = SUR({
      'eq1': {
          'dependent': df_1['sber'],
          'exog': df_1[['time', 'usd']]
      },
      'eq2': {
          'dependent': df_1['vtb'],
          'exog': df_1[['usd', 'time']]
      }
  }).fit()
  print(model_sur.summary)
  a1, a2, b1, b2 = model_sur.params
  # найденные коэффициенты
  ''')

def sistema_ident():
    return('''
    это задание на бумаге можно делать

    Определяем вектор(столбец) эндогенных переменных: Y = (y1, y2)
    Определяем вектор(столбец) экзогенных переменных: X = (x1, x2)
    Вектор(столбец) ошибок: U = (u1, u2)
    Переносим все X и Y влево в уравнениях, справа ошибки остаются.

    Определяем матрицу коэффициентов эндогенных переменных
    A = sp.Matrix() # размер (колво уравнений, колво Y)
    Определяем матрицу коэффициентов экзогенных переменных
    B = sp.Matrix() # размер (колво уравнений, колво X)

    Приведенная форма находится из: Y = -A**(-1) * B * X + A**(-1) * U

    Условие ранга:
    Расширенная матрица структурной формы модели
    A_hat = A.row_join(B)

    Далее берем первую строку этой матрицы (A1_hat) и 
    определяе матрицу коэффициентов системы ограничений 1 уравнения
    R1 = sp.Matrix() #размер (колво нулей в A1_hat * колво столбцов в A1_hat)
    Смотрим ранг матрицы: r = (A_hat * R1.T).rank()
    Если r = m - 1 (m - колво уравнений в системе), то 1 ур. идентифицируемо.
    Повторяем для всех!
    Если все ур. идентифицируемы, то и система.

    Правило порядка(необходимое усл):
    Считаем для уравнения H и D. 
    H - число эндогенных в данному ур.
    D - число экзогенных, которых нет! в этом ур., но они есть в системе
    Если D = H - 1, то ур. точно идент.
    Если D > H - 1, то ур. сверхидент.
    Если D < H - 1, то ур. неидент.

    Если хотя бы одно неидент., то и система.
    Если хотя одно сверх, то и система.
    Если все точно, то и система.
    ''')

def panel():
    return('''
    df = df.set_index(['i','t']) #i территориальный столбец, t отвечает за временной момент
    y = df['Y']
    X = df.drop(['Y'], axis=1)

    # Объединенная модель(pool)
    from linearmodels import PooledOLS
    pool = PooledOLS(Y, X).fit()
    print(pool.summary)

    #FE 
    from linearmodels.panel import PanelOLS
    FE = PanelOLS(Y, X, entity_effects=True).fit()
    print(FE.summary)

    #RE
    from linearmodels.panel import RandomEffects
    RE = RandomEffects(Y, X).fit()
    print(RE.summary)

    #F-тест (pool vs FE) H0: мю_1 = ... = мю_i = ... = мю_n
    from scipy.stats import f

    RSS_pool = pool.resid_ss
    RSS_FE = FE.resid_ss
    #k - колво эндогенных
    #T - колво временных моментов
    #n - колво строк в одном временном моменте! 
    n = len(Y)/T
    F = ((RSS_pool - RSS_FE)/(n - 1))/(RSS_FE/(n*T - n - k))
    F_crit = f(n - 1, n*T - n - k).isf(0.95)
    # Если F < F_crit, то H0 не отклоняется - лучше пул. Если F > F_crit, то H0 отвергается - лучше FE
    # фиксированные эффекты в FE, учитывающие гетерогенность объектов, статистически значимо влияют на Y

    #тест Хаусмана (RE vs FE); H0: отсутствует корреляция случайного эффекта с регрессорами(cov=0); H1: cov=!0
    import scipy.stats as stats

    delta_cov = FE.cov - RE.cov
    delta_coef = FE.params - RE.params
    hausman_stat = np.dot(np.dot(delta_coef.T, np.linalg.inv(delta_cov)), delta_coef)
    k = len(delta_coef) #степени свободы
    p_value = stats.chi2.sf(hausman_stat, k)

    print('Статистика Хаусмана:', hausman_stat)
    print('p-значение:', p_value)
    #Если p_value < 0.05, то H0 отвергается - лучше FE
    #Если p_value > 0.05, то H0 не отвергается - лучше RE

    #тест Бройша-Пагана (pool vs RE) H0: равенство межгрупповой дисперсии нулю (сигма:2 = 0)
    def BP_test(df, pool, alpha=0.05):
    df_pool_resids = pd.concat([df, pool.resids], axis=1)
    df_pool_resids_mean = df_pool_resids.groupby(level=0).mean()
    ssr_grouped_resids_mean = (df_pool_resids_mean['residual']**2).sum()
    ssr_pool_resids = (pool.resids**2).sum()
    n = df_pool_resids_mean.index.size
    T = df.shape[0]/n
    bp_statistic = (n * T)/(2 * (T-1)) * ((T**2 *ssr_grouped_resids_mean)/ssr_pool_resids - 1)**2
    chi2_critical = chi2.ppf((1.0-alpha), 1)
    print(f'Значение статистики : {bp_statistic:.4f}', end=' ')
    if bp_statistic < chi2_critical:
        print(f'< {chi2_critical:.4f} Пул модель')
    else:
        print(f'> {chi2_critical:.4f} - Модель RE')

    BP_test(df, pool_res, 0.05)
    ''')

def auto_arima():
    return('''
        import pmdarima as pm
        import pandas as pd
        from sklearn.datasets import load_iris
        from pmdarima import utils
        from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

        model_1 = pm.auto_arima(
            data, # сами значения y
            start_p=1, 
            start_q=1,
            max_p=3,
            max_q=3,
            max_d = 3,
            seasonal=False, # базовый параметр для того, чтобы не учитывать сезонность
            trace=True,
            test = 'adf' # тест Дикки-Фулера для получения оптимального d
        )

        print(model_1.summary())
        # модель сама подобрала нужные значения d, p, q
        #получим дифференцированный датасет
        data_diff = utils.diff(data, differences = d)
        #построим acf(Функция автокорреляции (ACF) - это статистический метод, который мы можем использовать для определения того, насколько коррелированы значения во временном ряду друг с другом.)
        plot_acf(delta_y, lags=20)
        plt.title('Визуализация ACF')
        plt.xlabel('Лаги')
        plt.ylabel('Корреляция')
        plt.show()
        # построим функцию pacf(Частичная автокорреляция - это статистический показатель, который фиксирует корреляцию между двумя переменными после учета влияния других переменных.
        plot_pacf(delta_y, lags=20, method = 'ywm')
        plt.title('Визуализация PACF')
        plt.xlabel('Лаги')
        plt.ylabel('Корреляция')
        plt.show())
        ''')

def visualization():
    return('''
          from statsmodels.tsa.seasonal import seasonal_decompose
          import matplotlib.pyplot as plt
          result = seasonal_decompose(y, model='additive', period=4)
          fig, axes = plt.subplots(ncols=1, nrows=4, sharex=True, figsize=(10,8))
          result.observed.plot(ax=axes[0], legend=False, color='black')
          axes[0].set_ylabel('Наблюдаемые данные')
          result.trend.plot(ax=axes[1], legend=False, color='red')
          axes[1].set_ylabel('Тренд')
          result.seasonal.plot(ax=axes[2], legend=False, color='purple')
          axes[2].set_ylabel('Сезонность')
          result.resid.plot(ax=axes[3], legend=False, color='green')
          axes[3].set_ylabel('Остатки')
          plt.show()
    ''')

def metod_proverki_paznosti_srednix_yrovnei():
    return('''
      # считаем расчетное значение критерия Фишера
      med = round(len(y)/2)
      y1 = y[:med]
      y2 = y[med:]
      var1 = np.var(y1)
      var2 = np.var(y2)
      F = var2/var1

      # считаем табличное значение критерия Фишера
      from scipy.stats import f
      alpha = 0.05
      F_crit = f.ppf(1 - alpha, len(y1) - 1, len(y2) - 1)
      F < F_crit # если true гипотеза о равенстве дисперсий принимается
      # переходим к следующему этапу
      # если false, то метод не подходит!

      # считаем расчетное значение критерия Стьюдента
      n1, n2 = len(y1), len(y2)
      s = np.sqrt(((n1-1)*var1 + (n2-1)*var2)/(n1+n2-2))
      t = abs(np.mean(y1) - np.mean(y2))/(s*np.sqrt(1/n1 + 1/n2))

      # считаем табличное значение критерия Стьюдента
      from scipy.stats import t
      alpha = 0.05
      t_crit = t.ppf(1 - alpha/2, (n1+n2-2))
      # если t<t_crit принимается гипотеза об отсутствии тренда
    ''')

def Chetverikov_easy():
    return('''
    import pandas as pd
    import matplotlib.pyplot as plt
    import statsmodels.api as sm

    result = sm.tsa.seasonal_decompose(ser, model='additive', period=4)
    fig, axes = plt.subplots(ncols=1, nrows=4, sharex=True, figsize=(10,8))
    result.observed.plot(ax=axes[0], legend=False, color='black')
    axes[0].set_ylabel('наблюдаемые')
    result.trend.plot(ax=axes[1], legend=False, color='red')
    axes[1].set_ylabel('Тренд')
    result.seasonal.plot(ax=axes[2], legend=False, color='purple')
    axes[2].set_ylabel('Сезонность')
    result.resid.plot(ax=axes[3], legend=False, color='green')
    axes[3].set_ylabel('остатки')
    plt.show()


    fig, axes = plt.subplots(nrows=2, figsize=(12,10))
    #первая сезонная
    decomposition = sm.tsa.seasonal_decompose(ser, model='additive', period=4)
    axes[0].set_title('')
    decomposition.seasonal.plot(ax=axes[0], color='orange', marker='o')
    axes[0].grid()
    #вторая сезонная
    decomposition = sm.tsa.seasonal_decompose(ser, model='additive', period=4*2)
    axes[1].set_title('')
    decomposition.seasonal.plot(ax=axes[1], color='red', marker='o')
    axes[1].grid()

    #остатки
    fig, axes = plt.subplots(1,1, figsize=(12, 8))
    plt.title('Остатки')
    result.resid.plot(marker='o', color='green')
    plt.ylabel('y')
    plt.grid()
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
        'pacf' : pacf(),
        'модель тобита' : tobit(),
        'tobit' : tobit(),
        'скользящее среднее' : ma(),
        'ma' : ma(),
        'ar' : ar(),
        'авторегрессия' : ar(),
        'autoregression' : ar(),
        'arima' : arima(),
        'arma' : arma(),
        'кмнк' : kmnk(),
        'kmnk' : kmnk(),
        'dmnk' : dmnk(),
        'дмнк' : dmnk(),
        'tmnk' : tmnk(),
        'тмнк' : tmnk(),
        '3мнк' : tmnk(),
        'сур' : sur(),
        'sur' : sur(),
        'идентифицируемость, приведенная форма, правила ранга и порядка' : sistema_ident(),
        'панельные данные' : panel(),
        'panel' : panel(),
        'auto arima' : auto_arima(),
        'авто arima' : auto_arima(),
        'визуализация' : visualization(),
        'visualization' : visualization(),
        'метод проверки разностей средних уровней' : metod_proverki_paznosti_srednix_yrovnei(),
        'metod proverki paznosti srednix yrovnei' : metod_proverki_paznosti_srednix_yrovnei(),
        'Chetverikov easy' : Chetverikov_easy(),
        'легкий четвериков' : Chetverikov_easy()
        
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
