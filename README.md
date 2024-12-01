# Engilore
The main site of Engilore 🧐

Engilore is a platform aimed at fostering intellectual growth, collaboration, and innovation. This repository hosts the main site for Engilore.

## Prerequisites

Before setting up the project, ensure you have the following installed:

1. **Python 3.10 or later**: Download and install Python [here](https://www.python.org/downloads/).
2. **Pip**: Included with Python installations.
3. **Virtualenv**: Install with `pip install virtualenv`.
4. **Git**: Install from [here](https://git-scm.com/).

---

## Setting Up the Development Environment

### 1. Clone the Repository

```bash
git clone https://github.com/your_username/engilore.git
cd engilore
```

### 2. Create a Virtual Environment

```bash
virtualenv venv
```

### 3. Activate Virtual Environment

- Windows:
    ```bash
    venv\Scripts\activate
    ```
- Mac/Linux:
    ```bash
    source venv/bin/activate
    ```

### 4. Install Project Dependencies

```bash
pip install -r requirements.txt
```

## Setting Up the Project

### 1. Apply Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

## Running the Project

```bash
python manage.py runserver
```
The site will be accessible at http://127.0.0.1:8000.
