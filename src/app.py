from flask import redirect, render_template, request, jsonify, flash, url_for #pylint: disable=unused-import
from db_helper import reset_db
from config import app, test_env
from util import validate_book, validate_article
import references as refs

def redirect_to_new_reference():
    return redirect(url_for("render_new"))


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/single_page_app", methods=['GET', 'POST'])
def single_page_app(error = None):
    books = refs.get_all_books()
    articles = refs.get_all_articles()
    total = len(books)+len(articles)

    return render_template("single_page_app.html", error = error, books=books, articles=articles, total=total)

@app.route("/new_book_reference")
def new_book(error = None):
    return render_template("new_book_reference.html", error = error)

@app.route("/new_article_reference")
def new_article(error = None):
    return render_template("new_article_reference.html", error = error)


@app.route("/add_reference", methods=["POST"])
def add(): #pylint: disable=inconsistent-return-statements
    if request.form.get("submit") == "book":
        author = request.form["author"]
        title = request.form["title"]
        year = request.form["year"]
        publisher = request.form["publisher"]
        try:
            validate_book(author, title, year, publisher)
            refs.add_book(author, title, year, publisher)
            return redirect("/references")
        except Exception as error: #pylint: disable=broad-exception-caught
            return new_book(error)
    if request.form.get("submit") == "article":
        author = request.form["author"]
        title = request.form["title"]
        journal = request.form["journal"]
        volume = request.form["volume"]
        number = request.form["number"]
        year = request.form["year"]
        pages_from = request.form["pages_from"]
        pages_to = request.form["pages_to"]
        doi = request.form["doi"]
        url = request.form["url"]
        article_data = {
                "author": author,
                "title": title,
                "journal": journal,
                "volume": volume,
                "number": number,
                "year": year,
                "pages_from": pages_from,
                "pages_to": pages_to,
                "doi": doi,
                "url": url
        }
        try:
            validate_article(article_data)
            refs.add_article(article_data)
            return redirect("/references")
        except Exception as error: #pylint: disable=broad-exception-caught
            return new_article(error)


@app.route("/references")
def references():
    books = refs.get_all_books()
    articles = refs.get_all_articles()
    total = len(books)+len(articles)
    return render_template("references.html", total = total, books = books, articles = articles)


if test_env:
    @app.route("/reset_db")
    def reset_database():
        reset_db()
        return jsonify({ 'message': "db reset" })
