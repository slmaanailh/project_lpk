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
