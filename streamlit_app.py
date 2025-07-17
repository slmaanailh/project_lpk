import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score

st.set_page_config(page_title="Regresi Polinomial dari Tabel", layout="centered")
st.title("Regresi Polinomial dan Korelasi dari Tabel Data")

st.markdown("""
Masukkan data X dan Y melalui tabel di bawah ini. Kemudian pilih satu atau beberapa orde regresi
(orde 0 = konstan, orde 1 = linear, orde 2 = kuadratik, dst) yang ingin ditampilkan.
""")

# Tabel input data
default_data = pd.DataFrame({
    'X': [1, 2, 3, 4, 5, 6],
    'Y': [2.5, 3.7, 7.2, 13.8, 21.5, 30.1]
})
data = st.data_editor(default_data, num_rows="dynamic", use_container_width=True)

# Validasi jumlah data
if len(data.dropna()) >= 2:
    try:
        x = data['X'].astype(float).to_numpy()
        y = data['Y'].astype(float).to_numpy()

        # Pilih ordo regresi
        selected_orders = st.multiselect("Pilih orde regresi yang ingin ditampilkan", options=list(range(0, 6)), default=[0, 1, 2])

        # Buat grafik
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.scatter(x, y, label="Data", color="black")

        # Loop setiap orde terpilih
        for order in selected_orders:
            coeffs = np.polyfit(x, y, order)
            poly_eq = np.poly1d(coeffs)
            y_pred = poly_eq(x)
            r2 = r2_score(y, y_pred)

            # Buat label persamaan
            eq_str = " + ".join([f"{c:.3f}x^{i}" if i > 1 else (f"{c:.3f}x" if i == 1 else f"{c:.3f}")
                                 for i, c in zip(range(order, -1, -1), coeffs)])
            label = f"Orde {order}: y = {eq_str}, R² = {r2:.4f}"

            # Plot garis regresi
            x_line = np.linspace(x.min(), x.max(), 200)
            y_line = poly_eq(x_line)
            ax.plot(x_line, y_line, label=label)

        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_title("Regresi Polinomial")
        ax.legend()
        st.pyplot(fig)
