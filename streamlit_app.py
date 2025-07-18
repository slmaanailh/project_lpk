import streamlit as st
import pandas as pd
import math

st.set_page_config(page_title="Penentu Orde Reaksi", layout="wide")
st.title("🧪 Penentuan Orde Reaksi - Step by Step Wizard")

# Langkah 1: Input Data
data_default = pd.DataFrame({
    '[A] (M)': [0.4, 0.8, 0.8],
    '[B] (M)': [0.2, 0.2, 0.8],
    'Laju (v)': [10, 20, 40],
})

# Tambahkan nomor urut (1, 2, 3,...)
data_default.insert(0, "No", range(1, len(data_default) + 1))

st.header("1️⃣ Masukkan Data Percobaan")
st.write("Silakan masukkan konsentrasi reaktan dan laju reaksi.")

data = st.data_editor(data_default, num_rows="dynamic", use_container_width=True, key="data_input")

if len(data) < 2:
    st.warning("Masukkan minimal 2 baris data untuk melanjutkan.")
    st.stop()

# Ambil daftar nomor "No"
nomor_baris = data["No"].tolist()

# Langkah 2: Pilih dua baris untuk orde terhadap A
st.header("2️⃣ Pilih Data untuk Menentukan Orde terhadap A")
st.markdown("Pilih dua nomor baris **dengan nilai [B] yang sama**")

pair_A = st.multiselect("Pilih dua nomor baris:", nomor_baris, default=[1, 2], key="select_pair_A")

x = None
if len(pair_A) == 2:
    idx1, idx2 = sorted(pair_A)
    d1 = data[data["No"] == idx1].iloc[0]
    d2 = data[data["No"] == idx2].iloc[0]

    if d1['[B] (M)'] != d2['[B] (M)']:
        st.error("Nilai [B] harus sama untuk menentukan orde terhadap A.")
    else:
        st.header("3️⃣ Rumus Orde terhadap A")
        st.latex(r"\frac{v_2}{v_1} = \left( \frac{[A]_2}{[A]_1} \right)^x")

        v1, v2 = d1['Laju (v)'], d2['Laju (v)']
        A1, A2 = d1['[A] (M)'], d2['[A] (M)']

        ratio_v = max(v1, v2) / min(v1, v2)
        ratio_A = max(A1, A2) / min(A1, A2)

        try:
            st.markdown("Substitusi ke dalam rumus:")
            st.latex(rf"\frac{{{max(v1,v2)}}}{{{min(v1,v2)}}} = \left( \frac{{{max(A1,A2)}}}{{{min(A1,A2)}}} \right)^x")

            x_value = math.log(ratio_v) / math.log(ratio_A)
            x = round(x_value, 2)

            st.success(f"Orde reaksi terhadap A adalah x = {x} (hasil asli: {x_value:.4f})")
        except Exception as e:
            st.error(f"Terjadi kesalahan dalam perhitungan orde terhadap A: {e}")

# Langkah 4: Pilih dua baris untuk orde terhadap B
st.divider()
st.header("4️⃣ Pilih Data untuk Menentukan Orde terhadap B")
st.markdown("Pilih dua nomor baris **dengan nilai [A] yang sama**")

pair_B = st.multiselect("Pilih dua nomor baris:", nomor_baris, default=[1, 3], key="select_pair_B")

y = None
if len(pair_B) == 2:
    idx1, idx2 = sorted(pair_B)
    d1 = data[data["No"] == idx1].iloc[0]
    d2 = data[data["No"] == idx2].iloc[0]

    if d1['[A] (M)'] != d2['[A] (M)']:
        st.error("Nilai [A] harus sama untuk menentukan orde terhadap B.")
    else:
        st.header("5️⃣ Rumus Orde terhadap B")
        st.latex(r"\frac{v_2}{v_1} = \left( \frac{[B]_2}{[B]_1} \right)^y")

        v1, v2 = d1['Laju (v)'], d2['Laju (v)']
        B1, B2 = d1['[B] (M)'], d2['[B] (M)']

        ratio_v = max(v1, v2) / min(v1, v2)
        ratio_B = max(B1, B2) / min(B1, B2)

        try:
            st.markdown("Substitusi ke dalam rumus:")
            st.latex(rf"\frac{{{max(v1,v2)}}}{{{min(v1,v2)}}} = \left( \frac{{{max(B1,B2)}}}{{{min(B1,B2)}}} \right)^y")

            y_value = math.log(ratio_v) / math.log(ratio_B)
            y = round(y_value, 2)

            st.success(f"Orde reaksi terhadap B adalah y = {y} (hasil asli: {y_value:.4f})")
        except Exception as e:
            st.error(f"Terjadi kesalahan dalam perhitungan orde terhadap B: {e}")

# Orde total reaksi
if x is not None and y is not None:
    st.divider()
    st.header("📊 Orde Total Reaksi")
    total = x + y
    st.success(f"🔢 Orde total reaksi adalah x + y = {x} + {y} = {total}")
    st.info(f"📘 Persamaan laju reaksi: v = k [A]^{x} [B]^{y}")
