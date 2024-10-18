import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from tqdm import tqdm
import time
import os

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def colorful_intro():
    clear_console()
    print("\n" + "\033[1;34m" + "+" + "-" * 24 + "+")
    print(" |" + "\033[1;33m" + "      Metode Tabel      " + "\033[1;34m" + "|")
    print(" +" + "-" * 24 + "+\033[0m\n")

# Animasi loading
def loading_animation():
    for _ in tqdm(range(10), desc="Memuat...", bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}", colour='green'):
        time.sleep(0.2)  # Simulasi waktu loading

loading_animation()
colorful_intro()

# (1) Definisikan fungsi f(x)
fungsi = input("\033[1;36m Masukkan Fungsi  : \033[0m")
fungsi = fungsi.replace('E', 'e').replace('X', 'x').replace('^', '**')  # Ganti simbol dan format
fungsi = re.sub(r'\s+', '', fungsi)  # Hapus spasi
exec(f"""
def f(x):
    return {fungsi}
""")

# (2) Tentukan range untuk x yang berupa batas bawah xbawah dan batas atas xatas
batas_bawah = float(input("\033[1;36m Batas bawah      : \033[0m"))
batas_atas = float(input("\033[1;36m Batas atas       : \033[0m"))

# Pastikan batas bawah lebih kecil dari batas atas
if batas_bawah > batas_atas:
    batas_bawah, batas_atas = batas_atas, batas_bawah

# (3) Tentukan jumlah pembagian N
iterasi_maksimum = int(input("\033[1;36m Iterasi Maksimum : \033[0m"))

# (4) Hitung step pembagi h
h = (batas_atas - batas_bawah) / iterasi_maksimum

# (5) Untuk i = 0 s/d N, hitung xi = xbawah + i.h dan yi = f(xi)
tabel_hasil = []
akar_ditemukan = None  # Menyimpan informasi tentang akar

print("\n\033[1;34m +----------+----------+-------------+-------------+---------------------+")
print(" | Iterasi  |    xi    |    f(xi)    |  f(x(i+1))  |  f(xi)*f(x(i+1))    |")
print(" +----------+----------+-------------+-------------+---------------------+\033[0m")

for i in range(iterasi_maksimum + 1):
    xi = batas_bawah + i * h
    f_xi = f(xi)
    
    # Hitung f(xi+1) hanya jika i < iterasi_maksimum
    if i < iterasi_maksimum:
        f_xi_1 = f(batas_bawah + (i + 1) * h)
    else:
        f_xi_1 = None  # Tidak ada f(xi+1) di iterasi terakhir

    # (6) Cari k, apakah f(xk) = 0 atau ada perubahan tanda
    if f_xi == 0:
        akar_ditemukan = (xi, xi)
        break
    elif i < iterasi_maksimum and f_xi * f_xi_1 < 0:  # Periksa perubahan tanda hanya jika f_xi_1 valid
        if abs(f_xi) < abs(f_xi_1):
            akar_ditemukan = (xi, batas_bawah + (i + 1) * h)  # Akar di xi
        else:
            akar_ditemukan = (batas_bawah + (i + 1) * h, xi)  # Akar di xi+1

    f_xi_f_xi_1 = f_xi * f_xi_1 if f_xi_1 is not None else None
    tabel_hasil.append([i, xi, f_xi, f_xi_1, f_xi_f_xi_1])

    # Mencetak hasil dengan penanganan None
    f_xi_str = f"{f_xi:<11.4f}" if f_xi is not None else "N/A"
    f_xi_1_str = f"{f_xi_1:<11.4f}" if f_xi_1 is not None else "N/A"
    f_xi_f_xi_1_str = f"{f_xi_f_xi_1:<19.4f}" if f_xi_f_xi_1 is not None else "N/A"

    print(f" | {i:<8} | {xi:<8.4f} | {f_xi_str} | {f_xi_1_str} | {f_xi_f_xi_1_str} |")
    print(" +----------+----------+-------------+-------------+---------------------+")

# Plotting with Animation
x_values = [batas_bawah + i * h for i in range(iterasi_maksimum + 1)]
y_values = [f(x) for x in x_values]

fig, ax = plt.subplots(figsize=(10, 6))
line, = ax.plot([], [], label=f'f(x) = {fungsi}', color='b')
ax.axhline(0, color='red', linestyle='--', label='y = 0 (Akar)')
ax.set_xlim(batas_bawah, batas_atas)
ax.set_ylim(min(y_values) - 10, max(y_values) + 10)
ax.set_title('Pencarian Akar Menggunakan Metode Tabel', fontsize=16)
ax.set_xlabel('x', fontsize=14)
ax.set_ylabel('f(x)', fontsize=14)
ax.grid(True)
ax.legend()

# Initialize the background of the plot
def init():
    line.set_data([], [])
    return line,

# Update function for animation
def update(frame):
    line.set_data(x_values[:frame + 1], y_values[:frame + 1])
    return line,

# Create the animation
ani = FuncAnimation(fig, update, frames=len(x_values), init_func=init, blit=True, repeat=False)

plt.show()

# Hasil output dalam bentuk tabel
df_hasil = pd.DataFrame(tabel_hasil, columns=["Iterasi", "xi", "f(xi)", "f(x(i+1))", "f(xi)*f(x(i+1))"])
print("\n\033[1;34mTabel Hasil dalam bentuk DataFrame:\033[0m")
print(df_hasil)

# Menampilkan hasil akar yang ditemukan
if akar_ditemukan:
    print(f"\n\033[1;32mAkar ditemukan di antara x = {akar_ditemukan[0]} dan x = {akar_ditemukan[1]}\033[0m")
else:
    print("\n\033[1;31mTidak ditemukan akar di rentang yang diberikan.\033[0m")
