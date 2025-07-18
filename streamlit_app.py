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

# Tambahkan kolom No
data_default.insert(0, "No", range(1, len(data_default) + 1))
st.header("1️⃣ Masukkan Data Percobaan")
st.write("Silakan masukkan konsentrasi reaktan dan laju reaksi dari beberapa eksperimen.")

data = st.data_editor(data_default, num_rows="dynamic", use_container_width=True, key="data_input")

if len(data) < 2:
    st.warning("Masukkan minimal 2 baris data untuk melanjutkan.")
    st.stop()

# Langkah 2: Pilih data untuk menentukan orde terhadap A
st.header("2️⃣ Pilih Baris untuk Menentukan Orde terhadap A")
st.markdown("Pilih dua baris *dengan nilai B yang sama*")

row_numbers = data["No"].tolist()
pair_A = st.multiselect("Pilih dua nomor baris (sesuai kolom 'No'):", row_numbers, default=[1, 2], key="select_pair_A")

x = None
if len(pair_A) == 2:
    # Cari indeks berdasarkan nomor 'No'
    idx1 = data.index[data["No"] == pair_A[0]][0]
    idx2 = data.index[data["No"] == pair_A[1]][0]
    d1, d2 = data.loc[idx1], data.loc[idx2]

    if d1['[B] (M)'] != d2['[B] (M)']:
        st.error("Nilai B harus sama untuk menentukan orde terhadap A")
    else:
        st.header("3️⃣ Rumus Lengkap untuk Orde terhadap A")
        st.latex(r"\frac{v_2}{v_1} = \left( \frac{[A]_2}{[A]_1} \right)^x")

        st.header("4️⃣ Masukkan Angka ke dalam Rumus")
        A1, A2 = d1['[A] (M)'], d2['[A] (M)']
        v1, v2 = d1['Laju (v)'], d2['Laju (v)']

        # Koreksi otomatis: gunakan pembagian besar/kecil
        ratio_v = max(v1, v2) / min(v1, v2)
        ratio_A = max(A1, A2) / min(A1, A2)

        st.markdown("Substitusi:")
        st.latex(f"\\frac{{{max(v1, v2)}}}{{{min(v1, v2)}}} = \\left( \\frac{{{max(A1, A2)}}}{{{min(A1, A2)}}} \\right)^x")

        try:
            x_value = math.log(ratio_v) / math.log(ratio_A)
            x = round(x_value, 2)
            st.success(f"6️⃣ Orde reaksi terhadap A adalah x = {x}")
        except:
            st.error("Terjadi kesalahan dalam perhitungan orde terhadap A.")

# Langkah 7-11: Ulangi untuk B
st.divider()
st.header("7️⃣ Pilih Baris untuk Menentukan Orde terhadap B")
st.markdown("Pilih dua baris *dengan nilai A yang sama*")

pair_B = st.multiselect("Pilih dua nomor baris (sesuai kolom 'No'):", row_numbers, default=[1, 3], key="select_pair_B")

y = None
if len(pair_B) == 2:
    idx1 = data.index[data["No"] == pair_B[0]][0]
    idx2 = data.index[data["No"] == pair_B[1]][0]
    d1, d2 = data.loc[idx1], data.loc[idx2]

    if d1['[A] (M)'] != d2['[A] (M)']:
        st.error("Nilai A harus sama untuk menentukan orde terhadap B")
    else:
        st.header("8️⃣ Rumus Lengkap untuk Orde terhadap B")
        st.latex(r"\frac{v_2}{v_1} = \left( \frac{[B]_2}{[B]_1} \right)^y")

        st.header("9️⃣ Masukkan Angka ke dalam Rumus")
        B1, B2 = d1['[B] (M)'], d2['[B] (M)']
        v1, v2 = d1['Laju (v)'], d2['Laju (v)']

        ratio_v = max(v1, v2) / min(v1, v2)
        ratio_B = max(B1, B2) / min(B1, B2)

        st.markdown("Substitusi:")
        st.latex(f"\\frac{{{max(v1, v2)}}}{{{min(v1, v2)}}} = \\left( \\frac{{{max(B1, B2)}}}{{{min(B1, B2)}}} \\right)^y")

        try:
            y_value = math.log(ratio_v) / math.log(ratio_B)
            y = round(y_value, 2)
            st.success(f"🔟 Orde reaksi terhadap B adalah y = {y}")
        except:
            st.error("Terjadi kesalahan dalam perhitungan orde terhadap B.")

# Orde total
if x is not None and y is not None:
    st.divider()
    st.header("📊 Orde Total Reaksi")
    st.success(f"🔢 Orde total reaksi adalah x + y = {x} + {y} = {round(x + y, 2)}")
