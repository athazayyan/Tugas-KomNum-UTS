import streamlit as st
import time
import sympy as sp
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

st.markdown("# Halaman Utama 🎈")
st.sidebar.markdown("# Metode Tabel 🎈")

with st.form("Metode tabel"):
    input_string = st.text_input("Masukkan fungsi f(x): ")
    N = st.number_input("masukkan Maks Iterasi", min_value=1, max_value=10, value=10)
    bawah = st.number_input("masukkan batas bawah", value=0.0)
    atas = st.number_input("masukkan batas atas", value=0.1)
    st.form_submit_button("Jalankan")
h = float((atas - bawah) / N)
i = 0
x = sp.symbols('x')
hasil = None
x_array = []
fx1_array= []
fx2_array= []
fx3_array= []
fx1_array1= []
fx2_array1 = []
fx3_array1 = []
st.write("batas bawah adalah", bawah, "dan batas atas adalah", atas, "batas maksimum iterasi adalah", N)
st.write("H", h)
Na = N +1
if input_string:
    try:
        exp = sp.sympify(input_string)
    except (sp.SympifyError, ValueError) as e:
        st.error(f"Error parsing input string: {e}")
        exp = None

    if exp:
        xA = 0
        def f(xA):
            f_sympy = sp.lambdify(x, exp)
            return f_sympy(xA)

        'Memulai Metode Tabel...'
        latest_iteration = st.empty()
        bar = st.progress(1)
        for i in range(1, Na):
            latest_iteration.text(f'Iterasi {i}')
            x_val = bawah + (i * h)
            fx1 = f(x_val)
            fx2 = f(bawah + ((i + 1) * h))
            fx3 = fx1 * fx2
            x_array.append(x_val)
            fx1_array.append(fx1)
            fx2_array.append(fx2)
            fx3_array.append(fx3)
            fx1_array1.append(abs(fx1))
            fx2_array1.append(abs(fx2))
            fx3_array1.append(abs(fx3))
            if fx1 == 0:
                hasil = x_val
            elif fx1 * fx2 < 0:
                if abs(fx1) < abs(fx2):
                    hasil = float(x_val)
                else:
                    hasil = float(x_val + h)
            st.markdown(
                f"""
                <div style='background-color: #f0f0f0; padding: 10px; border-radius: 5px;'>
                    <strong style='color: #ff6347;'>Iterasi {i}</strong> | 
                    <span style='color: #4682b4;'>Akar: {x_val:.4f}</span> | 
                    <span style='color: #32cd32;'>f(x): {fx1:.4f}</span> | 
                    <span style='color: #ffa500;'>f(x+h): {fx2:.4f}</span> | 
                    <span style='color: #8a2be2;'>f(x) * f(x+h): {fx3:.4f}</span>
                </div>
                """, 
                unsafe_allow_html=True
            )
            st.write(f"<hr style='border: none; border-top: 1px solid #ccc;' />", unsafe_allow_html=True)
            bar.progress(i / N)
            time.sleep(0.5)

        if hasil is not None:
            st.write("Akar ditemukan pada akar =", hasil)
        else:
            st.write("Akar tidak ditemukan dalam batas iterasi yang diberikan.")
else:
    st.write("Silakan masukkan fungsi f(x) untuk memulai.")

'...Selesai..'
