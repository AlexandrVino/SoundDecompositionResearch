from scipy.integrate import quad
from numpy import *
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

N = 256


def S(t):
    U = 5;
    t0 = 20;
    tau = 60
    if t0 <= t <= t0 + tau:
        return U
    else:
        return 0


plt.figure()
plt.title('Прямоугольный импульс', size=12)
y = [S(t) for t in arange(0, 120, 1)]
x = [t for t in arange(0, 120, 1)]
plt.plot(x, y)
plt.grid()


def w(a, b):
    f = lambda t: (1 / a ** 0.5) * exp(-0.5 * ((t - b) / a) ** 2) * (((t - b) / a) ** 2 - 1) * S(t)
    r = quad(f, -N, N)
    return round(r[0], 3)


x = arange(1, 100, 1)
y = arange(1, 100, 1)
z = array([w(i, j) for j in y for i in x])
X, Y = meshgrid(x, y)
Z = z.reshape(99, 99)
fig = plt.figure("3D-график вейвлет спектрограммы")
ax = Axes3D(fig)
ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.jet)
ax.set_xlabel(' Масштаб:a')
ax.set_ylabel('Задержка: b')
ax.set_zlabel('Амплитуда ВП: $ N_{ab}$')
plt.figure("2D-график для z = w (a,b)")
plt.title('Плоскость ab с цветовыми областями ВП', size=12)
plt.contourf(X, Y, Z, 100)
plt.show()
