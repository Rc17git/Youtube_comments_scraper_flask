from flask import Flask, render_template, request, send_file
from scrape_comments import scrape_youtube_comments_to_csv
import base64


app = Flask(__name__)

# Define a custom filter for Base64 encoding
@app.template_filter('custom_b64encode')
def custom_b64encode(s):
    return base64.b64encode(s.encode('utf-8')).decode('utf-8')

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        video_url = request.form.get("video_url")
        scroll_count = int(request.form.get("scroll_count"))

        # Scrape comments and get the CSV content
        csv_content = scrape_youtube_comments_to_csv(video_url, scroll_count)

        return render_template("download.html", csv_content=csv_content)

    return render_template("index.html")

@app.route("/download_csv/<filename>")
def download_csv(filename):
    return send_file(filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)

