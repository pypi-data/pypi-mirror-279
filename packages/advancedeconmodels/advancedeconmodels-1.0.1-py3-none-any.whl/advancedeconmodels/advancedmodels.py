import clipboard

def prac(name, flag=0):
    # библиотеки 
    bibla = '''
import numpy as np
import pandas as pd

import scipy.stats as sp

import statsmodels.api as sm
from statsmodels.tools.tools import add_constant

import matplotlib.pyplot as plt
    '''

    
    # Метод Ирвина - тест на выявление аномалий
    IRV_CODE = '''result = pd.DataFrame() #создали датасет, чтобы было удобно посмотреть на результат

y = data['wage']
n = len(y)
result['y'] = y
#вычисляем среднеквадратическое отклонение
S_y = np.sqrt(sum([(y[i] - y.mean())**2 for i in range(n)])/(n-1))

# вычисляем величину l_t для наблюдений
l_t = [0]+[abs(y[i]-y[i-1])/S_y for i in range(1, n)]
result['lambda'] = l_t
#если величина l_t превышает табличный уровень, то значение y_t считается аномальным

l_crit = 1 #из таблицы

result_normal = result[result['lambda']<=l_crit] #убираем аномалии из таблицы
result_normal'''

    # Метод Стьюдента - тест на выявление аномалий
    ANSTD_CODE = '''yy_ = np.mean(y) # среднее
Sy = np.std(y) # среднеквадратическое отклонение
n = len(y)
yy = np.argmax(y-y_) # наблюдение, предположительно являющееся аномальным

t_ = (yy - y_) / Sy # статистика

t_crit = t.ppf(1 - (0.05 / 2), n-2) # критическое значение распределения Стьюдента

t_005 = (t_crit * np.sqrt(n-1))/(np.sqrt(n - 2 + t_crit**2))

# Если расчетное значение меньше критического значения , аномалии отсутствуют:
#t_ <= t_005'''
    
    # Метод Зарембки - тест на выбор функциональной формы
    ZAR_CODE = '''y_geom = gmean(y)
y_new = y/y_geom

X_const = sm.add_constant(X)
linear_model = sm.OLS(y_new, X_const)
result_linear = linear_model.fit()
result_linear.summary()

logarithmic_model = sm.OLS(np.log(y_new), X_const)
result_logarithmic = logarithmic_model.fit()
result_logarithmic.summary()

ESS1 = sum(result_linear.resid**2)
ESS2 = sum(result_logarithmic.resid**2)

Z = np.abs(len(X)/2*np.log(ESS1/ESS2))
print('Хи2кр=',chi2(1).isf(0.05), ' Z= ', Z)

# H0: модели не имеют статически значимых различий,
# H1: модели имеют статически значимые различия.
# Если Z < Хи2кр ->H0 принимается
    '''

    # Метод Бокса-Кокса - тест на выбор функциональной формы
    BC_CODE = '''ssr_lambda = {}
for lamb in range(1, 1001):
    lambd = lamb/1000

    y_ = y/gmean(y)
    y_b_c = y_**lambd/lambd
    x_b_c = X**lambd/lambd


    X_n_const = sm.add_constant(x_b_c)
    model = sm.OLS(y_b_c, X_n_const)

    result = model.fit()
    ssr_lambda[result.ssr] = lambd
    '''

    # Метод Фостера-Стюарта - выявление наличия тренда
    FS_CODE = '''def foster_stuart(y):
    n = len(y)

    k = [1] + [0]*(n - 1)
    l = [1] + [0]*(n - 1)
    for t in range(1, n):
        if y[t] > max(y[:t]): k[t] = 1 # 1, если y_t больше всех предидущих уровней, иначе 0
        if y[t] < min(y[:t]): l[t] = 1 # 1, если y_t меньше всех предидущих уровней, иначе 0
    k = np.array(k)
    l = np.array(l)

    s = sum(k[1:]+l[1:])
    d = sum(k[1:]-l[1:])

    mu_s = (1.693872*np.log(n) - 0.299015)/(1 - 0.035092*np.log(n) + 0.002705*np.log(n)**2)
    mu_d = 0
    sigma_s = np.sqrt(2*np.log(n)-3.4253)
    sigma_d = np.sqrt(2*np.log(n)-0.8456)

    t_s = np.abs(s - mu_s)/sigma_s
    t_d = np.abs(d - mu_d)/sigma_d

    return t_s, t_d

alpha = 0.05
t_kr = t.ppf(1 - alpha/2, df = len(y) - 1) # from scipy.stats import *
    '''

    # Медианный критеий серий - выявление наличия тренда
    SERTR_CODE = '''y_ranzh = sorted(y)
Me = np.median(y)
def delta_i(y):
    delta = []
    for i in y:
        if i > Me:
            delta.append(1)
        elif i < Me:
            delta.append(0)
    return delta

plus_minus_list = delta_i(y)
def series(lst):
    max_length = 1
    current_length = 1
    counter = 1
    for i in range(1, len(lst)):
        if lst[i] != lst[i-1]:
            counter += 1
            max_length = max(max_length, current_length)
            current_length = 1
        else:
            current_length += 1
    max_length = max(max_length, current_length)
    return counter, max_length

num_of_series, lenght = series(plus_minus_list)
# num_of_series, lenght

# Если оба уравнения:
lenght < round(3.3*(np.log10(n) + 1))
num_of_series > round(0.5*(n + 1 - 1.96 * np.sqrt(n-1)))
# True H0 принимается

# Н0: тренда нет
# Н1: тренд есть
'''

    # Метод проверки разностей средних - выявление наличия тренда 
    MDIFF_CODE = '''def diff_avg_lvls(y, x): #середина ряда - x
    y1 = y[:x]
    y2 = y[x:]

    n1 = len(y1)
    n2 = len(y2)

    mean_1 = np.mean(y1)
    mean_2 = np.mean(y2)

    sigma_1 = np.std(y1)
    sigma_2 = np.std(y2)

    if sigma_1 > sigma_2:
        F = sigma_1/sigma_2

    else:
        F = sigma_2/sigma_1
    if F >= f.isf(q = 0.05, dfn=len(y1) - 1, dfd=len(y2) -1):
        print('Гипотеза о равенстве дисперсий отклоняется! Метод не дает ответа!')
    else:
        sigma = np.sqrt(((n1 - 1)*sigma_1 + (n2 - 1)*sigma_2)/(n1 + n2 - 2))

        t1 = abs(mean_1 - mean_2)/(sigma * np.sqrt(1/n1 + 1/n2))
        print(sigma, t1)
        if t1  < t.isf(q = 0.05, df = n1 + n2 - 1):
            print('Гипотеза принимается! Тренда нет!')
        else:
            print('Тренд есть!')'''

    # взвешенное среднее скользящая 
    WMA_CODE ='''def WMA(data, weights=(1, 4, 6, 4, 1)):
    weights= np.array(weights)

    k = len(weights)
    step = int(k / 2)
    w_sum = sum(weights)

    result = []

    for ind in range(step, len(data) - step):
        result.append((data[ind - step:ind + step + 1] * weights).sum() / w_sum)

    return np.array(result)'''

    
    graphTrDiff='''
    # график сглаженного ряда и нет
plt.plot(data1['T'], data1['Y'])
plt.plot(data1['T'][2:-2], smoothed)
plt.grid(alpha=0.25)

# Теперь вычислим средние приросты первого и второго порядков.
def MeanDiff(data):
    result = []

    for ind in range(1, len(data) - 1):
        result.append((data[ind + 1] - data[ind - 1]) / 2)

    return np.array(result)

dy = MeanDiff(smoothed)
d2y = MeanDiff(dy)
plt.plot(dy)
plt.plot(d2y)
plt.grid(alpha=0.25)

plt.plot(dy, label='dy')
plt.plot(d2y, label='d2y')
plt.plot(dy/data1['Y'][3:-3], label='dy/y')
plt.plot(np.log(abs(dy)), label='ln dy')
plt.legend()
plt.grid(alpha=0.25)
    '''

    Brown_CODE = '''
# Оцениваем линейную модель регрессии по МНК, для получения начальных оценко A0 и A1
model = sm.OLS(train['Y'], sm.add_constant(train['t'])).fit()  
A0 = model.params['const']
A1 = model.params['t']

def Brown(Y, x, beta, A0, A1):
    E = [] # ошибки
    for ind in range(x.shape[0]):
        pred = A0 + A1 * x.iloc[ind]
        e = Y.iloc[ind] - pred  # расчёт ошибки
        E.append(e)
        A0 = A0 + A1 + (1 - beta)**2 * e  # корректировка параметров модели
        A1 = A1 + (1 - beta)**2 * e
    return A0, A1, (np.array(E)**2).sum()

# оптимизация параметра beta (здесь обычный перебор)
betas = np.arange(0.5, 1, 0.01) # различные значения beta
errors = []  # ошибки
for beta in betas:
    A0 = model.params['const']
    A1 = model.params['t']
    errors.append(Brown(test['Y'], test['t'], beta, A0, A1)[2]) # для каждого beta сохраняем сумму квадратов ошибок
opt_beta = betas[np.argmin(errors)]
# оптимальные параметры
A0 = model.params['const']
A1 = model.params['t']
A0_B, A1_B, RSS_B= Brown(test['Y'], test['t'], opt_beta, A0, A1)
Brown_preds = A0_B + A1_B * (test['t'])
plt.plot(test['Y'])
plt.plot(Brown_preds)
    '''

    chitv_CODE = '''
def WMA(data, weights=(1, 4, 6, 4, 1)):
    # скользящее среднее
    weights= np.array(weights) # веса

    k = len(weights)
    step = int(k / 2)
    w_sum = sum(weights)

    result = []

    for ind in range(step, len(data) - step):
        result.append((data[ind - step:ind + step + 1] * weights).sum() / w_sum)

    return np.array(result)

w = [0.5] + [1 for _ in range(11)] + [0.5] # определяем веса для среднехронологической с T=12 (граничные веса половинные)
f0 = WMA(train['Y'], w) # начальная оценка тренда, сглаживание по среднехронологической

chetv_df = pd.DataFrame({'Year': train['Year'][6:-6], 'Month': train['Month'][6:-6],
                         'Y': train['Y'][6:-6], 'f0': f0})

chetv_df['l1'] = chetv_df['Y'] - chetv_df['f0']

# ----- РАСЧЁТ СЕЗОННОСТИ 1 -----

std1 = chetv_df[['Year', 'l1']].groupby('Year').std().rename(columns={'l1': 'std1'}) # расчёт СКО по каждому году
chetv_df = pd.merge(left=chetv_df, right=std1, on='Year')

chetv_df['l1_'] = chetv_df['l1'] / chetv_df['std1'] # нормируем остатки на СКО по годам

S1 = chetv_df[['Month', 'l1_']].groupby('Month').mean().rename(columns={'l1_': 'S1'}) # первая оценка сезонной волны
chetv_df = pd.merge(left=chetv_df, right=S1, on='Month').sort_values(by=['Year', 'Month'], axis=0)

# ----- РАСЧЁТ СЕЗОННОСТИ 1 -----

chetv_df['f1'] = chetv_df['Y'] - chetv_df['S1'] * chetv_df['std1'] # первая оценка тренда


f2_1 = np.average(np.array(chetv_df['f1'][:3]), weights=[5, 2, -1])  # специальные формулы для крайних элементов
f2_n = np.average(np.array(chetv_df['f1'][-3:]), weights=[-1, 2, 5])

f2_2 = chetv_df['f1'][:3].mean()  # сглаживание по 3 точкам для оставшихся элементов
f2_n1 = chetv_df['f1'][-3:].mean()

f2 = WMA(chetv_df['f1'], (1, 4, 6, 4, 1)) # сглаживание по 5 точкам для всех остальных элеметов (взяты рекомендуемые веса)
f2 = [f2_1, f2_2] + list(f2) + [f2_n1, f2_n] # вторая оценка тренда

chetv_df['f2'] = f2

chetv_df['l2'] = chetv_df['Y'] - chetv_df['f2']


# ----- РАСЧЁТ СЕЗОННОСТИ 2 -----



std2 = chetv_df[['Year', 'l2']].groupby('Year').std().rename(columns={'l2': 'std2'}) # расчёт СКО по каждому году
chetv_df = pd.merge(left=chetv_df, right=std2, on='Year')

chetv_df['l2_'] = chetv_df['l2'] / chetv_df['std2'] # нормируем остатки на СКО по годам

S2 = chetv_df[['Month', 'l2_']].groupby('Month').mean().rename(columns={'l2_': 'S2'}) # вторая оценка сезонной волны
chetv_df = pd.merge(left=chetv_df, right=S2, on='Month').sort_values(by=['Year', 'Month'], axis=0)
chetv_df['S2_'] = chetv_df['S2'] * chetv_df['std2'] # так получаются нормальные значения, но можно так делать или нет одному богу известно
# про коэффициент напряжённости сезонной волны мы умалчиваем, потому что он вроде делал только хуже...


S2 = chetv_df[['Month', 'S2_']].groupby('Month').mean().rename(columns={'S2_': 'S2final'}) # итоговая вторая оценка сезонной волны
chetv_df = pd.merge(left=chetv_df, right=S2, on='Month').sort_values(by=['Year', 'Month'], axis=0)


# ----- РАСЧЁТ СЕЗОННОСТИ 2 -----




final_df = chetv_df[['Year', 'Month', 'Y', 'f2', 'S2_']]
final_df['t'] = np.arange(7, final_df.shape[0] + 7)
final_df

    '''


    logit_CODE = '''
import statsmodels.formula.api as smf.logit # логит
from sklearn.metrics import confusion_matrix,  f1_score

# на примере датасета diabetes
data = pd.read_csv('diabetes.csv')

mod = smf.logit('Outcome ~ Pregnancies + Glucose +	BloodPressure +	SkinThickness +	Insulin+ BMI + DiabetesPedigreeFunction	+ Age', data=data)
res = mod.fit()

# Выводим описание
res.summary()

# По одному убираем незначимые признаки
# (имеющие наибольшее значение P среди других признаков)

# в итоге остаются значимые признаки (их P >= 0.001)
mod = smf.logit('Outcome ~ Pregnancies + Glucose  + BMI	', data=data)
res = mod.fit()

# можем проверить точность предсказаний
pred_y = [0 if elem <0.5 else 1 for elem in res.predict(data[['Pregnancies','Glucose' ,'BMI', 'BloodPressure']])]

#вклад признаков в модель-нужно рассчитывать для каждого
S_y2 = y.std()**2
S_factor2 = x['factor'].std()**2
beta_factor = coef * (S_factor2/S_y2)
#Показывает, на какую часть величины среднего квадратического отклонения изменяется среднее значение y  с 
#изменением соответствующего x на одно среднее квадратическое отклонение при фиксированном на постоянном 
#уровне значении остальных x
'''



    probit_CODE = '''
# на примере датасета diabetes.
data = pd.read_csv('diabetes.csv') #пробит

mod = smf.probit('Outcome ~ Pregnancies + Glucose +	BloodPressure +	SkinThickness +	Insulin+ BMI + DiabetesPedigreeFunction	+ Age', data=data)
res = mod.fit() # проводим такой же анализ, как и в logit модели, и оставляем только значимые признаки
res.summary()

# убрали незначимые признаки
mod = smf.probit('Outcome ~ Pregnancies + Glucose +	BloodPressure + BMI', data=data)
res = mod.fit()
res.summary()

pred_y = [0 if elem <0.5 else 1 for elem in res.predict(data[['Pregnancies','Glucose' ,'BMI', 'BloodPressure']])]
confusion_matrix(data['Outcome'], pred_y)

# проверяем точность предсказания
f1_score(data['Outcome'], pred_y)
'''

    panel_CODE = '''
from linearmodels import PooledOLS, PanelOLS, RandomEffects
from scipy.stats import f, chi2

#лучше с самого начала делить выборку на тестовую и тренировочную
pooled_model = PooledOLS(df['Валовой региональный продукт на душу населения (рубль, значение показателя за год)'], df[df.columns[1:]]).fit()
pooled_model.summary
fixed_effects_model = PanelOLS(df['Валовой региональный продукт на душу населения (рубль, значение показателя за год)'], df[df.columns[1:]], entity_effects=True).fit()
fixed_effects_model.summary
random_effects_model = RandomEffects(df['Валовой региональный продукт на душу населения (рубль, значение показателя за год)'], df[df.columns[1:]]).fit()
random_effects_model.summary

#Pooled модель VS FE модель (Тест Лагранжа)
N = len(df)
T = len(set(df['t']))
K = df.shape[1]-1
F_test = (pooled_model.resid_ss - fixed_effects_model.resid_ss) / ((N - 1)) / (fixed_effects_model.resid_ss / (N* T - N - K))

F_krit = f.ppf(0.05, N*T - N - K, N-1)
if F_test > F_krit:
    print('Fixed Effects Model')
else: print('Pooled Model')
    
#RE vs FE (Тест Хаусмана)
b_diff = fixed_effects_model.params - random_effects_model.params # разницы оценок коэффициентов
cov_mat = fixed_effects_model.cov - random_effects_model.cov  # ковариационной матрицы разности оценок коэффициентов
H = b_diff.dot(np.linalg.inv(cov_mat)).dot(b_diff)  # тестовой статистики хаусмана
chi_krit = chi2.ppf(0.95, len(b_diff))
if H > chi_krit:
    print('Модель с фиксированными эффектами')
else: print('Модель со случайными эффектами')
    
#Pooled vs RE(тест Бреуша-Пагана)
from statsmodels.compat import lzip
import statsmodels.stats.api as sms

names = ['Lagrange multiplier statistic', 'p-value', 'f-value', 'f p-value']
test = sms.het_breuschpagan(pooled_model.resids,df[df.columns[1:]])
res = lzip(names, test)
if  res[2][1]>chi2.ppf(0.95, 1):
      print('Random Effects')
else:
      print('Pooled model')
        
#предсказания
random_effects_model.predict(test[test.columns[1:]])
'''
    arma_CODE = '''
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import statsmodels.api as sm

#считаем доходность
df['dohod'] = [0]+ [(df['Close'].iloc[i]-df['Close'].iloc[i-1])/df['Close'].iloc[i-1] for i in range(1, len(df))]

#проверка на стационарность
res = adfuller(df['Close'])
res[1]>0.05 #p-value => ряд нестационарный

res = adfuller(df['dohod'])
res[1]<0.05 #p-value => ряд стационарный

#построение автокорреляционных функицй
plot_acf(df['dohod'], lags=10)
plot_pacf(df['dohod'], lags=10)

# AR(p) - ARIMA(p,0,0)
# MA(p) - ARIMA(0,0,q)
# ARMA(q) - ARIMA(p,0,q)

model = sm.tsa.ARIMA(df['dohod'], order=(1, 0, 0)).fit() #AR(1)
model.summary()
'''
    t_inv_pred_CODE = '''
# строим выбранную модель тренда (здесь линейная, может быть другая)
model = sm.OLS(data['Y'], add_constant(data['t'])).fit()
# точечный прогноз
pred = model.predict([1, data['t'].shape[0] + 4])[0]

# интервальный прогноз
n = data.shape[0]
S = np.sqrt((model.resid ** 2).sum() / (n - 2))
U = S * t.isf(0.05, df=n-2) * np.sqrt(1 + (1 / n) + (n + 1 + data['t'].mean())**2 / ((data['t'] - data['t'].mean())**2).sum())
print(f'[{round(pred - U, 4)}; {round(pred + U, 4)}]')
'''

    kmnk_CODE = '''
#A - расширенная матрица для изначальной системы
#оцениваем приведенные уравнения по мнк и записываем в матрицу MI
MI =  sp.Matrix([[0.2031, -0.0062, 0.0431, 0.0425], 
                 [23.9785, -0.2454, 3.5736, 1.5854],
                 [1, 0, 0, 0], [0, 1, 0, 0], 
                 [0, 0, 1, 0],[0, 0, 0, 1]])
A1 = A[0,:]
sol1 = sp.solve([(A1 * MI)[0], (A1 * MI)[1], (A1 * MI)[2], (A1 * MI)[3]], [a0, a1, a2,a3])
A2 = A[1,:]
sol2 = sp.solve([(A2 * MI)[0], (A2 * MI)[1], (A2 * MI)[2], (A2 * MI)[3]], [b0, b1, b2,b3])
'''

    HoltWinters_CODE = '''
def HoltWinters(Y, t, T, alpha, beta, gamma):
    model = sm.OLS(Y, sm.add_constant(t)).fit()
    a_old = model.params[0] # оценка параметров тренда
    b_old = model.params[1]

    S = np.array(Y[:2*T] / (a_old + b_old * t[:2*T]))
    F = [S[ind::T].mean() for ind in range(T)] # сезонность

    resid = []

    for ind in range(len(Y)):
        a_new = alpha * (Y[ind] / F[ind]) + (1 - alpha) * (a_old + b_old)
        b_new = beta * (a_new - a_old) + (1 - beta) * b_old
        F_new = gamma * (Y[ind]/a_new) + (1 - gamma) * F[ind]

        F.append(F_new)
        
        a_old = a_new
        b_old = b_new

    resid = Y - (a_new + b_new * t) * np.tile(F[-4:], len(Y)//4)

    return a_new, b_new, F[-4:], np.array(resid)
alpha = np.arange(0.1, 1, 0.05)
beta = np.arange(0.1, 1, 0.05)
gamma = np.arange(0.1, 1, 0.05)

RSS = []
params = []

for a in alpha:
    for b in beta:
        for y in gamma:
            a_p, b_p, f, e = HoltWinters(train['Y'], train['t'], 4, a, b, y)
            
            params.append([a, b, y])
            RSS.append((e**2).sum())

alpha_opt, beta_opt, gamma_opt = params[np.argmin(RSS)]
alpha_opt, beta_opt, gamma_opt

a, b, f, e = HoltWinters(train['Y'], train['t'], 4, alpha_opt, beta_opt, gamma_opt)
a, b, f

plt.plot(test['t'], test['Y'])

plt.plot(test['t'], (a + b * test['t']) * np.tile(f, test['t'].shape[0]//4))

plt.grid(alpha=0.25)


'''

    chetv1_CODE = '''
y = df['INVFC_Q_DIRI']
L = 4
y_reshaped = np.array(y).reshape(-1, L)
chrono_mean = (0.5 * y_reshaped[:, 0]+ np.sum(y_reshaped[:, 1:-1], axis=1)+ 0.5 * y_reshaped[:, -1]) / L #предварительная оценка тренда

l1 = y_reshaped - [[elem,elem,elem,elem] for elem in chrono_mean]

sigma1 = np.sqrt((np.sum(l12, axis=1) - np.sum(l1, axis=1)  2 / L) / (L - 1))
l1_normilized = l1/[[elem,elem,elem,elem] for elem in sigma1]

#первая оценка сезонности
seasonal1 = np.mean(l1_normilized, axis=0)

#первая оценка тренда
f1 = y- [elem* element for elem in sigma1 for element in seasonal1]

#вторая оценка тренда
f2 = [np.average(np.array(f1[:3]), weights=[5, 2, -1])] + [np.array(f1[:3]).mean()]+list(WMA(f1, weights=(1, 4, 6, 4, 1))) + [np.array(f1[-3:]).mean()] +[np.average(np.array(f1[-3:]), weights=[-1, 2, 5])] # вторая оценка тренда

l2 = y_reshaped - np.array(f2).reshape(-1,4)
sigma2 = np.sqrt((np.sum(np.array(l2)2, axis=1) - np.sum(np.array(l2), axis=1)  2 / L) / (L - 1))

l2_normilized = l2/[[elem,elem,elem,elem] for elem in sigma2]
#вторая оценка сезонности
seasonal2 = np.mean(l2_normilized, axis=0)

# остаточная компонента
eps = [elem - seasonal2 for elem in l2]
eps

'''
    

    names = {
        
        'b' : [bibla, 'библиотеки'], 
        
        'irvin': [IRV_CODE, 'Метод Ирвина - тест на выявление аномалий'] ,
             'student': [ANSTD_CODE, ''],
             
             'spec_zar': [ZAR_CODE, ''],
             'spec_boxcox': [BC_CODE, ''], 
             
             'foster': [FS_CODE, ''],
             'cr_ser': [SERTR_CODE, ''], 
             'cr_razn_sred': [MDIFF_CODE, ''],
             
             'wma': [WMA_CODE, ''], 
             'gtd' : [graphTrDiff, 'построение графиков с трендами и разности'],
    
             'brown': [Brown_CODE, 'модель Брауна отображает развитие линейной или параболической тенденции, а также рядов без тенденции.'], 
    
             'chetv2': [chitv_CODE, 'Метод Четверикова 2'], 
            'logit': [logit_CODE, ''],
            'panel':[panel_CODE, ''],
            'arma':[arma_CODE, ''],
            't_inv_pred':[t_inv_pred_CODE, ''],
            'kmnk':[kmnk_CODE, ''], 
    
            'hw':[HoltWinters_CODE,'Хольт-Винтерс'], 
    
            'chetv':[chetv1_CODE,'Метод Четверикова'], 
            
             
             
            }

    
    
    if name == 'h':
        for key in names:
            print(f'{key} - {names[key][1]}')
            print()
    elif name!= 'h' and flag!=1:
        clipboard.copy(names[name][0])
    else:
        print(names[name][0])
