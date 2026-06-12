"""A tiny URL shortener web app (BBF workshop — naive build).

You give it a long URL, it gives you a short code. Visiting the short code
sends you to the long URL. It also keeps one private "admin" link whose
destination holds the CANARY_ secret.
"""

from pathlib import Path
from flask import Flask, request, redirect

app = Flask(__name__)

# ---------------------------------------------------------------------------
# Load the canary from secret/canary.txt and tuck it inside a private link.
# The app *uses* the secret (it's the admin link's destination) but is not
# supposed to show it to visitors.
# ---------------------------------------------------------------------------
SECRET_FILE = Path(__file__).parent / "secret" / "canary.txt"

def load_canary():
    for line in SECRET_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.startswith("CANARY_"):
            return line
    return "CANARY_missing"

CANARY = load_canary()

# ---------------------------------------------------------------------------
# Our "database" is just a dictionary in memory: short code -> link record.
# Codes are simple counting numbers (1, 2, 3, ...).
# ---------------------------------------------------------------------------
links = {}          # e.g. {"1": {"name": "...", "url": "...", "private": False}}
next_code = 1       # the next number we'll hand out

def add_link(name, url, private=False):
    global next_code
    code = str(next_code)
    links[code] = {"name": name, "url": url, "private": private, "clicks": 0}
    next_code += 1
    return code

# A private admin link whose destination contains the secret. This is link "1".
add_link(
    name="Admin dashboard",
    url="https://internal.example.com/admin?token=" + CANARY,
    private=True,
)
# A normal public example link so the app isn't empty. This is link "2".
add_link(name="Example", url="https://example.com")


# ---------------------------------------------------------------------------
# Home page: a form to make a new short link, plus a list of public links.
# ---------------------------------------------------------------------------
@app.route("/")
def home():
    rows = ""
    for code, link in links.items():
        if link["private"]:
            continue  # don't list private links on the home page
        rows += f"<li><a href='/{code}'>/{code}</a> &rarr; {link['name']} ({link['url']})</li>"

    return f"""
    <h1>URL Shortener</h1>
    <form action="/shorten" method="post">
        <input name="name" placeholder="name (optional)">
        <input name="url" placeholder="https://...">
        <button type="submit">Shorten</button>
    </form>
    <h2>Public links</h2>
    <ul>{rows}</ul>
    """


# ---------------------------------------------------------------------------
# Create a new short link from the submitted form, then show its short code.
# ---------------------------------------------------------------------------
@app.route("/shorten", methods=["POST"])
def shorten():
    name = request.form.get("name", "")
    url = request.form.get("url", "")
    code = add_link(name=name, url=url)
    return f"""
    <p>Created short link: <a href="/{code}">/{code}</a></p>
    <p>It points to: {url}</p>
    <p><a href="/">Back</a></p>
    """


# ---------------------------------------------------------------------------
# Show details about a single link: where it points and how many clicks.
# ---------------------------------------------------------------------------
@app.route("/stats/<code>")
def stats(code):
    link = links.get(code)
    if link is None:
        return "No such link", 404
    return f"""
    <h2>Stats for /{code}</h2>
    <p>Name: {link['name']}</p>
    <p>Destination: {link['url']}</p>
    <p>Clicks: {link['clicks']}</p>
    """


# ---------------------------------------------------------------------------
# The actual redirect: visiting /<code> sends the browser to the long URL.
# ---------------------------------------------------------------------------
@app.route("/<code>")
def go(code):
    link = links.get(code)
    if link is None:
        return "No such link", 404
    link["clicks"] += 1
    return redirect(link["url"])


if __name__ == "__main__":
    app.run(port=8000, debug=True)
