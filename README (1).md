# Proyek Akhir: Menyelesaikan Permasalahan Perusahaan Edutech

## Business Understanding

Jaya Jaya Institut merupakan institusi pendidikan tinggi yang telah berdiri sejak tahun 2000 dan dikenal memiliki reputasi baik dalam mencetak lulusan berkualitas. Namun, dalam beberapa tahun terakhir, pihak kampus menghadapi tantangan serius berupa **tingginya angka mahasiswa yang tidak menyelesaikan studi atau dropout**.

Masalah dropout ini tidak hanya berdampak pada reputasi akademik institusi, tetapi juga mengganggu efisiensi operasional, perencanaan akademik, serta akreditasi program studi. Fenomena ini paling sering terjadi setelah mahasiswa memasuki semester kedua, di mana tingkat kegagalan mata kuliah meningkat dan kesulitan finansial mulai muncul.

Saat ini, pihak kampus belum memiliki sistem yang mampu mendeteksi potensi dropout secara dini. Akibatnya, tindakan intervensi hanya dilakukan setelah mahasiswa menunjukkan penurunan performa yang signifikan, dan pada tahap tersebut sering kali sudah terlambat.

Untuk menghadapi tantangan ini, proyek ini bertujuan untuk menyediakan **solusi machine learning dan dashboard interaktif** yang dapat membantu manajemen akademik dalam mengidentifikasi mahasiswa berisiko tinggi dropout secara proaktif.

---

### Permasalahan Bisnis

Berikut adalah permasalahan utama yang akan diselesaikan dalam proyek ini:

- Tingginya angka dropout mahasiswa, terutama setelah memasuki semester 2.
- Tidak adanya sistem prediktif untuk mengidentifikasi mahasiswa dengan risiko tinggi gagal studi.
- Keterbatasan visualisasi performa mahasiswa yang membuat pihak kampus kesulitan memantau indikator risiko dropout secara real-time.
- Ketiadaan sistem pendukung yang bisa digunakan untuk melakukan intervensi dini berdasarkan data akademik dan non-akademik.



### Cakupan Proyek

Proyek ini dirancang untuk membantu Jaya Jaya Institut dalam memprediksi dan memonitor risiko dropout mahasiswa dengan pendekatan berbasis data. Adapun cakupan dari proyek ini mencakup beberapa tahapan sebagai berikut:

- **Eksplorasi dan Analisis Data**  
  Melakukan eksplorasi terhadap dataset performa mahasiswa yang terdiri dari 38 kolom, mencakup faktor akademik (seperti jumlah mata kuliah lulus/gagal), status keuangan, dan variabel sosial lainnya.

- **Data Preparation**  
  Melakukan pembersihan data, transformasi fitur, encoding variabel kategorikal, dan pembagian data menjadi training dan testing untuk keperluan model.

- **Pembangunan Model Machine Learning**  
  Menggunakan algoritma XGBoost untuk membangun model klasifikasi yang memprediksi apakah mahasiswa akan dropout, tidak lulus, atau lulus. Model dievaluasi menggunakan metrik akurasi dan F1-score.

- **Pembuatan Dashboard Interaktif**  
  Mengembangkan dashboard berbasis Metabase yang menyajikan visualisasi indikator dropout, termasuk jumlah mata kuliah gagal per semester, kursus dengan risiko tertinggi, dan hubungan antara performa dan status keuangan mahasiswa.

- **Pengembangan Prototype Prediksi**  
  Membangun aplikasi berbasis Streamlit untuk menguji model secara real-time dan memberikan prediksi terhadap status kelulusan mahasiswa berdasarkan input fitur tertentu.

- **Dokumentasi & Deployment**  
  Menyediakan dokumentasi proyek dalam format README dan mendukung deploy aplikasi ke Streamlit Community Cloud agar dapat diakses secara online.



## Persiapan

- **Sumber data**: [Students Performance Dataset — Dicoding GitHub](https://github.com/dicodingacademy/dicoding_dataset/tree/main/students_performance)  
- **Jumlah fitur**: 38 kolom  
- **Target**: `Target` (0 = Tidak Lulus, 1 = Dropout, 2 = Lulus)

### 1. Setup Environment

Untuk menjaga isolasi proyek dan menghindari konflik antar dependensi:

```bash
python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows
```
### 2. Install Dependencies
Pastikan Anda berada di root folder proyek. Jalankan perintah berikut untuk menginstal semua dependensi:

```bash
pip install -r requirements.txt
```
**Library utama yang digunakan:**

- `pandas`, `numpy` – untuk manipulasi dan eksplorasi data.
- `scikit-learn`, `xgboost` – untuk pembangunan model machine learning dan evaluasi.
- `streamlit` – untuk membangun antarmuka aplikasi prediksi berbasis web.
- `matplotlib`, `seaborn` – untuk membuat visualisasi data (opsional).

### 3. File yang Dibutuhkan

Pastikan struktur folder proyek Anda mencakup file-file berikut:

- `app.py` – Aplikasi utama Streamlit yang digunakan untuk menjalankan prediksi dropout mahasiswa.
- `xgb_model.pkl` – File model machine learning (XGBoost) yang telah dilatih dan disimpan.
- `requirements.txt` – Daftar semua dependensi Python yang dibutuhkan untuk menjalankan proyek.
- `metabase.db.mv.db` – File database Metabase yang berisi konfigurasi dashboard.
- `faiq_rofifi-dashboard.png` – Screenshot tampilan dashboard yang menggambarkan visualisasi data performa mahasiswa.

### 4. Menjalankan Dashboard Metabase (Docker)

Jika Anda menggunakan Metabase untuk visualisasi performa mahasiswa, jalankan container-nya dengan perintah berikut:

```bash
docker run -d -p 3000:3000 \
  -v "$PWD/metabase-data":/metabase-data \
  -e "MB_DB_FILE=/metabase-data/metabase.db" \
  --name metabase-local metabase/metabase
```

Setelah container berjalan, buka browser dan akses:

```bash
http://localhost:3000
```
Gunakan kredensial berikut untuk login:

**Email**: mfaiqrofifi@mail.com

**Password**: root123


## Business Dashboard

Dashboard ini dibangun menggunakan **Metabase** dan berfungsi sebagai alat bantu visualisasi interaktif untuk membantu pihak Jaya Jaya Institut dalam memantau performa akademik mahasiswa serta mengidentifikasi pola yang mengarah pada risiko dropout.

Dashboard ini mencakup visualisasi berikut:

- **Perbandingan Jumlah Mata Kuliah Tidak Lulus di Semester 1 dan Semester 2**  
  Visualisasi ini menampilkan jumlah total mata kuliah yang gagal (DO) di setiap semester dari seluruh mahasiswa. Hasilnya menunjukkan bahwa semester 2 memiliki jumlah kegagalan lebih tinggi dibanding semester 1, menandakan bahwa semester 2 merupakan periode kritis dalam keberlangsungan studi mahasiswa.

- **Distribusi Mahasiswa Berdasarkan Status Pembayaran dan Kelulusan**  
  Grafik ini menunjukkan hubungan antara status pembayaran tuition fees mahasiswa dengan status kelulusan mereka (Dropout, Tidak Lulus, Lulus). Terlihat bahwa mahasiswa dengan status pembayaran tidak lancar memiliki kecenderungan lebih tinggi untuk dropout.

- **Distribusi Status Kelulusan Mahasiswa**  
  Pie chart atau bar chart ini menunjukkan proporsi mahasiswa dalam tiga kategori: Dropout, Tidak Lulus, dan Lulus. Visualisasi ini memberikan gambaran umum tentang tingkat keberhasilan akademik institusi.

- **Peringkat Mata Kuliah Berdasarkan Jumlah Kegagalan**  
  Menampilkan daftar mata kuliah yang memiliki jumlah ketidaklulusan (DO) tertinggi. Visualisasi ini dapat membantu fakultas mengevaluasi mata kuliah dengan tingkat kesulitan atau beban yang tinggi.

- **Distribusi Mahasiswa Berdasarkan Program Studi dan Status Kelulusan**  
  Visualisasi ini memperlihatkan performa akademik mahasiswa berdasarkan program studi. Beberapa program menunjukkan tingkat dropout lebih tinggi dibanding yang lain, yang dapat dijadikan bahan evaluasi kurikulum dan pembinaan.

- **Rata-Rata Jumlah Mata Kuliah Tidak Lulus Berdasarkan Status Kelulusan**  
  Visualisasi ini menunjukkan korelasi antara status kelulusan dan jumlah rata-rata mata kuliah yang tidak lulus, memperkuat insight bahwa mahasiswa yang dropout umumnya memiliki jumlah DO yang lebih tinggi.

Dashboard ini memungkinkan pihak akademik untuk:
- Melihat tren dan pola dropout secara real-time.
- Mengambil keputusan berbasis data untuk melakukan intervensi akademik atau kebijakan pembiayaan.
- Mengevaluasi kurikulum serta kinerja pengajaran pada mata kuliah tertentu.

#### Akses Dashboard
- File database: `metabase.db.mv.db`
- Email: `root@mail.com`
- Password: `root123`

#### Screenshot Dashboard
![Dashboard Screenshot](faiq_rofifi-dashboard.png)


## Menjalankan Sistem Machine Learning
Jelaskan cara menjalankan protoype sistem machine learning yang telah dibuat. Selain itu, sertakan juga link untuk mengakses prototype tersebut.

```

```

## Conclusion
Jelaskan konklusi dari proyek yang dikerjakan.

### Rekomendasi Action Items
Berikan beberapa rekomendasi action items yang harus dilakukan perusahaan guna menyelesaikan permasalahan atau mencapai target mereka.
- action item 1
- action item 2
