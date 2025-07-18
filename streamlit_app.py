import streamlit as st
import pandas as pd
import numpy as np
import math

st.set_page_config(page_title="Penentu Orde Reaksi", layout="wide")

st.title("🧪 Penentuan Orde Reaksi - Step by Step Wizard")

# Langkah 1: Input Data
data_default = pd.DataFrame({
    '[A] (M)': [0.4, 0.8, 0.8],
    '[B] (M)': [0.2, 0.2, 0.8],
    'Laju (v)': [10, 20, 40],
})

st.header("1️⃣ Masukkan Data Percobaan")
st.write("Silakan masukkan konsentrasi reaktan dan laju reaksi dari beberapa eksperimen.")
data = st.data_editor(data_default, num_rows="dynamic", use_container_width=True, key="data_input")

# Validasi minimal 2 baris
if len(data) < 2:
    st.warning("Masukkan minimal 2 baris data untuk melanjutkan.")
    st.stop()

# Langkah 2: Pilih data untuk menentukan orde terhadap A
st.header("2️⃣ Pilih Data untuk Menentukan Orde terhadap A")
st.markdown("Untuk menentukan orde reaksi terhadap A, pilih dua baris **dengan nilai B yang sama**")

options = data.index.tolist()
pair_A = st.multiselect("Pilih dua baris data:", options, default=[0, 1], key="select_pair_A")

# Lanjut jika dua baris dipilih
if len(pair_A) == 2:
    d1, d2 = data.loc[pair_A[0]], data.loc[pair_A[1]]
    if d1['[B] (M)'] != d2['[B] (M)']:
        st.error("Nilai B harus sama untuk menentukan orde terhadap A")
    else:
        st.header("3️⃣ Rumus untuk Orde terhadap A")
        st.latex(r"\frac{v_2}{v_1} = \left( \frac{[A]_2}{[A]_1} \right)^x")

        st.header("4️⃣ Masukkan Angka ke dalam Rumus")
        v1, v2 = d1['Laju (v)'], d2['Laju (v)']
        A1, A2 = d1['[A] (M)'], d2['[A] (M)']

        try:
            ratio_v = v2 / v1
            ratio_A = A2 / A1
            x = round(math.log(ratio_v) / math.log(ratio_A), 2)

            st.latex(f"\\frac{{{v2}}}{{{v1}}} = (\\frac{{{A2}}}{{{A1}}})^x")
            st.success(f"Orde reaksi terhadap A adalah x = {x}")
        except:
            st.error("Terjadi kesalahan dalam perhitungan. Periksa kembali datanya.")

# Langkah 5: Ulangi untuk B
st.divider()
st.header("5️⃣ Pilih Data untuk Menentukan Orde terhadap B")
st.markdown("Untuk menentukan orde reaksi terhadap B, pilih dua baris **dengan nilai A yang sama**")

pair_B = st.multiselect("Pilih dua baris data:", options, default=[0, 2], key="select_pair_B")

if len(pair_B) == 2:
    d1, d2 = data.loc[pair_B[0]], data.loc[pair_B[1]]
    if d1['[A] (M)'] != d2['[A] (M)']:
        st.error("Nilai A harus sama untuk menentukan orde terhadap B")
    else:
        st.latex(r"\frac{v_2}{v_1} = \left( \frac{[B]_2}{[B]_1} \right)^y")
        v1, v2 = d1['Laju (v)'], d2['Laju (v)']
        B1, B2 = d1['[B] (M)'], d2['[B] (M)']

        try:
            ratio_v = v2 / v1
            ratio_B = B2 / B1
            y = round(math.log(ratio_v) / math.log(ratio_B), 2)

            st.latex(f"\\frac{{{v2}}}{{{v1}}} = (\\frac{{{B2}}}{{{B1}}})^y")
            st.success(f"Orde reaksi terhadap B adalah y = {y}")

            total = x + y if 'x' in locals() else '...'  # Orde total jika x sudah dihitung
            if isinstance(total, (int, float)):
                st.info(f"**Orde total reaksi adalah {total}**")
        except:
            st.error("Terjadi kesalahan dalam perhitungan. Periksa kembali datanya.")
