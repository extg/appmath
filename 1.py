import math
import random
from pandas import DataFrame
from matplotlib import pyplot as plt
import numpy as np
import scipy.stats as st
from scipy.stats import *
from collections import Counter
import scipy.integrate as spint

f = open('1.txt')
serie = [int(i) for i in f.read().split()]
print(serie)
resulat = []
resulat.extend([np.mean(serie), np.var(serie), st.sem(serie), st.mode(serie)[0][0], np.percentile(serie, 25),
                np.percentile(serie, 50), np.percentile(serie, 75), np.std(serie, ddof=1), st.kurtosis(serie),
                st.skew(np.array(serie)), np.min(serie), np.max(serie)])
print("Среднее, дисперсия и стандартная ошибка: ", resulat[:3], "\nМода и квартили: ", resulat[3:7],
      "\nСтандартное отклонение, эксцесс, ассиметричность", resulat[7:10], "\nMin и max: ", resulat[10:])
DataFrame(serie).boxplot()
plt.show()
c = Counter(serie)
print(c)
nombres = list(c.keys())
nombres.sort()
fr = [c[i] for i in nombres]
for i in nombres:
    print("%3d" % i, end=' ')
print()
for i in fr:
    print("%3d" % i, end=' ')
print()

m, s = resulat[0], resulat[7]
min, max = resulat[-2:]
l = max - min
k = l // 6  # длина одного отрезка, всего их делаем шесть
j = 1
gamma = 0.95
alpha = 0.025
n = 100
df = 99

segments = [0 for i in range(6)]
for i in range(len(fr)):
    if nombres[i] > min + j * k:
        j += 1
    segments[j - 1] += fr[i]
# получаем нормальное распределение
normal = [norm.cdf((min + k * i - m) / s) * n for i in range(1, 7)]
for i in range(5, 1, -1):
    normal[i] -= normal[i - 1]
print(normal)
print(segments)
chi, chi_crit = st.chisquare(segments, normal)[0], st.chi2.ppf(1 - alpha, 5)  # 5 - степени свободы
print('Хи^2:', chi, '\nХи^2 критический:', chi_crit, "\nГипотеза верна" if (chi < chi_crit) else "\nГипотеза ложна")
t_ = t.ppf(gamma + 0.5 * (1 - gamma), df)
print("t = ", t_)
print("Интервал для мат. ожидания:", m - t_ * s / np.sqrt(n), m + t_ * s / np.sqrt(n))
print("Интервал для среднеквадр. отклонения", s * np.sqrt(df / st.chi2.ppf(0.5 * (1 + gamma), df)),
      s * np.sqrt(df / st.chi2.ppf(0.5 * (1 - gamma), df)))
plt.plot(x=serie)

plt.hist(serie, 10, facecolor='blue', align="left", edgecolor='black')
plt.xlabel("Значение")
plt.ylabel("Частота")
plt.show()

n_act = 0
somme = 0
for i in range(min, max + 1):
    if i == nombres[n_act]:
        somme += fr[n_act]
        n_act += 1
    plt.plot([i, i + 1], [somme, somme], color="blue")
plt.show()

plt.hist(serie, n, histtype='step', facecolor='blue', align="left", cumulative=True)
plt.xlim(min, max)
plt.show()
