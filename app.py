from pathlib import Path

from flask import Flask, jsonify, render_template, request
from werkzeug.utils import secure_filename

from services.analyzer import analyze_file
from utils.database import get_history, init_db, save_result

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "pdf"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = MAX_FILE_SIZE


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    if "file" not in request.files:
        return jsonify({"success": False, "error": "No file was selected."}), 400

    uploaded_file = request.files["file"]

    if not uploaded_file.filename:
        return jsonify({"success": False, "error": "No file was selected."}), 400

    if not allowed_file(uploaded_file.filename):
        return jsonify({
            "success": False,
            "error": "Unsupported file type. Use PNG, JPG, JPEG or PDF."
        }), 400

    safe_name = secure_filename(uploaded_file.filename)
    if not safe_name:
        return jsonify({"success": False, "error": "Invalid file name."}), 400

    file_path = UPLOAD_DIR / safe_name
    uploaded_file.save(file_path)

    try:
        result = analyze_file(file_path)
        save_result(result)
        return jsonify({"success": True, **result})
    except Exception as exc:
        return jsonify({
            "success": False,
            "error": f"Analysis failed: {exc}"
        }), 500
    finally:
        if file_path.exists():
            file_path.unlink()


@app.route("/history", methods=["GET"])
def history():
    return jsonify({"items": get_history()})


@app.errorhandler(413)
def too_large(_error):
    return jsonify({
        "success": False,
        "error": "File is larger than the 10 MB limit."
    }), 413


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
