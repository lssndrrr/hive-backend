## 🐝🧠 Hive (Backend)

Hive helps teams simplify group task management while still allowing for structured, detailed control when needed.
It is a group task management web app built with **Nuxt 3** and **Django**.\
\
Early work in progress — MVP coming soon!\
\
This repository contains the backend.
You can find the frontend [here](https://github.com/lssndrrr/hive.git).

### 🏠 Local Setup

Clone the project

```bash
  git clone https://github.com/lssndrrr/hive-mind
```

Go to the project directory

```bash
  cd hive-mind
```

Create and activate a virtual environment

```bash
  python -m venv .venv
  source env/bin/activate  # On Windows: env\Scripts\activate
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Apply migrations

```bash
  python manage.py migrate
```

Start the server

```bash
  python manage.py runserver
```

### 📚 Documentation

Each app has its own README containing the models, API endpoints, and any other notes.

- [user](./user/README.md)
- [hive](./hive/README.md)
- [task](./task/README.md)

### 🧑‍🌾🐝 Beekeepers

- [@lssndrrr](https://www.github.com/lssndrrr)
- [@cajober](https://www.github.com/cajober)
- [@Lanieza](https://www.github.com/Lanieza)

### 🌱 Setting up your `.env`

To run this project, you will need to add the following environment variables to your `.env` file.

_Nothing to see here right now. Check back again later?_
