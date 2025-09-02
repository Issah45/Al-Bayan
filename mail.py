import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_mail(guy):
    # Create the email
    msg = MIMEMultipart()
    msg['From'] = "issuseless4@gmail.com"
    msg['To'] = "abeebissa@gmail.com"
    msg['Subject'] = "Login Attempt Notification"

    # HTML content
    html_content = f"""
    <h2>{guy} is trying to login into Al-Bayan</h2>
    <p>Please click the button below to authorize:</p>
    <a href="your_authorization_link_here"><button>Authorize</button></a>
    """

    # Attach the HTML content
    msg.attach(MIMEText(html_content, 'html'))

    # Set up the server and send the email
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login("issuseless4@gmail.com", "webg olqy nnfj tcjx")  # Use your actual password

    # Send the email
    server.send_message(msg)
    server.quit()