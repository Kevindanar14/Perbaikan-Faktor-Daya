import streamlit as st
import matplotlib.pyplot as plt
import math

# Tetapan
pi = 3.14
f = 50  # Frekuensi dalam Hz

st.set_page_config(page_title="Perbaikan Faktor Daya RL", layout="centered")
st.title("🔧 Perhitungan Perbaikan Faktor Daya (Rangkaian RL)")
st.markdown("""
Program ini menghitung dan menampilkan segitiga daya untuk perbaikan faktor daya 
pada rangkaian **Resistor + Induktor (RL)** dengan menambahkan kapasitor paralel.
""")

# Input pengguna
V = st.number_input("Tegangan (Volt)", min_value=1.0, step=1.0)
R = st.number_input("Resistansi R (Ohm)", min_value=0.1, step=0.1)
L = st.number_input("Induktansi L (Henry)", min_value=0.0001, step=0.0001, format="%.4f")
pf_target = st.number_input("Faktor Daya Target (misal 0.95)", min_value=0.1, max_value=1.0, step=0.01)

if st.button("Hitung") and V > 0 and R > 0 and L > 0:
    # Hitung reaktansi dan impedansi
    Xl = 2 * pi * f * L
    Z = math.sqrt(R**2 + Xl**2)
    I = V / Z  # Arus total
    cos_phi_awal = R / Z
    phi_awal = math.acos(cos_phi_awal)
    
    # Daya
    P = V * I * cos_phi_awal  # Daya aktif
    Q = V * I * math.sin(phi_awal)  # Daya reaktif
    S = V * I  # Daya semu

    # Target Q
    phi_target = math.acos(pf_target)
    Q_target = P * math.tan(phi_target)
    delta_Q = Q - Q_target

    # Kapasitansi untuk koreksi faktor daya
    C = delta_Q / (2 * pi * f * V ** 2)

    # ====================
    # Output Hasil
    # ====================
    st.success("✅ Hasil Perhitungan Daya")
    st.write(f"• Daya Aktif (P): {P:.2f} Watt")
    st.write(f"• Daya Reaktif Awal (Q): {Q:.2f} VAR")
    st.write(f"• Daya Semu (S): {S:.2f} VA")
    st.write(f"• Faktor Daya Awal: {cos_phi_awal:.3f}")
    st.write(f"• Faktor Daya Target: {pf_target:.3f}")
    st.write(f"• Daya Reaktif Setelah Koreksi: {Q_target:.2f} VAR")
    st.write(f"• ΔQ yang Dikompensasi: {delta_Q:.2f} VAR")
    st.write(f"• Kapasitor yang Dibutuhkan: {C * 1e6:.2f} µF")

    # ====================
    # Plot Segitiga Daya
    # ====================
    fig, ax = plt.subplots(1, 2, figsize=(10, 4))

    # Segitiga Awal
    ax[0].plot([0, P], [0, 0], color='blue', label='P')
    ax[0].plot([P, P], [0, Q], color='red', label='Q')
    ax[0].plot([0, P], [0, Q], 'g--', label='S')
    ax[0].set_title("Segitiga Daya Awal")
    ax[0].legend()
    ax[0].axis('equal')
    ax[0].grid(True)

    # Segitiga Setelah Koreksi
    ax[1].plot([0, P], [0, 0], color='blue', label='P')
    ax[1].plot([P, P], [0, Q_target], color='orange', label='Q setelah koreksi')
    ax[1].plot([0, P], [0, Q_target], 'g--', label='S baru')
    ax[1].set_title("Segitiga Daya Setelah Koreksi")
    ax[1].legend()
    ax[1].axis('equal')
    ax[1].grid(True)

    st.pyplot(fig)
