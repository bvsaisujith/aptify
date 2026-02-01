# AptiFy

AptiFy is an AI-powered educational platform designed to identify and fix hidden learning gaps in students. Instead of only evaluating final scores, AptiFy analyses quiz performance at a conceptual level to determine exactly where a student's understanding breaks down.

Using Large Language Models, the system maps incorrect answers to underlying concepts and generates a personalized, time-bound learning roadmap tailored to each student's needs. This helps learners focus only on what truly matters — saving time and improving outcomes.

## ⚙️ Tech Stack

### Backend
- **Python (3.12+)** — Core programming language
- **Django** — Main backend framework for authentication, ORM, routing, and server-side logic
- **Django Allauth** — Social authentication and account management

### AI & Intelligence Layer
- **OpenAI API / LangChain** — Used for concept gap analysis and dynamic roadmap generation

### Database
- **PostgreSQL (Supabase)** — Stores student profiles, quiz attempts, performance data, and learning paths

### Environment & Tooling
- **uv** — Ultra-fast Python package manager for dependency and virtual environment management

### Frontend
- **Django Templates** — Server-side rendered views

### Deployment
- **Render** — Backend hosting
- **Supabase** — PostgreSQL database hosting

---

## ▶️ How to Run the Project

### 1️⃣ Prerequisites

Make sure the following are installed:
- Python 3.12+
- uv (Python package manager)
- PostgreSQL (running locally or remotely via Supabase)

### 2️⃣ Setup Instructions

```bash
# Clone the repository
git clone https://github.com/bvsaisujith/AptiFy.git
cd AptiFy

# Install dependencies using uv
uv sync
```

### 3️⃣ Environment Configuration

Create a `.env` file in the project root:

```bash
# Copy the sample environment file
cp .env.sample .env
```

Then edit `.env` with your actual credentials:
- Database connection string (Supabase PostgreSQL)
- OpenAI API keys
- Django secret key
- Google OAuth credentials (optional)

### 4️⃣ Run Migrations

```bash
uv run python manage.py migrate
```

### 5️⃣ Create Superuser (Optional)

```bash
uv run python manage.py createsuperuser
```

### 6️⃣ Start the Development Server

```bash
uv run python manage.py runserver
```

Open in browser:
```
http://127.0.0.1:8000
```

---

## 🚀 Quick Start Commands

```bash
# Full setup from scratch
git clone https://github.com/bvsaisujith/AptiFy.git
cd AptiFy
uv sync
cp .env.sample .env
# Edit .env with your credentials
uv run python manage.py migrate
uv run python manage.py createsuperuser
uv run python manage.py runserver
```

---

## 🌐 Deployment

### Render
- Backend is deployed on Render
- Configure environment variables in Render dashboard

### Supabase
- PostgreSQL database hosted on Supabase
- Connection string configured via `DATABASE_URL` in `.env`

---

## 📚 Features

- **AI-Powered Gap Analysis** — Identifies conceptual weaknesses
- **Personalized Learning Paths** — Custom roadmaps for each student
- **Social Authentication** — Google, GitHub, Facebook login via Django Allauth
- **Quiz Management** — Create and manage assessments
- **Performance Tracking** — Monitor student progress over time

---

## 🛠️ Admin Access

Access the Django admin panel at:
```
http://127.0.0.1:8000/aptify-admin/
```

---

## 📝 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

Developed by **BV Sai Sujith**

GitHub: [@bvsaisujith](https://github.com/bvsaisujith)