import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config("Wizard Orde Reaksi", layout="centered")

# Inisialisasi langkah
if 'step' not in st.session_state:
    st.session_state.step = 1

# ====================
# LANGKAH 1: INPUT TABEL
# ====================
if st.session_state.step == 1:
    st.title("🧪 Langkah 1: Input Data Eksperimen")

    default_data = pd.DataFrame({
        '[A]': [0.1, 0.1, 0.2],
        '[B]': [0.1, 0.2, 0.2],
        'v (laju reaksi)': [0.02, 0.08, 0.16]
    })

    data = st.data_editor(default_data, num_rows="dynamic", use_container_width=True, key="tabel_data")

    if len(data) >= 3:
        st.session_state.data = data
        st.button("➡️ Lanjut ke Langkah 2", on_click=lambda: st.session_state.__setitem__('step', 2))

# ====================
# LANGKAH 2: PILIH DATA UNTUK PERHITUNGAN
# ====================
elif st.session_state.step == 2:
    st.title("🧮 Langkah 2: Pilih Pasangan Baris untuk Hitung Orde")

    df = st.session_state.data

    st.subheader("🔹 Pilih dua baris untuk mencari orde terhadap [A] (dengan [B] tetap)")
    rows_A = st.multiselect("Pilih 2 baris (misalnya: baris 2 dan 3)", options=list(df.index), key="rows_A")

    st.subheader("🔹 Pilih dua baris untuk mencari orde terhadap [B] (dengan [A] tetap)")
    rows_B = st.multiselect("Pilih 2 baris (misalnya: baris 1 dan 2)", options=list(df.index), key="rows_B")

    if len(rows_A) == 2 and len(rows_B) == 2:
        st.session_state.rows_A = rows_A
        st.session_state.rows_B = rows_B
        st.button("➡️ Lanjut ke Langkah 3", on_click=lambda: st.session_state.__setitem__('step', 3))

    st.button("⬅️ Kembali ke Langkah 1", on_click=lambda: st.session_state.__setitem__('step', 1))

# ====================
# LANGKAH 3: TAMPILKAN RUMUS & HASIL
# ====================
elif st.session_state.step == 3:
    st.title("📊 Langkah 3: Hasil Perhitungan Orde Reaksi")

    df = st.session_state.data
    A = df['[A]'].values
    B = df['[B]'].values
    v = df['v (laju reaksi)'].values

    i, j = st.session_state.rows_A
    x = np.log(v[j]/v[i]) / np.log(A[j]/A[i])

    m, n = st.session_state.rows_B
    y = np.log(v[n]/v[m]) / np.log(B[n]/B[m])

    orde_total = x + y

    # Tampilkan langkah dengan LaTeX
    st.subheader("📘 Rumus Umum:")
    st.latex(r"v = k [A]^x [B]^y")

    st.subheader(f"🔢 Hitung Orde terhadap [A] (baris {i+1} & {j+1}):")
    st.latex(fr"""
        \frac{{v_{j+1}}}{{v_{i+1}}} = 
        \left( \frac{{[A]_{j+1}}}{{[A]_{i+1}}} \right)^x \Rightarrow 
        x = \frac{{\log({v[j]:.3f}/{v[i]:.3f})}}{{\log({A[j]:.3f}/{A[i]:.3f})}} = {x:.2f}
    """)

    st.subheader(f"🔢 Hitung Orde terhadap [B] (baris {m+1} & {n+1}):")
    st.latex(fr"""
        \frac{{v_{n+1}}}{{v_{m+1}}} = 
        \left( \frac{{[B]_{n+1}}}{{[B]_{m+1}}} \right)^y \Rightarrow 
        y = \frac{{\log({v[n]:.3f}/{v[m]:.3f})}}{{\log({B[n]:.3f}/{B[m]:.3f})}} = {y:.2f}
    """)

    st.success(f"✅ Orde Reaksi Total: {x:.2f} + {y:.2f} = {orde_total:.2f}")

    # Tombol Navigasi
    st.button("⬅️ Ulangi Pilihan", on_click=lambda: st.session_state.__setitem__('step', 2))
    st.button("🔁 Ulang dari Awal", on_click=lambda: st.session_state.__setitem__('step', 1))
