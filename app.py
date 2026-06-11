"""Tiny Flask app — applied-ai-sandbox.

Each task in tasks/ asks you to add or fix one piece. The tests in tests/
describe exactly what "done" means.
"""
from __future__ import annotations

from flask import Flask, render_template, request, redirect, url_for, abort


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "sandbox-not-a-real-secret"

    # In-memory store for the sandbox. Resets on every restart, which is
    # fine for practice. Real apps use a database.
    app.notes: list[dict] = []  # type: ignore[attr-defined]

    @app.route("/")
    def home():
        filter_starred = request.args.get("filter") == "starred"
        indexed = list(enumerate(app.notes))
        if filter_starred:
            indexed = [(i, n) for i, n in indexed if n.get("starred", False)]
        return render_template("home.html", notes=indexed, filter_starred=filter_starred)

    @app.route("/notes/new", methods=["GET", "POST"])
    def new_note():
        if request.method == "POST":
            title = (request.form.get("title") or "").strip()
            body = (request.form.get("body") or "").strip()
            # TASK 01 will add validation here.
            app.notes.append({"title": title, "body": body, "tags": [], "starred": False})
            return redirect(url_for("home"))
        return render_template("new_note.html")

    # TASK 02 will add a /notes/<idx>/delete route here.

    @app.route("/notes/<int:idx>/star", methods=["POST"])
    def star_note(idx):
        """Toggle the starred status of a note."""
        if idx < 0 or idx >= len(app.notes):
            abort(404)
        app.notes[idx]["starred"] = not app.notes[idx].get("starred", False)
        return redirect(url_for("home"))

    return app


if __name__ == "__main__":
    create_app().run(debug=True, port=5000)
