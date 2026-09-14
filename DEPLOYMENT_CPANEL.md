# Deploying to cPanel — Step-by-Step Guide

## What You Need
- A cPanel hosting account with **Python support**
- A MySQL database
- Your domain (`office.southeastlandmark.info`) pointed at your hosting

---

## Step 1: Create a MySQL Database in cPanel

1. Log in to cPanel
2. Find **MySQL Databases**
3. Create a new database — e.g., `southeas_crm`
4. Create a new database user — e.g., `southeas_crmuser` with a strong password
5. Add the user to the database with **All Privileges**
6. Note these values — you'll need them for your `.env`

---

## Step 2: Upload Your Files

1. In cPanel, open **File Manager**
2. Upload the entire project so that the root folder is at `/home/southeas/repositories/Real-Estate-CRM/`
3. Check that files like `passenger_wsgi.py`, `requirements.txt`, `run.py`, and the `backend/` folder are inside this root directory.
4. Manually create the `logs` folder and `uploads` folder if they don't exist:
   - `/home/southeas/repositories/Real-Estate-CRM/logs/`
   - `/home/southeas/repositories/Real-Estate-CRM/backend/uploads/`

---

## Step 3: Create Your .env File

1. In File Manager, navigate to `/home/southeas/repositories/Real-Estate-CRM/`
2. Create a new file named `.env`
3. Fill in your real database credentials and other settings:

```ini
FLASK_CONFIG=production
SECRET_KEY=generate-64-random-chars-here
JWT_SECRET_KEY=generate-another-64-random-chars
DATABASE_URL=mysql+pymysql://southeas_crmuser:YOUR_DB_PASSWORD@localhost/southeas_crm
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
META_VERIFY_TOKEN=some-random-string-you-choose
UPLOAD_FOLDER=/home/southeas/repositories/Real-Estate-CRM/backend/uploads
RECORDINGS_FOLDER=/home/southeas/repositories/Real-Estate-CRM/backend/uploads/recordings
```

---

## Step 4: Set Up Python App in cPanel

1. In cPanel, find **Setup Python App**
2. Click **Create Application**
3. Fill in exactly as follows:
   - **Python version**: `3.11` (or `3.12`/`3.13` if 3.11 is not available)
   - **Application root**: `repositories/Real-Estate-CRM`
   - **Application URL**: `office.southeastlandmark.info`
   - **Application startup file**: `passenger_wsgi.py`
   - **Application Entry point**: `application`
4. Click **Create**

---

## Step 5: Install Dependencies

1. Scroll down on the **Setup Python App** page to the **Configuration files** section.
2. In the "Add another file or directory" box, type `requirements.txt` and click **Add**.
3. Click the **Run Pip Install** button next to it. Wait for it to complete.

*(Alternative: You can open the cPanel **Terminal**, activate your virtual environment using the command shown at the top of the Setup Python App page, and run `pip install -r requirements.txt`)*

---

## Step 6: Initialize the Database (If starting fresh)

If you haven't set up the database tables yet, do this in the cPanel Terminal:

```bash
# First, activate your virtual environment (copy the exact command from the top of the "Setup Python App" page)
source /home/southeas/virtualenv/repositories/Real-Estate-CRM/3.11/bin/activate

# Go to your project root
cd /home/southeas/repositories/Real-Estate-CRM

# Create all database tables
python reset_db.py
# (Type 'yes' and 'RESET' to confirm)

# Alternatively, if you just want to create an admin account:
cd backend
flask create-admin
# Enter your email, password, and name when prompted
```

---

## Step 7: Restart and Test

1. Go back to the **Setup Python App** page in cPanel.
2. Click the **Restart** button next to your application.
3. Open your browser and go to `https://office.southeastlandmark.info`

If you encounter any 500 Internal Server errors, check the logs in `/home/southeas/repositories/Real-Estate-CRM/logs/bot.log` to see what went wrong.

---

## Folder Permissions
Ensure these permissions in File Manager for security:
```text
backend/uploads/           → 755
logs/                      → 755
.env                       → 600  (owner read-only)
```
