import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.optimize import fsolve
import datetime

# Gezegenlerin yörünge parametreleri (yarı büyük eksen a, eksantriklik e)
gezegenler = {
    "Merkür": (0.39, 0.205),
    "Venüs": (0.72, 0.007),
    "Dünya": (1.00, 0.017),
    "Mars": (1.52, 0.093),
    "Jüpiter": (5.20, 0.049),
    "Satürn": (9.58, 0.056),
    "Uranüs": (19.22, 0.046),
    "Neptün": (30.05, 0.010)
}

# Kepler Denklemi çözümü için fonksiyon
def kepler_coz(M, e):
    E_cozum = fsolve(lambda E: E - e * np.sin(E) - M, M)
    return E_cozum[0]

# Zaman ölçeği (gün cinsinden, 1 yıl = 360 gün kabul ediliyor)
zaman = np.linspace(0, 360, 500)

def gezegen_konumlari(a, e):
    x_liste, y_liste = [], []
    
    for t in zaman:
        M = 2 * np.pi * (t / 360)  # Ortalama anomali
        E = kepler_coz(M, e)  # Eksantrik anomali
        
        # Gerçek Anomali
        theta = 2 * np.arctan(np.sqrt((1 + e) / (1 - e)) * np.tan(E / 2))
        
        # Eliptik yörünge denkleminden x, y koordinatları
        r = a * (1 - e**2) / (1 + e * np.cos(theta))
        x, y = r * np.cos(theta), r * np.sin(theta)
        
        x_liste.append(x)
        y_liste.append(y)
    
    return np.array(x_liste), np.array(y_liste)

fig, ax = plt.subplots(figsize=(8, 8))
ax.set_xlim(-35, 35)
ax.set_ylim(-35, 35)
ax.set_xlabel("X Ekseni (AU)")
ax.set_ylabel("Y Ekseni (AU)")
ax.set_title("Gezegenlerin Gerçek Yörüngeleri")
ax.scatter(0, 0, color='yellow', marker='o', s=200, label='Güneş')  # Güneş

gezegen_noktalar = {}
gezegen_yorungeleri = {}

# Yörünge hesaplamalarını baştan yap
for gezegen, (a, e) in gezegenler.items():
    x, y = gezegen_konumlari(a, e)
    gezegen_yorungeleri[gezegen] = (x, y)
    gezegen_noktalar[gezegen], = ax.plot([], [], 'o', label=f'{gezegen} (konum)')
    
# Şu anki saati almak
current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Saat bilgisini görsele eklemek
ax.text(0.05, 0.95, f"Çalışma Zamanı: {current_time}", transform=ax.transAxes, fontsize=12, verticalalignment='top')


def guncelle(frame):
    for gezegen, (a, e) in gezegenler.items():
        x, y = gezegen_yorungeleri[gezegen]
        gezegen_noktalar[gezegen].set_data([x[frame]], [y[frame]])  # x[frame] ve y[frame] tek bir değer, bunu listeye çevirdik
    return gezegen_noktalar.values()


ani = animation.FuncAnimation(fig, guncelle, frames=len(zaman), interval=50, blit=True)
plt.legend()
plt.show()
