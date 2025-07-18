import streamlit as st
import pandas as pd
import numpy as np
import math
from fractions import Fraction

st.set_page_config(page_title="Penentu Orde Reaksi", layout="wide")
st.title("🧪 Penentuan Orde Reaksi - Step by Step Wizard")

# Langkah 1: Input Data
data_default = pd.DataFrame({
    '[A] (M)': [0.4, 0.8, 0.8],
    '[B] (M)': [0.2, 0.2, 0.8],
    'Laju (v)': [10, 20, 40],
})

data_default.index = range(1, len(data_default) + 1)

st.header("1️⃣ Masukkan Data Percobaan")
st.write("Silakan masukkan konsentrasi reaktan dan laju reaksi dari beberapa eksperimen.")

styled_data = data_default.copy()
styled_data.insert(0, "No", range(1, len(styled_data)+1))
data = st.data_editor(styled_data, num_rows="dynamic", use_container_width=True, key="data_input")

if len(data) < 2:
    st.warning("Masukkan minimal 2 baris data untuk melanjutkan.")
    st.stop()

# Langkah 2: Pilih data untuk menentukan orde terhadap A
st.header("2️⃣ Pilih Data untuk Menentukan Orde terhadap A")
st.markdown("Untuk menentukan orde reaksi terhadap A, pilih dua baris **dengan nilai B yang sama**")
options = list(data['No'])
pair_A = st.multiselect("Pilih dua nomor baris data:", options, default=[1, 2], key="select_pair_A")

x = None
if len(pair_A) == 2:
    d1, d2 = data[data['No'] == pair_A[0]].iloc[0], data[data['No'] == pair_A[1]].iloc[0]
    if d1['[B] (M)'] != d2['[B] (M)']:
        st.error("Nilai B harus sama untuk menentukan orde terhadap A")
    else:
        st.header("3️⃣ Rumus Lengkap untuk Orde terhadap A")
        st.latex(r"\frac{v_2}{v_1} = \left( \frac{[A]_2}{[A]_1} \right)^x \left( \frac{[B]_2}{[B]_1} \right)^y")

        st.header("4️⃣ Masukkan Angka ke dalam Rumus")
        v1, v2 = d1['Laju (v)'], d2['Laju (v)']
        A1, A2 = d1['[A] (M)'], d2['[A] (M)']

        try:
            if any(val in [0, None, ''] for val in [v1, v2, A1, A2]):
                st.error("Nilai [A] dan Laju (v) tidak boleh nol atau kosong.")
                st.stop()

            ratio_v = Fraction(v2, v1)
            ratio_A = Fraction(A2, A1)

            if float(ratio_v) <= 0 or float(ratio_A) <= 0:
                st.error("Rasio tidak boleh negatif atau nol untuk logaritma.")
                st.stop()

            st.markdown(f"Substitusi ke dalam persamaan:")
            st.latex(f"\\frac{{{ratio_v.numerator}}}{{{ratio_v.denominator}}} = (\\frac{{{ratio_A.numerator}}}{{{ratio_A.denominator}}})^x")

            x_value = math.log(float(ratio_v)) / math.log(float(ratio_A))
            x = round(x_value, 2)

            st.markdown(f"Langkah logaritma untuk x:")
            st.latex(rf"x = \frac{{\log({float(ratio_v):.2f})}}{{\log({float(ratio_A):.2f})}}")

            st.success(f"6️⃣ Orde reaksi terhadap A adalah x = {x}")

            with st.expander("🔍 Debug info"):
                st.write(f"v1 = {v1}, v2 = {v2}, A1 = {A1}, A2 = {A2}")
                st.write(f"ratio_v = {float(ratio_v):.4f}, ratio_A = {float(ratio_A):.4f}")
        except Exception as e:
            st.error(f"Terjadi kesalahan dalam perhitungan orde terhadap A: {e}")

# Langkah 7-11: Ulangi untuk B
st.divider()
st.header("7️⃣ Pilih Data untuk Menentukan Orde terhadap B")
st.markdown("Untuk menentukan orde reaksi terhadap B, pilih dua baris **dengan nilai A yang sama**")
pair_B = st.multiselect("Pilih dua nomor baris data:", options, default=[1, 3], key="select_pair_B")

y = None
if len(pair_B) == 2:
    d1, d2 = data[data['No'] == pair_B[0]].iloc[0], data[data['No'] == pair_B[1]].iloc[0]
    if d1['[A] (M)'] != d2['[A] (M)']:
        st.error("Nilai A harus sama untuk menentukan orde terhadap B")
    else:
        st.header("8️⃣ Rumus Lengkap untuk Orde terhadap B")
        st.latex(r"\frac{v_2}{v_1} = \left( \frac{[A]_2}{[A]_1} \right)^x \left( \frac{[B]_2}{[B]_1} \right)^y")

        st.header("9️⃣ Masukkan Angka ke dalam Rumus")
        v1, v2 = d1['Laju (v)'], d2['Laju (v)']
        B1, B2 = d1['[B] (M)'], d2['[B] (M)']

        try:
            if any(val in [0, None, ''] for val in [v1, v2, B1, B2]):
                st.error("Nilai [B] dan Laju (v) tidak boleh nol atau kosong.")
                st.stop()

            ratio_v = Fraction(v2, v1)
            ratio_B = Fraction(B2, B1)

            if float(ratio_v) <= 0 or float(ratio_B) <= 0:
                st.error("Rasio tidak boleh negatif atau nol untuk logaritma.")
                st.stop()

            st.markdown(f"Substitusi ke dalam persamaan:")
            st.latex(f"\\frac{{{ratio_v.numerator}}}{{{ratio_v.denominator}}} = (\\frac{{{ratio_B.numerator}}}{{{ratio_B.denominator}}})^y")

            y_value = math.log(float(ratio_v)) / math.log(float(ratio_B))
            y = round(y_value, 2)

            st.markdown(f"Langkah logaritma untuk y:")
            st.latex(rf"y = \frac{{\log({float(ratio_v):.2f})}}{{\log({float(ratio_B):.2f})}}")

            st.success(f"11️⃣ Orde reaksi terhadap B adalah y = {y}")

            with st.expander("🔍 Debug info"):
                st.write(f"v1 = {v1}, v2 = {v2}, B1 = {B1}, B2 = {B2}")
                st.write(f"ratio_v = {float(ratio_v):.4f}, ratio_B = {float(ratio_B):.4f}")
        except Exception as e:
            st.error(f"Terjadi kesalahan dalam perhitungan orde terhadap B: {e}")

# Langkah akhir: Orde total & konstanta k
if x is not None and y is not None:
    st.divider()
    st.header("📊 Orde Total Reaksi")
    total_order = round(x + y, 2)
    st.success(f"🔢 Orde total reaksi adalah x + y = {x} + {y} = {total_order}")

    # Hitung k dari baris 1
    d = data.iloc[0]
    A, B, v = d['[A] (M)'], d['[B] (M)'], d['Laju (v)']
    try:
        k = v / ((A ** x) * (B ** y))
        k = round(k, 4)
        st.info(f"📌 Konstanta laju reaksi (k) dihitung dari baris 1: k = {k}")
    except:
        st.warning("Gagal menghitung konstanta laju k. Pastikan tidak ada nilai nol.")

    # Ringkasan akhir
    st.markdown("### 📘 Ringkasan Akhir")
    st.markdown(f"""
    - Orde terhadap A = **{x}**
    - Orde terhadap B = **{y}**
    - Orde total = **{total_order}**
    - Persamaan laju: **v = {k} × [A]<sup>{x}</sup> × [B]<sup>{y}</sup>**
    """, unsafe_allow_html=True)
