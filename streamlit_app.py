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

# Validasi dan ekstrak X, Y
if len(data.dropna()) >= 2:
    try:
        x = data['X'].astype(float).to_numpy()
        y = data['Y'].astype(float).to_numpy()

        # Pilih ordo regresi (bisa lebih dari satu, termasuk orde 0)
        selected_orders = st.multiselect("Pilih orde regresi yang ingin ditampilkan", options=list(range(0, 6)), default=[0, 1, 2])

        if selected_orders:
            fig, ax = plt.subplots(figsize=(10,6))
            except Exception as e:
    st.error(f"Terjadi kesalahan: {e}")
