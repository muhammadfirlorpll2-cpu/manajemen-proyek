<?php
include 'koneksi.php';

$proyek = mysqli_num_rows(mysqli_query($conn, "SELECT * FROM db_manajemen_proyek"));
$anggota = mysqli_num_rows(mysqli_query($conn, "SELECT DISTINCT anggota_proyek FROM db_manajemen_proyek WHERE anggota_proyek IS NOT NULL AND anggota_proyek <> ''"));
$tugas = mysqli_num_rows(mysqli_query($conn, "SELECT * FROM db_manajemen_proyek WHERE nama_tugas IS NOT NULL AND nama_tugas <> ''"));
$status_selesai = mysqli_num_rows(mysqli_query($conn, "SELECT * FROM db_manajemen_proyek WHERE status_pekerjaan = 'Selesai'"));
?>

<!DOCTYPE html>
<html>
<head>
    <title>Dashboard Manajemen Proyek</title>
    <style>
        body {
            font-family: Arial;
            background: #f1f5f9;
            margin: 0;
        }
        header {
            background: #1e293b;
            color: white;
            padding: 20px;
        }
        .content {
            padding: 30px;
        }
        .cards {
            display: flex;
            gap: 20px;
            flex-wrap: wrap;
        }
        .card {
            background: white;
            padding: 25px;
            border-radius: 10px;
            flex: 1;
            min-width: 150px;
            text-align: center;
        }
        h2 {
            color: #2563eb;
        }
    </style>
</head>
<body>

<header>
    <h1>Dashboard Manajemen Proyek</h1>
</header>

<div class="content">
    <h2>Ringkasan Data</h2>

    <div class="cards">
        <div class="card">
            <h3>Total Proyek</h3>
            <h2><?= $proyek ?></h2>
        </div>

        <div class="card">
            <h3>Anggota Tim</h3>
            <h2><?= $anggota ?></h2>
        </div>

        <div class="card">
            <h3>Total Tugas</h3>
            <h2><?= $tugas ?></h2>
        </div>

        <div class="card">
            <h3>Tugas Selesai</h3>
            <h2><?= $status_selesai ?></h2>
        </div>
    </div>
</div>

</body>
</html>