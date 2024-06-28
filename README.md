# VeriFace

VeriFace adalah aplikasi web yang digunakan untuk mengelola data kehadiran menggunakan teknologi deep learning untuk pengenalan wajah. Aplikasi ini memanfaatkan model deep learning untuk mendeteksi dan mengenali wajah sehingga proses presensi menjadi lebih mudah dan efisien.

## Fitur

- **Pengenalan Wajah**: Menggunakan teknologi deep learning untuk mendeteksi dan mengenali wajah.
- **Pengelolaan Kehadiran**: Memungkinkan pengelolaan data kehadiran dengan mudah.
- **Antarmuka Web**: Menyediakan antarmuka web yang intuitif dan mudah digunakan.

## Persyaratan Sistem

- Python 3.9 hingga 3.11
- VS Code
- pip (Python package installer)

## Instalasi dan Cara Menjalankan Aplikasi

Ikuti langkah-langkah berikut untuk menginstal dan menjalankan VeriFace di sistem Anda:

1. **Clone repository**:
    ```bash
    git clone https://github.com/Iq11k/VeriFace
    cd VeriFace
    ```

2. **Buka dengan VS Code**:
    - Buka Visual Studio Code.
    - Buka folder VeriFace yang telah di-clone.

3. **Pilih Interpreter Python**:
    - Tekan `CTRL + SHIFT + P`.
    - Cari dan pilih `Python: Select Interpreter`.
    - Pilih interpreter Python yang sesuai (disarankan menggunakan versi 3.9 hingga 3.11).

4. **Buat Virtual Environment**:
    - Di terminal VS Code, jalankan perintah berikut untuk membuat virtual environment:
    ```bash
    python -m venv venv
    ```

5. **Aktifkan Virtual Environment**:
    - Tutup terminal Anda lalu buka terminal baru di VS Code.
    - Aktifkan virtual environment:
        - Windows:
        ```bash
        venv\Scripts\activate
        ```
        - MacOS/Linux:
        ```bash
        source venv/bin/activate
        ```

6. **Install Dependencies**:
    - Install semua dependency yang diperlukan dengan menjalankan perintah berikut:
    ```bash
    pip install -r requirements.txt
    ```

7. **Jalankan Aplikasi**:
    - Setelah semua dependency terinstal, jalankan aplikasi dengan perintah berikut:
    ```bash
    python app.py
    ```

## Struktur Direktori

```plaintext
VeriFace/
├── app.py
├── facerecognition.py
├── requirements.txt
├── README.md
├── venv/
├── static/
│   ├── faces/
│   ├── img/
    ├── models/
│   └── styles/
└── templates/
    ├── base.html
    ├── eventpage.html
    ├── index.html
    ├── loginPage.html
    ├── mainpage.html
    ├── presensi.html
    └── registerPage.html
```

## Kontak

Untuk informasi lebih lanjut atau pertanyaan, Anda dapat menghubungi kami melalui email di naprittt@gmail.com.

---

Terima kasih telah menggunakan VeriFace! Kami berharap aplikasi ini dapat membantu Anda dalam mengelola data kehadiran dengan lebih baik dan efisien.