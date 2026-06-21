from csv_handler import baca_csv, tulis_csv
from queue_pesanan import *
from stack_riwayat import *

# =========================
# LIHAT PRODUK
# =========================
def lihat_produk():
    data = baca_csv("produk.csv")

    print("\n===== DAFTAR PRODUK =====")
    for p in data:
        print(f"{p['id_produk']} | {p['nama_produk']} | Rp{p['harga']} | Stok: {p['stok']}")
    print("=========================\n")


# =========================
# TAMBAH PRODUK
# =========================
def tambah_produk():
    data = baca_csv("produk.csv")

    data.append({
        "id_produk": input("ID Produk: "),
        "nama_produk": input("Nama Produk: "),
        "harga": input("Harga: "),
        "stok": input("Stok: ")
    })

    tulis_csv("produk.csv",
              ["id_produk","nama_produk","harga","stok"],
              data)

    print("✔ Produk ditambah")


# =========================
# CARI PRODUK
# =========================
def cari_produk():
    keyword = input("Cari: ")
    data = baca_csv("produk.csv")

    found = False
    for p in data:
        if keyword.lower() in p["nama_produk"].lower():
            print(f"{p['id_produk']} | {p['nama_produk']} | Rp{p['harga']} | Stok: {p['stok']}")
            found = True

    if not found:
        print("❌ Tidak ditemukan")


# =========================
# SORT PRODUK
# =========================
def urutkan_produk():
    data = baca_csv("produk.csv")
    data.sort(key=lambda x: int(x["harga"]))

    print("\n=== TERMURAH ===")
    for p in data:
        print(f"{p['id_produk']} | {p['nama_produk']} | Rp{p['harga']} | Stok: {p['stok']}")
    print("==============\n")


# =========================
# BELI PRODUK (KERANJANG + TOTAL)
# =========================
def pesan():
    data = baca_csv("produk.csv")

    keranjang = []
    total_harga = 0

    while True:
        print("\n===== PRODUK =====")
        for p in data:
            print(f"{p['id_produk']} | {p['nama_produk']} | Rp{p['harga']} | Stok: {p['stok']}")
        print("==================")

        id_produk = input("ID produk (stop untuk selesai): ")

        if id_produk.lower() == "stop":
            break

        jumlah = int(input("Jumlah: "))

        found = False

        for p in data:
            if p["id_produk"] == id_produk:
                found = True

                if int(p["stok"]) < jumlah:
                    print("❌ Stok kurang")
                    break

                harga = int(p["harga"])
                subtotal = harga * jumlah

                p["stok"] = str(int(p["stok"]) - jumlah)

                keranjang.append({
                    "nama": p["nama_produk"],
                    "jumlah": jumlah,
                    "harga": harga,
                    "subtotal": subtotal
                })

                total_harga += subtotal

                print(f"✔ Ditambahkan | Rp{subtotal}")
                break

        if not found:
            print("❌ Tidak ditemukan")

    if keranjang:
        nama = input("Nama pembeli: ")

        tambah_pesanan({
            "nama": nama,
            "keranjang": keranjang,
            "total_harga": total_harga
        })

        tulis_csv("produk.csv",
                  ["id_produk","nama_produk","harga","stok"],
                  data)

        print(f"📥 Masuk antrian | Total: Rp{total_harga}")
    else:
        print("❌ Tidak ada pembelian")


# =========================
# PROSES PESANAN (RAPI)
# =========================
def proses():
    p = proses_pesanan()

    if p:
        tambah_riwayat(p)

        print("\n📦 PESANAN DIPROSES")
        print(f"Nama Pembeli: {p['nama']}")

        total_item = 0

        print("Isi Keranjang:")
        for item in p['keranjang']:
            print(f"- {item['nama']} x{item['jumlah']} = Rp{item['subtotal']}")
            total_item += item['jumlah']

        print(f"TOTAL BAYAR: Rp{p['total_harga']}")
        print("====================\n")

    else:
        print("❌ Antrian kosong")


# =========================
# RIWAYAT
# =========================
def lihat_riwayat_menu():
    data = lihat_riwayat()

    print("\n===== RIWAYAT =====")

    if not data:
        print("Belum ada transaksi")
        return

    for r in data:
        print(f"\nNama: {r['nama']}")
        print("Keranjang:")
        for item in r['keranjang']:
            print(f"- {item['nama']} x{item['jumlah']} = Rp{item['subtotal']}")
        print(f"TOTAL: Rp{r['total_harga']}")
        print("-------------------")

    print("====================\n")


# =========================
# MENU
# =========================
while True:
    print("""
===== MARKETPLACE =====
1. Lihat Produk
2. Tambah Produk
3. Cari Produk
4. Urutkan Produk
5. Pesan Produk
6. Proses Pesanan
7. Riwayat
0. Keluar
""")

    pilih = input("Pilih: ")

    if pilih == "1":
        lihat_produk()
    elif pilih == "2":
        tambah_produk()
    elif pilih == "3":
        cari_produk()
    elif pilih == "4":
        urutkan_produk()
    elif pilih == "5":
        pesan()
    elif pilih == "6":
        proses()
    elif pilih == "7":
        lihat_riwayat_menu()
    elif pilih == "0":
        break