# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 16:16:28 2020
@ автор: Хоу Минхуэй
"""
import math
import matplotlib.pyplot as plt

N = 128
data = [0] * N
# Читать 128 данных в файле
fo = open("../../source/raw/wav/shashlindos.wav", "r")
list_x = list(fo.read().splitlines(False))
fo.close()
for i in range(N):
    data[i] = float(list_x[i])


# Волновое преобразование
def DWT():
    k = 3
    # k установлено на 3
    A = [[]] * k
    D = [[]] * k


    plt.plot(data)
    plt.axis([0, 128, 0, 25])
    plt.show()

    # Вейвлет разложение
    for i in range(int(N / 2)):
        A[0] = A[0] + [(data[2 * i] + data[2 * i + 1]) / math.sqrt(2)]
        D[0] = D[0] + [(data[2 * i] - data[2 * i + 1]) / math.sqrt(2)]
    n = N / 2
    for j in range(1, k):
        for i in range(int(n / 2)):
            A[j] = A[j] + [(A[j - 1][2 * i] + A[j - 1][2 * i + 1]) / math.sqrt(2)]
            D[j] = D[j] + [(A[j - 1][2 * i] - A[j - 1][2 * i + 1]) / math.sqrt(2)]
        n = n / 2
    DWT_x = A[j]
    for i in range(k):
        DWT_x = DWT_x + D[i]

    plt.plot(DWT_x)
    plt.axis([0, 128, -4, 60])
    plt.show()
    # Фильтрация
    Deltaw = 10
    for i in range(N):
        if DWT_x[i] < Deltaw:  # Вернуть к нулю значение DWT_x, которое меньше Deltaw
            DWT_x[i] = 0
    print("Изображение после фильтрации (Deltaw = 10):")
    plt.plot(DWT_x)
    plt.axis([0, 128, -4, 60])
    plt.show()
    # Обратное преобразование
    for i in range(len(A[j])):  # Возвращаем к нулю значение в A [j], которое меньше Deltaw
        if A[j][i] < Deltaw:
            A[j][i] = 0
    for i in range(k):
        for l in range(len(D[i])):  # Вернуть к нулю значение в D [k], которое меньше Deltaw
            if D[i][l] < Deltaw:
                D[i][l] = 0
    for m in range(k - 1, -1, -1):
        for i in range(len(A[m])):
            if m - 1 > -1:
                A[m - 1][2 * i] = (A[m][i] + D[m][i]) / math.sqrt(2)
                A[m - 1][2 * i + 1] = (A[m][i] - D[m][i]) / math.sqrt(2)
    for i in range(len(A[1])):
        A[0][2 * i] = (A[1][i] + D[1][i]) / math.sqrt(2)
        A[0][2 * i + 1] = (A[1][i] - D[1][i]) / math.sqrt(2)
    new_data = [0] * N
    for i in range(len(A[0])):
        new_data[2 * i] = (A[0][i] + D[0][i]) / math.sqrt(2)
        new_data[2 * i + 1] = (A[0][i] - D[0][i]) / math.sqrt(2)

    plt.plot(new_data)
    plt.axis([0, 128, 0, 25])
    plt.show()
    return


DWT()

