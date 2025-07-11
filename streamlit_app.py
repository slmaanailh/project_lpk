import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import pandas as pd

# Fungsi untuk menghitung regresi linier dan R^2
def hitung_r2(x, y):
    x = x.reshape(-1, 1)
    model = LinearRegression().fit(x, y)
    y_pred = model.predict(x)
    return r2_score(y, y_pred), model.coef_[0], model.intercept_

# Fungsi utama
def tentukan_orde_reaksi(data_t, data_A):
    t = np.array(data_t)
    A = np.array(data_A)
    
    orde0 = A
    orde1 = np.log(A)
    orde2 = 1 / A

    r2_0, m0, c0 = hitung_r2(t, orde0)
    r2_1, m1, c1 = hitung_r2(t, orde1)
    r2_2, m2, c2 = hitung_r2(t, orde2)

    r2_list = [r2_0, r2_1, r2_2]
    orde = np.argmax(r2_list)

    print(f"R² Orde 0: {r2_0:.4f}")
    print(f"R² Orde 1: {r2_1:.4f}")
    print(f"R² Orde 2: {r2_2:.4f}")
    print(f"Reaksi paling sesuai adalah orde {orde}")

    # Plot grafik
    plt.figure(figsize=(12, 4))

    plt.subplot(1, 3, 1)
    plt.plot(t, orde0, 'bo-', label='[A] vs t')
    plt.title(f'Orde 0 (R²={r2_0:.4f})')
    plt.xlabel('t')
    plt.ylabel('[A]')

    plt.subplot(1, 3, 2)
    plt.plot(t, orde1, 'go-', label='ln[A] vs t')
    plt.title(f'Orde 1 (R²={r2_1:.4f})')
    plt.xlabel('t')
    plt.ylabel('ln[A]')

    plt.subplot(1, 3, 3)
    plt.plot(t, orde2, 'ro-', label='1/[A] vs t')
    plt.title(f'Orde 2 (R²={r2_2:.4f})')
    plt.xlabel('t')
    plt.ylabel('1/[A]')

    plt.tight_layout()
    plt.show()
