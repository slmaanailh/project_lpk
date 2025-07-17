import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score
import re
from io import BytesIO

st.set_page_config(page_title="Regresi Polinomial Interaktif", layout="centered")
st.title("📈 Regresi Polinomial dan Korelasi dari Tabel Data")

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

if len(data.dropna()) >= 2:
    try:
        x = data['X'].astype(float).to_numpy()
        y = data['Y'].astype(float).to_numpy()

        selected_orders = st.multiselect("Pilih orde regresi:", options=list(range(0, 6)), default=[0, 1, 2])

        # Plot
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.scatter(x, y, label='Data', color='black', s=80, edgecolors='white', linewidths=0.5)

        result_table = []
        for order in selected_orders:
            coef = np.polyfit(x, y, order)
            poly_func = np.poly1d(coef)
            y_pred = poly_func(x)
            r2 = r2_score(y, y_pred)

            label = f"Orde {order}: y = {poly_func} | R² = {r2:.4f}"
            ax.plot(x, y_pred, label=label, linewidth=2.5)

            eq = re.sub(r"\n", " ", str(poly_func))
            latex_eq = poly_func.__str__().replace("\n", " ").replace("**", "^")
            result_table.append({
                "Orde": order,
                "Persamaan": eq,
                "R²": round(r2, 4),
                "LaTeX": f"${latex_eq}$"
            })

        ax.set_xlabel("X", fontsize=12)
        ax.set_ylabel("Y", fontsize=12)
        ax.set_title("Grafik Regresi Polinomial", fontsize=16)
        ax.grid(True, linestyle='--', alpha=0.5)
        ax.legend()
        st.pyplot(fig)

        st.markdown("---")
        st.markdown("### 📊 Hasil Regresi:")
        st.table(pd.DataFrame(result_table).drop(columns=["LaTeX"]))

        st.markdown("### 🧮 Persamaan Regresi (LaTeX View):")
        for row in result_table:
            st.latex(row["LaTeX"])

        # Ekspor ke Excel
        df_result = pd.DataFrame(result_table).drop(columns=["LaTeX"])
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df_result.to_excel(writer, index=False, sheet_name='Hasil Regresi')
            writer.save()
        st.download_button(
            label="📥 Unduh Hasil sebagai Excel",
            data=output.getvalue(),
            file_name="hasil_regresi.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        st.info("Gunakan multiselect di atas untuk memilih beberapa orde regresi sekaligus.")

    except Exception as e:
        st.error(f"Terjadi kesalahan saat memproses data: {e}")
else:
    st.warning("Masukkan setidaknya dua pasang data X dan Y untuk memulai analisis.")
