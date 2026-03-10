# FastAPI Items API with SQLite

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Framework-green)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey)

---

# Deskripsi Project

Project ini merupakan **REST API sederhana** yang dibangun menggunakan **FastAPI** dengan database **SQLite**.
API ini digunakan untuk mengambil dan menampilkan data item dari database.

Project ini dibuat sebagai bagian dari pembelajaran **backend development menggunakan Python** pada mata kuliah **Web Lanjutan**.

---

# Fitur Utama

1. Menampilkan seluruh data item dari database
2. Menampilkan data item berdasarkan ID
3. Menyediakan dokumentasi API otomatis menggunakan Swagger
4. Menggunakan struktur project backend yang terorganisir

---

# Tools yang Digunakan

- Python
- FastAPI
- SQLite
- SQLAlchemy
- Pydantic
- Uvicorn
- Git
- GitHub
- Visual Studio Code

---

# Struktur Project

```bash
FastApi-items-sqllite/
│
├── app/
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── database.py
│   └── requirements.txt
│
├── README.md
└── .gitignore
```

Penjelasan:

- **app/** → folder utama yang berisi seluruh source code aplikasi FastAPI
- **main.py** → file utama untuk menjalankan aplikasi FastAPI dan mendefinisikan endpoint API
- **models.py** → berisi model database menggunakan SQLAlchemy
- **schemas.py** → berisi schema validasi data menggunakan Pydantic
- **database.py** → berisi konfigurasi koneksi database SQLite
- **requirements.txt** → daftar library Python yang digunakan oleh project
- **README.md** → dokumentasi project
- **.gitignore** → menentukan file yang tidak akan diupload ke repository

---

# Cara Menjalankan Project

## 1 Clone Repository

```bash
git clone https://github.com/diestymendila/FastApi-items-sqllite.git
```

```
cd FastApi-items-sqllite
```

---

## 2 Membuat Virtual Environment

```bash
python -m venv venv
```

---

## 3 Mengaktifkan Virtual Environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / Mac

```bash
source venv/bin/activate
```

---

## 4 Install Dependencies

```bash
pip install -r app/requirements.txt
```

---

## 5 Menjalankan Server

```bash
uvicorn app.main:app --reload
```

Server akan berjalan pada alamat:

```
http://127.0.0.1:8000/docs
```

---

# Dokumentasi API

FastAPI menyediakan dokumentasi API otomatis yang dapat diakses melalui browser.

**Swagger UI**

```
http://127.0.0.1:8000/docs
```

**ReDoc**

```
http://127.0.0.1:8000/redoc
```

Melalui halaman tersebut pengguna dapat melihat endpoint API serta mencoba request secara langsung.

---

# Endpoint API

Endpoint yang tersedia dalam API ini:

- **GET /items/**

  Digunakan untuk mengambil seluruh data item dari database.

- **GET /items/{item_id}**

  Digunakan untuk mengambil data item berdasarkan ID tertentu.

---

# Contoh Response API

Contoh response ketika memanggil endpoint:

```
GET /items/
```

Response JSON:

```json
[
  {
    "id": 1,
    "name": "Laptop",
    "description": "Laptop untuk programming"
  },
  {
    "id": 2,
    "name": "Mouse",
    "description": "Mouse wireless"
  }
]
```

---

# Arsitektur Sistem

Alur kerja aplikasi secara sederhana:

```
User Request
     ↓
FastAPI Server
     ↓
API Endpoint
     ↓
Database Query
     ↓
SQLite Database
     ↓
JSON Response
```

Penjelasan:

1. User mengirim request ke server API.
2. FastAPI menerima request tersebut.
3. Endpoint memproses permintaan.
4. Aplikasi mengambil data dari database SQLite.
5. Data dikembalikan kepada user dalam format JSON.

---

# Penjelasan Kode

Berikut penjelasan kode pada setiap file utama.

---

# database.py

```bash
# Mengimpor fungsi SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# URL database SQLite
DATABASE_URL = "sqlite:///./items.db"

# Membuat koneksi ke database
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

# Membuat session database
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class untuk model database
Base = declarative_base()
```

---

# models.py

```bash
# Mengimpor tipe kolom SQLAlchemy
from sqlalchemy import Column, Integer, String

# Mengimpor Base dari database
from database import Base

# Model tabel Item
class Item(Base):

    # Nama tabel
    __tablename__ = "items"

    # Primary key
    id = Column(Integer, primary_key=True, index=True)

    # Nama item
    name = Column(String, index=True)

    # Deskripsi item
    description = Column(String)
```

---

# schemas.py

```bash
# Mengimpor BaseModel dari Pydantic
from pydantic import BaseModel

# Schema dasar item
class ItemBase(BaseModel):

    # Nama item
    name: str

    # Deskripsi item
    description: str


# Schema response API
class ItemResponse(ItemBase):

    # ID item
    id: int

    class Config:

        # Mengaktifkan ORM mode
        orm_mode = True
```

---

# main.py

```bash
# Mengimpor FastAPI dan dependency lain
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

# Mengimpor file project
import models
import schemas

# Mengimpor koneksi database
from database import SessionLocal, engine

# Membuat tabel database otomatis
models.Base.metadata.create_all(bind=engine)

# Membuat aplikasi FastAPI
app = FastAPI()


# Dependency koneksi database
def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# Endpoint untuk mengambil semua item
@app.get("/items/", response_model=list[schemas.ItemResponse])
def read_items(db: Session = Depends(get_db)):

    items = db.query(models.Item).all()

    return items


# Endpoint untuk mengambil item berdasarkan ID
@app.get("/items/{item_id}", response_model=schemas.ItemResponse)
def read_item(item_id: int, db: Session = Depends(get_db)):

    item = db.query(models.Item).filter(models.Item.id == item_id).first()

    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    return item
```

---

# requirements.txt

```bash
# Framework utama untuk membuat REST API
fastapi==0.135.1

# ASGI server untuk menjalankan FastAPI
uvicorn==0.41.0

# ORM untuk menghubungkan aplikasi dengan database
SQLAlchemy==2.0.48

# Library validasi data yang digunakan oleh FastAPI
pydantic==2.12.5

# Core internal dari Pydantic
pydantic_core==2.41.5

# Framework ASGI yang menjadi dasar FastAPI
starlette==0.52.1

# Library asynchronous yang digunakan oleh Starlette
anyio==4.12.1

# Digunakan untuk tipe data tambahan pada Python
typing_extensions==4.15.0

# Digunakan untuk inspeksi tipe data
typing-inspection==0.4.2

# Library HTTP protocol yang digunakan oleh Uvicorn
h11==0.16.0

# Digunakan untuk pengolahan URL
idna==3.11

# Library untuk menjalankan perintah CLI
click==8.3.1

# Digunakan untuk memberikan warna pada terminal
colorama==0.4.6

# Digunakan oleh SQLAlchemy untuk manajemen thread
greenlet==3.3.2

# Library tambahan untuk tipe anotasi
annotated-types==0.7.0

# Dokumentasi anotasi tambahan
annotated-doc==0.0.4

# Library tambahan yang digunakan pada project
KALENDER==0.0.1
```

---

# Kesimpulan

Project ini menunjukkan bagaimana membangun **REST API sederhana menggunakan FastAPI dan SQLite** dengan struktur project yang terorganisir.

Dengan memanfaatkan **FastAPI, SQLAlchemy, dan Pydantic**, aplikasi dapat mengelola data secara efisien serta menyediakan endpoint API yang mudah digunakan. Selain itu, FastAPI juga menyediakan dokumentasi API otomatis melalui Swagger sehingga mempermudah proses pengujian dan pengembangan.

Struktur kode yang dipisahkan menjadi beberapa file seperti `database.py`, `models.py`, `schemas.py`, dan `main.py` membantu meningkatkan keterbacaan kode serta memudahkan pengembangan aplikasi di masa mendatang.
