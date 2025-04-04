import re
from collections import defaultdict
import matplotlib.pyplot as plt

log_file_path = r"Path\to\your\logfile.log"

failed_login_count = 0
ip_counter = defaultdict(int)

try:
    with open(log_file_path, "r") as file:
        for line in file:
            if "Failed password" in line:
                failed_login_count += 1
                ip_match = re.search(r'from (\d+\.\d+\.\d+\.\d+)(?:\.\d+)?', line)
                if ip_match:
                    ip_counter[ip_match.group(1)] += 1

    print(f"\n❌ Total Failed Login Attempts: {failed_login_count:,}\n")
    
    # Get top 10 IPs
    sorted_ips = sorted(ip_counter.items(), key=lambda x: x[1], reverse=True)[:10]
    ip_labels = [ip for ip, _ in sorted_ips]
    attempt_counts = [count for _, count in sorted_ips]

    # Print results
    print("📊 Top 10 IPs with most failed login attempts:")
    for ip, count in sorted_ips:
        print(f"- {ip}: {count:,} failed attempts")

    # Enhanced visualization
    plt.style.use('ggplot')
    plt.figure(figsize=(14, 7))
    bars = plt.barh(ip_labels, attempt_counts, color='#dc3545')
    plt.bar_label(bars, padding=3, fontsize=9)
    
    plt.title(f"SSH Brute Force Attacks\nTotal Failed Attempts: {failed_login_count:,}", 
             fontsize=14, pad=20)
    plt.xlabel("Failed Attempts", fontsize=12)
    plt.ylabel("IP Address", fontsize=12)
    plt.grid(axis='x', alpha=0.4)
    
    plt.tight_layout()
    plt.savefig('ssh_attackers.png', dpi=300)
    print("\n✅ Visualization saved as 'ssh_attackers.png'")

except FileNotFoundError:
    print(f"❌ Error: File not found at {log_file_path}")
except Exception as e:
    print(f"⚠️ Error: {str(e)}")
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email_alert(suspicious_ips):
    sender_email = "youremail@gmail.com"  # Replace with your Gmail address
    receiver_email = "youremail@gmail.com"
    app_password = "Your password"  # Use the 16-digit Gmail App Password

    subject = "🚨 SSH Log Alert - Suspicious IPs Detected"
    body = "The following IPs had more than 1000 failed SSH login attempts:\n\n"

    for ip, count in suspicious_ips:
        body += f"{ip} → {count} failed attempts\n"

    # Create email
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, app_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        print("📧 Email alert sent successfully to youremail@gmail.com!")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
# 🚨 ALERT LOGIC
alert_threshold = 1000
suspicious_ips = [(ip, count) for ip, count in ip_counter.items() if count > alert_threshold]

if suspicious_ips:
    print("\n🚨 ALERT! Suspicious IPs detected (failed attempts > 1000):")
    for ip, count in suspicious_ips:
        print(f"🔴 {ip}: {count:,} failed attempts")

    # 👉 Call the function here
    send_email_alert(suspicious_ips)