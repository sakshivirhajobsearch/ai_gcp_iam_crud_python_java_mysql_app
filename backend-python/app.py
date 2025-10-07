from flask import Flask, jsonify, request
import mysql.connector
from config import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB
from gcp_iam import list_iam_users
from ai_module import analyze_iam_permissions

app = Flask(__name__)

# ---------- MySQL Connection Helper ----------
def get_mysql_connection():
    return mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB
    )

# ---------- Save IAM Users ----------
def save_iam_users(users):
    conn = get_mysql_connection()
    cursor = conn.cursor()
    for user in users:
        cursor.execute("""
            INSERT INTO iam_users (name, email, disabled)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE disabled=%s
        """, (user['name'], user['email'], user['disabled'], user['disabled']))
    conn.commit()
    cursor.close()
    conn.close()

# ---------- Save AI Alerts ----------
def save_ai_alerts(alerts):
    conn = get_mysql_connection()
    cursor = conn.cursor()
    for alert in alerts:
        # extract email from alert if possible
        email = alert.split()[1] if len(alert.split()) > 1 else "unknown"
        cursor.execute("""
            INSERT INTO iam_ai_alerts (email, alert_text)
            VALUES (%s, %s)
        """, (email, alert))
    conn.commit()
    cursor.close()
    conn.close()

# ---------- Root Route ----------
@app.route('/')
def home():
    return "AI + GCP IAM CRUD Backend is running! Use /iam/sync/<project_id> to fetch IAM users."

# ---------- IAM Sync Route ----------
@app.route('/iam/sync/<project_id>', methods=['GET'])
def sync_iam(project_id):
    try:
        # 1. Fetch IAM users (real or dummy)
        users = list_iam_users(project_id)

        # 2. Run AI analysis
        ai_alerts = analyze_iam_permissions(users)

        # 3. Save users and AI alerts to MySQL
        save_iam_users(users)
        save_ai_alerts(ai_alerts)

        # 4. Return JSON response
        return jsonify({
            'status': 'success',
            'users_count': len(users),
            'ai_alerts_count': len(ai_alerts),
            'users': users,
            'ai_alerts': ai_alerts
        })

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# ---------- Run Flask ----------
if __name__ == '__main__':
    # host="0.0.0.0" allows external access if needed
    app.run(host="0.0.0.0", port=5000, debug=True)
