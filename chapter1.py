import streamlit as st
import time
import sympy as sp
import matplotlib.pyplot as plt
import numpy as np

def load_html_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()
 
def main():
    st.markdown("# Halaman Utama 🎈")
    st.sidebar.markdown("# Metode Tabel 🎈")

    
    N = st.number_input("Masukkan Maks Iterasi", min_value=1, max_value=100)
    bawah = st.number_input("Masukkan Batas Bawah")
    atas = st.number_input("Masukkan Batas Atas")

    h = float((atas - bawah) / N)
    st.write(f"Batas bawah adalah {bawah}, batas atas adalah {atas}, dan batas maksimum iterasi adalah {N}")
    st.write(f"H = {h}")

    with st.form("Metode tabel"):
        input_string = st.text_input("Masukkan fungsi f(x): ")
        submit_button = st.form_submit_button("Hitung")

    if input_string and submit_button:
        process_input(input_string, bawah, atas, N, h)

def process_input(input_string, bawah, atas, N, h):
    x = sp.symbols('x' or 'X')
    try:
        exp = sp.sympify(input_string)
    except (sp.SympifyError, ValueError) as e:
        st.error(f"Error parsing input string: {e}")
        return

    def f(xA):
        f_sympy = sp.lambdify(x, exp)
        return f_sympy(xA)

    st.write("Memulai Metode Tabel...")
    latest_iteration = st.empty()
    bar = st.progress(0)

    x_array, fx1_array, fx2_array, fx3_array = [], [], [], []
    hasil = None

    for i in range(1, N + 1):
        latest_iteration.text(f'Iterasi {i}')
        x_val = bawah + (i * h)
        fx1 = f(x_val)
        fx2 = f(bawah + ((i + 1) * h))
        fx3 = fx1 * fx2
        x_array.append(x_val)
        fx1_array.append(fx1)
        fx2_array.append(fx2)
        fx3_array.append(fx3)

        if fx1 == 0:
            hasil = x_val
        elif fx1 * fx2 < 0:
            hasil = x_val if abs(fx1) < abs(fx2) else x_val + h

        display_iteration(i, x_val, fx1, fx2, fx3)
        bar.progress(i / N)
        time.sleep(0.3) 

    if hasil is not None:
        st.success(f"Akar ditemukan pada x = {hasil:.4f}")
    else:
        st.warning("Akar tidak ditemukan dalam batas iterasi yang diberikan.")

    st.write("...Selesai...")

    
    fig, ax = plt.subplots()
    ax.set_xlabel('Iterasi')
    ax.set_ylabel('f(x)')
    ax.set_title(f'Plot Titik f(x), f(x+h) - Jumlah Iterasi: {N}')
    ax.axhline(0, color='black', linewidth=0.5)
    ax.plot(range(1, N + 1), np.abs(fx1_array), 'bo', label='f(x)')
    ax.plot(range(1, N + 1), np.abs(fx2_array), 'gx', label='f(x+h)')
    ax.legend()

    st.pyplot(fig)

def display_iteration(i, x_val, fx1, fx2, fx3):
    st.markdown(
        f"""
        <div style='background-color: #f0f0f0; padding: 10px; border-radius: 5px; margin-bottom: 10px;'>
            <strong style='color: #ff6347;'>Iterasi {i}</strong> | 
            <span style='color: #4682b4;'>Akar: {x_val:.4f}</span> | 
            <span style='color: #32cd32;'>f(x): {fx1:.4f}</span> | 
            <span style='color: #ffa500;'>f(x+h): {fx2:.4f}</span> | 
            <span style='color: #8a2be2;'>f(x) * f(x+h): {fx3:.4f}</span>
        </div>
        """,
        unsafe_allow_html=True
    )

if _name_ == "_main_":
    main()
