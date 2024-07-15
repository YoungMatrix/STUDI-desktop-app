# STUDI Mobile Application

## Requirements
- **VS Studio Code** version >= 1.91.0
  - Python Extension version >= 2024.10.0
- **XAMPP** version >= 8.2.12 with Control Panel version >= 3.3.0
- **Python3** version => 3.7.9 with libraries:
    - **python-dotenv**: `pip3 install python-dotenv`
    - **mysql-connector-python**: `pip3 install mysql-connector-python`
- **Database connection parameters** (online or local database).

## Steps to Prepare the Application for Windows

### Clone Repository
1. Open VS Studio Code.
2. In the terminal:
   ```bash
   git clone https://github.com/YoungMatrix/STUDI-desktop-app
3. Login to GIT if necessary.

### Setup Environment
4. In VS Studio Code, open the directory directly in STUDI-mobile-app.
5. Create .env file in /app directory with the following content:
    # File verified

    # Database connection parameters (online or local database)
    DB_HOST=To Be Completed

    DB_USER=TBC

    DB_PASSWORD=TBC

    DB_DATABASE=TBC

    DB_PORT=TBC

    # Pepper used for hashing passwords
    PEPPER=Studi

### Database Setup
6. Start Apache and MySQL from XAMPP Control Panel.
7. Open MySQL as admin.
8. In phpMyAdmin, create a new database named ecf_studi_verified.
9. Import the file ecf_studi_verified.sql from STUDI-mobile-app/db directory into the newly created database.

### Steps to Launch the Application for Windows
10. Go to main.py file in STUDI-mobile-app/app.
11. Run the file.
