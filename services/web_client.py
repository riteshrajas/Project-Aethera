from flask import Flask, render_template_string, request

from core.information_management.data_analysis import analyze_text_frequency

TEMPLATE = """
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Project Aethera Web Client</title>
    <style>
      body {
        font-family: Arial, sans-serif;
        margin: 2rem auto;
        max-width: 800px;
        padding: 0 1rem;
      }
      textarea {
        width: 100%;
        min-height: 180px;
        margin-top: 0.5rem;
      }
      .actions {
        margin-top: 1rem;
      }
      .error {
        color: #b00020;
      }
      ul {
        padding-left: 1.2rem;
      }
    </style>
  </head>
  <body>
    <h1>Project Aethera Web Client</h1>
    <p>Paste text below to analyze word frequency.</p>
    {% if error %}
      <p class="error">{{ error }}</p>
    {% endif %}
    <form method="post">
      <label for="text">Text input</label>
      <textarea id="text" name="text">{{ text }}</textarea>
      <div class="actions">
        <button type="submit">Analyze</button>
      </div>
    </form>

    {% if results %}
      <h2>Top Words</h2>
      <ul>
        {% for word, count in results %}
          <li>{{ word }}: {{ count }}</li>
        {% endfor %}
      </ul>
    {% endif %}
  </body>
</html>
"""


def create_app():
    app = Flask(__name__)

    @app.route("/", methods=["GET", "POST"])
    def index():
        text = ""
        results = None
        error = None

        if request.method == "POST":
            text = request.form.get("text", "")
            if text.strip():
                stats = analyze_text_frequency(text)
                results = sorted(stats.items(), key=lambda item: item[1], reverse=True)[:10]
            else:
                error = "Please enter text to analyze."

        return render_template_string(TEMPLATE, text=text, results=results, error=error)

    return app


if __name__ == "__main__":
    create_app().run(host="127.0.0.1", port=5000, debug=False)
