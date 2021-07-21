import smtplib
import os


def send_mail(content, recipient=os.environ.get("RECIPIENT"), sender=os.environ.get("SENDER"),
              sender_pw=os.environ.get("SENDER_PW"), subject="New message from your personal blog"):
    try:
        # Establish and close connection
        with smtplib.SMTP("smtp.gmail.com") as connection:
            # Secure connection
            connection.starttls()
            # Login by providing account information
            connection.login(user=sender, password=sender_pw)
            # Send Mail
            connection.sendmail(
                from_addr=sender,
                to_addrs=recipient,
                msg=f"Subject:{subject}\n\n{content}"
            )
            print("Email successfully sent.")
    except ConnectionError:
        print("Could not establish connection")

