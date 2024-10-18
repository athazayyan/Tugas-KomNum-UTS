import numpy as np

# Fungsi untuk mengevaluasi persamaan
def f(x, persamaan):
    return eval(persamaan)

# Metode tabel untuk mencari akar
def metode_tabel(persamaan, batas_bawah, batas_atas, jumlah_titik):
    # Membagi rentang menjadi titik-titik
    x_values = np.linspace(batas_bawah, batas_atas, jumlah_titik)
    y_values = [f(x, persamaan) for x in x_values]

    # Mencari interval di mana terjadi perubahan tanda (akar)
    for i in range(len(y_values) - 1):
        if y_values[i] * y_values[i+1] < 0:
            print(f"Akar ditemukan di antara x = {x_values[i]} dan x = {x_values[i+1]}")
            print(f"f({x_values[i]}) = {y_values[i]}, f({x_values[i+1]}) = {y_values[i+1]}")
            return x_values[i], x_values[i+1]

    print("Tidak ditemukan akar di rentang yang diberikan.")
    return None, None

# Input dari pengguna
persamaan = input("Masukkan persamaan non-linier (gunakan 'x' sebagai variabel): ")
batas_bawah = float(input("Masukkan batas bawah: "))
batas_atas = float(input("Masukkan batas atas: "))
jumlah_titik = int(input("Masukkan jumlah titik: "))

# Mencari akar dengan metode tabel
metode_tabel(persamaan, batas_bawah, batas_atas, jumlah_titik)

