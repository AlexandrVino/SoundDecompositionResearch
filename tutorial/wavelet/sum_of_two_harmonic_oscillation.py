from scipy.integrate import quad
from numpy import *
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

N = 256


def S(t):
    return sin(2 * pi * t / 10) + sin(2 * pi * t / 50)


plt.figure(' Сумма двух гармонических колебаний')
plt.title(' Сумма двух гармонических колебаний', size=12)
y = [S(t) for t in arange(0, 250, 1)]
x = [t for t in arange(0, 250, 1)]
plt.plot(x, y)
plt.grid()


def w(a, b):
    f = lambda t: (1 / a ** 0.5) * exp(-0.5 * ((t - b) / a) ** 2) * (((t - b) / a) ** 2 - 1) * S(t)
    r = quad(f, -N, N)
    return round(r[0], 3)


x = arange(1, 50, 1)
y = arange(1, 50, 1)
z = array([w(i, j) for j in y for i in x])
X, Y = meshgrid(x, y)
Z = z.reshape(49, 49)
fig = plt.figure("Вейвлет-спектр:2-х гармонических колебаний")
ax = Axes3D(fig)
ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.jet)
ax.set_xlabel(' Масштаб:a')
ax.set_ylabel('Задержка: b')
ax.set_zlabel('Амплитуда ВП: $ N_{ab}$')
plt.figure("2D-график для z = w (a,b)")
plt.title('Плоскость ab с цветовыми областями ВП', size=12)
plt.contourf(X, Y, Z, 100)
plt.figure()
q = [w(2, i) for i in y]
p = [i for i in y]
plt.plot(p, q, label='w(2,b)')
q = [w(15, i) for i in y]
plt.plot(p, q, label='w(15,b)')
q = [w(30, i) for i in y]
plt.plot(p, q, label='w(30,b)')
plt.legend(loc='best')
plt.grid(True)
plt.figure()
q = [w(i, 13) for i in x]
p = [i for i in x]
plt.plot(p, q, label='w(a,13)')
q = [w(i, 17) for i in x]
plt.plot(p, q, label='w(a,17)')
plt.legend(loc='best')
plt.grid(True)
plt.show()
