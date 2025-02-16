## Project: Avatar

**Description:**  

Avatar is a Django-based web application. It includes a database (`db.sqlite3`), Django project files, and an application module named `web`.



## Installation & Setup

1. **Install Dependencies**  

   Ensure you have Python and Django installed. You can install dependencies using:  

   ```sh

   pip install django

   ```



2. **Database Migration**  

   Run the following commands to apply migrations:  

   ```sh

   python manage.py makemigrations

   python manage.py migrate

   ```



3. **Run the Development Server**  

   Start the Django server with:  

   ```sh

   python manage.py runserver

   ```  

   Access the app at `http://127.0.0.1:8000/`.



## Project Structure

- `manage.py` - Django project manager  

- `Avatar/` - Main Django project folder  

- `web/` - Django application containing models, admin configurations, and signals  

- `db.sqlite3` - SQLite database file  

"""
