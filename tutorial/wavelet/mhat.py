from numpy import *
import matplotlib.pyplot as plt

x = arange(-4, 30, 0.01)


def w(a, b, t):
    f = (1 / a ** 0.5) * exp(-0.5 * ((t - b) / a) ** 2) * (((t - b) / a) ** 2 - 1)
    return f


plt.title("Вейвлет «Мексиканская шляпа»:\n$1/\sqrt{a}*exp(-0,5*t^{2}/a^{2})*(t^{2}-1)$")
y = [w(1, 12, t) for t in x]
plt.plot(x, y, label="$\psi(t)$ a=1,b=12")
y = [w(2, 12, t) for t in x]
plt.plot(x, y, label="$\psi_{ab}(t)$ a=2 b=12")
y = [w(4, 12, t) for t in x]
plt.plot(x, y, label="$\psi_{ab}(t)$ a=4 b=12")
plt.legend(loc='best')
plt.grid(True)
plt.show()
