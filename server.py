from flask import Flask, request, render_template, Response
import json
import os
from datetime import datetime
from functools import wraps
import re

app = Flask(__name__)

Username = 'admin'
Password = 'admin'


def check_auth(username, password):
    return username == Username and password == Password


def authenticate():
    return Response(
    'Unauthorized', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'}
    )


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


def sanitize_filename(title):
    title = re.sub(r"\s+", "-", title)
    title = re.sub(r"[^a-zA-Zа-яА-Я0-9_-]", "", title)
    return title.lower()


def get_articles():
    articles = []

    for filename in os.listdir('articles'):
        if filename.endswith(".json"):
            with open(os.path.join('articles', filename), "r", encoding="utf-8") as file:
                data = json.load(file)
                data = {'title': data["title"], 'filename': filename, "date": data["date"]}
                articles.append(data)

    articles.sort(key=lambda x: x["date"], reverse=True)
    return articles


@app.route("/", methods=["GET"])
def home():
    articles = get_articles()
    return render_template("home.html", articles=articles)


@app.route('/admin', methods=['GET'])
@requires_auth
def admin():
    articles = get_articles()
    return render_template("admin.html", articles=articles)


@app.route('/admin/new', methods=['GET'])
@requires_auth
def new():
    return render_template("new.html")


@app.route('/admin/new/create', methods=['POST'])
@requires_auth
def create():
    title = sanitize_filename(request.form['title'])
    if not title:
        return 'Invalid Title'
    
    date = request.form['date']
    content = request.form['content']

    if os.path.exists(f'articles/{title}.json'):
        return 'Article already exists'
    
    else:
        data = {'title': title, 'date': date if date else str(datetime.today()).split(" ")[0], 'content': content}

        try:
            with open(f'articles/{title}.json', 'w') as f:
                json.dump(data, f)
            return 'Success'
        
        except Exception as err:
            return 'Invalid Text'
    

@app.route('/articles/<title>', methods=['GET'])
def get_article(title):
    file_path = os.path.join("articles", f"{title}")
    
    if not os.path.exists(file_path):
        return "Article not found", 404  

    with open(file_path, "r", encoding="utf-8") as file:
        article = json.load(file)
    
    return render_template("article.html", title=title, date=article['date'], content=article['content'])



@app.route('/admin/articles/<title>', methods=['GET'])
@requires_auth
def get_admin_article(title):
    file_path = os.path.join("articles", f"{title}")
    
    if not os.path.exists(file_path):
        return "Article not found", 404  

    with open(file_path, "r", encoding="utf-8") as file:
        article = json.load(file)
    
    return render_template("admin_article.html", title=title[:-5], date=article['date'], content=article['content'])


@app.route('/admin/articles/<title>/edit', methods=['GET'])
@requires_auth
def edit(title):
    file_path = os.path.join("articles", f"{title}.json")
    
    if not os.path.exists(file_path):
        return "Article not found", 404

    with open(file_path, "r", encoding="utf-8") as file:
        article = json.load(file)
    
    return render_template("edit.html", title=title, date=article['date'], content=article['content'])


@app.route('/admin/articles/<title>/edit/submit', methods=['POST'])
@requires_auth
def submit(title):
    file_path = os.path.join("articles", f"{title}.json")
    
    if not os.path.exists(file_path):
        return "Article not found", 404

    new_title = sanitize_filename(request.form['title'])
    if not new_title:
        return 'Invalid Title'
    
    if os.path.exists(f'articles/{new_title}.json') and new_title != title:
        return "Article already exists"
    
    date = request.form['date']
    content = request.form['content']

    data = {'title': new_title, 'date': date, 'content': content}
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f)

    os.rename(file_path, os.path.join("articles", f"{new_title}.json"))
    
    return 'Success'


@app.route('/admin/articles/<title>/delete', methods=['GET'])
@requires_auth
def delete(title):
    file_path = os.path.join("articles", f"{title}.json")
    
    if not os.path.exists(file_path):
        return "Article not found", 404

    os.remove(file_path)
    return 'Success'
    

if __name__ == "__main__":
    app.run(debug=True, port=5500)