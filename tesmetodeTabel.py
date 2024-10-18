import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def Intro():
    print("\n +------------------------+")
    print(" |      Metode Tabel      |")
    print(" +------------------------+\n")

Intro()

# Input
fungsi = input(" Masukkan Fungsi  : ")
batas_bawah = float(input(" Batas bawah      : "))
batas_atas = float(input(" Batas atas       : "))
iterasi_maksimum = int(input(" Iterasi Maksimum : "))

# Pastikan batas bawah lebih kecil dari batas atas
if batas_bawah > batas_atas:
    batas_bawah, batas_atas = batas_atas, batas_bawah

# Kebutuhan sistem
h = (batas_atas - batas_bawah) / iterasi_maksimum
fungsi = fungsi.replace('E', 'e').replace('X', 'x')
fungsi = fungsi.replace('e', '2.718281828')
fungsi = fungsi.replace('^', '**')
fungsi = re.sub(r'\s+', '', fungsi)
fungsi = re.sub(r'(\d+)(x)', r'\1*\2', fungsi)

# Definisikan fungsi dengan exec
exec(f"""
def f(x):
    return {fungsi}
""")

# Header tabel
print("\n +----------+----------+-------------+-------------+---------------------+")
print(" | Iterasi  |    xi    |    f(xi)    |  f(x(i+1))  |  f(xi)*f(x(i+1))    |")
print(" +----------+----------+-------------+-------------+---------------------+")

# Operasi
iterasi = 0
tabel_hasil = []

while iterasi <= iterasi_maksimum:
    xi = batas_bawah + iterasi * h
    xi_1 = batas_bawah + (iterasi + 1) * h
    
    # Panggil fungsi f dengan satu argumen
    f_xi = f(xi)
    f_xi_1 = f(xi_1)

    if iterasi == iterasi_maksimum:
        print(f" | {iterasi:<8} | {xi:<8.4f} | {f_xi:<11.4f} |")
        print(" +----------+----------+-------------+")
        break

    f_xi_f_xi_1 = f_xi * f_xi_1
    
    tabel_hasil.append([iterasi, xi, f_xi, f_xi_1, f_xi_f_xi_1])
    print(f" | {iterasi:<8} | {xi:<8.4f} | {f_xi:<11.4f} | {f_xi_1:<11.4f} | {f_xi_f_xi_1:<19.4f} |")
    print(" +----------+----------+-------------+-------------+---------------------+")
    
    iterasi += 1

# Plotting
x_values = [batas_bawah + i * h for i in range(iterasi_maksimum + 1)]
y_values = [f(x) for x in x_values]

plt.figure(figsize=(10, 6))
plt.plot(x_values, y_values, label=f'f(x) = {fungsi}', color='b')
plt.axhline(0, color='red', linestyle='--', label='y = 0 (Akar)')
plt.title('Pencarian Akar Menggunakan Metode Tabel')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.grid(True)
plt.legend()
plt.show()

# Hasil output dalam bentuk tabel
df_hasil = pd.DataFrame(tabel_hasil, columns=["Iterasi", "xi", "f(xi)", "f(x(i+1))", "f(xi)*f(x(i+1))"])
print("\nTabel Hasil dalam bentuk DataFrame:")
print(df_hasil)
