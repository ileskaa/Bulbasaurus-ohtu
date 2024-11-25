from flask import (
    redirect,
    render_template,
    request,
    jsonify,
    url_for,
)
from db_helper import reset_db
from config import app, test_env
from util import validate_book, validate_article, validate_misc, validate_inproceedings
import references as refs
import get_references
import edit_references

def redirect_to_new_reference():
    return redirect(url_for("render_new"))


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/new_book_reference")
def new_book(error=None):
    return render_template("new_book_reference.html", error=error)


@app.route("/new_article_reference")
def new_article(error=None):
    return render_template("new_article_reference.html", error=error)


@app.route("/new_misc_reference")
def new_misc(error=None):
    return render_template("new_misc_reference.html", error=error)


@app.route("/new_inproceedings_reference")
def new_inproceedings(error=None):
    return render_template("new_inproceedings_reference.html", error=error)


@app.route("/add_reference", methods=["POST"])
def add():  # pylint: disable=inconsistent-return-statements
    if request.form.get("submit") == "book":
        author = request.form["author"]
        title = request.form["title"]
        year = request.form["year"]
        publisher = request.form["publisher"]
        try:
            validate_book(author, title, year, publisher)
            refs.add_book(author, title, year, publisher)
            return redirect("/references")
        except Exception as error:  # pylint: disable=broad-exception-caught
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
            "url": url,
        }
        try:
            validate_article(article_data)
            refs.add_article(article_data)
            return redirect("/references")
        except Exception as error:  # pylint: disable=broad-exception-caught
            return new_article(error)
    if request.form.get("submit") == "misc":
        author = request.form["author"]
        title = request.form["title"]
        year = request.form["year"]
        note = request.form["note"]
        try:
            validate_misc(author, title, year, note)
            refs.add_misc(author, title, year, note)
            return redirect("/references")
        except Exception as error:  # pylint: disable=broad-exception-caught
            return new_misc(error)
    if request.form.get("submit") == "inproceedings":
        author = request.form["author"]
        title = request.form["title"]
        year = request.form["year"]
        booktitle = request.form["booktitle"]
        try:
            validate_inproceedings(author, title, year, booktitle)
            refs.add_inproceedings(author, title, year, booktitle)
            return redirect("/references")
        except Exception as error:  # pylint: disable=broad-exception-caught
            return new_inproceedings(error)


@app.route("/references")
def references():
    books = refs.get_all_books()
    articles = refs.get_all_articles()
    miscs = refs.get_all_misc()
    inproceedings = refs.get_all_inproceedings()
    total = len(books) + len(articles) + len(miscs) + len(inproceedings)
    return render_template(
        "references.html",
        total=total,
        books=books,
        articles=articles,
        miscs=miscs,
        inproceedings=inproceedings,
    )


@app.route("/remove_reference/<reference_id>", methods=["POST"])
def remove_reference(reference_id):
    refs.remove_reference(reference_id)
    books = refs.get_all_books()
    articles = refs.get_all_articles()
    miscs = refs.get_all_misc()
    inproceedings = refs.get_all_inproceedings()
    total = len(books) + len(articles) + len(miscs) + len(inproceedings)
    return render_template(
        "references.html",
        total=total,
        books=books,
        articles=articles,
        miscs=miscs,
        inproceedings=inproceedings,
    )


@app.route("/edit_reference", methods=["POST"])
def edit_reference():
    button_value = request.form.get("button")
    reference_id = request.form.get("reference_id")

    if button_value == "save_changes":
        form_data = request.form.to_dict()
        print(form_data)
        #[print(d, form_data[d]) for d in form_data]
        #value = edit_references.update_reference()

    reference_info, reference_type = get_references.get_reference_info_by_id(reference_id)
    return render_template("edit_reference.html",
                        reference_id=reference_id,
                        reference_info=reference_info,
                        reference_type=reference_type)

if test_env:

    @app.route("/reset_db")
    def reset_database():
        reset_db()
        return jsonify({"message": "db reset"})
