Berikut file **README.md lengkap** yang sudah rapi, profesional, dan siap langsung kamu copy-paste ke repo GitHub 👇

---

```markdown
# 🎯 Analisis Sentimen Komentar YouTube Menggunakan Deep Learning

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-orange.svg)](https://www.tensorflow.org/)
[![Keras](https://img.shields.io/badge/Keras-2.x-red.svg)](https://keras.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Dicoding](https://img.shields.io/badge/Dicoding-Submission-purple.svg)](https://www.dicoding.com/)

---

## 📌 Ringkasan Proyek

Proyek ini bertujuan untuk mengklasifikasikan **sentimen komentar YouTube** ke dalam tiga kategori utama menggunakan pendekatan Deep Learning.

### 🎭 Kategori Sentimen

| Kategori | Emoji | Deskripsi |
|----------|-------|----------|
| **Positif** | 😊 | Komentar yang mendukung, memuji, atau mengapresiasi |
| **Negatif** | 😞 | Komentar berisi kritik, keluhan, atau sentimen buruk |
| **Netral** | 😐 | Komentar informatif tanpa emosi dominan |

---

## 🎯 Tujuan Proyek

- Membangun model klasifikasi sentimen berbasis Deep Learning
- Membandingkan performa beberapa arsitektur model
- Mencapai **akurasi minimal >92%**
- Submission untuk kelas **Belajar Deep Learning – Dicoding**

---

## 📁 Struktur Proyek

```

📦 Analisis-Sentimen-Youtube/
│
├── 📄 scrapping.py              # Script scraping komentar YouTube
├── 📓 AnalisisSentimen.ipynb    # Notebook utama (preprocessing, training, evaluasi)
├── 📦 requirements.txt          # Dependencies Python
├── 📄 README.md                 # Dokumentasi proyek
│
└── 📊 youtube_comments_*.csv    # Dataset hasil scraping

````

---

## 🚀 Cara Menjalankan Proyek

### 📋 Prasyarat

- Python 3.8 atau lebih baru
- RAM minimal 8GB (disarankan 16GB)
- Koneksi internet
- (Opsional) YouTube API Key

---

### 1️⃣ Clone Repository

```bash
git clone https://github.com/username/analisis-sentimen-youtube.git
cd analisis-sentimen-youtube
````

---

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

Atau manual:

```bash
pip install google-api-python-client pandas python-dateutil urllib3 requests
pip install tensorflow scikit-learn matplotlib seaborn jupyter
```

---

### 3️⃣ Scraping Komentar (Opsional)

Dataset sudah tersedia di notebook. Gunakan langkah ini jika ingin mengambil data terbaru.

#### Cara mendapatkan API Key:

1. Buka Google Cloud Console
2. Buat project baru
3. Enable **YouTube Data API v3**
4. Buat API Key di menu Credentials

#### Jalankan:

```bash
python scrapping.py
```

---

### 4️⃣ Jalankan Notebook

#### ✅ Opsi 1 (Rekomendasi): Google Colab

* Upload `AnalisisSentimen.ipynb`
* Upload dataset (jika diperlukan)
* Klik **Run All**

#### 💻 Opsi 2: Lokal

```bash
jupyter notebook AnalisisSentimen.ipynb
```

---

## 🧠 Arsitektur Model

### 1. LSTM

```python
Sequential([
    Embedding(MAX_NB_WORDS, EMBEDDING_DIM),
    SpatialDropout1D(0.3),
    LSTM(128, dropout=0.3, recurrent_dropout=0.3),
    Dense(3, activation='softmax')
])
```

---

### 2. GRU ⭐ (Model Terbaik)

```python
Sequential([
    Embedding(MAX_NB_WORDS, EMBEDDING_DIM),
    SpatialDropout1D(0.3),
    GRU(128, dropout=0.3, recurrent_dropout=0.3),
    Dense(3, activation='softmax')
])
```

---

### 3. Bidirectional LSTM

```python
Sequential([
    Embedding(MAX_NB_WORDS, 64),
    SpatialDropout1D(0.4),
    Bidirectional(LSTM(64, dropout=0.4, recurrent_dropout=0.4)),
    Dense(3, activation='softmax')
])
```

---

## ⚙️ Konfigurasi Model

| Parameter           | Nilai                  |
| ------------------- | ---------------------- |
| MAX_NB_WORDS        | 10,000                 |
| MAX_SEQUENCE_LENGTH | 120                    |
| EMBEDDING_DIM       | 128 (64 untuk Bi-LSTM) |
| Batch Size          | 64                     |
| Epochs              | 8                      |

---

## 📝 Labeling Otomatis (Rule-Based)

### Kata Positif

```
mantap, keren, bagus, lucu, makasih, edukasi, manfaat
```

### Kata Negatif

```
jelek, kecewa, buruk, hoax, sedih, bosan, salah
```

### Fungsi Labeling

```python
def labeling_pro(text):
    tokens = set(text.split())
    if tokens.intersection(neg_words):
        return 'Negative'
    elif tokens.intersection(pos_words):
        return 'Positive'
    else:
        return 'Neutral'
```

---

## 📊 Hasil Evaluasi

### 🏆 Model Terbaik: GRU

| Metrik    | Negative | Neutral | Positive |
| --------- | -------- | ------- | -------- |
| Precision | 0.98     | 1.00    | 0.98     |
| Recall    | 0.80     | 1.00    | 1.00     |
| F1-Score  | 0.88     | 1.00    | 0.99     |

✅ **Akurasi Validasi: ~99.5%**

---

## ⚖️ Distribusi Dataset

```
Neutral   : 82.0%
Positive  : 16.3%
Negative  : 1.7%
```

⚠️ Dataset tidak seimbang (imbalanced)

---

## 📈 Visualisasi

Notebook menghasilkan:

* Grafik akurasi training vs validasi
* Confusion matrix
* Classification report

---

## 💬 Contoh Prediksi

| Teks                                      | Sentimen |
| ----------------------------------------- | -------- |
| "Terima kasih dokter, sangat bermanfaat!" | Positive |
| "Video ini membosankan dan salah."        | Negative |
| "Saya menonton video ini sambil makan."   | Neutral  |

---

## 🔮 Prediksi Teks Baru

```python
def predict_sentiment(text, model):
    labels = ['Negative', 'Neutral', 'Positive']
    cleaned = clean_text(text)
    seq = tokenizer.texts_to_sequences([cleaned])
    padded = pad_sequences(seq, maxlen=MAX_SEQUENCE_LENGTH)
    pred = model.predict(padded, verbose=0)
    return labels[np.argmax(pred)]
```

---

## 🛠️ Persyaratan Sistem

### Minimum

* Python 3.8+
* RAM 8 GB
* Storage 2 GB

### Rekomendasi

* Python 3.10+
* RAM 16 GB
* GPU NVIDIA CUDA

---

## ⚠️ Catatan Penting

### 1. Labeling Otomatis

* Tidak memahami konteks
* Tidak mendeteksi sarkasme
* Bergantung pada keyword

### 2. Imbalanced Dataset

* Bias ke kelas Neutral
* Performa kelas Negative lebih rendah

**Solusi:**

* Class weighting
* Oversampling (SMOTE)
* Data augmentation

### 3. YouTube API Quota

* Free: 10,000 request/hari

---

## 🚀 Pengembangan Selanjutnya

### Jangka Pendek

* Class weighting
* Hyperparameter tuning

### Jangka Menengah

* Word2Vec / GloVe / FastText
* Model Transformer (BERT, IndoBERT)

### Jangka Panjang

* Labeling manual
* Deployment (Flask / FastAPI)
* Dashboard real-time (Streamlit)

---

## 📞 Kontak

* Email: [sutha.satyawan@example.com](mailto:sutha.satyawan@example.com)
* GitHub: [https://github.com/suthasatyawan](https://github.com/suthasatyawan)
* LinkedIn: [https://linkedin.com/in/i-putu-sutha-satyawan](https://linkedin.com/in/i-putu-sutha-satyawan)

---

## 👨‍💻 Kredit

**I Putu Sutha Satyawan**
Tahun: 2026
Dicoding – Belajar Deep Learning

---


