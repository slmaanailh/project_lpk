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

if len(data) < 2:
    st.warning("Masukkan minimal 2 baris data untuk melanjutkan.")
    st.stop()

# Langkah 2: Pilih data untuk menentukan orde terhadap A
st.header("2️⃣ Pilih Data untuk Menentukan Orde terhadap A")
st.markdown("Untuk menentukan orde reaksi terhadap A, pilih dua baris **dengan nilai B yang sama**")

options = data.index.tolist()
pair_A = st.multiselect("Pilih dua baris data:", options, default=[0, 1], key="select_pair_A")

if len(pair_A) == 2:
    d1, d2 = data.loc[pair_A[0]], data.loc[pair_A[1]]
    if d1['[B] (M)'] != d2['[B] (M)']:
        st.error("Nilai B harus sama untuk menentukan orde terhadap A")
    else:
        st.header("3️⃣ Rumus Lengkap untuk Orde terhadap A")
        st.latex(r"\frac{v_2}{v_1} = \left( \frac{[A]_2}{[A]_1} \right)^x \left( \frac{[B]_2}{[B]_1} \right)^y")

        st.header("4️⃣ Masukkan Angka ke dalam Rumus")
        v1, v2 = d1['Laju (v)'], d2['Laju (v)']
        A1, A2 = d1['[A] (M)'], d2['[A] (M)']
        B1, B2 = d1['[B] (M)'], d2['[B] (M)']

        try:
            st.markdown(f"Substitusi ke dalam persamaan:")
            st.latex(f"\\frac{{{v2}}}{{{v1}}} = (\\frac{{{A2}}}{{{A1}}})^x \, (\\frac{{{B2}}}{{{B1}}})^y")
            st.markdown("Bagian B yang dicoret karena B sama:")
            st.latex(rf"\frac{{{v2}}}{{{v1}}} = \left( \frac{{{A2}}}{{{A1}}} \right)^x \cancel{{\left( \frac{{{B2}}}{{{B1}}} \right)^y}}")

            ratio_v = v2 / v1
            ratio_A = A2 / A1
            x_value = math.log(ratio_v) / math.log(ratio_A)
            x = round(x_value)

            st.success(f"6️⃣ Orde reaksi terhadap A adalah x = {x}")
        except:
            st.error("Terjadi kesalahan dalam perhitungan orde terhadap A.")

# Langkah 7-11: Ulangi untuk B
st.divider()
st.header("7️⃣ Pilih Data untuk Menentukan Orde terhadap B")
st.markdown("Untuk menentukan orde reaksi terhadap B, pilih dua baris **dengan nilai A yang sama**")

pair_B = st.multiselect("Pilih dua baris data:", options, default=[0, 2], key="select_pair_B")

if len(pair_B) == 2:
    d1, d2 = data.loc[pair_B[0]], data.loc[pair_B[1]]
    if d1['[A] (M)'] != d2['[A] (M)']:
        st.error("Nilai A harus sama untuk menentukan orde terhadap B")
    else:
        st.header("8️⃣ Rumus Lengkap untuk Orde terhadap B")
        st.latex(r"\frac{v_2}{v_1} = \left( \frac{[A]_2}{[A]_1} \right)^x \left( \frac{[B]_2}{[B]_1} \right)^y")

        st.header("9️⃣ Masukkan Angka ke dalam Rumus")
        v1, v2 = d1['Laju (v)'], d2['Laju (v)']
        A1, A2 = d1['[A] (M)'], d2['[A] (M)']
        B1, B2 = d1['[B] (M)'], d2['[B] (M)']

        try:
            st.markdown(f"Substitusi ke dalam persamaan:")
            st.latex(f"\\frac{{{v2}}}{{{v1}}} = (\\frac{{{A2}}}{{{A1}}})^x \, (\\frac{{{B2}}}{{{B1}}})^y")
            st.markdown("Bagian A yang dicoret karena A sama:")
            st.latex(rf"\frac{{{v2}}}{{{v1}}} = \cancel{{\left( \frac{{{A2}}}{{{A1}}} \right)^x}} \left( \frac{{{B2}}}{{{B1}}} \right)^y")

            ratio_v = v2 / v1
            ratio_B = B2 / B1
            y_value = math.log(ratio_v) / math.log(ratio_B)
            y = round(y_value)

            st.success(f"11️⃣ Orde reaksi terhadap B adalah y = {y}")

            if 'x' in locals():
                st.info(f"🔢 Orde total reaksi adalah {x + y}")
        except:
            st.error("Terjadi kesalahan dalam perhitungan orde terhadap B.")
