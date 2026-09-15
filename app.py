from flask import Flask, render_template, request, jsonify
from urllib.parse import urlparse
import ipaddress
import re

app = Flask(__name__)

SUSPICIOUS_WORDS = {
    "verify", "verification", "login", "signin", "account", "update",
    "secure", "security", "password", "confirm", "free", "winner",
    "prize", "gift", "bank", "payment", "wallet"
}

SHORTENERS = {"bit.ly", "tinyurl.com", "t.co", "is.gd", "cutt.ly", "shorturl.at"}

def analyze_url(raw_url):
    url = raw_url.strip()
    if not url:
        return {"status": "INVALID", "score": 100, "reasons": ["No URL was entered."]}

    test_url = url if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*://", url) else "https://" + url
    parsed = urlparse(test_url)
    host = (parsed.hostname or "").lower()
    score = 0
    reasons = []

    if parsed.scheme != "https":
        score += 10
        reasons.append("The URL does not use HTTPS.")

    if "@" in url:
        score += 25
        reasons.append("The URL contains '@', which can obscure the actual destination.")

    if len(url) > 100:
        score += 10
        reasons.append("The URL is unusually long.")

    try:
        ipaddress.ip_address(host)
        score += 25
        reasons.append("The host is an IP address instead of a normal domain.")
    except ValueError:
        pass

    if host in SHORTENERS:
        score += 15
        reasons.append("The link uses a URL-shortening service.")

    if host.count(".") >= 3:
        score += 10
        reasons.append("The domain contains many subdomains.")

    lower = url.lower()
    found = sorted({word for word in SUSPICIOUS_WORDS if word in lower})
    if found:
        score += min(20, 5 * len(found))
        reasons.append("Suspicious keywords detected: " + ", ".join(found) + ".")

    if "-" in host and len(host.split(".")) >= 2:
        # Only a small prototype heuristic; hyphens alone do not mean phishing.
        score += 3
        reasons.append("The domain contains hyphens; this is only a weak risk indicator.")

    score = min(score, 100)

    if score >= 60:
        status = "HIGH RISK"
    elif score >= 30:
        status = "SUSPICIOUS"
    else:
        status = "LOW RISK"

    if not reasons:
        reasons.append("No prototype risk indicators were detected.")

    return {"status": status, "score": score, "reasons": reasons, "normalized_url": test_url}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/scan", methods=["POST"])
def scan():
    data = request.get_json(silent=True) or {}
    return jsonify(analyze_url(data.get("url", "")))

if __name__ == "__main__":
    # Listen on the local network so a phone can connect during development.
    app.run(host="0.0.0.0", port=5000, debug=True)
