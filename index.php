<?php
$conn = mysqli_connect(
    "localhost",
    "root",
    "",
    "manajemen_proyek"
);

if (!$conn) {
    die("Koneksi gagal: " . mysqli_connect_error());
}

$query = mysqli_query($conn, "SELECT * FROM db_manajemen_proyek");
?>

<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <title>Manajemen Proyek</title>
</head>
<body>

<h1>Data Manajemen Proyek</h1>

<table border="1" cellpadding="10">
    <tr>
        <th>ID Proyek</th>
        <th>Nama Proyek</th>
        <th>Nama Anggota Tim</th>
        <th>Tanggal Mulai</th>
        <th>Tanggal Selesai</th>
        <th>Pembagian Tugas</th>
        <th>Deadline Tugas</th>
        <th>Status Pekerjaan</th>
        <th>Progres</th>
    </tr>

    <?php while ($data = mysqli_fetch_assoc($query)) { ?>
    <tr>
        <td><?= $data['id_proyek']; ?></td>
        <td><?= $data['nama_proyek']; ?></td>
        <td><?= $data['anggota_proyek']; ?></td>
        <td><?= $data['tanggal_mulai']; ?></td>
        <td><?= $data['tanggal_selesai']; ?></td>
        <td><?= $data['nama_tugas']; ?></td>
        <td><?= $data['deadline_tugas']; ?></td>
        <td><?= $data['status_pekerjaan']; ?></td>
        <td><?= $data['progres_persen']; ?>%</td>
    </tr>
    <?php } ?>
</table>

</body>
</html>
