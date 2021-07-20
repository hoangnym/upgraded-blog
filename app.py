from flask import Flask, render_template
from posts import Post
import requests

all_posts = requests.get("https://api.npoint.io/706ae5b51a7218849686").json()
post_objects = [Post(post["id"], post["title"], post["subtitle"], post["body"]) for post in all_posts]


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


@app.route('/contact')
def contact():
    return render_template("contact.html")


@app.route('/post/<int:index>')
def get_post(index):
    return render_template(
        "post.html",
        post=post_objects[index]
    )


if __name__ == '__main__':
    app.run(debug=True)
