import numpy as np
import matplotlib.pyplot as plt

# Fungsi untuk mengevaluasi persamaan
def f(x, persamaan):
    return eval(persamaan)

# Metode tabel untuk mencari akar
def metode_tabel(persamaan, batas_bawah, batas_atas, jumlah_titik):
    # Membagi rentang menjadi titik-titik
    x_values = np.linspace(batas_bawah, batas_atas, jumlah_titik)
    y_values = [f(x, persamaan) for x in x_values]

    # Mencari interval di mana terjadi perubahan tanda (akar)
    akar_ditemukan = False
    for i in range(len(y_values) - 1):
        if y_values[i] * y_values[i+1] < 0:
            print(f"Akar ditemukan di antara x = {x_values[i]} dan x = {x_values[i+1]}")
            akar_ditemukan = True

    if not akar_ditemukan:
        print("Tidak ditemukan akar di rentang yang diberikan.")
    
    # Visualisasi Grafik
    plt.figure(figsize=(10, 6))
    plt.plot(x_values, y_values, label='f(x)', color='b', marker='o')
    plt.axhline(0, color='r', linestyle='--')
