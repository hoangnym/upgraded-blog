from flask import Flask, render_template, request
from posts import Post
import requests
import os
import smtplib


all_posts = requests.get("https://api.npoint.io/706ae5b51a7218849686").json()
post_objects = [Post(post["id"], post["title"], post["subtitle"], post["body"]) for post in all_posts]

# Credentials
RECIPIENT = os.environ.get("RECIPIENT")
SENDER = os.environ.get("SENDER")
SENDER_PW = os.environ.get("SENDER_PW")

# Reminder: Turn on access for less secure apps in order to use this application
def send_mail(content, recipient=RECIPIENT, sender=SENDER,
              sender_pw=SENDER_PW, subject="New message from your personal blog"):
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

app = Flask(__name__)


@app.route('/')
def home():
    return render_template(
        "index.html",
        posts=post_objects
    )


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/contact', methods=["GET"])
def contact():
    print(request.method)
    return render_template(
        "contact.html",
        method=request.method
    )


@app.route('/contact', methods=["POST"])
def receive_data():
    print(request.method)
    data = request.form
    name = data["username"]
    email = data["email"]
    phone = data["phone"]
    message = data["message"]
    message_content = f"Name: {name}\n" \
              f"Email: {email}\n" \
              f"Phone: {phone}\n" \
              f"Message: {message}"
    send_mail(message_content)
    return render_template(
        "contact.html",
        method=request.method
    )

@app.route('/post/<int:index>')
def get_post(index):
    return render_template(
        "post.html",
        post=post_objects[index]
    )



if __name__ == '__main__':
    app.run(debug=True)
