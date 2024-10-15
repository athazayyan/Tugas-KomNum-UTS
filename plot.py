import numpy as np
import matplotlib.pyplot as plt

# Fungsi untuk plotting rumus matematika
def plot_formula(formula, x_range):
    # Mengubah rumus menjadi fungsi python menggunakan eval
    x = np.linspace(x_range[0], x_range[1], 1000)
    y = eval(formula)
    
    # Plotting hasilnya
    plt.figure(figsize=(8, 6))
    plt.plot(x, y, label=f"y = {formula}")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title(f"Plot of y = {formula}")
    plt.grid(True)
    plt.legend()
    plt.show()

# Contoh penggunaan
formula = input("Masukkan rumus (gunakan x sebagai variabel): ")  # Misalnya: "np.sin(x) + 0.5*x"
x_range = [-10, 10]  # Range nilai x
plot_formula(formula, x_range)
