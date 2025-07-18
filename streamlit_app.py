import streamlit as st
import pandas as pd
import numpy as np

# ====== SIDEBAR MENU ======
menu = st.sidebar.radio(
    "Pilih Menu",
    ["Home", "Input Data & Hitung Orde", "Tentang Aplikasi"]
)

st.title("📘 Aplikasi Penentu Orde Reaksi")

# ====== MENU: HOME ======
if menu == "Home":
    st.subheader("📊 Selamat datang di Aplikasi Penentu Orde Reaksi")
    st.markdown("""
    Aplikasi ini digunakan untuk menganalisis data eksperimen reaksi kimia dan menentukan:
    - Orde reaksi masing-masing reaktan
    - Orde total reaksi
    """)
    st.info("Gunakan menu di sebelah kiri untuk berpindah halaman.")

# ====== MENU: HITUNG ORDE ======
elif menu == "Input Data & Hitung Orde":
    st.subheader("🧪 Input Data & Hitung Orde Reaksi")

    # Input nama kolom
    col1 = st.text_input("Nama kolom reaktan 1", '[CHCl3] (M)')
    col2 = st.text_input("Nama kolom reaktan 2", '[Cl2] (M)')
    col3 = st.text_input("Nama kolom laju reaksi", 'Laju Reaksi (M/s)')

    # Tabel input
    default_data = pd.DataFrame({
        col1: [0.4, 0.8, 0.8],
        col2: [0.2, 0.2, 0.8],
        col3: [10, 20, 40]
    })

    data = st.data_editor(
        default_data,
        num_rows="dynamic",
        use_container_width=True
    )

    # Hitung orde jika data valid
    if len(data) >= 3:
        try:
            A = np.array(data[col1], dtype=float)
            B = np.array(data[col2], dtype=float)
            rate = np.array(data[col3], dtype=float)

            orde_A = np.log(rate[1]/rate[0]) / np.log(A[1]/A[0])
            orde_B = np.log(rate[2]/rate[1]) / np.log(B[2]/B[1])
            total = orde_A + orde_B

            st.success("✅ Hasil:")
            st.write(f"🔹 Orde terhadap {col1} = {orde_A:.2f}")
            st.write(f"🔹 Orde terhadap {col2} = {orde_B:.2f}")
            st.write(f"📘 **Orde total = {total:.2f}**")
        except:
            st.error("Pastikan semua data valid dan tidak kosong.")
    else:
        st.warning("Masukkan minimal 3 baris data!")

# ====== MENU: TENTANG ======
elif menu == "Tentang Aplikasi":
    st.subheader("ℹ️ Tentang Aplikasi")
    st.markdown("""
    **Aplikasi Penentu Orde Reaksi Kimia**  
    Dibuat menggunakan Python + Streamlit.  
    Cocok untuk digunakan dalam praktikum kimia fisika atau kinetika.

    **Fitur:**
    - Input data tabel eksperimen
    - Penentuan orde reaksi otomatis
    - Menu navigasi interaktif
    """)
    st.caption("Dikembangkan oleh: [Nama Kamu]")

