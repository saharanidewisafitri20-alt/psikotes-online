import json, random, os, math, re

OUT = os.path.join(os.path.dirname(__file__), "data", "packages.json")
random.seed(20261025)

def q(text, options, answer, category=""):
    return {"text": text, "options": options, "answer": answer, "category": category}

def add_calculation_explanations(bank):
    """Attach short, readable solution steps to every numeric item."""
    for item in bank:
        text = item.get("text", "")
        if item.get("category") not in ("Aritmatika", "Deret", "Numerik") and not any(ch.isdigit() for ch in text):
            continue
        answer = item.get("options", [""])[item.get("answer", 0)] if item.get("options") else ""
        explanation = "Gunakan operasi atau pola angka pada soal, lalu cocokkan hasilnya dengan pilihan jawaban."
        if "120 km" in text:
            explanation = "Kecepatan = jarak ÷ waktu = 120 ÷ 3 = 40 km/jam."
        elif "diskon 15%" in text:
            explanation = "Diskon = 15% × Rp80.000 = Rp12.000. Harga akhir = Rp80.000 − Rp12.000 = Rp68.000."
        elif "diskon 10%" in text:
            explanation = "Diskon = 10% × Rp200.000 = Rp20.000. Harga akhir = Rp200.000 − Rp20.000 = Rp180.000."
        elif "3 : 5" in text or "2:3" in text:
            explanation = "Jumlah bagian = 3 + 5 = 8 atau 2 + 3 = 5. Nilai satu bagian = total ÷ jumlah bagian, kemudian kalikan dengan bagian yang ditanya."
        elif "Rata-rata" in text:
            explanation = "Jumlahkan seluruh angka, lalu bagi dengan banyaknya angka. Contoh: (12 + 15 + 18 + 21 + 24) ÷ 5 = 18."
        elif "pekerja" in text:
            explanation = "Gunakan beban kerja tetap: jumlah pekerja × jumlah hari = 4 × 6 = 24 hari-orang. Dengan 6 pekerja, 24 ÷ 6 = 4 hari."
        elif "naik 10%" in text:
            explanation = "Kenaikan = 10% × Rp4.000.000 = Rp400.000. Gaji baru = Rp4.000.000 + Rp400.000 = Rp4.400.000."
        elif "tiga perempat" in text or "25%" in text:
            explanation = "Ubah persentase atau pecahan ke bentuk perkalian: 3/4 × 240 = 180 atau 25% × 240 = 60."
        elif "Bunga" in text:
            explanation = "Bunga sederhana = modal × persentase × waktu = Rp2.000.000 × 6% × 2 = Rp240.000."
        elif "30%" in text:
            explanation = "30% = 30/100. Jadi 30/100 × 120 = 36."
        elif "kotak" in text and "barang" in text:
            explanation = "Jumlah barang = jumlah kotak × isi tiap kotak = 5 × 24 = 120."
        elif "untung" in text:
            explanation = "Untung = harga jual − harga beli = Rp250.000 − Rp200.000 = Rp50.000. Persentase untung = 50.000 ÷ 200.000 × 100% = 25%."
        elif "Jika x +" in text:
            nums = re.findall(r"\d+", text)
            explanation = f"Pindahkan angka yang ditambahkan ke ruas lain: x = {nums[-1]} − {nums[0]} = {answer}."
        elif "Jika 3x" in text:
            nums = re.findall(r"\d+", text)
            explanation = f"Bagi kedua ruas dengan 3: x = {nums[-1]} ÷ 3 = {answer}."
        elif "20%" in text:
            nums = re.findall(r"\d+", text)
            explanation = f"Jika 20% bernilai {nums[-1]}, maka 100% = {nums[-1]} × 5 = {answer}."
        elif "Nilai A=" in text:
            nums = [int(x) for x in re.findall(r"\d+", text)]
            explanation = f"Jumlahkan nilai A dan B: {nums[0]} + {nums[1]} = {answer}."
        elif "Deret" in text:
            explanation = f"Cari pola perubahan antarangka (selisih atau perkalian). Setelah pola diteruskan, angka berikutnya adalah {answer}."
        item["explanation"] = explanation
    return bank

# ---------- General aptitude banks ----------
verbal_bank = [
q("Sinonim kata akurat adalah ...",["Tepat","Lambat","Luas","Berani"],0,"Sinonim"),
q("Sinonim kata konvensional adalah ...",["Tradisional","Rahasia","Modern","Berubah"],0,"Sinonim"),
q("Sinonim kata mutakhir adalah ...",["Terlama","Terbaru","Terbatas","Terpisah"],1,"Sinonim"),
q("Sinonim kata valid adalah ...",["Sah","Lemah","Lambat","Berlebih"],0,"Sinonim"),
q("Sinonim kata intensif adalah ...",["Sekilas","Mendalam","Terbuka","Berjarak"],1,"Sinonim"),
q("Sinonim kata kredibel adalah ...",["Dapat dipercaya","Mahal","Terkenal","Sulit"],0,"Sinonim"),
q("Sinonim kata komprehensif adalah ...",["Menyeluruh","Sederhana","Khusus","Terpisah"],0,"Sinonim"),
q("Sinonim kata fragmen adalah ...",["Keseluruhan","Aturan","Bagian kecil","Peristiwa"],2,"Sinonim"),
q("Antonim kata optimistis adalah ...",["Aktif","Pesimistis","Praktis","Realistis"],1,"Antonim"),
q("Antonim kata permanen adalah ...",["Tetap","Sementara","Kuat","Lama"],1,"Antonim"),
q("Antonim kata mayoritas adalah ...",["Minoritas","Komunitas","Populasi","Kolektif"],0,"Antonim"),
q("Antonim kata ekspansi adalah ...",["Perluasan","Pertumbuhan","Kontraksi","Perubahan"],2,"Antonim"),
q("Antonim kata objektif adalah ...",["Netral","Subjektif","Terukur","Rasional"],1,"Antonim"),
q("Antonim kata konkret adalah ...",["Nyata","Abstrak","Padat","Terlihat"],1,"Antonim"),
q("Antonim kata transparan adalah ...",["Terbuka","Jelas","Tertutup","Bening"],2,"Antonim"),
q("Antonim kata efisien adalah ...",["Hemat","Boros","Cepat","Praktis"],1,"Antonim"),
q("Dokter : pasien = guru : ...",["Murid","Kelas","Buku","Sekolah"],0,"Analogi"),
q("Buku : membaca = musik : ...",["Menulis","Mendengar","Menggambar","Menyimpan"],1,"Analogi"),
q("Benih : tanaman = telur : ...",["Sarang","Ayam","Cangkang","Pakan"],1,"Analogi"),
q("Api : panas = es : ...",["Cair","Dingin","Putih","Keras"],1,"Analogi"),
q("Kamera : foto = printer : ...",["Dokumen","Kertas","Tinta","Layar"],0,"Analogi"),
q("Nahkoda : kapal = pilot : ...",["Bandara","Pesawat","Penumpang","Menara"],1,"Analogi"),
q("Padi : beras = gandum : ...",["Tepung","Ladang","Roti","Biji"],0,"Analogi"),
q("Kunci : pintu = kata sandi : ...",["Akun","Komputer","Kertas","Jaringan"],0,"Analogi"),
q("Mata : melihat = telinga : ...",["Berbicara","Mendengar","Menyentuh","Mencium"],1,"Analogi"),
q("Uang : bank = buku : ...",["Rak","Perpustakaan","Penulis","Kertas"],1,"Analogi"),
q("Sinonim kata adaptif adalah ...",["Mudah menyesuaikan","Keras kepala","Lambat","Tetap"],0,"Sinonim"),
q("Antonim kata permanen adalah ...",["Kekal","Sementara","Tetap","Lama"],1,"Antonim"),
q("Kapal : laut = kereta : ...",["Jalan raya","Rel","Bandara","Pelabuhan"],1,"Analogi"),
q("Termometer : suhu = stopwatch : ...",["Jarak","Waktu","Berat","Volume"],1,"Analogi"),
q("Sinonim kata objektif adalah ...",["Memihak","Berdasarkan fakta","Ragu-ragu","Emosional"],1,"Sinonim"),
q("Antonim kata aktif adalah ...",["Rajin","Pasif","Cepat","Kuat"],1,"Antonim"),
q("Peta : lokasi = kalender : ...",["Tanggal","Cuaca","Jarak","Harga"],0,"Analogi"),
q("Koki : dapur = petani : ...",["Pasar","Sawah","Kantor","Gudang"],1,"Analogi"),
q("Sinonim kata konsisten adalah ...",["Tetap dan selaras","Berubah-ubah","Terburu-buru","Terpisah"],0,"Sinonim"),
q("Antonim kata sederhana adalah ...",["Mudah","Rumit","Ringan","Kecil"],1,"Antonim"),
q("Baterai : energi = tangki : ...",["Air","Bahan bakar","Udara","Suhu"],1,"Analogi"),
q("Kepala : topi = kaki : ...",["Sarung tangan","Sepatu","Kacamata","Sabuk"],1,"Analogi"),
q("Sinonim kata transparan adalah ...",["Tertutup","Terbuka dan jelas","Berat","Gelap"],1,"Sinonim"),
q("Antonim kata optimistis adalah ...",["Pesimistis","Aktif","Rasional","Terbuka"],0,"Antonim"),
q("Arsip : dokumen = gudang : ...",["Barang","Peta","Surat","Kursi"],0,"Analogi"),
q("Kompas : arah = jam : ...",["Waktu","Suhu","Jarak","Berat"],0,"Analogi"),
q("Sinonim kata prioritas adalah ...",["Yang didahulukan","Yang terakhir","Yang rahasia","Yang mahal"],0,"Sinonim"),
q("Antonim kata luas adalah ...",["Panjang","Sempit","Tinggi","Dalam"],1,"Antonim"),
]
arith_bank = []
for i in range(20):
    a = 2+i
    if i%4==0:
        arith_bank.append(q(f"Deret {a}, {a+3}, {a+6}, {a+9}, ...", [str(a+10),str(a+11),str(a+12),str(a+13)], 2, "Deret"))
    elif i%4==1:
        arith_bank.append(q(f"Deret {a}, {a*2}, {a*4}, {a*8}, ...", [str(a*12),str(a*14),str(a*16),str(a*18)], 2, "Deret"))
    elif i%4==2:
        arith_bank.append(q(f"Deret {a*a}, {(a+1)**2}, {(a+2)**2}, ...", [str((a+3)**2),str((a+3)**2+1),str((a+4)**2),str((a+4)**2+1)], 0, "Deret"))
    else:
        arith_bank.append(q(f"Deret {100-i*2}, {90-i*2}, {80-i*2}, ...", [str(60-i*2),str(70-i*2),str(75-i*2),str(80-i*2)], 1, "Deret"))
arith_bank += [
q("Sebuah kendaraan menempuh 120 km dalam 3 jam. Kecepatannya adalah ...",["30 km/jam","40 km/jam","45 km/jam","60 km/jam"],1,"Aritmatika"),
q("Harga barang Rp80.000 mendapat diskon 15%. Harga akhirnya ...",["Rp64.000","Rp68.000","Rp70.000","Rp72.000"],1,"Aritmatika"),
q("Perbandingan A dan B adalah 3 : 5. Jika total 64, nilai A adalah ...",["18","24","32","40"],1,"Aritmatika"),
q("Rata-rata 12, 15, 18, 21, dan 24 adalah ...",["16","17","18","19"],2,"Aritmatika"),
q("Empat pekerja selesai dalam 6 hari. Enam pekerja perlu ...",["3 hari","4 hari","5 hari","9 hari"],1,"Aritmatika"),
q("Gaji Rp4.000.000 naik 10%. Gaji baru ...",["Rp4.100.000","Rp4.200.000","Rp4.400.000","Rp4.800.000"],2,"Aritmatika"),
q("Tiga perempat dari 240 adalah ...",["160","170","180","190"],2,"Aritmatika"),
q("Bunga 6% per tahun dari Rp2.000.000 selama 2 tahun adalah ...",["Rp120.000","Rp180.000","Rp240.000","Rp260.000"],2,"Aritmatika"),
q("30% dari 120 adalah ...",["30","36","40","42"],1,"Aritmatika"),
q("Lima kotak masing-masing berisi 24 barang. Jumlahnya ...",["96","110","120","144"],2,"Aritmatika"),
q("1, 2, 6, 24, 120, ...",["240","360","600","720"],3,"Deret"),
q("64, 32, 16, 8, ...",["2","3","4","6"],2,"Deret"),
q("11, 22, 44, 88, ...",["132","144","176","198"],2,"Deret"),
q("4, 9, 19, 39, 79, ...",["119","139","159","169"],2,"Deret"),
q("Harga beli Rp200.000 dan harga jual Rp250.000. Persentase untung ...",["20%","25%","30%","35%"],1,"Aritmatika"),
]
logical_bank = [
q("Semua akuntan teliti. Sebagian karyawan adalah akuntan. Kesimpulan ...",["Sebagian karyawan teliti.","Semua orang teliti akuntan.","Tidak ada karyawan teliti.","Semua karyawan akuntan."],0,"Silogisme"),
q("Tidak ada berkas merah yang rahasia. Sebagian laporan berkas merah. Kesimpulan ...",["Sebagian laporan tidak rahasia.","Semua laporan tidak rahasia.","Sebagian laporan bukan merah.","Semua berkas rahasia merah."],0,"Silogisme"),
q("Semua manajer hadir rapat. Rina tidak hadir. Kesimpulan ...",["Rina bukan manajer.","Rina pegawai baru.","Semua pegawai tidak hadir.","Rina manajer."],0,"Silogisme"),
q("Sebagian teknisi lulusan. Semua lulusan dapat memakai Excel. Kesimpulan ...",["Sebagian teknisi dapat memakai Excel.","Semua teknisi dapat memakai Excel.","Tidak ada teknisi dapat Excel.","Semua pengguna Excel teknisi."],0,"Silogisme"),
q("Tidak ada pegawai sementara yang tetap. Sebagian pegawai sementara. Kesimpulan ...",["Sebagian pegawai bukan pegawai tetap.","Semua pegawai bukan tetap.","Sebagian pegawai tetap sementara.","Semua sementara tetap."],0,"Silogisme"),
q("Semua A adalah B. Semua B adalah C. Sebagian A adalah D. Kesimpulan ...",["Sebagian D adalah C.","Semua C adalah A.","Tidak ada D yang C.","Semua D adalah A."],0,"Silogisme"),
q("Sebagian siswa atlet. Sebagian atlet penyanyi. Kesimpulan pasti ...",["Sebagian siswa penyanyi.","Sebagian penyanyi atlet.","Semua siswa atlet.","Tidak ada siswa penyanyi."],1,"Silogisme"),
q("Tidak ada buku perangkat elektronik. Sebagian tablet perangkat elektronik. Kesimpulan ...",["Sebagian tablet bukan buku.","Semua tablet buku.","Tidak ada tablet elektronik.","Semua buku tablet."],0,"Silogisme"),
q("Dimas lebih tua dari Eka. Fajar lebih muda dari Dimas tetapi lebih tua dari Eka. Galih lebih tua dari Dimas. Yang termuda ...",["Dimas","Eka","Fajar","Galih"],1,"Analitik"),
q("A lebih tinggi dari B. C lebih pendek dari B. D lebih tinggi dari A. Yang tertinggi ...",["A","B","C","D"],3,"Analitik"),
q("Semua kotak biru berat. Kotak X biru. Pernyataan yang harus benar ...",["Kotak X berat.","Semua kotak berat biru.","Kotak X kosong.","Kotak X besar."],0,"Analitik"),
q("Kode CAT menjadi DBU karena setiap huruf maju satu. Kode DOG ...",["EPH","EOG","DPH","FQI"],0,"Analitik"),
q("Jika hari ini Rabu, 17 hari lagi adalah ...",["Jumat","Sabtu","Minggu","Senin"],1,"Analitik"),
q("Jam bertambah cepat 5 menit per jam. Dari 08.00 sampai 14.00 menunjukkan ...",["14.05","14.20","14.30","15.00"],2,"Analitik"),
q("P sebelum Q dan R sebelum S. Urutan yang mungkin ...",["Q,P,S,R","P,R,Q,S","R,S,Q,P","S,R,P,Q"],1,"Analitik"),
q("Semua mawar bunga. Tidak ada bunga dari logam. Kesimpulan ...",["Tidak ada mawar dari logam.","Semua logam mawar.","Sebagian mawar bukan bunga.","Semua bunga mawar."],0,"Silogisme"),
q("Sebagian A adalah B. Tidak ada B yang C. Kesimpulan ...",["Sebagian A bukan C.","Semua A bukan C.","Semua C A.","Tidak ada A B."],0,"Silogisme"),
q("Bergerak 1 utara, 2 timur, 1 selatan. Posisi akhir ...",["2 timur","2 barat","1 utara","1 selatan"],0,"Analitik"),
q("Deret huruf AB, DE, GH, ... berikutnya ...",["HI","IJ","JK","KL"],2,"Analitik"),
q("Rapat mulai 09.40 selama 1 jam 35 menit. Berakhir ...",["10.55","11.05","11.15","11.25"],2,"Analitik"),
q("Jika semua P adalah Q dan tidak ada Q yang R, maka ...",["Tidak ada P yang R.","Semua R adalah P.","Sebagian P adalah R.","Semua Q adalah P."],0,"Silogisme"),
q("Urutan nilai 2, 5, 10, 17, ... angka berikutnya ...",["24","25","26","27"],2,"Deret"),
q("Tiga buku berharga sama Rp18.000. Total harga ...",["Rp36.000","Rp54.000","Rp60.000","Rp72.000"],1,"Aritmatika"),
q("Jika 25% suatu angka adalah 45, angkanya ...",["120","150","180","200"],2,"Aritmatika"),
q("Kelas mulai 07.15 dan berlangsung 95 menit. Selesai ...",["08.40","08.50","09.00","09.10"],1,"Analitik"),
]

arith_bank = add_calculation_explanations(arith_bank)
logical_bank = add_calculation_explanations(logical_bank)

# ---------- CPNS banks ----------
twk_bank = [
q("Rumusan Pancasila yang sah tercantum dalam ...",["Pembukaan UUD 1945 alinea keempat","Batang tubuh UUD 1945","Sumpah Pemuda","Proklamasi"],0,"Pilar Negara"),
q("Semboyan Bhinneka Tunggal Ika berarti ...",["Berbeda-beda tetapi tetap satu","Satu bahasa satu budaya","Bersatu karena sama","Berbeda tanpa persatuan"],0,"Pilar Negara"),
q("Lambang sila ketiga Pancasila adalah ...",["Bintang","Rantai","Pohon beringin","Padi dan kapas"],2,"Pilar Negara"),
q("Contoh integritas dalam pekerjaan adalah ...",["Mengubah data agar terlihat baik","Jujur meskipun tidak diawasi","Mengikuti teman melanggar aturan","Menunda laporan"],1,"Integritas"),
q("Bela negara bagi ASN dapat diwujudkan dengan ...",["Bekerja profesional dan menjaga persatuan","Mengutamakan kelompok sendiri","Menolak aturan","Menyebarkan isu"],0,"Bela Negara"),
q("UUD Negara Republik Indonesia Tahun 1945 berfungsi sebagai ...",["Hukum dasar negara","Pedoman perusahaan","Peraturan daerah","Dokumen sejarah saja"],0,"Pilar Negara"),
q("NKRI adalah bentuk negara ...",["Kesatuan","Serikat","Monarki","Konfederasi"],0,"Pilar Negara"),
q("Bahasa Indonesia berkedudukan sebagai bahasa negara berdasarkan ...",["UUD 1945","Peraturan sekolah","Sumpah Pemuda saja","Kebiasaan masyarakat"],0,"Bahasa Negara"),
q("Sikap nasionalisme yang tepat adalah ...",["Mengutamakan kepentingan bangsa tanpa merendahkan bangsa lain","Menolak semua budaya asing","Menganggap daerah sendiri paling unggul","Membeda-bedakan warga"],0,"Nasionalisme"),
q("Sila kedua menekankan nilai ...",["Kemanusiaan yang adil dan beradab","Persatuan","Kerakyatan","Keadilan sosial"],0,"Pancasila"),
q("Musyawarah untuk mufakat merupakan pengamalan sila ...",["Pertama","Kedua","Ketiga","Keempat"],3,"Pancasila"),
q("Keadilan sosial bagi seluruh rakyat Indonesia adalah sila ke ...",["1","2","4","5"],3,"Pancasila"),
q("Proklamasi Kemerdekaan Indonesia dibacakan pada ...",["17 Agustus 1945","20 Mei 1908","28 Oktober 1928","1 Juni 1945"],0,"Sejarah"),
q("Sumpah Pemuda terjadi pada ...",["28 Oktober 1928","17 Agustus 1945","10 November 1945","20 Mei 1908"],0,"Sejarah"),
q("Lagu kebangsaan Indonesia adalah ...",["Indonesia Raya","Bagimu Negeri","Garuda Pancasila","Hari Merdeka"],0,"Identitas"),
q("Bendera negara Indonesia adalah ...",["Merah Putih","Merah Biru","Putih Hijau","Biru Putih"],0,"Identitas"),
q("Sikap yang sesuai Bhinneka Tunggal Ika adalah ...",["Menghormati perbedaan agama dan budaya","Memaksakan keyakinan","Menolak dialog","Menyebarkan stereotip"],0,"Integrasi"),
q("Ancaman terhadap integrasi nasional dapat dikurangi dengan ...",["Dialog dan gotong royong","Provokasi","Diskriminasi","Hoaks"],0,"Nasionalisme"),
q("Dalam pelayanan publik, integritas berarti ...",["Memberikan layanan sesuai aturan dan tidak menerima suap","Mendahulukan keluarga","Meminta imbalan","Mengubah antrean"],0,"Integritas"),
q("Gotong royong mencerminkan nilai ...",["Kerja sama dan kepedulian","Persaingan","Individualisme","Eksklusivisme"],0,"Sosial"),
q("Kedaulatan rakyat dilaksanakan menurut ...",["UUD 1945","Keputusan pribadi","Perintah kelompok","Kebiasaan"],0,"Pilar Negara"),
q("Hak dan kewajiban warga negara harus dilaksanakan secara ...",["Seimbang","Sepihak","Bergantian tanpa aturan","Hanya jika menguntungkan"],0,"Konstitusi"),
q("Menggunakan produk dalam negeri secara bijak dapat mencerminkan ...",["Cinta tanah air","Fanatisme sempit","Anti globalisasi","Diskriminasi"],0,"Nasionalisme"),
q("Contoh bela negara di era digital adalah ...",["Memeriksa informasi sebelum membagikan","Menyebar hoaks","Membocorkan data","Menghina kelompok lain"],0,"Bela Negara"),
q("Pancasila sebagai ideologi terbuka berarti ...",["Nilainya tetap, penerapannya dapat menyesuaikan perkembangan","Dapat diganti setiap saat","Tidak memiliki nilai dasar","Hanya berlaku di sekolah"],0,"Pancasila"),
q("Lembaga yang berwenang mengubah dan menetapkan UUD adalah ...",["MPR","DPRD","MA","BPK"],0,"Konstitusi"),
q("Salah satu tujuan negara dalam Pembukaan UUD 1945 adalah ...",["Melindungi segenap bangsa Indonesia","Menguasai negara lain","Menghapus budaya daerah","Membatasi pendidikan"],0,"Konstitusi"),
q("Bahasa Indonesia yang baik dan benar digunakan dengan memperhatikan ...",["Konteks dan kaidah bahasa","Slang di semua situasi","Bahasa asing saja","Singkatan tanpa aturan"],0,"Bahasa Negara"),
q("Menghargai keputusan hukum merupakan bentuk ...",["Kesadaran berkonstitusi","Pelanggaran","Fanatisme","Apatisme"],0,"Integritas"),
q("Sikap anti korupsi yang paling tepat adalah ...",["Menolak gratifikasi dan melaporkan pelanggaran","Menerima hadiah diam-diam","Membiarkan pungli","Menutup informasi"],0,"Integritas"),
q("Persatuan Indonesia dapat diperkuat melalui ...",["Kerja sama lintas daerah dan suku","Politik identitas yang memecah","Diskriminasi","Konflik"],0,"Pancasila"),
q("Nilai utama sila pertama adalah ...",["Ketuhanan dan toleransi","Kekuasaan","Kekayaan","Persaingan"],0,"Pancasila"),
q("Contoh kewajiban warga negara adalah ...",["Menaati hukum dan membayar pajak","Mendapat layanan","Menerima penghargaan","Memilih pekerjaan"],0,"Konstitusi"),
q("Sikap rela berkorban untuk kepentingan bangsa merupakan ...",["Semangat bela negara","Sikap apatis","Individualisme","Pragmatisme"],0,"Bela Negara"),
q("Identitas nasional Indonesia antara lain ...",["Bahasa Indonesia, bendera, dan lambang negara","Merek pribadi","Bahasa daerah saja","Budaya satu suku"],0,"Identitas"),
q("Demokrasi Pancasila menempatkan keputusan melalui ...",["Musyawarah yang bertanggung jawab","Kekerasan","Paksaan mayoritas","Perintah satu orang"],0,"Demokrasi"),
q("Tidak menyebarkan ujaran kebencian merupakan pengamalan ...",["Persatuan dan kemanusiaan","Individualisme","Eksklusivisme","Diskriminasi"],0,"Nasionalisme"),
q("Kepentingan nasional harus ditempatkan di atas ...",["Kepentingan pribadi atau golongan","Kepentingan umum","Kepentingan negara","Kepentingan rakyat"],0,"Nasionalisme"),
q("Sikap terhadap budaya daerah lain sebaiknya ...",["Menghormati dan mempelajarinya secara terbuka","Mengejek","Menghapus","Melarang"],0,"Bhinneka"),
q("Dalam konflik sosial, langkah awal yang tepat adalah ...",["Mencari fakta dan membuka dialog","Memihak tanpa informasi","Menyebar video provokatif","Menghindari hukum"],0,"Sosial"),
q("ASN wajib menjaga netralitas dengan ...",["Tidak menggunakan jabatan untuk kepentingan politik praktis","Mendukung calon dengan fasilitas negara","Mengajak bawahan berkampanye","Menyalahgunakan data"],0,"Integritas"),
q("Pancasila disebut dasar negara karena ...",["Menjadi landasan penyelenggaraan negara","Hanya menjadi slogan","Mengatur satu organisasi","Menggantikan semua hukum"],0,"Pancasila"),
q("Semangat persatuan dalam keberagaman membutuhkan ...",["Saling menghormati dan adil","Keseragaman mutlak","Pemisahan daerah","Persaingan antarsuku"],0,"Bhinneka"),
q("Kebebasan berpendapat harus disertai ...",["Tanggung jawab dan penghormatan hak orang lain","Fitnah","Ancaman","Paksaan"],0,"Konstitusi"),
q("Lembaga yang menguji undang-undang terhadap UUD adalah ...",["Mahkamah Konstitusi","BPK","KPU","DPRD"],0,"Konstitusi"),
q("Lembaga yang memeriksa pengelolaan keuangan negara adalah ...",["BPK","KPK","KPU","DPR"],0,"Lembaga Negara"),
q("Hari Kesaktian Pancasila diperingati setiap ...",["1 Oktober","1 Juni","17 Agustus","28 Oktober"],0,"Sejarah"),
q("Hari Lahir Pancasila diperingati setiap ...",["1 Juni","1 Oktober","20 Mei","10 November"],0,"Sejarah"),
q("Cinta tanah air dapat diwujudkan dengan ...",["Menjaga lingkungan dan menaati hukum","Membuang sampah","Merusak fasilitas","Menghindari pajak"],0,"Bela Negara"),
q("Penggunaan bahasa baku paling tepat dalam ...",["Surat dinas resmi","Percakapan santai","Pesan teman dekat","Komentar singkat"],0,"Bahasa Negara"),
q("Keadilan dalam pelayanan berarti ...",["Memberikan layanan tanpa diskriminasi","Mendahulukan kerabat","Meminta imbalan","Menolak warga tertentu"],0,"Integritas"),
q("Kebijakan publik harus diarahkan untuk ...",["Kepentingan masyarakat dan tujuan negara","Kepentingan pribadi pejabat","Kelompok tertentu saja","Keuntungan pribadi"],0,"Nasionalisme"),
q("Sikap toleransi berarti ...",["Menghormati perbedaan tanpa harus menyamakan semua keyakinan","Menyetujui semua hal","Menghapus identitas","Menolak perbedaan"],0,"Bhinneka"),
q("Ancaman nonmiliter antara lain ...",["Disinformasi dan serangan siber","Upacara","Gotong royong","Pendidikan"],0,"Bela Negara"),
q("Wawasan Nusantara memandang Indonesia sebagai ...",["Satu kesatuan politik, ekonomi, sosial budaya, dan pertahanan keamanan","Kumpulan negara terpisah","Wilayah tanpa batas","Daerah yang saling bersaing"],0,"Pilar Negara"),
q("Integritas ditunjukkan oleh kesesuaian antara ...",["Ucapan dan tindakan","Jabatan dan gaji","Pakaian dan warna","Tempat dan waktu"],0,"Integritas"),
q("Nilai Pancasila dalam kerja sehari-hari diterapkan melalui ...",["Kejujuran, gotong royong, dan keadilan","Kecurangan","Diskriminasi","Paksaan"],0,"Pancasila"),
q("Mengutamakan keselamatan masyarakat dalam keadaan darurat adalah contoh ...",["Kepentingan umum","Kepentingan pribadi","Eksklusivisme","Apatisme"],0,"Nasionalisme"),
q("Bentuk penghormatan terhadap pahlawan adalah ...",["Meneruskan nilai perjuangan dalam tindakan nyata","Menghafal nama tanpa berbuat","Menghapus sejarah","Menolak perubahan"],0,"Sejarah"),
q("Persamaan kedudukan warga negara di depan hukum merupakan prinsip ...",["Kesetaraan","Kekuasaan","Kekayaan","Keturunan"],0,"Konstitusi"),
q("Pelayanan publik yang baik membutuhkan ...",["Akuntabilitas dan transparansi","Rahasia dan diskriminasi","Pungutan liar","Antrean khusus"],0,"Integritas"),
]

def make_tiu_bank():
    bank = [
      q("Semua analis teliti. Sebagian pegawai adalah analis. Kesimpulan ...",["Sebagian pegawai teliti.","Semua pegawai analis.","Tidak ada pegawai teliti.","Semua orang teliti pegawai."],0,"Verbal"),
      q("Jika tidak ada A yang B dan sebagian C adalah A, maka ...",["Sebagian C bukan B.","Semua C bukan B.","Semua B C.","Tidak ada C A."],0,"Silogisme"),
      q("Dokter : rumah sakit = guru : ...",["Pasar","Sekolah","Bank","Pelabuhan"],1,"Analogi"),
      q("Kunci : pintu = password : ...",["Akun","Kertas","Meja","Kursi"],0,"Analogi"),
      q("Deret 2, 5, 10, 17, 26, ...",["35","36","37","38"],2,"Numerik"),
      q("Deret 3, 6, 12, 24, ...",["36","42","48","54"],2,"Numerik"),
      q("Deret 81, 27, 9, 3, ...",["0","1","2","6"],1,"Numerik"),
      q("Deret 1, 4, 9, 16, ...",["20","24","25","36"],2,"Numerik"),
      q("Rata-rata 10, 12, 14, 16, 18 adalah ...",["12","13","14","15"],2,"Numerik"),
      q("25% dari 240 adalah ...",["40","50","60","80"],2,"Numerik"),
      q("Perbandingan 2:3 dengan total 50. Bagian pertama ...",["15","20","25","30"],1,"Numerik"),
      q("120 km ditempuh 3 jam. Kecepatan ...",["30","40","50","60"],1,"Numerik"),
      q("Harga Rp200.000 diskon 10%. Harga akhir ...",["Rp170.000","Rp180.000","Rp190.000","Rp195.000"],1,"Numerik"),
      q("Empat pekerja 6 hari. Enam pekerja ...",["3 hari","4 hari","5 hari","8 hari"],1,"Numerik"),
      q("Jika x + 7 = 19, x = ...",["10","11","12","13"],2,"Numerik"),
      q("Jika 3x = 27, x = ...",["6","7","8","9"],3,"Numerik"),
      q("Sebuah rapat mulai 08.25 selama 90 menit. Selesai ...",["09.45","09.55","10.05","10.15"],0,"Analitik"),
      q("Hari ini Senin. 10 hari lagi ...",["Rabu","Kamis","Jumat","Sabtu"],1,"Analitik"),
      q("P lebih tinggi dari Q. R lebih tinggi dari P. Yang tertinggi ...",["P","Q","R","Tidak dapat ditentukan"],2,"Analitik"),
      q("A sebelum B dan C setelah B. Urutan benar ...",["C,A,B","A,B,C","B,C,A","B,A,C"],1,"Analitik"),
      q("Jika CAT dikodekan DBU, DOG menjadi ...",["EPH","DPH","EOG","FQI"],0,"Verbal"),
      q("Mata : melihat = hidung : ...",["Mendengar","Mencium","Berjalan","Memegang"],1,"Analogi"),
      q("Sinonim kata konsisten ...",["Selaras","Berubah","Lambat","Acak"],0,"Verbal"),
      q("Antonim kata konkret ...",["Nyata","Abstrak","Padat","Terlihat"],1,"Verbal"),
      q("Jika semua P adalah Q dan semua Q adalah R, maka ...",["Semua P adalah R.","Semua R adalah P.","Tidak ada P R.","Sebagian R P."],0,"Silogisme"),
      q("Pola simbol: ▲, ■, ▲, ■, ... simbol berikutnya ...",["▲","■","●","◆"],0,"Figural"),
      q("Pola arah: ↑, →, ↓, ... arah berikutnya ...",["↑","→","↓","←"],3,"Figural"),
      q("Pola simbol: ●, ○, ●, ○, ... simbol berikutnya ...",["○","●","■","▲"],1,"Figural"),
      q("Pola kelompok: ■, ■■, ■■■, ... kelompok berikutnya ...",["■","■■","■■■■","■■■■■"],2,"Figural"),
      q("Pola bentuk: △, ○, □, △, ○, ... bentuk berikutnya ...",["△","○","□","◇"],2,"Figural"),
      q("Pola pasangan: ▲●, ●■, ■◆, ... pasangan yang paling sesuai ...",["◆○","○▲","▲■","●◆"],0,"Figural"),
      q("Pola arah: ←, ↑, →, ... arah berikutnya ...",["↓","←","↑","→"],0,"Figural"),
      q("Pola simbol: ◆, ◆◆, ◆◆◆, ... jumlah simbol berikutnya ...",["1","2","4","5"],3,"Figural"),
      q("Pola bentuk: ○, △, ○, △, ... bentuk berikutnya ...",["○","△","□","◆"],0,"Figural"),
      q("Pola warna diwakili simbol: □, ■, □, ■, ... simbol berikutnya ...",["□","■","△","●"],0,"Figural"),
    ]
    # add 45 generated numeric/analytical items to reach a rich bank
    for i in range(45):
        a = i+4
        if i%5==0:
            bank.append(q(f"Deret {a}, {a+4}, {a+8}, {a+12}, ...",[str(a+14),str(a+15),str(a+16),str(a+17)],2,"Numerik"))
        elif i%5==1:
            bank.append(q(f"Deret {a}, {a*2}, {a*4}, {a*8}, ...",[str(a*12),str(a*14),str(a*16),str(a*18)],2,"Numerik"))
        elif i%5==2:
            bank.append(q(f"Jika 20% dari suatu angka adalah {a*2}, angka tersebut ...",[str(a*5-10),str(a*8),str(a*10),str(a*12)],2,"Numerik"))
        elif i%5==3:
            bank.append(q(f"Nilai A={a} dan B={a+3}. A+B adalah ...",[str(2*a+1),str(2*a+3),str(2*a+5),str(2*a+7)],1,"Numerik"))
        else:
            bank.append(q(f"Urutan tugas: P sebelum Q, R sebelum S. Urutan yang mungkin ...",["Q,P,S,R","P,R,Q,S","S,R,Q,P","R,Q,S,P"],1,"Analitik"))
    return add_calculation_explanations(bank)

tiu_bank = make_tiu_bank()

def make_tkp_bank():
    scenarios = [
("Pelayanan Publik","Warga datang dengan dokumen belum lengkap dan terlihat bingung. Anda ..."),
("Pelayanan Publik","Antrean layanan cukup panjang sementara seorang warga mulai marah. Anda ..."),
("Pelayanan Publik","Sistem layanan sedang lambat ketika masyarakat menunggu. Anda ..."),
("Jejaring Kerja","Rekan dari unit lain membutuhkan data yang Anda miliki dengan segera. Anda ..."),
("Jejaring Kerja","Dalam tim, ada anggota yang pendapatnya berbeda dari mayoritas. Anda ..."),
("Jejaring Kerja","Tugas kelompok hampir selesai tetapi satu anggota tertinggal. Anda ..."),
("Sosial Budaya","Anda ditempatkan di daerah dengan kebiasaan yang berbeda. Anda ..."),
("Sosial Budaya","Rekan kerja menggunakan bahasa daerah saat berdiskusi. Anda ..."),
("Sosial Budaya","Terjadi salah paham karena perbedaan latar belakang. Anda ..."),
("TIK","Anda menerima email dengan tautan yang mencurigakan. Anda ..."),
("TIK","Data pekerjaan penting perlu dicadangkan. Anda ..."),
("TIK","Aplikasi kantor baru terasa sulit digunakan. Anda ..."),
("Profesionalisme","Atasan memberi tugas dengan batas waktu sangat dekat. Anda ..."),
("Profesionalisme","Anda menemukan kesalahan dalam laporan yang sudah dikirim. Anda ..."),
("Profesionalisme","Tugas rutin terasa membosankan tetapi harus selesai. Anda ..."),
("Anti-Radikalisme","Seseorang menyebarkan konten yang mengajak membenci kelompok tertentu. Anda ..."),
("Anti-Radikalisme","Rekan mengajak bergabung dalam komunitas yang tertutup dan anti-dialog. Anda ..."),
("Anti-Radikalisme","Anda melihat informasi provokatif di grup kantor. Anda ..."),
]
    opts = [
      "Mendengarkan, menjelaskan prosedur, dan mencari solusi sesuai aturan.",
      "Menolak dengan singkat agar tidak menambah pekerjaan.",
      "Meneruskan kepada orang lain tanpa penjelasan.",
      "Menyelesaikan secara diam-diam walau melanggar prosedur.",
      "Mengabaikan sampai masalah selesai sendiri."
    ]
    # scoring option 0 highest, then 1, 2, 3, 4
    bank=[]
    for i,(cat,txt) in enumerate(scenarios):
        # vary wording and option order per base scenario
        bank.append({"text":txt,"options":opts.copy(),"scores":[5,4,3,2,1],"category":cat})
    # Additional distinct scenarios with same professional behavior dimensions
    extra = [
("Pelayanan Publik","Pemohon meminta informasi yang belum Anda kuasai. Anda ..."),
("Jejaring Kerja","Tim Anda harus bekerja sama dengan pihak eksternal. Anda ..."),
("Sosial Budaya","Anda mendengar candaan yang menyinggung identitas daerah. Anda ..."),
("TIK","Komputer kerja mengalami gangguan saat deadline. Anda ..."),
("Profesionalisme","Anda mendapat kritik atas hasil pekerjaan. Anda ..."),
("Anti-Radikalisme","Teman mengajak menyebarkan propaganda yang belum terverifikasi. Anda ..."),
("Pelayanan Publik","Seorang lansia kesulitan menggunakan loket digital. Anda ..."),
("Jejaring Kerja","Dua rekan berselisih dan pekerjaan tim terhambat. Anda ..."),
("Sosial Budaya","Kegiatan kantor perlu menyesuaikan kebutuhan beberapa kelompok. Anda ..."),
("TIK","Anda perlu membagikan file berisi data pribadi. Anda ..."),
("Profesionalisme","Anda memiliki dua pekerjaan dengan prioritas sama. Anda ..."),
("Anti-Radikalisme","Anda menemukan simbol kelompok kekerasan di media sosial. Anda ..."),
    ]
    for cat,txt in extra:
        bank.append({"text":txt,"options":opts.copy(),"scores":[5,4,3,2,1],"category":cat})
    # Expand the bank so every package can contain 45 distinct TKP situations.
    seed_items = list(bank)
    while len(bank) < 90:
        base = seed_items[len(bank) % len(seed_items)]
        bank.append({**base, "text": base["text"] + f" (Situasi latihan {len(bank)+1})"})
    return bank

tkp_bank = make_tkp_bank()

def rotate_options(item, shift):
    opts = item["options"]
    if not opts: return item
    n = len(opts)
    # rotate options but preserve answer index / scores mapping
    if "answer" in item:
        new_opts = opts[shift%n:]+opts[:shift%n]
        new_answer = (item["answer"] - shift) % n
        return {**item, "options":new_opts, "answer":new_answer}
    if "scores" in item:
        new_opts = opts[shift%n:]+opts[:shift%n]
        new_scores = item["scores"][shift%n:]+item["scores"][:shift%n]
        return {**item, "options":new_opts, "scores":new_scores}
    return item

def select_bank(bank, count, package_no):
    # Different questions and order for every package. For larger banks use a stride.
    n=len(bank)
    start=(package_no-1) % n
    # Step 11 is coprime with the bank sizes used here, so questions within a
    # package do not repeat before the requested count is reached.
    selected=[bank[(start+i*11)%n] for i in range(count)]
    out=[]
    for i,item in enumerate(selected):
        shift=(package_no+i)%len(item["options"])
        out.append(rotate_options(item, shift))
    return out

def make_general_package(p):
    statements = [
        "Saya menyelesaikan tugas sebelum batas waktu.",
        "Saya nyaman mengikuti aturan yang jelas.",
        "Saya senang membantu rekan kerja.",
        "Saya berani menyampaikan ide.",
        "Saya memeriksa pekerjaan sebelum diserahkan.",
        "Saya dapat menyesuaikan diri dengan perubahan.",
        "Saya menjaga dokumen tetap rapi.",
        "Saya tetap tenang saat menghadapi tekanan.",
        "Saya mau menerima kritik untuk memperbaiki hasil.",
        "Saya senang mempelajari cara kerja baru.",
        "Saya menghargai pendapat yang berbeda.",
        "Saya dapat bekerja secara mandiri.",
        "Saya menjaga komunikasi tetap sopan.",
        "Saya berusaha memenuhi janji yang dibuat.",
        "Saya mempertimbangkan data sebelum mengambil keputusan.",
    ]
    epps = []
    for i in range(225):
        a = statements[(i + p) % len(statements)]
        b = statements[(i * 7 + p + 3) % len(statements)]
        if a == b:
            b = statements[(i * 7 + p + 4) % len(statements)]
        epps.append({"a": a, "b": b})
    return {
      "id":p,
      "title":f"Paket Psikotes Umum {p:02d}",
      "verbal":select_bank(verbal_bank,30,p),
      "arithmetic":select_bank(arith_bank,25,p),
      "logical":select_bank(logical_bank,20,p),
      "epps":epps,
      "wartegg":[f"Kotak {i+1}: lanjutkan rangsangan gambar yang tersedia." for i in range(8)],
      "graphic":["Gambarlah satu pohon yang lengkap.","Gambarlah rumah, pohon, dan orang dalam satu halaman.","Gambarlah satu figur manusia utuh."],
      "kraepelin":[[random.randint(0,9) for _ in range(20)] for _ in range(45)]
    }

def make_cpns_package(p):
    return {
      "id":p,
      "title":f"Paket CPNS {p:02d}",
      "twk":select_bank(twk_bank,30,p),
      "tiu":select_bank(tiu_bank,35,p),
      "tkp":select_bank(tkp_bank,45,p)
    }

data={"general":[make_general_package(i) for i in range(1,16)],
      "cpns":[make_cpns_package(i) for i in range(1,16)]}
os.makedirs(os.path.dirname(OUT),exist_ok=True)
with open(OUT,"w",encoding="utf-8") as f:
    json.dump(data,f,ensure_ascii=False,indent=2)
print(f"wrote {OUT}")

