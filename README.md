# Alfagift Task Tracker

Aplikasi manajemen tugas sederhana berbasis web yang dikembangkan sebagai bagian dari technical assessment **Full-Stack Developer Intern**.

Aplikasi ini memungkinkan pengguna untuk mengelola tugas melalui fitur tambah, lihat, ubah, dan hapus tugas. Saya juga menambahkan fitur filter yaitu mengelompokkan tugas berdasarkan status.
## Teknologi yang Digunakan

### Frontend
- **Vue 3** - menggunakan Composition API.
- **Vite** - development server dan build tool.
- **Axios** - komunikasi dengan REST API.
- **CSS** - styling dan responsive layout.

### Backend
- **Python** - bahasa pemrograman backend.
- **FastAPI** - framework untuk membangun REST API.
- **SQLAlchemy** - ORM untuk interaksi dengan database.
- **Pydantic** - validasi dan pengelolaan data.

### Database
- **PostgreSQL** - relational database.
- **Docker Compose** - menjalankan PostgreSQL dalam container.

## Fitur

- Menampilkan seluruh daftar tugas.
- Menambahkan tugas baru.
- Mengubah judul, deskripsi, dan status tugas.
- Menghapus tugas.
- Memfilter tugas berdasarkan status.
- Validasi input untuk memastikan data yang dimasukkan sesuai.
- Antarmuka responsif yang dapat digunakan pada berbagai ukuran layar.

## Struktur Proyek

```text
project_tracker/
├── backend/
│   ├── app/
│   │   ├── routers/
│   │   │   └── tasks.py
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── database.py
│   │   ├── models.py
│   │   └── schemas.py
│   ├── .env.example
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── App.vue
│   │   ├── main.js
│   │   └── style.css
│   ├── index.html
│   ├── package.json
│   ├── package-lock.json
│   └── vite.config.js
│
├── docker-compose.yml
├── .gitignore
└── README.md
```

## Persyaratan Sistem

Pastikan perangkat sudah memiliki beberapa tools berikut:

- Git
- Python 3.11
- Node.js dan npm
- Docker Desktop
- Docker Compose

## Instalasi dan Konfigurasi

### 1. Clone Repository

Clone repository berikut dan masuk ke direktori proyek:

```bash
git clone https://github.com/narutostg/Project_Tracker.git
cd project_tracker
```


### 2. Konfigurasi Environment Variables

Buat file `.env` pada direktori utama proyek (root directory).

Gunakan `backend/.env.example` sebagai referensi konfigurasi.

Contoh isi file `.env`:

```env
DATABASE_URL=postgresql+psycopg://task_tracker:your_password@localhost:5432/task_tracker

POSTGRES_DB=task_tracker
POSTGRES_USER=task_tracker
POSTGRES_PASSWORD=your_password
```

Sesuaikan `your_password` dengan password PostgreSQL yang digunakan. Pastikan username, password, dan nama database pada `DATABASE_URL` sesuai dengan konfigurasi PostgreSQL.



### 3. Menjalankan Database

Pastikan Docker Desktop sudah berjalan.

Dari direktori utama proyek, jalankan:

```bash
docker compose up -d db
```

Perintah tersebut akan menjalankan PostgreSQL melalui Docker Compose.

Untuk memeriksa status container:

```bash
docker compose ps
```

Pastikan container database sudah berjalan sebelum melanjutkan ke tahap berikutnya.


### 4. Menjalankan Backend

Buka terminal baru dan masuk ke direktori backend:

```bash
cd backend
```

Buat virtual environment:

```bash
python -m venv .venv
```

Aktifkan virtual environment.

**Windows (PowerShell):**

```powershell
.venv\Scripts\Activate.ps1
```

**Windows (Git Bash):**

```bash
source .venv/Scripts/activate
```

Instal seluruh dependency:

```bash
pip install -r requirements.txt
```

Jalankan server FastAPI:

```bash
uvicorn app.main:app --reload
```

Backend akan berjalan pada:

`http://127.0.0.1:8000`

**Dokumentasi API (Swagger UI):**

`http://127.0.0.1:8000/docs`

**Catatan:** Tabel database akan dibuat secara otomatis ketika aplikasi backend pertama kali dijalankan.


### 5. Menjalankan Frontend

Buka terminal baru dan masuk ke direktori frontend:

```bash
cd frontend
```

Instal dependency:

```bash
npm install
```

Jalankan development server:

```bash
npm run dev
```

Frontend akan tersedia pada:

`http://localhost:5173`

Buka alamat tersebut melalui browser untuk menggunakan aplikasi.

## Dokumentasi API

Backend menyediakan REST API untuk mengelola data tugas.

| Method | Endpoint | Deskripsi |
|---|---|---|
| GET | `/tasks` | Mengambil seluruh daftar tugas |
| POST | `/tasks` | Membuat tugas baru |
| PUT | `/tasks/{id}` | Mengubah data tugas |
| DELETE | `/tasks/{id}` | Menghapus tugas |

### Format Data Task

Setiap task memiliki struktur data sebagai berikut:

| Field | Tipe Data | Deskripsi |
|---|---|---|
| `id` | Integer | Identitas unik tugas |
| `title` | String | Judul tugas |
| `description` | String | Deskripsi tugas |
| `status` | String | Status pengerjaan tugas |

### Status Tugas

Terdapat tiga pilihan status yang tersedia:

- `Todo`
- `In Progress`
- `Done`

### Contoh Request

**POST `/tasks`**

Request body:

```json
{
  "title": "Mengerjakan tugas",
  "description": "Menyelesaikan technical assessment",
  "status": "Todo"
}
```

API melakukan validasi terhadap input yang diterima. Judul tugas tidak boleh kosong dan status harus menggunakan salah satu dari tiga pilihan yang tersedia.

### Swagger UI

Dokumentasi interaktif API dapat diakses melalui:

`http://127.0.0.1:8000/docs`

Swagger UI dapat digunakan untuk melihat endpoint, memeriksa struktur request dan response, serta mencoba API secara langsung.

## Troubleshooting

**1. Database tidak dapat dihubungkan**

- Pastikan Docker Desktop sedang berjalan.
- Periksa status container menggunakan `docker compose ps`.
- Pastikan konfigurasi database pada file `.env` sudah sesuai.
- Pastikan PostgreSQL berjalan pada port `5432`.

**2. Backend gagal dijalankan**

- Pastikan virtual environment sudah diaktifkan.
- Pastikan dependency sudah terinstal menggunakan `pip install -r requirements.txt`.
- Pastikan file `.env` tersedia di direktori utama proyek.

**3. Frontend tidak dapat terhubung ke backend**

- Pastikan server FastAPI sedang berjalan.
- Pastikan backend tersedia pada `http://127.0.0.1:8000`.
- Pastikan frontend berjalan pada `http://localhost:5173`.

---

**Alfagift Task Tracker**  
Dikembangkan sebagai bagian dari technical assessment Full-Stack Developer Intern.
