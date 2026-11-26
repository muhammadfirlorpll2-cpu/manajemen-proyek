
import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# ================= DATABASE =================

def koneksi():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="manajemen_proyek"
    )


def siapkan_database():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password=""
    )
    cursor = db.cursor()

    cursor.execute(
        "CREATE DATABASE IF NOT EXISTS manajemen_proyek"
    )

    cursor.close()
    db.close()

    db = koneksi()
    cursor = db.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS db_manajemen_proyek (
            id_proyek INT AUTO_INCREMENT PRIMARY KEY,
            nama_proyek VARCHAR(150) NOT NULL,
            anggota_proyek VARCHAR(150),
            tanggal_mulai VARCHAR(30),
            tanggal_selesai VARCHAR(30),
            nama_tugas VARCHAR(150),
            deadline_tugas VARCHAR(30),
            status_pekerjaan VARCHAR(50),
            progres_persen INT DEFAULT 0
        )
    """)

    # Tambahkan kolom yang belum tersedia
    cursor.execute("SHOW COLUMNS FROM db_manajemen_proyek")
    kolom = [data[0] for data in cursor.fetchall()]

    tambahan = {
        "nama_proyek": "VARCHAR(150) DEFAULT ''",
        "anggota_proyek": "VARCHAR(150)",
        "tanggal_mulai": "VARCHAR(30)",
        "tanggal_selesai": "VARCHAR(30)",
        "nama_tugas": "VARCHAR(150)",
        "deadline_tugas": "VARCHAR(30)",
        "status_pekerjaan": "VARCHAR(50)",
        "progres_persen": "INT DEFAULT 0"
    }

    for nama, tipe in tambahan.items():
        if nama not in kolom:
            cursor.execute(
                f"ALTER TABLE db_manajemen_proyek ADD COLUMN {nama} {tipe}"
            )

    db.commit()
    cursor.close()
    db.close()


# ================= FUNGSI =================

def kosongkan():
    entry_nama.delete(0, tk.END)
    entry_anggota.delete(0, tk.END)
    entry_mulai.delete(0, tk.END)
    entry_selesai.delete(0, tk.END)
    entry_tugas.delete(0, tk.END)
    entry_deadline.delete(0, tk.END)
    combo_status.set("Belum Mulai")
    progres_var.set(0)


def tampilkan_data(keyword=""):
    for item in tabel.get_children():
        tabel.delete(item)

    try:
        db = koneksi()
        cursor = db.cursor()

        sql = """
            SELECT id_proyek, nama_proyek, anggota_proyek,
                   tanggal_mulai, tanggal_selesai, nama_tugas,
                   deadline_tugas, status_pekerjaan, progres_persen
            FROM db_manajemen_proyek
        """

        if keyword.strip():
            sql += """
                WHERE CONCAT_WS(' ',
                    id_proyek,
                    nama_proyek,
                    anggota_proyek,
                    tanggal_mulai,
                    tanggal_selesai,
                    nama_tugas,
                    deadline_tugas,
                    status_pekerjaan,
                    progres_persen
                ) LIKE %s
            """
            cursor.execute(sql, ("%" + keyword + "%",))
        else:
            cursor.execute(sql)

        data = cursor.fetchall()

        for baris in data:
            tabel.insert("", tk.END, values=baris)

        cursor.close()
        db.close()

    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", str(e))


def tambah_data():
    nama = entry_nama.get().strip()
    anggota = entry_anggota.get().strip()
    mulai = entry_mulai.get().strip()
    selesai = entry_selesai.get().strip()
    tugas = entry_tugas.get().strip()
    deadline = entry_deadline.get().strip()
    status = combo_status.get().strip()
    try:
        progres = int(spin_progres.get())
    except ValueError:
        messagebox.showwarning("Peringatan", "Progres harus berupa angka 0 sampai 100!")
        return

    if progres < 0 or progres > 100:
        messagebox.showwarning("Peringatan", "Progres harus berada pada rentang 0 sampai 100!")
        return

    if not nama:
        messagebox.showwarning(
            "Peringatan",
            "Nama proyek harus diisi!"
        )
        return

    try:
        db = koneksi()
        cursor = db.cursor()

        sql = """
            INSERT INTO db_manajemen_proyek
            (nama_proyek, anggota_proyek, tanggal_mulai, tanggal_selesai,
             nama_tugas, deadline_tugas, status_pekerjaan, progres_persen)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(sql, (nama, anggota, mulai, selesai,
                             tugas, deadline, status, progres))
        db.commit()

        cursor.close()
        db.close()

        tampilkan_data()
        update_card()
        kosongkan()

        messagebox.showinfo(
            "Berhasil",
            "Data proyek berhasil ditambahkan!"
        )

    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", str(e))


def ubah_data():
    pilihan = tabel.selection()
    if not pilihan:
        messagebox.showwarning("Peringatan", "Pilih data yang ingin diperbarui!")
        return

    nama = entry_nama.get().strip()
    anggota = entry_anggota.get().strip()
    mulai = entry_mulai.get().strip()
    selesai = entry_selesai.get().strip()
    tugas = entry_tugas.get().strip()
    deadline = entry_deadline.get().strip()
    status = combo_status.get().strip()

    try:
        progres = int(spin_progres.get())
    except ValueError:
        messagebox.showwarning("Peringatan", "Progres harus berupa angka 0 sampai 100!")
        return

    if not nama:
        messagebox.showwarning("Peringatan", "Nama proyek harus diisi!")
        return
    if progres < 0 or progres > 100:
        messagebox.showwarning("Peringatan", "Progres harus berada pada rentang 0 sampai 100!")
        return

    try:
        id_proyek = tabel.item(pilihan[0])["values"][0]
        db = koneksi()
        cursor = db.cursor()
        cursor.execute("""
            UPDATE db_manajemen_proyek
            SET nama_proyek=%s, anggota_proyek=%s,
                tanggal_mulai=%s, tanggal_selesai=%s,
                nama_tugas=%s, deadline_tugas=%s,
                status_pekerjaan=%s, progres_persen=%s
            WHERE id_proyek=%s
        """, (nama, anggota, mulai, selesai, tugas, deadline,
              status, progres, id_proyek))
        db.commit()
        cursor.close()
        db.close()

        tampilkan_data()
        update_card()
        kosongkan()
        messagebox.showinfo("Berhasil", "Data proyek berhasil diperbarui!")
    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", str(e))


def hapus_data():
    pilihan = tabel.selection()

    if not pilihan:
        messagebox.showwarning(
            "Peringatan",
            "Pilih data yang ingin dihapus!"
        )
        return

    konfirmasi = messagebox.askyesno(
        "Konfirmasi",
        "Yakin ingin menghapus proyek ini?"
    )

    if not konfirmasi:
        return

    try:
        item = tabel.item(pilihan[0])
        id_proyek = item["values"][0]

        db = koneksi()
        cursor = db.cursor()

        cursor.execute(
            "DELETE FROM db_manajemen_proyek WHERE id_proyek = %s",
            (id_proyek,)
        )

        db.commit()
        cursor.close()
        db.close()

        tampilkan_data()
        update_card()
        kosongkan()

        messagebox.showinfo(
            "Berhasil",
            "Data berhasil dihapus!"
        )

    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", str(e))


def cari_data():
    keyword = entry_cari.get()
    tampilkan_data(keyword)


def reset_data():
    entry_cari.delete(0, tk.END)
    tampilkan_data()
    update_card()


def pilih_data(event):
    pilihan = tabel.selection()

    if pilihan:
        data = tabel.item(pilihan[0])["values"]

        kosongkan()

        entry_nama.insert(0, data[1] or "")
        entry_anggota.insert(0, data[2] or "")
        entry_mulai.insert(0, data[3] or "")
        entry_selesai.insert(0, data[4] or "")
        entry_tugas.insert(0, data[5] or "")
        entry_deadline.insert(0, data[6] or "")
        combo_status.set(data[7] or "Belum Mulai")
        progres_var.set(data[8] or 0)


# ================= TAMPILAN =================

siapkan_database()

root = tk.Tk()
root.title("Sistem Manajemen Proyek")
root.geometry("1150x720")
root.configure(bg="#F1F5F9")
root.minsize(950, 600)

# Warna
NAVY = "#172554"
BIRU = "#2563EB"
PUTIH = "#FFFFFF"
ABU = "#64748B"
HIJAU = "#16A34A"
MERAH = "#DC2626"

# ================= SIDEBAR =================

sidebar = tk.Frame(root, bg=NAVY, width=220)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)

tk.Label(
    sidebar,
    text="PROJECT APP",
    font=("Arial", 19, "bold"),
    bg=NAVY,
    fg="white"
).pack(pady=(35, 5))

tk.Label(
    sidebar,
    text="Sistem Manajemen Proyek",
    font=("Arial", 9),
    bg=NAVY,
    fg="#BFDBFE"
).pack(pady=(0, 40))

tk.Label(
    sidebar,
    text="MENU UTAMA",
    font=("Arial", 9, "bold"),
    bg=NAVY,
    fg="#93C5FD"
).pack(anchor="w", padx=22, pady=10)

def menu_sidebar(teks, halaman):
    return tk.Button(
        sidebar,
        text=teks,
        command=lambda: tampilkan_halaman(halaman),
        font=("Arial", 11),
        bg="#1E40AF",
        fg="white",
        activebackground="#2563EB",
        activeforeground="white",
        anchor="w",
        padx=20,
        pady=14,
        relief="flat",
        cursor="hand2",
        borderwidth=0
    )

tombol_dashboard = menu_sidebar("▣  Dashboard", "dashboard")
tombol_dashboard.pack(fill="x", padx=10, pady=4)

tombol_data = menu_sidebar("▤  Data Proyek", "data")
tombol_data.pack(fill="x", padx=10, pady=4)

tk.Label(
    sidebar,
    text="© 2026 Project App",
    font=("Arial", 9),
    bg=NAVY,
    fg="#94A3B8"
).pack(side="bottom", pady=20)


# ================= KONTEN =================

konten = tk.Frame(root, bg="#F1F5F9")
konten.pack(side="right", fill="both", expand=True)

header = tk.Frame(konten, bg=PUTIH, height=75)
header.pack(fill="x")
header.pack_propagate(False)

judul_halaman = tk.Label(
    header,
    text="Dashboard Manajemen Proyek",
    font=("Arial", 20, "bold"),
    bg=PUTIH,
    fg=NAVY
)
judul_halaman.pack(side="left", padx=25, pady=20)

halaman_dashboard = tk.Frame(konten, bg="#F1F5F9")
halaman_data = tk.Frame(konten, bg="#F1F5F9")

def tampilkan_halaman(nama):
    halaman_dashboard.pack_forget()
    halaman_data.pack_forget()

    if nama == "dashboard":
        tombol_dashboard.configure(bg="#2563EB")
        tombol_data.configure(bg="#1E40AF")
        judul_halaman.configure(text="Dashboard Manajemen Proyek")
        halaman_dashboard.pack(fill="both", expand=True)
        update_card()
    else:
        tombol_dashboard.configure(bg="#1E40AF")
        tombol_data.configure(bg="#2563EB")
        judul_halaman.configure(text="Data Proyek")
        halaman_data.pack(fill="both", expand=True)
        tampilkan_data()


# ================= DASHBOARD CARD =================

card_area = tk.Frame(halaman_dashboard, bg="#F1F5F9")
card_area.pack(fill="x", padx=25, pady=20)

def buat_card(parent, judul, isi, warna):
    card = tk.Frame(
        parent,
        bg=PUTIH,
        highlightbackground="#E2E8F0",
        highlightthickness=1
    )
    card.pack(side="left", fill="both", expand=True, padx=7)

    tk.Label(
        card,
        text=judul,
        font=("Arial", 10),
        bg=PUTIH,
        fg=ABU
    ).pack(anchor="w", padx=18, pady=(17, 5))

    label = tk.Label(
        card,
        text=isi,
        font=("Arial", 22, "bold"),
        bg=PUTIH,
        fg=warna
    )
    label.pack(anchor="w", padx=18, pady=(0, 17))

    return label


card_total = buat_card(
    card_area,
    "Total Proyek",
    "0",
    BIRU
)

card_anggota = buat_card(
    card_area,
    "Anggota Tim",
    "0",
    HIJAU
)

card_tugas = buat_card(
    card_area,
    "Total Tugas",
    "0",
    BIRU
)

card_progres = buat_card(
    card_area,
    "Rata-rata Progres",
    "0%",
    "#D97706"
)


def update_card():
    try:
        db = koneksi()
        cursor = db.cursor()

        cursor.execute(
            "SELECT COUNT(*) FROM db_manajemen_proyek"
        )
        jumlah = cursor.fetchone()[0]
        card_total.config(text=str(jumlah))

        cursor.execute(
            "SELECT COUNT(DISTINCT anggota_proyek) FROM db_manajemen_proyek "
            "WHERE anggota_proyek IS NOT NULL AND anggota_proyek <> ''"
        )
        jumlah_anggota = cursor.fetchone()[0]
        card_anggota.config(text=str(jumlah_anggota))

        cursor.execute(
            "SELECT COUNT(*) FROM db_manajemen_proyek "
            "WHERE nama_tugas IS NOT NULL AND nama_tugas <> ''"
        )
        jumlah_tugas = cursor.fetchone()[0]
        card_tugas.config(text=str(jumlah_tugas))

        cursor.execute(
            "SELECT COALESCE(AVG(progres_persen), 0) FROM db_manajemen_proyek"
        )
        rata_progres = cursor.fetchone()[0]
        card_progres.config(text=f"{rata_progres:.0f}%")

        cursor.close()
        db.close()

    except mysql.connector.Error:
        pass


# ================= FORM INPUT =================

form = tk.Frame(
    halaman_data,
    bg=PUTIH,
    highlightbackground="#E2E8F0",
    highlightthickness=1
)
form.pack(fill="x", padx=32, pady=10)

tk.Label(
    form,
    text="Tambah Data Proyek",
    font=("Arial", 14, "bold"),
    bg=PUTIH,
    fg=NAVY
).grid(row=0, column=0, columnspan=4, sticky="w",
       padx=18, pady=15)


def buat_input(parent, teks, baris, kolom):
    tk.Label(
        parent,
        text=teks,
        font=("Arial", 10, "bold"),
        bg=PUTIH,
        fg="#334155"
    ).grid(row=baris, column=kolom, sticky="w",
           padx=18, pady=(5, 3))

    ent = tk.Entry(
        parent,
        font=("Arial", 11),
        bd=1,
        relief="solid"
    )
    ent.grid(
        row=baris + 1,
        column=kolom,
        sticky="ew",
        padx=18,
        pady=(0, 12),
        ipady=7
    )
    return ent


entry_nama = buat_input(form, "Nama Proyek", 1, 0)
entry_anggota = buat_input(form, "Nama Anggota Tim", 1, 1)
entry_mulai = buat_input(form, "Tanggal Mulai", 1, 2)
entry_selesai = buat_input(form, "Tanggal Selesai", 1, 3)

entry_tugas = buat_input(form, "Pembagian Tugas", 4, 0)
entry_deadline = buat_input(form, "Deadline Tugas", 4, 1)

tk.Label(
    form,
    text="Status Pekerjaan",
    font=("Arial", 10, "bold"),
    bg=PUTIH,
    fg="#334155"
).grid(row=4, column=2, sticky="w", padx=18, pady=(5, 3))

combo_status = ttk.Combobox(
    form,
    values=("Belum Mulai", "Dalam Pengerjaan", "Selesai", "Ditunda"),
    state="readonly",
    font=("Arial", 11)
)
combo_status.set("Belum Mulai")
combo_status.grid(row=5, column=2, sticky="ew", padx=18, pady=(0, 12), ipady=7)

tk.Label(
    form,
    text="Progres (%)",
    font=("Arial", 10, "bold"),
    bg=PUTIH,
    fg="#334155"
).grid(row=4, column=3, sticky="w", padx=18, pady=(5, 3))

progres_var = tk.IntVar(value=0)

spin_progres = tk.Spinbox(
    form,
    from_=0,
    to=100,
    textvariable=progres_var,
    font=("Arial", 11),
    bd=1,
    relief="solid"
)
spin_progres.grid(row=5, column=3, sticky="ew", padx=18, pady=(0, 12), ipady=7)

for i in range(4):
    form.grid_columnconfigure(i, weight=1)


# ================= TOMBOL =================

tombol_area = tk.Frame(form, bg=PUTIH)
tombol_area.grid(
    row=6,
    column=0,
    columnspan=4,
    sticky="w",
    padx=18,
    pady=(0, 15)
)


def tombol(parent, teks, warna, fungsi):
    return tk.Button(
        parent,
        text=teks,
        command=fungsi,
        bg=warna,
        fg="white",
        font=("Arial", 10, "bold"),
        relief="flat",
        cursor="hand2",
        padx=17,
        pady=9
    )


tombol(
    tombol_area,
    " + Tambah Proyek ",
    BIRU,
    tambah_data
).pack(side="left", padx=(0, 8))

tombol(
    tombol_area,
    "Perbarui Data",
    "#D97706",
    ubah_data
).pack(side="left", padx=8)

tombol(
    tombol_area,
    "Hapus Data",
    MERAH,
    hapus_data
).pack(side="left", padx=8)

tombol(
    tombol_area,
    "Refresh",
    HIJAU,
    reset_data
).pack(side="left", padx=8)


# ================= PENCARIAN =================

cari_area = tk.Frame(halaman_data, bg="#F1F5F9")
cari_area.pack(fill="x", padx=32, pady=(10, 5))

tk.Label(
    cari_area,
    text="Cari Proyek:",
    font=("Arial", 11, "bold"),
    bg="#F1F5F9",
    fg=NAVY
).pack(side="left", padx=(0, 10))

entry_cari = tk.Entry(
    cari_area,
    font=("Arial", 11),
    bd=1,
    relief="solid",
    width=35
)
entry_cari.pack(side="left", ipady=7)

tombol(
    cari_area,
    "Cari",
    BIRU,
    cari_data
).pack(side="left", padx=8)

entry_cari.bind("<Return>", lambda event: cari_data())


# ================= TABEL =================

tabel_frame = tk.Frame(
    halaman_data,
    bg=PUTIH,
    highlightbackground="#E2E8F0",
    highlightthickness=1
)
tabel_frame.pack(
    fill="both",
    expand=True,
    padx=32,
    pady=(5, 20)
)

tk.Label(
    tabel_frame,
    text="Daftar Data Proyek",
    font=("Arial", 14, "bold"),
    bg=PUTIH,
    fg=NAVY
).pack(anchor="w", padx=15, pady=12)

kolom = (
    "id_proyek",
    "nama_proyek",
    "anggota_proyek",
    "tanggal_mulai",
    "tanggal_selesai",
    "nama_tugas",
    "deadline_tugas",
    "status_pekerjaan",
    "progres_persen"
)

style = ttk.Style()
style.theme_use("clam")

style.configure(
    "Treeview",
    font=("Arial", 10),
    rowheight=32,
    background="white",
    fieldbackground="white"
)

style.configure(
    "Treeview.Heading",
    font=("Arial", 10, "bold"),
    background=NAVY,
    foreground="white",
    padding=10
)

style.map(
    "Treeview",
    background=[("selected", "#BFDBFE")],
    foreground=[("selected", NAVY)]
)

tabel = ttk.Treeview(
    tabel_frame,
    columns=kolom,
    show="headings"
)

judul_kolom = {
    "id_proyek": "ID",
    "nama_proyek": "Nama Proyek",
    "anggota_proyek": "Nama Anggota Tim",
    "tanggal_mulai": "Tanggal Mulai",
    "tanggal_selesai": "Tanggal Selesai",
    "nama_tugas": "Pembagian Tugas",
    "deadline_tugas": "Deadline Tugas",
    "status_pekerjaan": "Status Pekerjaan",
    "progres_persen": "Progres (%)"
}

for nama in kolom:
    tabel.heading(nama, text=judul_kolom[nama])

tabel.column("id_proyek", width=55, anchor="center")
tabel.column("nama_proyek", width=170)
tabel.column("anggota_proyek", width=150)
tabel.column("tanggal_mulai", width=115, anchor="center")
tabel.column("tanggal_selesai", width=115, anchor="center")
tabel.column("nama_tugas", width=170)
tabel.column("deadline_tugas", width=115, anchor="center")
tabel.column("status_pekerjaan", width=130, anchor="center")
tabel.column("progres_persen", width=90, anchor="center")

scroll_y = ttk.Scrollbar(
    tabel_frame,
    orient="vertical",
    command=tabel.yview
)

tabel.configure(yscrollcommand=scroll_y.set)

scroll_y.pack(side="right", fill="y", pady=(0, 10))
tabel.pack(fill="both", expand=True, padx=10, pady=(0, 10))

tabel.bind("<<TreeviewSelect>>", pilih_data)


# ================= JALANKAN =================

tampilkan_halaman("dashboard")

root.mainloop()
