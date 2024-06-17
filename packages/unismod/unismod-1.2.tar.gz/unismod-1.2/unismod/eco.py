import pandas as pd
import numpy as np

import scipy.stats as stats
import statsmodels.api as sm
from statsmodels.tsa import holtwinters

from statsmodels.tsa.stattools import adfuller


def imports():
    return """
  import pandas as pd
  import numpy as np

  import scipy.stats as stats
  import statsmodels.api as sm 
  from statsmodels.tsa import holtwinters

  from statsmodels.tsa.stattools import adfuller
  from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

  import seaborn as sns
  import matplotlib.pyplot as plt

  %load_ext rpy2.ipython
  
  %%R
  install.packages("systemfit")
  install.packages("readxl")
  install.packages("plm")"""


def is_anomaly_stdnt(y0, Y, alpha=0.05):
    n = len(Y)
    tau = abs(y0 - Y.mean()) / Y.std()

    t_kr = stats.t(1 - alpha, n - 2).ppf(1 - alpha)
    tau_kr = t_kr * np.sqrt(n - 1) / np.sqrt((n - 2) + t_kr ** 2)

    is_anomaly = True

    if tau < tau_kr:
        is_anomaly = False

    return is_anomaly, tau_kr


# Метод Ирвина
def is_anomalies_irvn(Y, alpha=0.05):
    n = len(Y)
    l_tabl = 0
    if n == 2:
        l_tabl = 2.8
    if n == 3:
        l_tabl = 2.2
    if n <= 10:
        l_tabl = 1.5
    if n <= 20:
        l_tabl = 1.3
    if n <= 30:
        l_tabl = 1.2
    if n <= 50:
        l_tabl = 1.1
    else:
        l_tabl = 1

    return abs(Y.diff(1)) / Y.std() > l_tabl


# Критерий серий, основанный на медиане
def median_crit(Y):
    n = len(Y)
    Me = Y.median()
    series = Y < Me

    series_len = np.array(list(map(len, ''.join(map(str, list(series.to_numpy().astype(np.int8)))).split('01')))) + 1
    max_ser = series_len.max()  # Протяженность самой большой серии
    n_ser = len(series_len)  # Количество серий

    if (max_ser < 3.3 * (np.log(n) + 1)) and (n_ser > 1 / 2 * (n + 1 - 1.96 * np.sqrt(n - 1))):
        return 'Гипотеза об отсутствии тренда принимается (Тренда нет)'
    else:
        return 'Гипотеза об отсутствии тренда откланяется (Тренд есть)'


# Метод проверки разностей средних уровней
def mean_lvl(Y, alpha=0.05):
    n = len(Y)
    n1 = n // 2

    n2 = n - n1

    y1 = Y[:n1]
    y2 = Y[n1:]

    F = y1.var() / y2.var() if y1.var() > y2.var() else y2.var() / y1.var()

    F_kr = stats.f.ppf(1 - alpha, n1 - 1, n2 - 1)

    if F < F_kr:
        # Принимается гипотеза о равенстве дисперсий принимается
        sig = np.sqrt(((n1 - 1) * y1.var() + (n2 - 1) * y2.var()) / (n1 + n2 - 2))
        t = abs(y1.mean() - y2.mean()) / (sig * np.sqrt(1 / n1 + 1 / n2))

        t_kr = stats.t.ppf(1 - alpha, df=n1 + n2 - 2)

        if t < t_kr:
            return 'Гипотеза об отсутствии тренда принимается (Тренда нет)'
        else:
            return 'Гипотеза об отстутствии тренда откланяется (Тренд есть)'
    else:
        return 'Метод ответа не даёт'


# Метод Фостера-Стьюарта
def foster_stuart(Y, alpha=0.05):
    n = len(Y)

    k = []
    l = []

    for i in range(1, n):
        k.append(1 if Y[i] > Y[:i].max() else 0)
        l.append(1 if Y[i] < Y[:i].min() else 0)

    s = sum(k) + sum(l)
    d = np.sum(k) - sum(l)

    mean_s = (1.693872 * np.log(n) - 0.299015) / (1 - 0.035092 * np.log(n) + 0.002705 * np.log(n) ** 2)

    t_s = (s - mean_s) / np.sqrt(2 * np.log(n) - 3.4253)
    t_d = (d - 0) / np.sqrt(2 * np.log(n) - 0.8456)

    t_kr = stats.t.ppf(1 - alpha / 2, n)

    s_trand = ''
    d_trand = ''
    if t_s > t_kr:
        s_trand = 'Есть тренд ряда'
    else:
        s_trand = 'Тренда ряда нет'

    if t_d > t_kr:
        d_trand = 'Тренд дисперсии есть'
    else:
        d_trand = 'Тренда дисперсии нет'

    return s_trand, d_trand


# Взвешенная (Средневзвешенная скользящая средняя)
def weighted_avg(Y, window=5):
    if window == 5:
        weights = np.array([-3, 12, 17, 12, -3])
    elif window == 7:
        weights = np.array([-2, 3, 6, 7, 6, 3, -2])
    else:
        raise ValueError(f'window argument must be equal either 5 or 7, not {window}')

    def weighted(win):
        win = win.to_numpy()
        return sum(win * weights) / sum(weights)

    return Y.rolling(window=window, center=True).apply(weighted)


# Средняя хронологическая
def hron_mean(Y, T):
    def windowed(win):
        win = win.to_numpy()
        return (win[0] / 2 + win[-1] / 2 + sum(win[1:-1])) / (len(win) - 1)

    return Y.rolling(window=T, center=True).apply(windowed)


# Экспоненциальное сглаживание
def exp_smooth(Y, alpha):
    n = len(Y)

    result = [Y[0]]  # first value is same as series
    for i in range(1, n):
        result.append(alpha * Y[i] + (1 - alpha) * result[i - 1])
    return pd.Series(result)


# Доверительный интервал прогноза (Линейная модель)
def interval_for_criv_rost(k, m, Y, t, resid, alpha=0.05):
    n = len(Y)

    S = np.sqrt(sum(resid ** 2) / n - m - 1)
    t_a = stats.t.ppf(1 - alpha, n - m - 1)
    return S * t_a * np.sqrt((1 + 1 / n + (n + k - t.mean()) ** 2) / sum((t - t.mean()) ** 2))


# Модель Брауна
def braun(Y, T, first_k, degree=1, beta=0.6):
    T = sm.add_constant(T)
    for i in range(2, degree + 1):
        T = np.c_[T, T[:, 1] ** (i)]
    Y = Y.to_numpy().reshape(-1, 1)
    first_k_model = sm.OLS(Y[:first_k], T[:first_k]).fit()

    model = first_k_model.params.reshape(-1, 1)

    for i in range(first_k, len(T)):
        # Ошибка i-го предсказания
        future = np.dot(T[i], model).flatten()
        e = (Y[i] - future)[0]
        # Исправление коэффициентов
        model[0, 0] = model[0, 0] + model[1, 0] + (1 - beta) ** 2 * e
        model[1, 0] = model[1, 0] + (1 - beta) ** 2 * e

    return model


def holt_winters():
    # Модель Хольта-Уинтерса
    res = holtwinters.ExponentialSmoothing(Y, seasonal_periods=4, trend='add', seasonal='mul').fit()
    return res


# Метод Четверикова
def chetverikov(Y, T):
    f = hron_mean(Y, T).dropna()
    l = Y[f.index] - f

    n_years = len(Y) / T

    for year, i_ in ((l.loc[i:i + T - 1], i) for i in range(0, len(l), T)):
        sig_i = ((sum(year ** 2) - (sum(year) ** 2 / T)) / (T - 1))
        l[i_:i_ + T - 1] = l[i_:i_ + T - 1] / sig_i
    S = []
    for s_i in range(T):
        res = 0
        count = 0
        for i in range(s_i, len(l), T):
            res += l[i]
            count += 1
        S.append(res / count)

    return l


def adfuller_(Y):
    return 'Не стационарен' if adfuller(Y)[1] > 0.05 else 'Стационарен'


def auto_corr_plt_code():
    return """
  fig, ax = plt.subplots(nrows=1, ncols=2)
  fig.set_figheight(5)
  fig.set_figwidth(10)


  plot_acf(Y.diff(4).dropna(), lags=10, ax=ax[0])
  plot_pacf(Y.diff(4).dropna(), lags=10, ax=ax[1])

  plt.show()
  
  model = sm.tsa.ARIMA(first_diff_y, order=(p, 0, q)).fit()
  """


def panels_models():
    return """
  spec <- Y~X1 + X2 + X3 + X4 + X5 + X6
  
  # Модель пула
  p_model <- plm(spec, data=df, index=c("Reg", "Year"), model="pooling")
  summary(pool_model)

  # Модель c фикс. эффктом
  fe_model <- plm(spec, data=df, index=c("Reg", "Year"), model="within")
  # Модель с случайным эффектом
  re_model <- plm(spec, data=df, index=c("Reg", "Year"), model="random")
  summary(re_model)
  """


def panels_compare():
    return """
  # pool vs fe
  pFtest(fe_model, p_model) # если pv < 0.05 => Fe лучше
  qf(0.05, 79, 154, lower.tail=TRUE)

  # pool vs re (Бреуш-Паган)
  plmtest(re_model, type = "bp") # если pv < 0.05 => re лучше

  # fe vs re
  phtest(fe_model, re_model) # если pv < 0.05 => re лучше
  """


def logit_percentage():
	return """# Получение долей значимых факторов в модели Logit
	coefs = logit.params
	ratios = np.exp(coefs)
	factors = ratios[ratios != 1]
	factors_percentage = (factors - 1) * 100

	print('\nДоли значимых факторов в модели Logit:')
	for factor, percentage in zip(factors.index, factors_percentage):
    print(f'{factor}: {percentage:.2f}%')"""
	
	
def probit_percentage():
	return """# Получение долей значимых факторов в модели Probit
	coefs = probit.params
	probab = norm.cdf(coefs)
	factors = probab[probab != 0.5]
	factors_percentage = (factors - 0.5) * 100

	print('\nДоли значимых факторов в модели Probit:')
	for factor, percentage in zip(coefs.index, factors_percentage):
    print(f'{factor}: {percentage:.2f}%')"""