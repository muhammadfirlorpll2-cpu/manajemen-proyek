# ================= FORM INPUT MODERN =================

form = tk.Frame(content, bg=WHITE, padx=25, pady=22)
form.pack(fill="x", pady=15)

tk.Label(
    form,
    text="Tambah Proyek Baru",
    bg=WHITE,
    fg=NAVY,
    font=("Segoe UI", 16, "bold")
).pack(anchor="w")

tk.Label(
    form,
    text="Masukkan informasi proyek di bawah ini",
    bg=WHITE,
    fg=GRAY,
    font=("Segoe UI", 9)
).pack(anchor="w", pady=(3, 18))


def buat_input(parent, judul, nilai=""):
    frame = tk.Frame(parent, bg=WHITE)
    frame.pack(side="left", fill="x", expand=True, padx=8)

    tk.Label(
        frame,
        text=judul,
        bg=WHITE,
        fg=TEXT,
        font=("Segoe UI", 10, "bold")
    ).pack(anchor="w", pady=(0, 8))

    entry = tk.Entry(
        frame,
        font=("Segoe UI", 11),
        bg="#F8FAFC",
        fg=TEXT,
        relief="flat",
        highlightthickness=1,
        highlightbackground="#CBD5E1",
        highlightcolor=BLUE
    )

    entry.pack(fill="x", ipady=11)

    if nilai:
        entry.insert(0, nilai)

    return entry


input_frame = tk.Frame(form, bg=WHITE)
input_frame.pack(fill="x")

entry_anggota = buat_input(
    input_frame,
    "Jumlah Anggota",
    "Contoh: 5"
)

entry_mulai = buat_input(
    input_frame,
    "Tanggal Mulai",
    "2026-11-19"
)

entry_selesai = buat_input(
    input_frame,
    "Tanggal Selesai",
    "2026-11-30"
)

# Tombol simpan
tk.Button(
    form,
    text="＋  SIMPAN DATA PROYEK",
    bg=BLUE,
    fg=WHITE,
    activebackground=NAVY,
    activeforeground=WHITE,
    font=("Segoe UI", 10, "bold"),
    relief="flat",
    cursor="hand2",
    padx=20,
    pady=12,
    command=tambah_data
).pack(anchor="e", pady=(20, 0))