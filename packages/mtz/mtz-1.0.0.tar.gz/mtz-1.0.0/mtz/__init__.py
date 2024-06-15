anomalies = {
    "распределение Стьюдента": """
# распределение Стьюдента

data = pd.read_excel('df_example (1).xlsx')

# визуальная оценка
plt.plot(data.Close);
sns.boxplot(data.Close);

data['tau'] = abs(data.Close - data.Close.mean()) / data.Close.std()

n = len(data)

# критические значения
tau_cr_005 = (st.t(n - 2).ppf(1 - 0.05 / 2) * np.sqrt(n - 1)) / (np.sqrt(n - 2 + st.t(n - 2).ppf(1 - 0.05 / 2) ** 2))

tau_cr_0001 = (st.t(n - 2).ppf(1 - 0.001 / 2) * np.sqrt(n - 1)) / (np.sqrt(n - 2 + st.t(n - 2).ppf(1 - 0.001 / 2) ** 2))

# t < tau_cr_005 не аномалия
# tau_cr_005 < t < tau_cr_0001 может быть аномалией
# tau_cr_0001 < t аномалия""",
    "метод Ирвина": """# пример для колонки clode
data['lambd'] = abs(data.Close - data.Close.shift(1)) / data.Close.std()

# n   | P=0.95 | P=0.99
# 2   |    2.8 |    3.7 
# 3   |    2.2 |    2.9 
# 10  |    1.5 |    2.0 
# 20  |    1.3 |    1.8 
# 30  |    1.2 |    1.7 
# 50  |    1.1 |    1.6 
# 100 |    1.0 |    1.5

# исходя из n и alpha выбираем подходящее критическое значение
n = 49
alpha = 0.05
# =>
cr = 1.1

data[data['lambd'] >= 1.1]""",
    "метод Ирвина": """# метод Ирвина

# пример для колонки clode
data['lambd'] = abs(data.Close - data.Close.shift(1)) / data.Close.std()

# n   | P=0.95 | P=0.99
# 2   |    2.8 |    3.7 
# 3   |    2.2 |    2.9 
# 10  |    1.5 |    2.0 
# 20  |    1.3 |    1.8 
# 30  |    1.2 |    1.7 
# 50  |    1.1 |    1.6 
# 100 |    1.0 |    1.5

# исходя из n и alpha выбираем подходящее критическое значение
n = 49
alpha = 0.05
# =>
cr = 1.1

data[data['lambd'] >= 1.1]""",
}

trend = {
    "разность средних уровней": """
# разность средних уровней

import pandas as pd
import numpy as np
import scipy.stats as scs

data = pd.read_excel('your_path.xlsx')

def diff_average_levels(data, alpha=0.05):
    delim = len(data)//2
    first = data.iloc[:delim]
    second = data.iloc[delim:]

    n1 = len(first)
    n2 = len(second)

    f_mean = sum(first)/n1
    s_mean = sum(second)/n2

    f_var = sum((first - f_mean)**2) / (n1 - 1)
    s_var = sum((second - s_mean)**2) / (n2 - 1)

    F = max(f_var, s_var) / min(f_var, s_var)
    f_stat = scs.f(n1 - 1, n2 - 1).isf(alpha)
    assert F < f_stat, 'дисперсии не равны, метод не сможет дать ответ'

    sigma = np.sqrt(((n1 - 1) * f_var + (n2 - 1) * s_var)/(n1 + n2 - 2))
    t_stat = abs(f_mean - s_mean)/(sigma * np.sqrt(1/n1 + 1/n2))
    t_table = scs.t(n1 + n2 -2).isf(alpha)

    if t_stat < t_table:
        print('Тренда нет')
    else:
        print('Тренд есть')

diff_average_levels(data['Close'])""",
    "критерий серий": """
# критерий серий

temp = data.copy()

temp['delta'] = np.where(temp.y > temp.y.median(), 1, 0)

mx_len = 1
current = temp.delta[0]
current_len = 1
seria_count = 1

for d in temp.delta.iloc[1:]:
    if d == current:
        current_len += 1
    else:
        current_len = 1
        current = d
        seria_count += 1
    if current_len > mx_len:
        mx_len = current_len

print(mx_len, seria_count) #108, 62

# Если хотя бы одно из неравенств нарушается, то гипотеза об отсутствии тренда отвергается.

# $
# \begin{cases}
# \tau_{max}(n) < [3,3(ln(n)+1)]> \\
# \nu > [\frac1 2 (n+1-1,96\sqrt{n-1})]
# \end{cases}
# $

108 < round(3.3 * (np.log(397) + 1)), 62 > round(0.5 * (397 + 1 - 1.96 * np.sqrt(397 - 1)))
""",
    "критерий Фостера-Стьюрта": """
def Foster(y, x):
    n = len(y)

    k = []
    l = []
    for i in range(len(y)):
        if max(y[:(i + 1)]) == y[i]:
            k.append(1)
        else:
            k.append(0)

        if min(y[:(i + 1)]) == y[i]:
            l.append(1)
        else:
            l.append(0)

    s = sum(k) + sum(l)
    d = sum(k) - sum(l)

    mu = (1.693872 * np.log(n) - 0.299015) / (1 - 0.035092 * np.log(n) + 0.002705 * np.log(n) ** 2)
    sigma1 = np.sqrt(2 * np.log(n) - 3.4253)
    sigma2 = np.sqrt(2 * np.log(n) - 0.8456)

    ts = abs(s - mu) / sigma1
    td = abs(d - 0) / sigma2

    t_crit = scs.t(n).isf(0.05)
    
    is_trend = td < t_crit

    is_var = ts < t_crit

    return f"{ts=}\n{td=}\n{t_crit=}\n{is_trend=}\n{is_var=}\n"

print(Foster(data.iloc[:, 1], data.index))

# ts=4.526167684396396
# td=4.974669057169713
# t_crit=1.7011309342659315
# is_trend=False
# is_var=False
""",
}

growth_curve = """
# кривая роста

df_curve1 = #read data

# сглаживание ряда скользящей средней

# корреляция до
plt.figure(figsize=(10, 8))
plt.title('Корреляционная матрица')
sns.heatmap(df_curve1[['t', 'rolling_mean']].corr(), annot=True, vmax=1, vmin=-1);

df_curve1['rolling_mean'] = df_curve1['y'].rolling(window=4).mean()

df_curve1.dropna(inplace=True)

# корреляция после, должна стать выше
plt.figure(figsize=(10, 8))
plt.title('Корреляционная матрица')
sns.heatmap(df_curve1[['t', 'rolling_mean']].corr(), annot=True, vmax=1, vmin=-1);

plt.plot(df_curve1.y, c='blue', label='Исходный ряд', alpha=0.5, linestyle=':')
plt.plot(df_curve1.rolling_mean, c='orange', label='Скользящее среднее', linewidth=3)


# графики приростов для выбора наилучшей кривой
df_curve1['delta1'] = (df_curve1.rolling_mean.shift(-1) - df_curve1.rolling_mean.shift(1)) / 2

df_curve1['delta2'] = (df_curve1.delta1.shift(-1) - df_curve1.delta1.shift(1)) / 2

df_curve1['delta1_div_y'] = df_curve1.delta1 / df_curve1.y

df_curve1['ln_delta1'] = np.log(df_curve1.delta1)

df_curve1['ln_delta1_div_y'] = np.log(df_curve1.delta1_div_y)

df_curve1['ln_delta1_div_y2'] = np.log(df_curve1.delta1_div_y / df_curve1.y)

df_curve1.head(10)

plt.figure(figsize=(14, 7))
plt.suptitle('Графики средних приростов')

for i, col in enumerate(df_curve1.columns[3:]):
    plt.subplot(2, 3, i + 1)
    plt.title(col)
    plt.ylim(-15, 15)
    plt.grid(alpha=0.5, linestyle='--')
    plt.plot(df_curve1.t, df_curve1[col], c='red')

# выбор кривой роста

# | Показатель | Характер изменений | Кривая роста |
# | --- | --- | --- |
# | $\Delta y_t$ | Примерно постоянный | Полином первого порядка |
# | $\Delta y_t$ | Примерно линейный | Полином второго порядка |
# | $\Delta^2 y_t$ | Примерно линейный | Полином третьего порядка |
# | $\frac{\Delta y_t}{y_t}$ | Примерно постоянный | Экспонента |
# | $\ln \Delta y_t$ | Примерно линейный | Модифицированная экспонента |
# | $\ln \frac{\Delta y_t}{y_t}$ | Примерно линейный | Кривая Гомперца |
# | $\ln \frac{\Delta y_t}{y^2_t}$ | Примерно линейный | Логистическая кривая |

# если требуется, линеаризуем модель, строим её и возвращаемся к исходному виду

curve = sm.OLS(np.log(df_curve1.rolling_mean), sm.add_constant(df_curve1.t)).fit()

curve.summary()

# визуализация
plt.plot(df_curve1.t, np.exp(curve.predict(sm.add_constant(df_curve1.t))), c='green', label='Кривая роста', linewidth=3)

# точечный прогноз

t_predict = [56, 57, 58, 59]

y_pred = np.exp(curve2.predict(sm.add_constant(t_predict)))

# интервальный прогноз. Для этого посчитаем отклонение от точечного:

# $U(k) = S_{\hat y} t_\alpha \sqrt{1 + \vec{x}_0^T (X^T X)^{-1} \vec{x}_0}$,

# где $S_{\hat y} = \sqrt{\frac{\sum_{t=1}^{n} \varepsilon_t^2}{n-m-1}}$ и $\vec{x}_0$ - вектор прогнозных оценок регрессоров

Sy = np.sqrt(sum(curve2.resid ** 2) / (len(df[:-4]) - 1 - 1))

from scipy.stats import t
ta = t(len(df[:-4] - 2)).isf(0.05)

x0 = sm.add_constant(t_predict)

X = np.array(sm.add_constant(df_curve2.t))
XT_X = np.linalg.inv(X.T @ X)

Uks = []
for t_pred in x0:
    Uks.append(Sy * ta * np.sqrt(1 + t_pred.T @ XT_X @ t_pred))
Uks = np.array(Uks)

# интервалы
down = np.exp(curve2.predict(sm.add_constant(t_predict)) - Uks)
up = np.exp(curve2.predict(sm.add_constant(t_predict)) + Uks)"""

browns_model = """
# Модель Брауна

# поиск начальных параметров A0, A1
first24 = sm.OLS(df[:24].y, sm.add_constant(df[:24].t)).fit()
first24.summary()

# оптимальное beta подбором
model_params = [[131.7152, 2.0508]] * 24
beta = 0.85

for i in range(24, len(df)):
    y_pred = model_params[-1][0] + model_params[-1][1] * df.iloc[i].t

    error = df.iloc[i].y - y_pred
    
    temp = [0, 0]
    temp[0] = model_params[-1][0] + model_params[-1][1] + (1 - beta) ** 2 * error
    temp[1] = model_params[-1][1] + (1 - beta) ** 2 * error

    model_params.append(temp)

model_params = np.array(model_params)
y_pred = model_params[:, 0] + model_params[:, 1] * df.t

def find_best_beta(data_offset=None):
    res = []
    
    for beta in np.linspace(0, 1, 10000):
        first24 = sm.OLS(df[:24].y, sm.add_constant(df[:24].t)).fit()

        model_params = [list(first24.params.values)] * 24

        for i in range(24, len(df[:data_offset])):
            y_pred = model_params[-1][0] + model_params[-1][1] * df.iloc[i].t

            error = df.iloc[i].y - y_pred
            
            temp = [0, 0]
            temp[0] = model_params[-1][0] + model_params[-1][1] + (1 - beta) ** 2 * error
            temp[1] = model_params[-1][1] + (1 - beta) ** 2 * error

            model_params.append(temp)

        model_params = np.array(model_params)

        y_pred = model_params[:, 0] + model_params[:, 1] * df.t[:data_offset]

        res.append(np.sum((df.y[:data_offset] - y_pred) ** 2))

    return res
    
results = find_best_beta()
np.argmin(results) / 10000, min(results)

# прогнозные значения и их интервалы
Sy = y_pred.std()
n = len(df)
ta = t(n - 2).isf(0.05)
Uk = lambda k: Sy * ta * np.sqrt(1 + 1 / n + 3 * (n + 2 * k - 1) ** 2 / n / (n ** 2 - 1))
Uks = Uk(np.arange(60, 64))
y_pred_new = model_params[-1, 0] + model_params[-1, 1] * np.arange(60, 64)
down = y_pred_new - Uks
up = y_pred_new + Uks

down, y_pred_new, up

# c использование 4 последних точек, как валидации

results = find_best_beta(data_offset=-4)

#rebuild model with offset

Sy = y_pred.std()
n = len(df) - 4
ta = t(n - 4 - 2).isf(0.05)
Uk = lambda k: Sy * ta * np.sqrt(1 + 1 / n + 3 * (n + 2 * k - 1) ** 2 / n / (n ** 2 - 1))
Uks = Uk(np.arange(56, 60))
y_pred_new = model_params[-1, 0] + model_params[-1, 1] * np.arange(56, 60)
down = y_pred_new - Uks
up = y_pred_new + Uks

down, y_pred_new, up
"""
holt_winters_model = """
# Модель Хольта-Уинтерса

def HolterWinter(t, y, alpha, beta, gamma, L, data_offset=None):
    a = [y[0]]
    b = [0]
    F = [1] * L

    for i in range(1, L):
        a_temp = alpha * (y[i] / 1) + (1 - alpha) * (a[i - 1] + b[i - 1])
        b_temp = beta * (a_temp - a[i - 1]) + (1 - beta) * b[i - 1]

        a.append(a_temp)
        b.append(b_temp)
    
    for i in range(L, len(y[:data_offset])):
        a_temp = alpha * (y[i] / F[i - L]) + (1 - alpha) * (a[i - 1] + b[i - 1])
        b_temp = beta * (a_temp - a[i - 1]) + (1 - beta) * b[i - 1]
        F_temp = gamma * (y[i] / a_temp) + (1 - gamma) * F[i - L]

        a.append(a_temp)
        b.append(b_temp)
        F.append(F_temp)

    return map(np.array, [a, b, F])

# с валидационной выборкой

alpha, beta, gamma = 0.1, 0.1, 0.9

a, b, F = HolterWinter(df.t, df.y, alpha, beta, gamma, 4, data_offset=-4)

y_pred = (a + b) * F

k = np.arange(1, 5)

y_pred_new = (a[-1] + b[-1] * k) * F[-5 + (k % 4)]

plt.figure(figsize=(10, 5))
plt.title(f'Модель Холтера-Уинторса ({alpha=}, {beta=}, {gamma=})')
plt.grid(alpha=0.5, linestyle='--')
plt.xlabel('t, период времени')
plt.ylabel('y')
plt.plot(df.t[-6:-4] + 1, [df.y.iloc[-5], y_pred_new[0]], c='lightgreen', linewidth=3)
plt.plot(df.t[:-4], y_pred, c='orange', label='Модель Холтера-Уинторса', linewidth=3)
plt.plot(df.t[-4:], y_pred_new, c='lightgreen', label='Прогноз', linewidth=3, marker='o', markerfacecolor='pink')
plt.plot(df.t, df.y, c='blue', label='Исходный ряд', alpha=0.5, linestyle=':')
plt.legend(loc='upper left');

# экстраполяция вперёд

alpha, beta, gamma = 0.179, 0.1, 0.762

a, b, F = HolterWinter(df.t, df.y, alpha, beta, gamma, 4)

y_pred = (a + b) * F

k = np.arange(1, 5)

y_pred_new = (a[-1] + b[-1] * k) * F[-5 + (k % 4)]

y_pred_new
"""
chetverikov_method = """
# метод Четверикова


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


res = Chetverikov(df.t[:-3], df.y[:-3], 4)

# диаграммы тренды

plt.figure(figsize=(8, 8))
plt.suptitle("Диаграммы тренда")
plt.subplots_adjust(hspace=0.5)

titles = [
    "Исходный ряд",
    "Предварительная оценка тренда",
    "Первая оценка тренда",
    "Вторая оценка тренда",
]

for i, col in enumerate([df.y[:-3], res["chrono_mean"], res["f1"], res["f2"]]):
    plt.subplot(4, 1, i + 1)
    plt.title(titles[i])
    if i == 3:
        plt.xlabel("t, период времени")
    if i:
        plt.ylim(90, 150)
    else:
        plt.ylim(50, 300)
    plt.grid(alpha=0.5, linestyle="--")
    plt.plot(df.t[:-3], col, c=("orange" if i else "blue"))

# данные о сезонности

plt.figure(figsize=(10, 7))
plt.suptitle("Диаграммы сезонной волны")
plt.subplots_adjust(hspace=0.5)


titles = ["Первая оценка сезонности", "Вторая оценка сезонности", "Сравнение"]

for i, col in enumerate([res["s1"], res["s2"], [res["s1"], res["s2"]]]):
    plt.subplot(3, 1, i + 1)
    plt.title(titles[i])
    if i == 2:
        plt.xlabel("L, квартал")
    plt.grid(alpha=0.5, linestyle="--")
    if i < 2:
        plt.plot(np.arange(1, 5), col, c=("red" if i else "lightgreen"), linewidth=1)
    else:
        plt.plot(np.arange(1, 5), col[0], c="red", linewidth=1)
        plt.plot(np.arange(1, 5), col[1], c="lightgreen", linewidth=1)

# диаграмма остаточной компоненты

plt.figure(figsize=(10, 5))
plt.title("Остаточная компонента")
plt.grid(alpha=0.5, linestyle="--")
plt.xlabel("t, период времени")
plt.ylabel("e")
plt.ylim(-20, 20)
plt.xlim(-1, 57)
plt.hlines(0, -5, 70, color="black", linewidth=0.4)
plt.plot(
    df.t[:-3], res["eps"], c="lightblue", label="Остаточная компонента", linewidth=3
)
plt.legend(loc="upper left");

"""
information_criteria = {
    "Критерий Акаике": """
def AIC_criterion(data):
    ess =sum(sm.OLS(data['Y'], data[['const', 'X']]).fit().resid**2)

    return np.log(ess/len(data))+2/len(data)+1+np.log(2*np.pi)""",
    "Критерий Шварца": """
def BIC_criterion(data):
    ess =sum(sm.OLS(data['Y'], data[['const', 'X']]).fit().resid**2)
    
    return np.log(ess/len(data))+np.log(len(data))/len(data)+1+np.log(2*np.pi)""",
}

semi_log_models_tests = {
    "Метод Зарембки": """
#метод Зарембки

data = sm.add_constant(data)
data1 = data.copy()
data1['y'] = np.log(data['y'])

def Zarembki(data, data1):
    y_geom = np.exp(1/len(data) * np.sum(data1['y']))
    
    data_norm = data.copy()
    data1_norm = data1.copy()
    
    data_norm['y'] = data_norm['y']/y_geom
    data1_norm['y'] = np.log(data_norm['y']/y_geom)
    
    result = sm.OLS(data_norm['y'], data_norm[['const', 'X']]).fit()
    result1 = sm.OLS(data1_norm['y'], data1_norm[['const', 'X']]).fit()
    
    ess1=sum(result.resid**2)
    ess2=sum(result1.resid**2)
    
    z=abs(len(data)/2*np.log(ess1/ess2))
    
    print(f'z: {z}, Хи^2 критическое: {scs.chi2.ppf(0.95,1)}')
    
    if z>scs.chi2.ppf(0.95,1):
        print('Модели имеют разницу, полулогарифмическая модель лучше, так как она лучше описывает зависимости между данными')
    else:
        print('Модели имеют разницу, линейная модель лучше, так как она легче')

Zarembki(data, data1)
""",
    "Тест Бокса-Кокса": """
# Тест Бокса-Кокса

def B_C_test(data, lamda):
    ess_list = []
    
    for i in lamda:
        data_help=data.copy()
        data_help['X']=data_help['X']**i/i
        ess_list.append(sum(sm.OLS(data['y']**i/i, data_help[['const', 'X']]).fit().resid**2))
        
    return ess_list

lamda = np.arange(0.001, 1, 0.01)
plt.plot(lamda, B_C_test(data, lamda))

print(f'Значение лямбда с наименьшим ESS: {lamda[err.index(min(err))]}')

если ESS меньше для $\lambda$ = 0, то сделаем выбор в пользу полулогарифмической модели, иначе в пользу линейной
""",
}

logit_model = """
# логит модель

logit_model = sm.Logit(y, X).fit()
logit_model.summary()

# спецификация
# $ \huge Y^* =  \frac{1}{1 + e^{-4.3377	(1.615) + 0.8840(0.401) \cdot x_0 -0.1353(0.455) \cdot x_1 + 0.3341(0.256) \cdot x_2}} $

# Расчет средних предельных эффектов (значимость факторов)
# Это изменение вероятности исхода при изменении предиктора на единицу, с учетом среднего значения всех других предикторов.
marginal_effects = logit_model.get_margeff(at='mean', method='dydx')
print(marginal_effects.summary())
"""

probit_model = """
# пробит модель

probit_model = sm.Probit(y, X).fit()
probit_model.summary()

# спецификация
# $ Y^* =  \Phi(- 2.5312(0.894) + 0.4945(0.215) \cdot x_0 - 0.0650(0.26) \cdot x_1 + 0.1952(0.154) \cdot x_2) $

# Расчет средних предельных эффектов (значимость факторов)
# Это изменение вероятности исхода при изменении предиктора на единицу, с учетом среднего значения всех других предикторов.
marginal_effects = probit_model.get_margeff(at='mean', method='dydx')
print(marginal_effects.summary())
"""

heckit_model = """
# хекит модель
https://github.com/statsmodels/statsmodels/blob/92ea62232fd63c7b60c60bee4517ab3711d906e3/statsmodels/regression/heckman.py

# NaN если цензурируется
Y_cens = Y.copy()
Y_cens[Y_cens == 800] = np.NaN
cens = pd.Series(np.ones((len(Y),))).astype(int)

#разделение экзогенных переменных на имеющие непрерывное (Xh) и дискретное распределение (Sh)

Sh = X.iloc[:, -2:]
Xh = X.iloc[:, :-2]

import heckman as heckman
heckman_model = heckman.Heckman(Y_cens_train, X_train, cens_train)
res_h = heckman_model.fit(method='twostep')
print(res_h.summary())

# первые коэффициенты - Response equation (Модель линейной регрессии)

# вторые коэффициенты - Selection equation (Модель выбора - пробита)
# спецификация записывается как Phi(a_0*Z_0 + a_1*Z_1 _ eps)
"""

tobit_model = """
# тобит модель
https://github.com/jamesdj/tobit

# Здесь, чтобы обозначить левостороннее цензурирование, передаем в вектор cens -1 (в нашем случае такого нет, т.к. нет наблюдений == 200),
# для правостороннего передаем 1, а если не цензурировалось - 0.

cens[Y == 800] = 1

from tobit import *

tobit_model = TobitModel()
tobit_model.fit(sm.add_constant(X_train), Y_train, cens)

tobit_model.coef_
"""

smooth = """
import pandas as pd
import numpy as np

# Создание фиктивного DataFrame с временными рядами
np.random.seed(42)  # для воспроизводимости
data = {
    'date': pd.date_range(start='2020-01-01', periods=100, freq='M'),
    'value': np.random.normal(loc=100, scale=10, size=100)  # фиктивные данные
}
df = pd.DataFrame(data)

# Простая (среднеарифметическая) скользящая средняя
def simple_moving_average(data, p):
    return data.rolling(window=2*p+1, center=True).mean()

# Взвешенная (средневзвешенная) скользящая средняя
def weighted_moving_average(data, weights):
    p = len(weights) // 2
    def weighted_avg(x):
        return np.sum(weights * x) / np.sum(weights)
    return data.rolling(window=len(weights), center=True).apply(weighted_avg, raw=True)

# Среднехронологическая
def chronological_average(data, T):
    result = []
    half_T = T // 2
    for t in range(len(data)):
        if t < half_T or t >= len(data) - half_T:
            result.append(np.nan)
        else:
            avg = (0.5 * data[t - half_T] + np.sum(data[t - half_T + 1 : t + half_T]) + 0.5 * data[t + half_T]) / T
            result.append(avg)
    return pd.Series(result, index=data.index)

# Важно отметить, что методы выше оставляют крайние точки несглаженными. Эту проблему можно решить двумя способами:
# - Исключить крайние точки из ряда
# - Применить специальные формулы сглаживания для крайних точек, например для трёх точек:
#     - $\tilde y_1 = \frac{5 y_1 + 2 y_2 - y_3} 6$
#     - $\tilde y_n = \frac{5 y_n + 2 y_{n-1} - y_{n-2}} 6$

# Экспоненциальное сглаживание
def exponential_smoothing(data, alpha):
    result = [data[0]]
    for n in range(1, len(data)):
        result.append(alpha * data[n] + (1 - alpha) * result[n-1])
    return pd.Series(result, index=data.index)
"""

dickie_fuller_test = """
from statsmodels.tsa.stattools import adfuller
adfuller(data)

#если p-value > 0.05$, то нулевая гипотеза не отвергается и ряд не является стационарным.
# => преобразование 

diff = (data.shift(1) - data).iloc[1:]

# и снова
adfuller(diff)
# и снова преобрзаование, если ряд не стал стационарным
"""

stationary_models = {
    "AR": """
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.ar_model import AutoReg
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

# # Создание фиктивного DataFrame с временными рядами
# data = {
#     'date': pd.date_range(start='2020-01-01', periods=100, freq='M'),
#     'value': np.random.normal(loc=100, scale=10, size=100)
# }
# df = pd.DataFrame(data)
# df.set_index('date', inplace=True)

# Визуализация временного ряда
plt.figure(figsize=(10, 6))
plt.plot(df['value'])
plt.title('Time Series')
plt.show()

# Построение ACF и PACF для выбора параметра p
fig, ax = plt.subplots(2, 1, figsize=(12, 8))
plot_acf(df['value'], lags=20, ax=ax[0])
plot_pacf(df['value'], lags=20, ax=ax[1])
plt.show()

#автоматически
                     
from statsmodels.tsa.stattools import acf, pacf

values_acf, confint_acf = acf(x_t.squeeze(), nlags=5, alpha=0.05)
values_pacf, confint_pacf = pacf(x_t.squeeze(), nlags=5, method='ywm', alpha=0.05)

for i in range(5):
    if confint_acf[i][0] // 1 == confint_acf[i][1] // 1:
        print(f"{i} по ACF значимо")

for i in range(5):
    if confint_pacf[i][0] // 1 == confint_pacf[i][1] // 1:
        print(f"{i} по PACF значимо")


# Выбор параметра p
p = 3  # Например, выбираем p = 3 на основе PACF

# Построение модели
model = AutoReg(df['value'], lags=p).fit()

# Вывод параметров модели
print(model.summary())

# Прогнозирование
forecast_steps = 12
forecast = model.predict(start=len(df), end=len(df) + forecast_steps - 1, dynamic=False)

# Визуализация прогноза
plt.figure(figsize=(10, 6))
plt.plot(df['value'], label='Original Series')
plt.plot(pd.date_range(start=df.index[-1], periods=forecast_steps + 1, freq='M')[1:], forecast, label='Forecast', color='red')
plt.title('AR Model Forecast')
plt.legend()
plt.show()
""",
    "ARMA": """
#графики
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

plot_acf(x_t.squeeze(), lags=40, alpha=0.05)
plt.title("ACF (AutoСorrelation Function)")

plot_pacf(x_t.squeeze(), lags=40, alpha=0.05, method="ywm")
plt.title("PACF (Partial AutoСorrelation Function)")

#автоматическая проверка значимости
from statsmodels.tsa.stattools import acf, pacf

values_acf, confint_acf = acf(x_t.squeeze(), nlags=5, alpha=0.05)
values_pacf, confint_pacf = pacf(x_t.squeeze(), nlags=5, method='ywm', alpha=0.05)

for i in range(5):
    if confint_acf[i][0] // 1 == confint_acf[i][1] // 1:
        print(f"{i} по ACF значимо")

for i in range(5):
    if confint_pacf[i][0] // 1 == confint_pacf[i][1] // 1:
        print(f"{i} по PACF значимо")

from statsmodels.tsa.arima.model import ARIMA

model = ARIMA(x_t, order=(1, 0, 2)) #d=0 => ARMA
result = model.fit()
print(result.summary())

# прогноз
forecast = result.get_forecast(steps=10)
forecast_summary = forecast.summary_frame()

plt.figure(figsize=(18, 6))
plt.plot(x_t, label='Известные значения')
plt.plot(forecast_summary['mean'], label='Прогноз', color='red')
plt.fill_between(
    forecast_summary.index,
    forecast_summary['mean_ci_lower'],
    forecast_summary['mean_ci_upper'],
    color='pink',
    alpha=0.3,
    label='Доверительный интервал прогноза',
)
plt.title('Ежемесячная доходность корпоративных облигаций класса Aaa')
plt.xlabel('Время')
plt.ylabel('Доходность')
plt.legend()
plt.grid(True)
plt.show()

#качество
m.r2_score(x_t[:-1], result.predict()[1:])
""",
    "ARIMA": """
#графики
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

plot_acf(x_t.squeeze(), lags=40, alpha=0.05)
plt.title("ACF (AutoСorrelation Function)")

plot_pacf(x_t.squeeze(), lags=40, alpha=0.05, method="ywm")
plt.title("PACF (Partial AutoСorrelation Function)")

#автоматическая проверка значимости
from statsmodels.tsa.stattools import acf, pacf

values_acf, confint_acf = acf(x_t.squeeze(), nlags=5, alpha=0.05)
values_pacf, confint_pacf = pacf(x_t.squeeze(), nlags=5, method='ywm', alpha=0.05)

for i in range(5):
    if confint_acf[i][0] // 1 == confint_acf[i][1] // 1:
        print(f"{i} по ACF значимо")

for i in range(5):
    if confint_pacf[i][0] // 1 == confint_pacf[i][1] // 1:
        print(f"{i} по PACF значимо")

from statsmodels.tsa.arima.model import ARIMA

# берём x_t = (df.AAA.shift(1) - df.AAA).dropna()
# пока не станет стационарным или же указываем нужное d
model = ARIMA(x_t, order=(1, d, 2)) #d=0 => ARMA
result = model.fit()
print(result.summary())

# прогноз
forecast = result.get_forecast(steps=10)
forecast_summary = forecast.summary_frame()

plt.figure(figsize=(18, 6))
plt.plot(x_t, label='Известные значения')
plt.plot(forecast_summary['mean'], label='Прогноз', color='red')
plt.fill_between(
    forecast_summary.index,
    forecast_summary['mean_ci_lower'],
    forecast_summary['mean_ci_upper'],
    color='pink',
    alpha=0.3,
    label='Доверительный интервал прогноза',
)
plt.title('Ежемесячная доходность корпоративных облигаций класса Aaa')
plt.xlabel('Время')
plt.ylabel('Доходность')
plt.legend()
plt.grid(True)
plt.show()

#качество
m.r2_score(x_t[:-1], result.predict()[1:])
""",
}

general_conc = """
# пример переменных
a1, a2, b1, b2, SBER_t, VTB_t, USD_t, t, u_t, v_t = sp.symbols(
    'a1, a2, b1, b2, SBER_t, VTB_t, USD_t, t, u_t, v_t')

# эндогенные
Y = sp.Matrix([SBER_t, VTB_t])

# экзогенная
X = sp.Matrix([USD_t, t])

# случайные возмущения
U = sp.Matrix([u_t, v_t])

# $\begin{cases}
# \text{SBER}_t = a_1 t + a_2 \text{VTB}_t + u_t \\
# \text{VTB}_t = b_1 \text{USD}_t + b_2 \text{SBER}_t + v_t
# \end{cases}$
# исходя из вида системы
A = sp.Matrix([[1, -a2], [-b2, 1]])

B = sp.Matrix([[0, -a1], [-b1, 0]])

# приведённая форма

Y_priv = -(A**-1) * B * X + A**-1 * U
"""

rank_rule = """
# A, B расписаны в Общие понятия
A_full = sp.Matrix.hstack(A, B)

def get_r_matrix(row):
    zero_indices = [i for i, value in enumerate(row) if value == 0]

    r = sp.zeros(len(zero_indices), len(row))
    for i, index in enumerate(zero_indices):
        r[i, index] = 1

    return r

for i in range(A_full.shape[0]):
    print((A_full * get_r_matrix(A_full[i, :]).T).rank())

#все значения должны быть равны m-1, где m - кол-во уравнений
"""

order_rule = """
Правило порядка (необходимое условие):

D - число экзогенных уравнений в системе, но не в уравнении

H - число эндогенных переменных в уравнении

1. Если D + 1 = H - точно идентифицируемо
2. Если D + 1 < H - неидентифицируемо
3. Если D + 1 > H - сверхидентифицируемо
"""
kmnk = """
# если все уравнения ТОЧНО идентифицируемы

# оцениваем каждое уравнение
model = sm.OLS(df.SBER, np.array([df.USD, np.array(df.index)]).T)
result1 = model.fit()

model = sm.OLS(df.VTB, np.array([df.USD, np.array(df.index)]).T)
result2 = model.fit()

# объединяем полученные регрессии
M = sp.Matrix([list(result1.params), list(result2.params)])
ME = sp.Matrix.vstack(M, sp.eye(A_full.shape[1] - M.shape[0]))

# возвращаемся к исходным параметрам
final_params = {}
for i in range(A_full.shape[0]):
    for k, v in sp.solve(A_full[i, :] * ME).items():
        final_params[k] = v
"""

mnk2 = """
from linearmodels import IV2SLS
# если все уравнения идентифицируемы
model1 = IV2SLS(
    dependent=df['SBER'], exog=df[['t']], endog=df['VTB'], instruments=df['USD']
).fit()

model1.params

model2 = IV2SLS(
    dependent=df['VTB'], exog=df[['USD']], endog=df['SBER'], instruments=df['t']
).fit()

model2.params

#обычно, оценки совпадают с кмнк
"""

mnk3 = """
from linearmodels import IV3SLS
# если все уравнения идентифицируемы
# учитывает автокорреляцию между уравнениями

eq1 = {
    'dependent': df['SBER'],
    'exog': df[['t']],
    'endog': df[['VTB']],
    'instruments': df[['USD']],
}


eq2 = {
    'dependent': df['VTB'],
    'exog': df[['USD']],
    'endog': df[['SBER']],
    'instruments': df[['t']],
}

system = IV3SLS({'SBER': eq1, 'VTB': eq2})

results = system.fit()

results.params

# или же

eq1 = "Y ~ C + I + G + NX"
eq2 = "C ~ 1 + Y_minus_T"
eq3 = "I ~ 1 + r"
eq4 = "NX ~ 1 + e"
eq5 = "CF ~ 1 + r"
eq6 = "NX ~ CF_neg"

formula = {str(x): x for x in [eq1, eq2, eq3, eq4, eq5, eq6]}

mod = IV3SLS.from_formula(
    formula,
    data=train_df,
)

results = mod.fit()

results
"""

sur = """
from linearmodels import SUR
# если все уравнения идентифицируемы

eq1 = {"dependent": df["SBER"], "exog": df[["t", "USD"]]}
eq2 = {"dependent": df["VTB"], "exog": df[["t", "USD"]]}

system = SUR({"SBER": eq1, "VTB": eq2})

results = system.fit()

print(results.params)
"""
h_test = """
# коеф дарбина-уотсона
db = float(model_koika.summary().tables[2][0][3].data)

ro_hat = 1 - db / 2
n = new_data.shape[0]
D_hat = model_koika.bse[-1] ** 2
h = ro_hat * np.sqrt(n / (1 - n * D_hat))

alpha = 0.05
h_cr = scs.norm().ppf(1 - alpha/2)

abs(h) > h_cr #если True, то гипотеза о независимости остатков отклоняется и присутствует автокорреляция
"""
dynamic_models = {
    "Метод геометрической прогрессии": """
def geom_profression_method(X, y, delta, lambd_n=100, max_lag=20):
    best_rsquared = 0
    best_model = None

    for lambd in tqdm.tqdm(np.linspace(0, 1, lambd_n + 1)):
        X_ = X.copy()
        y_ = y.copy()
        p = 0
        z = [sum(np.mean(X_, axis=0))]
        while True:
            p += 1
            temp = X_[p:]
            for i in range(0, p + 1):
                temp += lambd**i * X_.shift(i).dropna()
            z.append(sum(np.mean(temp, axis=0)))
            if np.abs((z[-1] - z[-2]) / z[-2]) < delta or p >= max_lag:
                break

        model = sm.OLS(y[temp.index], sm.add_constant(temp)).fit()
        if model.rsquared > best_rsquared:
            best_rsquared = model.rsquared
            best_model = model
            p_best = p
            lambd_best = lambd

    return best_model, p_best, lambd_best

y = all_data.Close
X = all_data[["psr", "m2"]]

delta = 0.005

best_model, best_p, best_lambd = geom_profression_method(X, y, delta)
best_model.summary()
""",
    "Преобразование Койка": """
# $ Y_t = (1 - \lambda) a_0 + b_0 \cdot X_t + \lambda \cdot Y_{t-1} + \varepsilon_t - \lambda \cdot \varepsilon_{t-1} $

new_data = pd.concat([X, y.shift(1)], axis=1).dropna()
new_data.columns.values[4] = "Close_{t-1}"

model_koika = sm.OLS(y, sm.add_constant(X)).fit()

b0 = round(model_koika.params["psr"], 4)
b1 = round(model_koika.params["m2"], 4)
lambd = round(model_koika.params["Close_{t-1}"], 4)
a0 = round(model_koika.params.const / (1 - lambd), 4)
b0, b1, lambd, a0

# модель с бесконечными лагами: a0 + b1 * lambd**p для p от 0 до inf
""",
    "Модель адаптивных ожиданий": """
# Оценивается следующий вид модели:
# $Y_t = a + b X^*_t + \varepsilon_t$
# С помощью преобразования можем прийти к удобному виду:
# $Y_t = \gamma a + \gamma b X_t + (1 - \gamma) Y_{t - 1} + u_t$

model_koika = sm.OLS(y, sm.add_constant(X)).fit()
gamma = round(1 - model_koika.params["Close_{t-1}"], 4)
b0 = round(model_koika.params["psr"] / gamma, 4)
b1 = round(model_koika.params["m2"] / gamma, 4)
a0 = round(model_koika.params.const / gamma, 4)
a0, b0, b1, gamma
""",
    "Модель частичных корректировок": """
# Необходимо построить следующую модель:
# $Y^*_t = a + b X_t + \varepsilon_t$
# При помощи преобразований можем осуществить оценку параметров:
# $Y_t = \lambda a + (1 - \lambda) Y_{t-1} + \lambda b X_t + \lambda \varepsilon_t$

model_koika = sm.OLS(y, sm.add_constant(X)).fit()
lambd = round(1 - model_koika.params["Close_{t-1}"], 4)
b0 = round(model_koika.params["psr"] / lambd, 4)
b1 = round(model_koika.params["m2"] / lambd, 4)
a0 = round(model_koika.params.const / lambd, 4)
a0, b0, b1, gamma
""",
    "Лаги Алмон": """
# Для построение модели с использованием лагов Алмон, необходимо вычислить следующие величины:
# $Z_{tp} = \sum_{i = 0}^{k} {i^p X_{t-i}}$
# где $p$ - степень полинома, $k$ - количество лагов

def get_almon(X, p, k):
    Z = []

    data = pd.DataFrame(X.copy())
    for i in range(1, k + 1):
        data[f'X{i}'] = X.shift(i)

    data = data.dropna()

    for j in range(p):
        temp = 0
        for i in range(1, k + 1):
            temp += i ** j * data.iloc[:, i]
        Z.append(temp)

    result = pd.concat(Z, axis=1)

    result.columns = [f"X{i}" for i in range(1, p + 1)]

    return result

k = 14
p = 3

z = get_almon(X, p, k)

# Оценим следующую модель:
# $Y_t = a_0 + \nu_0 Z_{t0} + \nu_1 Z_{t1} + \nu_2 Z_{t2} + \epsilon_t$

model = sm.OLS(y[k:], sm.add_constant(z)).fit()

#модель лагов алмон
nu1 = model.params.X1
nu2 = model.params.X2
nu3 = model.params.X3

# или изначальный вид
coefs = [a0] + [nu1 + nu2 * i + nu3 * i ** 2 for i in range(k + 1)] + [None]
stds  = [model.bse.const] + [None] * (k + 1)
vars  = [None, 'X_t'] + [f'X_{{t - {i}}}' for i in range(1, k + 1)] + ['\\varepsilon_t']
""",
}

panel_data_models = {
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
""",
}

panel_data_tests = {
    "Pooled vs FE (тест Фишера)": """
# $F = \frac{(RSS_P - RSS_{FE}) / (n - 1)}{RSS_{FE} / (nT - n - k)}$
# $F_{крит} = F_\alpha(n - 1; nT - n - k)$

from scipy.stats import f

RSSp = pooled.resid_ss
RSSfe = FE.resid_ss

T = data.reset_index().Year.nunique()
k = len(X.columns)

n = len(y) / T
F = (RSSp - RSSfe) / (n - 1) / (RSSfe / (n * T - n - k))
F_cr = f(n - 1, n * T - n - k).isf(0.95)

# если $F > F_{крит} \Rightarrow H_0$ отвергается, $\text{FE}$ лучше $\text{Pooled}$. 
""",
    "Pooled vs RE (тест Брауша-Пагана)": """
import statsmodels.stats.diagnostic as dg

_, _, _, pv = dg.het_breuschpagan(pooled.resids, sm.add_constant(pooled.model.exog.dataframe))

# если pv < alpha, то остатки не гомоскедастичны (так как отвергается H_0), а значит RE лучше Pooled$.
""",
    "FE vs RE (тест Хаусмана)": """
import numpy.linalg as la 
from scipy import stats  

def hausman(fe, re): 
    b = fe.params     
    B = re.params   
    v_b = fe.cov     
    v_B = re.cov     
    df = b.size     
    chi2 = np.dot((b - B).T, la.inv(v_b - v_B).dot(b - B))    
    pval = stats.chi2.sf(chi2, df)     
    return chi2, pval

hausman(FE, RE)

# если p-value < alpha, то есть достаточно высокого значения статистики хи-квадрат, 
# оно попадает в критическую область и H_0 отвергается, 
# поэтому между RE и FE лучше оказывается FE
""",
}


themes = {
    "1. Аномалии, трендь, сглаживание": {
        "Аномалии": anomalies,
        "Тренд": trend,
        "Сглаживание": smooth,
    },
    "2. Тренд сезонные модели": {
        "Кривая роста": growth_curve,
        "Модель Брауна": browns_model,
        "Модель Хольта-Уинтерса": holt_winters_model,
        "метод Четверикова": chetverikov_method,
    },
    "3. Логит и пробит (мб хэкит и пробит)": {
        "Логит модель": logit_model,
        "Пробит модель": probit_model,
        "Хекит модель": heckit_model,
        "Тобит модель": tobit_model,
    },
    "4. Стационарные ряды": {
        "Тест Дики-Фуллера": dickie_fuller_test,
        "Модели": stationary_models,
    },
    "5. Системы уравнений": {
        "Общие понятия": general_conc,
        "Проверки идентифицируемости": {
            "Правило ранга": rank_rule,
            "Правило порядка": order_rule,
        },
        "Методы оценки моделей": {
            "КМНК": kmnk,
            "2-МНК": mnk2,
            "3-МНК": mnk3,
            "SUR": sur,
        },
    },
    "6. Динамические модели": {"H-тест": h_test, "Модели": dynamic_models},
    "7. Панельные данные": {"Тесты": panel_data_tests, "Модели": panel_data_models},
    "8. Информационные критерии": information_criteria,
    "9. Модели бинарного выбора": semi_log_models_tests,
}


def print_dict(x):
    if isinstance(x, dict):
        for k, v in x.items():
            print(k)
            print_dict(v)
    else:
        print(len(x))


print_dict(themes)
