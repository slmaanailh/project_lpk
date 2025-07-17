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

# Validasi dan proses regresi
if len(data.dropna()) >= 2:
    try:
        # Ambil data
        x = data['X'].astype(float).to_numpy()
        y = data['Y'].astype(float).to_numpy()

        # Pilih orde regresi
        selected_orders = st.multiselect(
            "Pilih orde regresi yang ingin ditampilkan", 
            options=list(range(0, 6)), 
            default=[0, 1, 2]
        )

        # Plot awal
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.scatter(x, y, label='Data', color='black')

        # Hitung dan plot tiap orde regresi
        for order in selected_orders:
            coef = np.polyfit(x, y, order)
            poly_func = np.poly1d(coef)
            y_pred = poly_func(x)
            r2 = r2_score(y, y_pred)

            label = f"Orde {order}: y = {poly_func} | R² = {r2:.4f}"
            ax.plot(x, y_pred, label=label)

        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_title("Regresi Polinomial")
        ax.legend()
        st.pyplot(fig)

    except Exception as e:
        st.error(f"Terjadi kesalahan saat memproses data: {e}")
else:
    st.warning("Masukkan setidaknya dua pasang data.")
