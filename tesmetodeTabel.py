import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from tqdm import tqdm
import time

# Warna untuk tampilan
class Color:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def Intro():
    print(Color.HEADER + "\n +------------------------------+")
    print(" |  " + Color.BOLD + Color.OKBLUE + "  Metode Tabel  " + Color.ENDC + "  |")
    print(" +------------------------------+\n" + Color.ENDC)
    print(" " + Color.OKGREEN + "Selamat datang di Program Pencarian Akar!" + Color.ENDC)
    print(" " + Color.WARNING + "Silakan masukkan fungsi yang diinginkan." + Color.ENDC)

# Animasi loading yang lebih menarik
def loading_animation():
    loading_steps = ["Memulai Program", "Mempersiapkan Fungsi", "Menghitung Rentang", "Menyiapkan Tabel"]
    for step in loading_steps:
        for _ in tqdm(range(10), desc=step, bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}"):
            time.sleep(0.1)  # Simulasi waktu loading
    print(Color.OKGREEN + "\nProgram Siap!" + Color.ENDC)

loading_animation()
Intro()

# (1) Definisikan fungsi f(x)
fungsi = input(" Masukkan Fungsi  : ")
fungsi = fungsi.replace('E', 'e').replace('X', 'x').replace('^', '**')  # Ganti simbol dan format
fungsi = re.sub(r'\s+', '', fungsi)  # Hapus spasi
exec(f"""
def f(x):
    return {fungsi}
""")

# (2) Tentukan range untuk x yang berupa batas bawah xbawah dan batas atas xatas
batas_bawah = float(input(" Batas bawah      : "))
batas_atas = float(input(" Batas atas       : "))

# Pastikan batas bawah lebih kecil dari batas atas
if batas_bawah > batas_atas:
    batas_bawah, batas_atas = batas_atas, batas_bawah

# (3) Tentukan jumlah pembagian N
iterasi_maksimum = int(input(" Iterasi Maksimum : "))

# (4) Hitung step pembagi h
h = (batas_atas - batas_bawah) / iterasi_maksimum

# (5) Untuk i = 0 s/d N, hitung xi = xbawah + i.h dan yi = f(xi)
tabel_hasil = []
akar_ditemukan = None  # Menyimpan informasi tentang akar

print("\n +----------+----------+-------------+-------------+---------------------+")
print(" | Iterasi  |    xi    |    f(xi)    |  f(x(i+1))  |  f(xi)*f(x(i+1))    |")
print(" +----------+----------+-------------+-------------+---------------------+")

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

# Plotting dengan animasi
x_values = [batas_bawah + i * h for i in range(iterasi_maksimum + 1)]
y_values = [f(x) for x in x_values]

fig, ax = plt.subplots(figsize=(10, 6))
line, = ax.plot([], [], label=f'f(x) = {fungsi}', color='cyan', linewidth=2)
ax.axhline(0, color='red', linestyle='--', label='y = 0 (Akar)')
ax.set_title('Pencarian Akar Menggunakan Metode Tabel', fontsize=16, fontweight='bold', color='purple')
ax.set_xlabel('x', fontsize=12)
ax.set_ylabel('f(x)', fontsize=12)
ax.set_xlim(batas_bawah, batas_atas)
ax.set_ylim(min(y_values) - 10, max(y_values) + 10)  # Set initial limits
ax.grid(True, linestyle='--', color='lightgray')
ax.legend()

# Animasi plotting
def init():
    line.set_data([], [])
    return line,

def update(frame):
    line.set_data(x_values[:frame], y_values[:frame])
    # Hanya set ylim jika frame > 0
    if frame > 0:
        ax.set_ylim(min(y_values[:frame]) - 10, max(y_values[:frame]) + 10)
    return line,

ani = FuncAnimation(fig, update, frames=len(x_values), init_func=init, blit=True, repeat=False)
plt.show()

# Hasil output dalam bentuk tabel
df_hasil = pd.DataFrame(tabel_hasil, columns=["Iterasi", "xi", "f(xi)", "f(x(i+1))", "f(xi)*f(x(i+1))"])
print("\nTabel Hasil dalam bentuk DataFrame:")
print(df_hasil)

# Menampilkan hasil akar yang ditemukan
if akar_ditemukan:
    print(f"\nAkar ditemukan di antara x = {akar_ditemukan[0]} dan x = {akar_ditemukan[1]}")
else:
    print("\nTidak ditemukan akar di rentang yang diberikan.")
