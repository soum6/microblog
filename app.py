import os
from flask import Flask, render_template, request
import datetime
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()


def create_app():
    app = Flask(__name__)
    """
    """
    client = MongoClient(os.environ.get("MONGODB_URI"))
    app.db = client.microblog


    @app.route("/", methods=["GET", "POST"])
    def index():

        print([e for e in app.db.entries.find({})])
        print("abc")

        if request.method == "POST":
            entry_content = request.form.get("content")
            date_formatted = datetime.datetime.today().strftime("%Y-%m-%d")
            app.db.entries.insert({"content": entry_content, "date": date_formatted})

        entries_with_date = [
            (
                entry["content"],
                entry["date"],
                datetime.datetime.strptime(entry["date"], "%Y-%m-%d").strftime("%b %d"),
            )
            for entry in app.db.entries.find({})
        ]
        return render_template("index.html", entries=entries_with_date)
    
    return app


if __name__ == "__main__":
    app.run(debug=True)
