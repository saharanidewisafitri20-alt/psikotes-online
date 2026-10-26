# Psikotes Online Python

Aplikasi web latihan psikotes berbasis Python tanpa instalasi Flask. Dapat dibuka di Google Chrome dan menyimpan hasil peserta ke SQLite.

## Isi aplikasi

- 15 paket Psikotes Umum
  - Tes verbal 30 soal
  - Aritmatika dan deret 25 soal
  - Penalaran logis 20 soal
  - Kraepelin atau Pauli 45 kolom
  - EPPS 225 pasangan
  - Wartegg 8 kotak
  - Tes grafis pohon, HTP, dan Draw A Man
- 15 paket CPNS
  - TWK 30 soal
  - TIU 35 soal
  - TKP 45 soal dengan skor perilaku
- Jawaban peserta tersimpan dalam data/results.sqlite3.
- Admin dapat melihat rincian jawaban, kunci, skor, dan mengunduh CSV.

## Menjalankan di Windows

1. Pastikan Python 3.10 atau lebih baru terpasang.
2. Klik dua kali JALANKAN_WEB_PSIKOTES.bat.
3. Buka Google Chrome dan masuk ke http://127.0.0.1:8000.
4. PIN admin bawaan adalah 123456.
5. Ganti PIN sebelum dibagikan dengan mengatur variabel: set PSIKOTES_ADMIN_PIN=PINBARU

## Agar dapat diakses beberapa orang pada Wi-Fi yang sama

1. Klik dua kali JALANKAN_WEB_PSIKOTES_LAN.bat.
2. Cari alamat IPv4 komputer yang menjalankan aplikasi dengan perintah ipconfig.
3. Peserta lain membuka http://ALAMAT-IP-KOMPUTER:8000 di Chrome.
4. Izinkan Python pada Windows Firewall jika diminta.

Database berada di komputer yang menjalankan aplikasi, sehingga semua jawaban peserta terkumpul di sana.

## Membuka dengan data seluler atau dari luar Wi-Fi

Alamat `127.0.0.1` hanya dapat dibuka di komputer yang menjalankan aplikasi. Agar peserta dapat membuka aplikasi dari data seluler melalui Google Chrome, aplikasi harus diunggah ke hosting online. File `render.yaml` dan `Procfile` sudah disiapkan untuk layanan hosting Python.

Langkah umum: buat akun hosting Python, unggah folder ini dari GitHub atau ZIP, pilih layanan web Python, masukkan perintah berikut, lalu gunakan URL HTTPS yang diberikan hosting:

python app.py --host 0.0.0.0 --port $PORT

Set variabel lingkungan PSIKOTES_ADMIN_PIN pada hosting. Setelah mendapat URL seperti `https://nama-aplikasi.example`, URL itu bisa dibuka melalui Chrome memakai Wi-Fi maupun data seluler dan dibagikan kepada banyak peserta. Jika hosting menggunakan penyimpanan sementara, gunakan database eksternal atau disk persisten agar hasil tidak hilang.

## Struktur

- app.py server Python dan halaman web
- generate_data.py pembuat 30 paket soal
- data/packages.json 15 paket umum dan 15 paket CPNS
- data/results.sqlite3 database hasil peserta
- JALANKAN_WEB_PSIKOTES.bat launcher lokal
- JALANKAN_WEB_PSIKOTES_LAN.bat launcher jaringan lokal

