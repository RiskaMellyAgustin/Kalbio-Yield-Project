# Kalbio Production Performance Dashboard

A full-stack web application developed as a functional prototype for PT Kalbio Global Medika to digitize and centralize their production yield and Plant Cycle Time (PCT) monitoring. This project transforms a manual, spreadsheet-based workflow into a real-time, role-based, and interactive web dashboard.

## Key Features

* **📊 Interactive Dashboards:** Role-specific dashboards for Management/MSTD, Operators, and Quality Control, providing relevant data and actions for each user group.
* **🔐 Role-Based Access Control:** A secure authentication and authorization system that ensures users can only access features relevant to their roles (e.g., Operators cannot see management analytics).
* **🚀 Real-Time Production Tracking:** An Operator-focused dashboard that provides live visibility of work-in-progress batches and their current production stage.
* **📈 Advanced KPI Analysis:** A centralized dashboard for management featuring multi-level filtering (by date range, product, etc.) and visualizations for key KPIs like Yield vs. Target, Pareto Analysis for production loss, and more.
* **📄 Smart CSV Import:** A feature for MSTD to bulk-upload historical production data. The system includes a staging area to validate data integrity before loading it into the main database.
* **📝 Issue & Action Plan Tracking:** An integrated system for operators to report production issues and for MSTD to document and track corrective action plans.

## Tech Stack

* **Backend:** Django
* **Database:** PostgreSQL
* **Data Processing:** Pandas
* **Frontend:** HTML, CSS, JavaScript
* **UI/UX:** Bootstrap 5
* **Data Visualization:** Chart.js

## Local Setup Guide

Follow these steps to run the project on your local machine.

### 1. Prerequisites
- Python 3.10+
- PostgreSQL

### 2. Setup
**a. Clone the repository and navigate to the `backend` directory:**
```bash
git clone [https://github.com/RiskaMellyAgustin/Kalbio-Yield-Project.git](https://github.com/RiskaMellyAgustin/Kalbio-Yield-Project.git)
cd Kalbio-Yield-Project/backend
```

**b. Create and activate a virtual environment:**
```bash
# Create the virtual environment
python -m venv .venv

# Activate on Windows
.\.venv\Scripts\activate

# Activate on macOS/Linux
source .venv/bin/activate
```

**c. Install dependencies:**
First, create a `requirements.txt` file if it's not already in the project by running this command in your active virtual environment:
```bash
pip freeze > requirements.txt
```
Then, install the packages:
```bash
pip install -r requirements.txt
```

**d. Setup the Database:**
- Open pgAdmin or your preferred PostgreSQL client.
- Create a new, empty database (e.g., `kalbio_db`).
- Open the `kalbio_dashboard/settings.py` file.
- Update the `DATABASES` configuration with your own database credentials:
  ```python
  DATABASES = {
      'default': {
          'ENGINE': 'django.db.backends.postgresql',
          'NAME': 'kalbio_db',        # Your database name
          'USER': 'postgres',        # Your PostgreSQL username
          'PASSWORD': 'your_password', # Your PostgreSQL password
          'HOST': 'localhost',
          'PORT': '5432',
      }
  }
  ```

**e. Run Migrations:**
This will create all the necessary tables in your new database.
```bash
python manage.py migrate
```

**f. Create a Superuser:**
This account will have access to the Django Admin panel.
```bash
python manage.py createsuperuser
```
Follow the prompts to create your admin username and password.

### 3. Running the Application
```bash
python manage.py runserver
```
The application will be available at `http://127.0.0.1:8000/`.

### 4. Initial Admin Setup (Important)
- Go to `http://127.0.0.1:8000/admin/` and log in with your superuser account.
- Navigate to the **"Groups"** section.
- Click **"+ Add group"** and create the following groups:
    - `Operator`
    - `MSTD`
    - `QC`
    - `Manajemen`
- Go to each group and assign the appropriate permissions.
- You can now create new users and assign them to these groups.
