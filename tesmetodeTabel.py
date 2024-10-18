import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Fungsi untuk mengevaluasi persamaan
def f(x, fungsi):
    return eval(fungsi)

# Metode tabel untuk mencari akar
def metode_tabel(fungsi, batas_bawah, batas_atas, iterasi_maks):
    # Membagi rentang menjadi titik-titik
    x_values = np.linspace(batas_bawah, batas_atas, iterasi_maks)
    y_values = [f(x, fungsi) for x in x_values]

    # Mencari interval di mana terjadi perubahan tanda (akar)
    akar_ditemukan = False
    tabel_hasil = pd.DataFrame({'x': x_values, 'f(x)': y_values})
    
    for i in range(len(y_values) - 1):
        if y_values[i] * y_values[i+1] < 0:
            akar_info = (x_values[i], x_values[i+1])
            akar_ditemukan = True
            tabel_hasil.loc[i, 'Akar Ditemukan?'] = 'Ya'
            break
    else:
        akar_info = None
    
    # Plotting
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
    print("Tabel Hasil:")
    print(tabel_hasil.head(15))  # Menampilkan 15 nilai pertama sebagai contoh

    if akar_ditemukan:
        return f"Akar ditemukan di antara x = {akar_info[0]} dan x = {akar_info[1]}"
    else:
        return "Tidak ditemukan akar di rentang yang diberikan."

# Input dari pengguna
fungsi = input("Masukkan persamaan non-linier (gunakan 'x' sebagai variabel, contoh: 'x**3 - 5*x + 3'): ")
batas_bawah = float(input("Masukkan batas bawah: "))
batas_atas = float(input("Masukkan batas atas: "))
iterasi_maks = int(input("Masukkan iterasi maksimum: "))

# Menampilkan hasil, tabel, dan plot
hasil = metode_tabel(fungsi, batas_bawah, batas_atas, iterasi_maks)
print(hasil)
