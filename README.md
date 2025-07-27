
# 📚 Library Manager

A Django-based Library Management System to efficiently manage books, users, and transactions. Built for academic institutions and small libraries.

---

## 🚀 Features

- 🔐 User Authentication (Admin, Librarian, Student)
- 📖 Book Management (Add, Update, Delete, View)
- 👥 User Management
- 📆 Issue / Return Tracking
- 🔎 Advanced Book Search
- 📊 Dashboard with Statistics

---

## 🛠️ Tech Stack

- **Framework**: Django
- **Database**: SQLite (default) or MySQL/PostgreSQL
- **Frontend**: HTML5, CSS3, Bootstrap
- **Version Control**: Git + GitHub

---

## ⚙️ Setup Instructions

### 1. Clone the repo
```bash
git clone https://github.com/Lekhan11/Library_Manager.git
cd Library_Manager
```

### 2. Create a virtual environment
```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create superuser (Admin)
```bash
python manage.py createsuperuser
```

### 6. Start the server
```bash
python manage.py runserver
```

Visit: [http://localhost:8000](http://localhost:8000)

---

## 📁 Project Structure

```bash
Library_Manager/
├── library_app/       # Core app for managing books, users, etc.
├── templates/         # HTML templates
├── static/            # CSS, JS, and other static files
├── media/             # Uploaded files (if any)
├── db.sqlite3         # Default DB
├── manage.py
└── requirements.txt
```


---

## 📄 License

This project is licensed under the **MIT License**. Feel free to use and modify.

---

## 🙌 Want to Contribute?

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
