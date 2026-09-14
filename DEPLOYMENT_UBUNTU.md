# Deploying to Ubuntu VPS — Step-by-Step Guide

This guide will walk you through deploying your Flask CRM on a fresh Ubuntu 22.04 or 24.04 VPS using **Gunicorn**, **Nginx**, and **systemd**.

## Step 1: Update Server and Install Dependencies

Log into your server via SSH and run:

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip python3-dev python3-venv build-essential libssl-dev libffi-dev python3-setuptools nginx git curl certbot python3-certbot-nginx -y
```

## Step 2: Set Up the Database (MySQL or PostgreSQL)

### Option A: Install MySQL
```bash
sudo apt install mysql-server -y
sudo systemctl start mysql.service
sudo mysql
```
In the MySQL prompt, run:
```sql
CREATE DATABASE crm_db;
CREATE USER 'crm_user'@'localhost' IDENTIFIED BY 'your_strong_password';
GRANT ALL PRIVILEGES ON crm_db.* TO 'crm_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

## Step 3: Clone the Repository

Create a directory for your project and clone your code:

```bash
cd /var/www
sudo git clone https://github.com/yourusername/Real-Estate-CRM.git
sudo chown -R $USER:$USER /var/www/Real-Estate-CRM
cd Real-Estate-CRM
```

## Step 4: Create Virtual Environment & Install Requirements

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

*(Note: If you run into issues installing cryptography or pycryptodome, ensure `build-essential` and `libssl-dev` were installed in Step 1)*

## Step 5: Configure the Environment (.env)

Create your `.env` file in the project root:

```bash
nano .env
```

Paste your production configurations:
```ini
FLASK_CONFIG=production
SECRET_KEY=generate-64-random-chars-here
JWT_SECRET_KEY=generate-another-64-random-chars
DATABASE_URL=mysql+pymysql://crm_user:your_strong_password@localhost/crm_db
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
META_VERIFY_TOKEN=some-random-string-you-choose
UPLOAD_FOLDER=/var/www/Real-Estate-CRM/backend/uploads
RECORDINGS_FOLDER=/var/www/Real-Estate-CRM/backend/uploads/recordings
```
Save and exit (`CTRL+O`, `Enter`, `CTRL+X`).

## Step 6: Initialize the Database

Now run the database reset wrapper to create the tables:

```bash
python reset_db.py
# Type 'yes' and 'RESET' to confirm
```

*Alternatively, create just the admin user:*
```bash
cd backend
flask create-admin
cd ..
```

## Step 7: Create a systemd Service for Gunicorn

To keep your app running in the background and restart it on reboots, create a systemd service file:

```bash
sudo nano /etc/systemd/system/crm.service
```

Paste the following:

```ini
[Unit]
Description=Gunicorn instance to serve Southeast Landmark CRM
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/Real-Estate-CRM
Environment="PATH=/var/www/Real-Estate-CRM/venv/bin"
# Ensure logs and uploads directories exist with right permissions
ExecStartPre=/bin/mkdir -p /var/www/Real-Estate-CRM/logs /var/www/Real-Estate-CRM/backend/uploads/recordings
ExecStartPre=/bin/chown -R www-data:www-data /var/www/Real-Estate-CRM/logs /var/www/Real-Estate-CRM/backend/uploads
ExecStart=/var/www/Real-Estate-CRM/venv/bin/gunicorn --workers 1 --threads 5 --bind unix:crm.sock -m 007 "backend.app:create_app('production')"

[Install]
WantedBy=multi-user.target
```
*(Note: We use 1 worker and 5 threads because APScheduler handles background tasks internally, and multiple workers could duplicate scheduled jobs without an external Redis broker).*

Start and enable the Gunicorn service:
```bash
sudo systemctl start crm
sudo systemctl enable crm
```

## Step 8: Configure Nginx as a Reverse Proxy

Create an Nginx server block:

```bash
sudo nano /etc/nginx/sites-available/crm
```

Paste the following (replace `office.southeastlandmark.info` with your domain):

```nginx
server {
    listen 80;
    server_name office.southeastlandmark.info;

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/Real-Estate-CRM/crm.sock;
        
        # Increase timeout for large file uploads
        proxy_read_timeout 300;
        proxy_connect_timeout 300;
        proxy_send_timeout 300;
        client_max_body_size 50M;
    }
}
```

Enable the configuration and restart Nginx:
```bash
sudo ln -s /etc/nginx/sites-available/crm /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

## Step 9: Enable HTTPS with Certbot (Let's Encrypt)

Secure your application with a free SSL certificate:

```bash
sudo certbot --nginx -d office.southeastlandmark.info
```
Follow the prompts. Certbot will automatically update your Nginx configuration to force HTTPS.

## Step 10: Final Permissions Check

Ensure Nginx and Gunicorn (`www-data`) have permissions to read your files and write to the logs/uploads directories:

```bash
sudo chown -R www-data:www-data /var/www/Real-Estate-CRM/logs
sudo chown -R www-data:www-data /var/www/Real-Estate-CRM/backend/uploads
sudo chmod -R 755 /var/www/Real-Estate-CRM/backend/uploads
sudo chmod 600 /var/www/Real-Estate-CRM/.env
```

---
**Done!** Your CRM is now live on your Ubuntu VPS. Check `sudo journalctl -u crm` or `/var/www/Real-Estate-CRM/logs/bot.log` if you encounter any errors.
