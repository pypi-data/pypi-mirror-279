import pyperclip as pc

def hhelp():
    """в словаре название темы - название функции"""
    z = ''' во всех функциях (кроме импортов) аргументом является часть задания, если выводить функцию от 0, выведет общее условие
{'Импорты' : 'imports',
'Ирвин' : 'irvin',
'Браун-Четвериков' : 'brown',
'Панельные данные' : 'panel',
'Хольт-Уинстер-Четвериков' : 'holt',
'ARMA' : 'arma',
'Логит' : 'logit',
'СОУ' : 'sou'}'''
    pc.copy(z)


def imports():
    pc.copy('''
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller
from scipy.stats import shapiro
from scipy.stats import t
import numpy as np            
''')

def irvin(n):
    if n == 0:
        pc.copy('''
1. Предварительный анализ временных рядов. Построить график и провести визуальный анализ. Результаты описать.  (5 баллов)											
											
2.Провести выявление аномальных наблюдений с помощью использования распределения Стьюдента, Метода Ирвина. Написать выводы. Использовать один метод на выбор.  (9 баллов)											
											
3. Провести проверку наличия тренда с помощью: Критерия серий, основанный на медиане,
Метода проверки разности средних уровней, Метода Фостера-Стьюарта. Использовать один метод на выбор.  (9 баллов)											
											
4. Провести сглаживание временных рядов с помощью:  Взвешенной (средневзвешенной) скользящей средней,  а также провести Экспоненциальное сглаживание. Привести аналитические выводы.  (7 баллов)											             
''')
        
    if n == 1:
        pc.copy('''
df = pd.read_excel('Билеты.xlsx', sheet_name='Вариант1')
df1 = df[['T', 'EMPLDEC_Y']].dropna()
df1['EMPLDEC_Y'] = df1['EMPLDEC_Y'].astype(float)
df1['T'] = pd.period_range(start='1994', end='2021', freq='Y')
df1.head()

plt.figure(figsize = (8, 5))
plt.plot(range(len(df1)),df1['EMPLDEC_Y'], marker = '.')
plt.title('Потребность в работниках (EMPLDEC_Y)')
plt.xlabel('Временной период')
plt.ylabel('EMPLDEC_Y')
plt.show()

# Проверим данные на стационарность
            
adf_test = adfuller(df1['EMPLDEC_Y'])
if adf_test[1] > 0.05:
    print(adf_test[1], ': ряд не стационарен, значит есть сезонность и тренд присутсвуют')
else:
    print(adf_test[1], 'ряд стационарен')
            
# Проверим данные на нормальность
            
statistic, p_value = shapiro(df1['EMPLDEC_Y'])
alpha = 0.05
if p_value > alpha:
    print(f"{p_value=} > {alpha=}")
    print("Данные имеют нормальное распределение (H0 не отвергается)")
else:
    print(f"{p_value=} < {alpha=}")
    print("Данные распределены не нормально(H0 отвергается)")
''')
        
    if n == 2:
        pc.copy('''            
def calculate_irwin_scores(df):
    df['Expected'] = df['EMPLDEC_Y'].rolling(window=5).mean()
    df['Std'] = df['EMPLDEC_Y'].rolling(window=5).std()
    df['Irwin Score'] = abs(df['EMPLDEC_Y'] - df['Expected']) / df['Std']
    return df
data = calculate_irwin_scores(df1)
table_score = 1.8
anomalies = df1[df1['Irwin Score'] > table_score]
print("Аномальные наблюдения:", anomalies)
            
if anomalies.empty:
    print("Аномальных наблюдений не обнаружено")
else:
    print("Обнаружены аномальные наблюдения. Необходимо дополнительное исследование.")
            
# Воспользовавшись методом Ирвина, аномалий выявлено не было, следовательно можно продолжить исследование тренда.
''')
        
    if n == 3:
        pc.copy('''            
# Воспользуемся методом критерий серий, основанный на медиане. Ранжируем исходный ряд, найдем медиану, образуется последовательность $\delta_i$ из положительных и отрицательных значений, подсчитаем число серий и проверим гипотезу о наличии тренда.

y = df1['EMPLDEC_Y'].sort_values()
n = len(y)
delta_i = y > np.median(y)
series_count = 2
max_ser = max(len(np.where(delta_i == False)[0]), len(np.where(delta_i == True)[0])) # протяженность самой длинной серии
condition_1 = 3.3*(np.log10(n)+1)
condition_2 = 1/2*(n+1-1.96*np.sqrt(n-1))
if not max_ser < condition_1 or not series_count > condition_2:
    print('H_0 отвергается. Тренд присутствует')
else:
    print('H_0 принимается. Тренда нет')
            

# Метод показал, что тренд присутствует
''')
    
    if n == 4:
        pc.copy('''
# Проведем сглаживание с помощью взвешенной скользящей средней

moving_average = df1['EMPLDEC_Y'].rolling(window = 4).mean()
moving_average
                
plt.figure(figsize = (8, 6))
plt.plot(df1['EMPLDEC_Y'], label ='EMPLDEC_Y',)
plt.plot(df1['EMPLDEC_Y'].rolling(window = 4).mean(),label = 'Скользящее среднее по годам')
plt.legend()
plt.xlabel('Годы')
plt.ylabel('EMPLDEC_Y')
plt.show()
                
# Применим экспоненциальное сглаживание
                
df1['Exponential_Smoothing'] = df1['EMPLDEC_Y'].ewm(alpha=0.25).mean()
print("Экспоненциальное сглаживание:")
print(df1['Exponential_Smoothing'])
                
plt.figure(figsize = (8, 6))
plt.plot(df1['EMPLDEC_Y'],label = 'EMPLDEC_Y',)
plt.plot(df1['Exponential_Smoothing'],label = 'экспоненциальное сглаживание')
plt.legend()
plt.xlabel('Годы')
plt.plot()
                
# Можно заметить, что взвешенная скользящая средняя является более точной по сравнению с экспоненциальным сглаживанием, следовательно ее значения расположены ближе к действительным значениям потребности работников.
''')
        

def brown(n):
    
    if n == 0:
        pc.copy('''
1. Провести прогнозирование с помощью кривой роста. Рассчитать точечный и интервальный прогноз на 4 периода вперед. (10 баллов)											
											
2. Осуществить прогнозирование с применением адаптивной модели прогнозирования Брауна.  (10 баллов)											
											
"3. Выделение компонент тренд-сезонного временного ряда. Метод Четверикова: По заданным значениям временного ряда y_t выделить компоненты временного ряда: тренд f_t, сезонную компоненту S_t и остаточную последовательность ε_t.   (10 баллов)
Построить следующие диаграммы: 
1. Исходный ряд, тренды: предварительный, первый и второй. 
2. Сезонную волну: первую и вторую. 
3. Остаточную компоненту."''')
    
    if n == 1:
        pc.copy('''
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.seasonal import seasonal_decompose

df = pd.read_excel('Билеты.xlsx', sheet_name='Вариант2')

df = df[['T','INVFC_Q_DIRI']].dropna()
df['INVFC_Q_DIRI'] = df['INVFC_Q_DIRI'].astype(float)
df['T'] = pd.period_range(start='1/1/2008', end='10/1/2021', freq='Q').to_timestamp()
df = df.set_index(['T'])

plt.figure(figsize = (10,6))
plt.plot(df.index, df['INVFC_Q_DIRI'], '-o')
plt.title('Индекс реальных инвестиций в основной капитал')
plt.ylabel('INVFC_Q_DIRI')
plt.grid()
plt.show()
                
# Найдем значения точечного прогноза и границы доверительных интервалов с помощью кривой роста

train = df[:-4]
test = df[-4:]

model = ExponentialSmoothing(train['INVFC_Q_DIRI'], seasonal_periods=12, trend='add', seasonal='add')
fit = model.fit()
forecast = fit.forecast(steps=4)
point_forecast = forecast.values

forecast_errors = df.values - forecast.values
stderr = np.std(forecast_errors)

lower = [fc - (1.96 * stderr / 2) for fc in point_forecast]
upper = [fc + (1.96 * stderr / 2) for fc in point_forecast]

print(f'Прогноз: {point_forecast}\nНижняя граница: {lower}\nВерхняя граница: {upper}')

# График

plt.figure(figsize=(10,6))
plt.plot(test.index, test['INVFC_Q_DIRI'], '-o', label='INVFC_Q_DIRI')
plt.plot(forecast.index, forecast, '-o', label='Прогноз')
plt.fill_between(forecast.index, lower, upper, alpha=0.25, label='Доверительный интервал',)
plt.legend()
plt.title('Кривая роста')
plt.grid()
plt.show()                                
                ''')
        
    if n == 2:
        pc.copy('''
def brown_single(v, alpha):
    forecast = np.zeros(len(v))
    level = np.zeros(len(v))
    error = np.zeros(len(v))
    level[0] = v[0]
    error[0] = v[1] - v[0]
    for i in range(1, len(v)):
        if i == 1:
            level[i] = v[i]
            error[i] = v[i] - v[i-1]
        else:
            level[i] = alpha * v[i] + (1 - alpha) * level[i-1]
            error[i] = alpha * (v[i] - v[i-1]) + (1 - alpha) * error[i-1]
        forecast[i] = level[i] + error[i]
    forecast[0] = v[0]- 3
    return forecast, level, error
                
alpha = 0.4
v = df['INVFC_Q_DIRI']
forecast, level, error = brown_single(v, alpha)

sse = np.sum(error**2)
std_error = np.sqrt(sse / (len(v) - 2))
coeff = t.isf(0.05/2, df.shape[0] - 1) # 95% доверительный интервал

plt.figure(figsize=(12, 6))
plt.plot(v.index, v, label='INVFC_Q_DIRI', marker='o')
plt.plot(v.index, forecast, label='Прогноз', marker='o')
plt.title('Метод адаптивного прогнозирования Брауна')
plt.grid()
plt.fill_between(v.index, forecast - coeff * std_error, forecast + coeff * std_error, alpha=0.25, label='Доверительный интервал',)
plt.legend();
                
# График показывает тренд изменения индекса реальных инвестиций со временем и сезонные колебания. Можно увидеть, что исходные данные и прогнозируемые значения практически близки, следовательно, прогнозирование является досточно точным.                
''')
        
    if n == 3:
        pc.copy('''
preliminary_trend = df['INVFC_Q_DIRI'].rolling(window=len(df)//2, center=True).mean()
first_trend = df['INVFC_Q_DIRI'].rolling(window=len(df)//3, center=True).mean()
second_trend = df['INVFC_Q_DIRI'].rolling(window=len(df)//4, center=True).mean()
fig = plt.figure(figsize=(10, 20))
result = seasonal_decompose(df, model='additive')


fig.add_subplot(711)
plt.plot(df.index, df['INVFC_Q_DIRI'])
plt.title('Исходный ряд')
plt.grid()

fig.add_subplot(712)
plt.title('Предварительный тренд')
plt.plot(preliminary_trend)
plt.grid();

fig.add_subplot(713)
plt.title('Первый тренд')
plt.plot(first_trend)
plt.grid();

fig.add_subplot(714)
plt.title('Второй тренд')
plt.plot(second_trend)
plt.grid();

fig.add_subplot(715)
seasonal_decompose(df['INVFC_Q_DIRI'], model='additive', period=12).seasonal.plot()
plt.title('Первая сезонная волна')
plt.grid()

fig.add_subplot(716)
seasonal_decompose(df['INVFC_Q_DIRI'], model='additive', period=12*2).seasonal.plot()
plt.title('Вторая сезонная волна')
plt.grid()

fig.add_subplot(717)
plt.title('Остатки временного ряда')
result.resid.plot()
plt.grid()

plt.tight_layout()
plt.show()
                
# На диаграммах видно, что данные имеют восходящий тренд и ярко выраженную сезонность
                ''')
        
def panel(n):
    if n == 0:
        pc.copy('''
Построить  модель, используя панельные данные, для прогнозирования коэффициента рождаемости с учетом специфики регионов РФ.
1.  составить спецификацию моделей (Pool, RM, FM) (5 баллов),
2. построить три типа моделей панельных данных, провести аналитическое исследование качества модолей. (10 баллов)
3. провести сравнительный анализ моделей, используя тесты Лагранжа, Хаусмана,Бреуша-Пагана. Сделать выводы.(5 баллов)
4. Построить прогноз по лучшей модели (выбор обосновать). Результаты моделирования и прогнозирования изобразить на графике. (10 баллов)	
                ''')

    if n == 1:
        pc.copy('''
"Pooled Regression": """
from linearmodels import PooledOLS

data = data.set_index(['Reg', 'Year'])

pooled = PooledOLS(y, X).fit()
pooled.summary

# спецификация как лин рег
""",
    "Fixed Effect Model": """
from linearmodels import PanelOLS

data = data.set_index(['Reg', 'Year'])

FE = PanelOLS(y, X, entity_effects=True).fit()
FE.summary

#коэффы областей
FE.estimated_effects

# спецификация как лин рег + FE.estimated_effects
""",
    "Random Effect Model": """
from linearmodels import RandomEffects

data = data.set_index(['Reg', 'Year'])

RE = RandomEffects(y, X).fit()
RE.summary

#коэффы областей
RE.estimated_effects

# спецификация как лин рег + RE.estimated_effects + u (сам случайный эффект)
"""
                ''')
        
    if n == 2:
        pc.copy('''
df = pd.read_excel('Билеты.xlsx', sheet_name='Вариант4')
data = df.drop(columns=df.columns[[7,8,9]])
data = data.set_index(['Название региона', 'Год'])
years = data.index.get_level_values('Год').to_list()
data['Год'] = pd.Categorical(years)
data.head()
                
# Функции для проверки значимости коэффициентов и уравнения в целом
def valuable(model):
    for coeff in model.pvalues.index:
        if model.pvalues[coeff] < 0.05:
            print(f'p-value = {model.pvalues[coeff]:.3f} < 0.05 => {coeff} значимый')
        else:
            print(f'p-value = {model.pvalues[coeff]:.3f} > 0.05 => {coeff} не значимый')

def valuable_exp(model):
    if model.f_statistic.pval < 0.05:
        print(f'p-value = {model.f_statistic.pval:.3f} < 0.05 => уравнение значимое')
    else:
        print(f'p-value = {model.f_statistic.pval:.3f} > 0.05 => уравнение не значимое')
                
# Построим модель Пула (Объединенную модель)
                
import statsmodels.api as sms
from linearmodels.panel import PanelOLS, PooledOLS

x = ['БЕЗРАБОТИЦА', 'СООТНОШЕНИЕ Б/Р', 'ИПЦ НА ЖИЛЬЕ', 'ИПЦ НА ПРОД ТОВАРЫ']
X = sms.add_constant(data[x])
y = data['КОЭФ РОЖД НА 1000 ЧЕЛ']
pooled_model = PooledOLS(y, X).fit(cov_type='clustered', cluster_entity=True)
print(pooled_model.params)
                
valuable(pooled_model)
                
x = ['БЕЗРАБОТИЦА', 'ИПЦ НА ЖИЛЬЕ', 'ИПЦ НА ПРОД ТОВАРЫ']
X = sms.add_constant(data[x])
pooled_model = PooledOLS(y, X).fit(cov_type='clustered', cluster_entity=True)
print(pooled_model.pvalues)
                
# перебираем коэф X пока все не станут значимы
                
x = ['БЕЗРАБОТИЦА']
X = sms.add_constant(data[x])
pooled_model = PooledOLS(y, X).fit(cov_type='clustered', cluster_entity=True)
print(pooled_model)
                
valuable(pooled_model), valuable_exp(pooled_model)
                
# Уравнение примет следующий вид:
# $ \hat{y} = -3.9051 + 0.5593x_1 + ϵ$
                
# Построим модель с фиксированными эффектами
                
x = ['БЕЗРАБОТИЦА', 'СООТНОШЕНИЕ Б/Р', 'ИПЦ НА ЖИЛЬЕ', 'ИПЦ НА ПРОД ТОВАРЫ']
X = sms.add_constant(data[x])
fix_model = PanelOLS(y, X, entity_effects=True, time_effects = False).fit(cov_type='clustered', cluster_entity=True)
print(fix_model.params)
                
#перебираем X по аналогии
x = ['БЕЗРАБОТИЦА', 'СООТНОШЕНИЕ Б/Р', 'ИПЦ НА ЖИЛЬЕ']
X = sms.add_constant(data[x])
fix_model = PanelOLS(y, X, entity_effects=True, time_effects = False).fit(cov_type='clustered', cluster_entity=True)
print(fix_model)
        
valuable(fix_model), valuable_exp(fix_model)
                
# Уравнение примет следующий вид:
# $ \hat{y} = 5.893 + 0.27x_1 - 0.0093x_2 - 0.0191x_3 + ϵ$

# Построим модель со случайными эффектами
                
from linearmodels.panel import RandomEffects
x = ['БЕЗРАБОТИЦА', 'СООТНОШЕНИЕ Б/Р', 'ИПЦ НА ЖИЛЬЕ', 'ИПЦ НА ПРОД ТОВАРЫ']
X = sms.add_constant(data[x])
random_model = RandomEffects(y, X).fit(cov_type='clustered', cluster_entity=True)
print(random_model.params, valuable(random_model))
                
#перебираем X по аналогии
x = ['БЕЗРАБОТИЦА', 'СООТНОШЕНИЕ Б/Р', 'ИПЦ НА ЖИЛЬЕ']
X = sms.add_constant(data[x])
random_model = RandomEffects(y, X).fit(cov_type='clustered', cluster_entity=True)
print(random_model)
                
valuable(random_model), valuable_exp(random_model)
                
# Уравнение примет следующий вид:
# $ \hat{y} = 5.4675 + 0.2949x_1 - 0.0089x_2 - 0.0193x_3 + ϵ$
                ''')
        
    if n == 3:
        pc.copy('''
# Сравним построенные модели и выберем наилучшую
# Объединенная модель VS модель с фиксированными эффектами(Тест Лагранжа)
                
from scipy.stats import f, chi2
SSr = pooled_model.resid_ss
SSur = fix_model.resid_ss
N = len(data)
T = 11
K = data.shape[1]-1
F = ((SSr - SSur) / (N-1)) / (SSur / (N*T - N - K))
F_krit = f.ppf(0.05, N*T - N - K, N-1)
print(f'F-статистика = {F:.3f}\nF_кр = {F_krit:.3f}\nЛучшая модель:')
if F > F_krit:
    print('Модель с фиксированными эффектами')
else: print('Объединенная модель')
                
# Объединенная модель VS случайные эффекты(Тест Бройша-Пагана )
                
LM = N*T/(2*(T-1)) * (sum(pooled_model.resids)**2 / pooled_model.resid_ss - 1)**2
print(f'chi2 = {LM:.3f}\nchi2_кр = {3.84}\nЛучшая модель:')
if LM > 3.84:  # при 0.05% уровне значимости хи2 распределение с 1 степенью свободы
    print('Модель со случайными эффектами')
else: print('объединенная модель')
                
# Модель с фиксированными эффектами VS модель со случайными эффектами(тест Хаусмана)
                
b_diff = fix_model.params - random_model.params # разницы оценок коэффициентов
cov_mat = fix_model.cov - random_model.cov  # ковариационной матрицы разности оценок коэффициентов
H = b_diff.dot(np.linalg.inv(cov_mat)).dot(b_diff)  # тестовой статистики хаусмана
chi_krit = chi2.ppf(0.95, len(b_diff))
print(f'статистика Хаусмана = {3.027}')
print(f'chi2_кр = {chi_krit:.3f}\nЛучшая модель:')
if H > chi_krit:
    print('Модель с фиксированными эффектами')
else: print('Модель со случайными эффектами')
                
# Проверки показали, что модель со случайными эффектами является наилучшей.
                ''')
    if n == 4:
        pc.copy('''
#Прогноз
data1 = data[data['Год'] == 2019]
X = sms.add_constant(data1[['БЕЗРАБОТИЦА', 'СООТНОШЕНИЕ Б/Р', 'ИПЦ НА ЖИЛЬЕ']])
pred_re = random_model.predict(X)
pred_re.reset_index(inplace=True)
plt.plot(pred_re['Название региона'], pred_re['predictions'].values, '-o', label='Прогноз', color='r')
plt.plot(pred_re['Название региона'], data1['КОЭФ РОЖД НА 1000 ЧЕЛ'].values, '-o', label='Реальные данные')
plt.grid()
plt.xticks(rotation=90)
plt.legend()
plt.plot();
                
# В данной работе была произведена обрабока и анализ панельных данных, построение моделей трех видов и их сравнение. Было выяснено, что наилучшей моделью является модель со случайными эффектами.

#Рассчет фиксированных эффектов
fix_model.estimated_effects
                ''')

def holt(n):
    if n == 0:
        pc.copy('''
1. Провести прогнозирование с помощью кривой роста. Рассчитать точечный и интервальный прогноз на 4 периода вперед. (10 баллов)
2. Моделирование тренд-сезонных процессов. Применить Модель Хольта-Уинтерса. (10 баллов) 											
3. Выделение компонент тренд-сезонного временного ряда. Метод Четверикова: По заданным значениям временного ряда y_t выделить компоненты временного ряда: тренд f_t, сезонную компоненту S_t и остаточную последовательность ε_t.   (10 баллов)
Построить следующие диаграммы: 
1. Исходный ряд, тренды: предварительный, первый и второй. 
2. Сезонную волну: первую и вторую. 
3. Остаточную компоненту.																		
                    ''')
    
    if n == 1:
        pc.copy('''
df = pd.read_excel('Билеты.xlsx', sheet_name='Вариант5')

df2 = df[['T','INVFC_Q_DIRI']].dropna()
df2['INVFC_Q_DIRI'] = df2['INVFC_Q_DIRI'].astype(float)
df2['T'] = pd.period_range(start='1/1/2007', end='10/1/2021', freq='Q').to_timestamp()
df2 = df2.set_index(['T'])

plt.figure(figsize = (10,6))
plt.plot(df2.index, df2['INVFC_Q_DIRI'], color='r')
plt.title('Индекс реальных инвестиций в основной капитал')
plt.ylabel('INVFC_Q_DIRI')
plt.grid()
plt.show()
                    
# Рассчитаем точечный и интервальный прогноз на 4 периода вперед

train = df2[:-4]
test = df2[-4:]

model = ExponentialSmoothing(train['INVFC_Q_DIRI'], seasonal_periods=12, trend='add', seasonal='add')
fit = model.fit()
forecast = fit.forecast(steps=4)
point_forecast = forecast.values

forecast_errors = df2.values - forecast.values
stderr = np.std(forecast_errors)

lower = [fc - (1.96 * stderr / 2) for fc in point_forecast]
upper = [fc + (1.96 * stderr / 2) for fc in point_forecast]

print(f'Прогноз: {point_forecast}\nНижняя граница: {lower}\nВерхняя граница: {upper}')
plt.figure(figsize=(10,6))
plt.plot(test.index, test['INVFC_Q_DIRI'], label='INVFC_Q_DIRI')
plt.plot(forecast.index, forecast, label='Прогноз')
plt.fill_between(forecast.index, lower, upper, alpha=0.25, label='Доверительный интервал',)
plt.legend()
plt.grid()
plt.show()

# Точечные и интервальные прогнозы достаточно сходятся с реальными значениями, что говорит о хорошей предсказательной способности                    
                    ''')
    if n == 2:
        pc.copy('''
#Применяем метод Хольта-Винтерса с сезонностью
model = ExponentialSmoothing(df2['INVFC_Q_DIRI'], seasonal_periods=12, trend='add', seasonal='add')
fit = model.fit()
forecast = fit.forecast(steps=12)
fit.summary()
                
#Строим прогноз с ее помощью
forecast_errors = df2.values - forecast.values
stderr = np.std(forecast_errors)

lower = [fc - (1.96 * stderr / 2) for fc in forecast.values]
upper = [fc + (1.96 * stderr / 2) for fc in forecast.values]

plt.figure(figsize=(10,6))
plt.plot(df2.index, df2['INVFC_Q_DIRI'], label='INVFC_Q_DIRI')
plt.plot(forecast.index, forecast, label='Прогноз')
plt.fill_between(forecast.index, lower, upper, alpha=0.25, label='Доверительный интервал',)
plt.legend()
plt.grid()
plt.show()
                
# Прогноз полученный при помощи модель Хольта-Винтерса достаточно точен. Точечные значения попадают в диапазон доверительного интервала                
                ''')
    if n == 3:
        pc.copy('''
# Прогноз полученный при помощи модель Хольта-Винтерса достаточно точен. Точечные значения попадают в диапазон доверительного интервала
# Построим графики:
# 1. Исходный ряд
# 2. Предварительный тренд
# 3. Первый тренд
# 4. Второй тренд
# 5. Первая сезонная волна
# 6. Вторая сезонная волна
# 7. Остатки временного ряда

preliminary_trend = df2['INVFC_Q_DIRI'].rolling(window=len(df2)//2, center=True).mean()
first_trend = df2['INVFC_Q_DIRI'].rolling(window=len(df2)//3, center=True).mean()
second_trend = df2['INVFC_Q_DIRI'].rolling(window=len(df2)//4, center=True).mean()
fig = plt.figure(figsize=(10, 20))
result = seasonal_decompose(df2, model='additive')


fig.add_subplot(711)
plt.plot(df2.index, df2['INVFC_Q_DIRI'], color='r')
plt.title('Исходный ряд')
plt.grid()

fig.add_subplot(712)
plt.title('Предварительный тренд')
plt.plot(preliminary_trend)
plt.grid();

fig.add_subplot(713)
plt.title('Первый тренд')
plt.plot(first_trend)
plt.grid();

fig.add_subplot(714)
plt.title('Второй тренд')
plt.plot(second_trend)
plt.grid();

fig.add_subplot(715)
seasonal_decompose(df2['INVFC_Q_DIRI'], model='additive', period=12).seasonal.plot(color='g')
plt.title('Первая сезонная волна')
plt.grid()

fig.add_subplot(716)
seasonal_decompose(df2['INVFC_Q_DIRI'], model='additive', period=12*2).seasonal.plot(color='g')
plt.title('Вторая сезонная волна')
plt.grid()

fig.add_subplot(717)
plt.title('Остатки временного ряда')
result.resid.plot(color='y')
plt.grid()

plt.tight_layout()
plt.show()
                ''')
        
def arma(n):
    if n == 0:
        pc.copy('''
1. Скачать с любого сайта данные о дневных ценах закрытия выбранной Вами акции в период с 01.06.2021 по 01.06.2022. (ряд 1)																	
2. Рассчитать доходность акции за выбранный период. (ряд 2) (2 балла)																	
3. Ряды 1 и 2 проверить, соответствуют ли они определению стационарных рядов. (8 баллов)																	
4. Построить автоковариационные функции. Построить их графики. Сделать аналитические выводы.(5 баллов)																	
5. Построить автокорреляционные функции. Построить их графики. Сделать аналитические выводы. (5 баллов)																	
6. Для ряда 2 построить: Модель AR(1), AR(2), ARMA(1,1)  и провести их сравнение. Сделать аналитические выводы (10 баллов)																	
                ''')
        
    if n == 1:
        pc.copy('''
from statsmodels.tsa.stattools import adfuller
import statsmodels.api as sm
from statsmodels.tsa.ar_model import AutoReg
from statsmodels.tsa.stattools import acovf
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error, mean_squared_error,  r2_score

df = pd.read_csv('NIKE2.csv', sep=';')
df['<DATE>'] = pd.to_datetime(df['<DATE>'])
df.set_index(['<DATE>'], inplace = True)
df = df.drop(df.columns[[0, 1, 2]], axis = 1)

plt.figure(figsize=(10, 3))
plt.plot(df.index, df['<CLOSE>'], label='<CLOSE>', linewidth=1.5)
plt.title('Котировки Nike')
plt.legend()
plt.show()
                ''')
    if n == 2:
        pc.copy('''
#Построение графика доходности акции
df['Доходность'] = df['<CLOSE>'].pct_change() * 100

df = df.dropna()

plt.figure(figsize=(10, 3))
plt.plot(df['Доходность'], label='Доходность', linewidth=1.5)
plt.legend()
plt.show()
                    ''')
    if n == 3:
        pc.copy('''
# Проверка на стационарность

def dickey_fuller(x):
    print('Статистика Дики-Фуллера: %f' % adfuller(x)[0])
    print('Р-value: %f' % adfuller(x)[1])

    if adfuller(x)[1] > 0.05:
        print(f"Ряд '{x.name}' не является стационарным, принимаем гипотезу H0")
    else:
        print(f"Ряд '{x.name}' является стационарным, отвергаем гипотезу H0")
                
dickey_fuller(df['<CLOSE>'])
                
dickey_fuller(df['Доходность'])
                ''')
    if n == 4:
        pc.copy('''
#Построение автоковариационных функций
#Для котировок
acf_values = acovf(df['<CLOSE>'], nlag=100)
plt.figure(figsize=(10, 3))
plt.stem(range(len(acf_values)), acf_values, markerfmt='bo', basefmt='b-')
plt.title('Автоковариационная функция')
plt.xlabel('Лаг')
plt.ylabel('Ковариация')
plt.show()
                
#Для доходности
acf_values = acovf(df['Доходность'], nlag=30)
plt.figure(figsize=(10, 3))
plt.stem(range(len(acf_values)), acf_values, markerfmt='bo', basefmt='b-')
plt.title('Автоковариационная функция')
plt.xlabel('Лаг')
plt.ylabel('Ковариация')
plt.show()
                ''')
    if n == 5:
        pc.copy('''
#Построение автокорреляционных функций
                
#Для котировок

fig = plt.figure(figsize = (12, 6))
ax1 = fig.add_subplot(211)
fig = sm.graphics.tsa.plot_acf(df['<CLOSE>'].values.squeeze(), lags=30, ax=ax1, title='Автокорреляционная функция (ACF)')
ax2 = fig.add_subplot(212)
fig = sm.graphics.tsa.plot_pacf(df['<CLOSE>'], lags=3, ax=ax2, title='Частная автокорреляционная функция (PACF)')
                
#доходность

fig = plt.figure(figsize = (12, 6))
ax1 = fig.add_subplot(211)
fig = sm.graphics.tsa.plot_acf(df['Доходность'].values.squeeze(), lags=30, ax=ax1, title='Автокорреляционная функция (ACF)')
ax2 = fig.add_subplot(212)
fig = sm.graphics.tsa.plot_pacf(df['Доходность'], lags=3, ax=ax2, title='Частная автокорреляционная функция (PACF)')
                ''')
    if n == 6:
        pc.copy('''
#Для ряда доходностей построить AR(1), AR(2), ARMA(1,1)

model_fit_ar1 = AutoReg(df['Доходность'], lags = 1).fit()

print(f"Критерий Акаике = {model_fit_ar1.aic:.3f}")

model_fit_ar2 = AutoReg(df['Доходность'], lags = 2).fit()

print(f"Критерий Акаике = {model_fit_ar2.aic:.3f}")

model_fit_arma = sm.tsa.arima.ARIMA(df['Доходность'], order=(1, 0, 1)).fit()

print(f"Критерий Акаике = {model_fit_arma.aic:.3f}")

aic_values = [model_fit_ar1.aic, model_fit_ar2.aic, model_fit_arma.aic]

model_names = ['AR(1)', 'AR(2)', 'ARMA(1,1)']

sorted_indices = sorted(range(len(aic_values)), key=lambda k: aic_values[k])
sorted_aic_values = [aic_values[i] for i in sorted_indices]
sorted_model_names = [model_names[i] for i in sorted_indices]

plt.bar(sorted_model_names, sorted_aic_values, color=['blue', 'green', 'orange'])
plt.xlabel('Модели')
plt.ylabel('Критерий Акаике')
plt.title('Сравнение моделей временных рядов (по возрастанию AIC)')
plt.show()
                ''')
def logit(n):
    if n == 0:
        pc.copy('''
здесь все в первом пункте, так как автор не сделал нормального разделения (прим. редакции)
1. Постройте спецификацию Логит и Пробит моделей для объясняющей переменной Default (6 баллов)								
2. Постройте Логит и Пробит модели со значимыми факторами, определите их прогнозную достоверность. (10 баллов)								
3. Определите долю каждого значимого фактора в моделях. (10 баллов)								
4. Сделайте аналитические выводы.																						
                ''')
    if n == 1:
        pc.copy('''
#логит
import statsmodels.discrete.discrete_model as sm
import statsmodels.tools.tools as smtools
import statsmodels.api as sma
from sklearn.metrics import accuracy_score
from scipy import stats

df = pd.read_excel('Билеты.xlsx', sheet_name='Вариант12', index_col=0)
df = df[df.columns[:6]]
y = df['Default']
X = df.drop(columns=['Default'])
df.head()
                
#Logit модель
logit = sm.Logit(y, smtools.add_constant(X)).fit()
print(logit.summary())
                
LR = 2*(logit.llf - logit.llnull)
print(f"Критерий отношения правдоподобия {LR:.3f}")
alpha = 0.05
k = 5
critical_value = stats.chi2.ppf(1 - alpha, k)
print(f"Критическое значение критерия {critical_value:.3f}")
                
# Критическое значение критерия хи-квадрат меньше, чем критерий отношения правдоподобия, следовательно, уравнение в целом значимо
                
z_values = logit.params.to_numpy() / np.sqrt(np.diag(logit.cov_params()))
z_crit = stats.norm.ppf(1 - alpha / 2)

print(f'z критическое {z_crit:.3f}\n')
print(f"z для каждого из признаков: {', '.join(map(lambda x: str(round(x, 3)), z_values.tolist()))}\n")
print(f"Признаки: const, {', '.join(X.columns)}")
                
# По результатам вычислений коэффициенты при признаках WC/TA, EBIT/TA, S/TA, RE/TA оказались не значимы, значит, необходимо построить модель без них
                
y = df['Default']
X = df.drop(columns=['Default', 'WC/TA', 'RE/TA', 'EBIT/TA', 'S/TA'])

logit = sm.Logit(y, smtools.add_constant(X)).fit()
print(logit.summary())
                
LR = 2*(logit.llf - logit.llnull)
print(f"Критерий отношения правдоподобия {LR:.3f}")
alpha = 0.05
k = 1
critical_value = stats.chi2.ppf(1 - alpha, k)
print(f"Критическое значение критерия {critical_value:.3f}")
                
# Критическое значение критерия хи-квадрат меньше, чем критерий отношения правдоподобия, следовательно, уравнение в целом значимо
                
z_values = logit.params.to_numpy() / np.sqrt(np.diag(logit.cov_params()))
z_crit = stats.norm.ppf(1 - alpha / 2)

print(f'z критическое {z_crit:.3f}\n')
print(f"z для каждого из признаков: {', '.join(map(lambda x: str(round(x, 3)), z_values.tolist()))}\n")
print(f"Признаки: const, {', '.join(X.columns)}")
                
# Все признаки модели значимы
                
print(f"Коэффициенты модели: b_0 = {logit.params[0]:.3f}, b_1 = {logit.params[1]:.3f}")

# Итоговый вид модели: $P(y = 1) = \frac{1}{1 + e^{-(-4.824 + 2.649 \cdot ME/TL)}}$
                
y_pred = np.where(logit.predict(smtools.add_constant(X)) > 0.5, 1, 0)
print(f"Точность предсказания модели {accuracy_score(y, y_pred)}")
                
# Получение долей значимых факторов в модели Logit
logit_coefficients = logit.params
logit_odds_ratios = np.exp(logit_coefficients)
logit_significant_factors = logit_odds_ratios[logit_odds_ratios != 1]
logit_significant_factors_percentage = (logit_significant_factors / sum(logit_significant_factors)) * 100
print('\nДоли значимых факторов в модели Logit:')
for factor, percentage in zip(logit_significant_factors.index, logit_significant_factors_percentage):
    print(f'{factor}: {percentage:.2f}%')
                
ls = np.linspace(min(X['ME/TL']), max(X['ME/TL']), 1000)
y_prob = 1 / (1 + np.exp(-(logit.params[0] + ls * logit.params[1])))

plt.scatter(X, y, label='Данные')
plt.plot(ls, y_prob, color='r', label='Предсказание модели')
plt.grid()
plt.legend()
plt.xlabel('ME/TL')
plt.ylabel('Вероятность')
plt.show()
                
#Пробит
y = df['Default']
X = df.drop(columns=['Default'])

probit = sm.Probit(y, smtools.add_constant(X)).fit()
print(probit.summary())
                
LR = 2*(probit.llf - probit.llnull)
print(f"Критерий отношения правдоподобия {LR:.3f}")
alpha = 0.05
k = 5
critical_value = stats.chi2.ppf(1 - alpha, k)
print(f"Критическое значение критерия {critical_value:.3f}")
                
# Критическое значение критерия хи-квадрат меньше, чем критерий отношения правдоподобия, следовательно, уравнение в целом значимо
                
z_values = probit.params.to_numpy() / np.sqrt(np.diag(probit.cov_params()))
z_crit = stats.norm.ppf(1 - alpha / 2)

print(f'z критическое {z_crit:.3f}\n')
print(f"z для каждого из признаков: {', '.join(map(lambda x: str(round(x, 3)), z_values.tolist()))}\n")
print(f"Признаки: const, {', '.join(X.columns)}")

# По результатам вычислений коэффициенты при признаках WC/TA, EBIT/TA, S/TA, RE/TA оказались не значимы, значит, необходимо построить модель без них
                
y = df['Default']
X = df.drop(columns=['Default', 'WC/TA', 'EBIT/TA', 'S/TA', 'RE/TA'])

probit = sm.Probit(y, smtools.add_constant(X)).fit()
print(probit.summary())По результатам вычислений коэффициенты при признаках WC/TA, EBIT/TA, S/TA, RE/TA оказались не значимы, значит, необходимо построить модель без них  

LR = 2*(probit.llf - probit.llnull)
print(f"Критерий отношения правдоподобия {LR:.3f}")
alpha = 0.05
k = 1
critical_value = stats.chi2.ppf(1 - alpha, k)
print(f"Критическое значение критерия {critical_value:.3f}")

# Критическое значение критерия хи-квадрат меньше, чем критерий отношения правдоподобия, следовательно, уравнение в целом значимо

z_values = probit.params.to_numpy() / np.sqrt(np.diag(probit.cov_params()))
z_crit = stats.norm.ppf(1 - alpha / 2)

print(f'z критическое {z_crit:.3f}\n')
print(f"z для каждого из признаков: {', '.join(map(lambda x: str(round(x, 3)), z_values.tolist()))}\n")
print(f"Признаки: const, {', '.join(X.columns)}")

# Все признаки модели значимы

print(f"Коэффициенты модели: b_0 = {probit.params[0]:.3f}, b_1 = {probit.params[1]:.3f}")

# Итоговый вид модели: $P(y = 1) = \Phi(-2.504 + 1.312 \cdot ME/TL)$                

y_pred = np.where(probit.predict(smtools.add_constant(X)) > 0.5, 1, 0)
print(f"Точность предсказания модели {accuracy_score(y, y_pred):.3f}")

# Получение долей значимых факторов в модели Probit
probit_coefficients = probit.params
probit_probabilities = stats.norm.cdf(probit_coefficients)
probit_significant_factors = probit_probabilities[probit_probabilities != 0.5]
probit_significant_factors_percentage = (probit_significant_factors / sum(probit_significant_factors)) * 100
print('\nДоли значимых факторов в модели Probit:')
for factor, percentage in zip(probit_coefficients.index, probit_significant_factors_percentage):
    print(f'{factor}: {percentage:.2f}%')

ls = np.linspace(min(X['ME/TL']), max(X['ME/TL']), 1000)
y_prob = stats.norm.cdf(probit.params[0] + ls * probit.params[1])

plt.scatter(X, y, label='Данные')
plt.plot(ls, y_prob, color='r', label='Предсказание модели')
plt.grid()
plt.legend()
plt.xlabel('ME/TL')
plt.ylabel('Вероятность')
plt.show()

# Вывод - Обе полученные модели имеют достаточно высокую степень правильности прогноза                
                ''')
        
def sou(n):
    if n == 0:
        pc.copy('''
# на это не было задания, так что тут все в нулевом номере
                
import pandas as pd
import sympy as sp
import numpy as np
import statsmodels.api as sm
                
# 1. приведенная форма

SBER_t, a_1, t, a2, VTB_t, u_t, b1, b2, v_t, USD_t = sp.symbols('SBER_t a_1 t a2 VTB_t u_t b1 b2 v_t USD_t')

A  = sp.Matrix(2,2,[1,-a2,-b2,1])
B = sp.Matrix(2,2,[-a_1, 0, 0, -b1])
U = sp.Matrix(2,1,[u_t, v_t])
-A**(-1) * B

A**(-1) * U

X  = sp.Matrix(2,1,[t,USD_t])
Y = sp.Matrix(2,1,[SBER_t, VTB_t])

display(Y, '=', (-A**(-1) * B) * X + A**(-1) * U)

# 2. правило порядка

2) D = 1, H = 2; D + 1 = H => точно идентифицируемо

1) D = 1, H = 2; D + 1 = H => точно идентифицируемо

# 3. правило ранга

A_hat = sp.Matrix.hstack(A,B)
R1 = sp.Matrix(1, 4, [0,0,0,1])
R2 = sp.Matrix(1, 4, [0,0,1,0])
A_hat * R1.T, (A_hat * R1.T).rank(), A_hat * R2.T, (A_hat * R2.T).rank()

# Так как для обоих уравнений, ранг = m - 1, где m - число уравнений системы, оба уравнения идентифицируемы

# 4. КМНК

m11, m12, m21, m22 = sp.symbols('m_11 m_12 m_21 m_22')
M_I = sp.Matrix(4, 2, [m11, m12, m21, m22,1,0,0,1])
(A_hat[0,:]*M_I)

(A_hat[1,:]*M_I)

data = pd.read_csv('usd_sber_vtb.csv')
data = data.iloc[::-1].reset_index(drop=True) 
data = pd.concat([data,pd.Series([i for i in range(488)])], axis=1)
data

# 1e уравнение      

sm.OLS(data['SBER'], data[[0,'USD']]).fit().summary()

# 2е уравнение

sm.OLS(data['VTB'], data[[0,'USD']]).fit().summary()

m_11 = 0.1064
m_12 = 2.2216
m_21 = -3.269e-05
m_22 = 0.0004
_a2 = m_12/m_22
_a1 = -(m_12*m_21/m_22) + m_11
_b2 = m_21/m_11
_b1 = -(m_12*m_21/m_11) + m_22
_a2, _a1, _b2, _b1

display(SBER_t, '=', _a1 * t + _a2 * VTB_t + u_t)

display(VTB_t, '=', _b1 * USD_t + _b2 * SBER_t + v_t)

# 5. 2МНК

t = data[0]
USD = data['USD']
SBER = data['SBER']
VTB = data['VTB']

X1 = sm.add_constant(pd.DataFrame({'t': t, 'USD': USD}))
model1 = sm.OLS(VTB, X1).fit() # модель для VTB_hat, а также модель 2го уравнения
data['VTB_hat'] = model1.predict(X1)

X2 = sm.add_constant(pd.DataFrame({'t': t, 'VTB_hat': data['VTB_hat']}))
model2 = sm.OLS(SBER, X2).fit() # модель для SBER_t, учитывая предсказания VTB_hat по мнк
data['SBER_hat'] = model2.predict(X2)

model1.summary()

model2.summary()

# 6. 3МНК

data['u_hat'] = SBER - data['SBER_hat']
data['v_hat'] = VTB - data['VTB_hat']

cov_matrix = data[['u_hat', 'v_hat']].cov()
cov_matrix

omega = sp.Matrix(cov_matrix)

(X.T * omega**(-1) * X)**(-1) * (X.T * omega**(-1) * Y)

# 7. SUR-модель

from linearmodels.system import SUR

data = pd.read_csv('usd_sber_vtb.csv')
data.columns = ['Date', 'USD', 'SBER', 'VTB']

data['t'] = np.arange(len(data))

combined_data = data[['SBER', 'VTB', 'USD', 't']]

formula = {
    'SBER': 'SBER ~ t + VTB',
    'VTB': 'VTB ~ t + USD'
}

model = SUR.from_formula(formula, data=combined_data)
results = model.fit()

results.summary
                                                     
                ''')