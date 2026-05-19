# 🌍 amcho Dashboard — ETL & Visualization

> Web application for visualizing global **Cocoa Prices** and **Producer Price Index (PPI)**
> from 2020 to 2026, with an automated ETL pipeline and interactive charts.

---

## 📋 Prerequisites

Make sure the following are installed on your machine before proceeding:

| Tool | Version |
|------|---------|
| Python | 3.12+ |
| PostgreSQL | 14+ |
| Git | any |

---

## ⚙️ Environment Configuration

Create a `.env` file inside the `etl/` folder based on the provided example:

```bash
cp etl/.env.example etl/.env
```

Then edit `etl/.env` and fill in your database credentials:

```env
DATABASE_URL=postgresql://YOUR_USER:YOUR_PASSWORD@localhost:5432/YOUR_DB_NAME
```

> ⚠️ If your password contains special characters (spaces, @, etc.), encode them in URL format.  
> Example: a space becomes `%20` → `my%20password`

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/amcho-dashboard.git
cd amcho-dashboard
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
```

### 3. Activate the virtual environment

```bash
# Linux / macOS
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🗄️ Database Setup

Create the database in PostgreSQL before running the ETL:

```sql
CREATE DATABASE camcho_db;
```

---

## 🔄 Run the ETL Pipeline

The ETL pipeline extracts data from the CSV files in `data/`, transforms it, and loads it into your PostgreSQL database.

```bash
cd etl && python3 run.py
```

Expected output: