import clipboard

def prac(name):
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
            print('Тренд есть!')
'''

    names = {'an_irv': IRV_CODE, 'an_stud': ANSTD_CODE, 'spec_zar': ZAR_CODE, 
             'spec_boxcox': BC_CODE, 'trend_fs': FS_CODE, 'trend_ser': SERTR_CODE, 
             'trend_diff': MDIFF_CODE}

    clipboard.copy(names[name])

