import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score

st.set_page_config(page_title="Regresi Polinomial dari Tabel", layout="centered")
st.title("Regresi Polinomial dan Korelasi dari Tabel Data")

st.markdown("""
Masukkan data X dan Y melalui tabel di bawah ini. Kemudian pilih satu atau beberapa orde regresi
(orde 1 = linear, orde 2 = kuadratik, dst) yang ingin ditampilkan.
""")

# Tabel input data
default_data = pd.DataFrame({
    'X': [1, 2, 3, 4, 5, 6],
    'Y': [2.5, 3.7, 7.2, 13.8, 21.5, 30.1]
})
data = st.data_editor(default_data, num_rows="dynamic", use_container_width=True)

# Validasi dan ekstrak X, Y
if len(data.dropna()) >= 2:
    try:
        x = data['X'].astype(float).to_numpy()
        y = data['Y'].astype(float).to_numpy()

        # Pilih ordo regresi (bisa lebih dari satu)
        selected_orders = st.multiselect("Pilih orde regresi yang ingin ditampilkan", options=list(range(1, 6)), default=[1, 2, 3])

        if selected_orders:
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.scatter(x, y, color='black', label='Data')
            colors = ['red', 'green', 'blue', 'orange', 'purple', 'brown']

            for idx, order in enumerate(selected_orders):
                coef = np.polyfit(x, y, order)
                poly_func = np.poly1d(coef)
                y_pred = poly_func(x)
                r2 = r2_score(y, y_pred)

                # Format persamaan
                terms = [f"{coef[i]:+.2f}x^{order - i}" if i < order else f"{coef[i]:+.2f}"
                         for i in range(order + 1)]
                equation = " ".join(terms).replace('x^1', 'x').replace('x^0', '')

                # Plot garis
                x_line = np.linspace(min(x), max(x), 200)
                y_line = poly_func(x_line)
                ax.plot(x_line, y_line, label=f"Orde {order}: {equation} | R²={r2:.4f}",
                        color=colors[idx % len(colors)], linestyle='--')

            ax.set_xlabel("X")
            ax.set_ylabel("Y")
            ax.set_title("Regresi Polinomial dari Tabel Data")
            ax.grid(True)
            ax.legend()
            st.pyplot(fig)
        else:
            st.info("Silakan pilih setidaknya satu orde regresi.")

    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")
else:
    st.warning("Masukkan setidaknya dua pasang data numerik di kolom X dan Y.")
