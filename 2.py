import numpy
from matplotlib import pyplot as plt


def vect_pos(n):
    s = 0
    interm = []
    for _ in range(n):
        a = numpy.random.uniform(0, 1)
        s += a
        interm.append(a)
    return [i / s for i in interm]


n = 8
trans = [vect_pos(n) for i in range(n)]
print("Матрица переходов:")
for i in trans:
    print(i)
print("Сумма по строкам:", numpy.sum(trans, axis=1))

# Аналитический метод
g = [[trans[i][j] if i != j else trans[i][j] - 1 for i in range(n)] for j in range(n - 1)]
g.append([1 for i in range(n)])
dr = numpy.append(numpy.zeros(n - 1), 1)
print("Левая часть уравнения:")
for i in g:
    print(i)
print("Правая часть уравнения:\n", dr)
print("Решение уравнения: ", numpy.linalg.solve(g, dr))

# Численный метод
eps = 10**-8
deb1 = numpy.array(vect_pos(n))
deb2 = numpy.array(vect_pos(n))


def meth_num(av, eps):
    gr = []
    while True:
        apr = numpy.dot(av, trans)
        diff = apr - av
        res = numpy.sqrt(numpy.dot(diff, diff.transpose())/len(diff))
        gr.append(res)
        if res < eps:
            break
        av = apr
    plt.plot(range(len(gr)), gr)
    plt.scatter(range(len(gr)), gr)
    plt.xlabel("Номер итерации")
    plt.ylabel("Среднеквадратичное отклонение")
    plt.show()
    return apr


res1, res2 = meth_num(deb1, eps), meth_num(deb2, eps)
print("Численные результаты: ")
print(res1, res2, sep="\n")
