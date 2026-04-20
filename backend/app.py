from flask import Flask, request, jsonify, render_template
import os
import datetime
from hash_utils import compute_model_hash
from blockchain_utils import register_model, verify_model, get_model_info, is_connected, is_model_registered

app = Flask(__name__, template_folder="../templates")

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "../model")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def index():
    connected = is_connected()
    return render_template("index.html", connected=connected)

@app.route("/register", methods=["POST"])
def register():
    try:
        model_name = request.form.get("model_name")
        model_file = request.files.get("model_file")

        if not model_name or not model_file:
            return render_template("result.html", status="error", message="Model name and file are required.")

        if is_model_registered(model_name):
            return render_template("result.html", status="error", message=f"Model '{model_name}' is already registered on the blockchain.")

        save_path = os.path.join(UPLOAD_FOLDER, model_file.filename)
        model_file.save(save_path)

        model_hash = compute_model_hash(save_path)
        tx_hash = register_model(model_name, model_hash)

        return render_template("result.html",
            status="registered",
            model_name=model_name,
            model_hash=model_hash,
            tx_hash=tx_hash,
            message="Model successfully registered on blockchain!"
        )
    except Exception as e:
        return render_template("result.html", status="error", message=str(e))

@app.route("/verify", methods=["POST"])
def verify():
    try:
        model_name = request.form.get("model_name")
        model_file = request.files.get("model_file")

        if not model_name or not model_file:
            return render_template("result.html", status="error", message="Model name and file are required.")

        if not is_model_registered(model_name):
            return render_template("result.html", status="error", message=f"Model '{model_name}' is not registered on the blockchain.")

        save_path = os.path.join(UPLOAD_FOLDER, "verify_" + model_file.filename)
        model_file.save(save_path)

        current_hash = compute_model_hash(save_path)
        is_valid = verify_model(model_name, current_hash)

        info = get_model_info(model_name)
        registered_time = datetime.datetime.fromtimestamp(info["timestamp"]).strftime("%Y-%m-%d %H:%M:%S")

        return render_template("result.html",
            status="verified" if is_valid else "tampered",
            model_name=model_name,
            current_hash=current_hash,
            stored_hash=info["hash"],
            registered_by=info["registered_by"],
            registered_time=registered_time,
            message="Model is VERIFIED - Authentic and Unmodified!" if is_valid else "Model is TAMPERED - Hash mismatch detected!"
        )
    except Exception as e:
        return render_template("result.html", status="error", message=str(e))

@app.route("/info/<model_name>")
def model_info(model_name):
    try:
        info = get_model_info(model_name)
        info["timestamp"] = datetime.datetime.fromtimestamp(info["timestamp"]).strftime("%Y-%m-%d %H:%M:%S")
        return jsonify(info)
    except Exception as e:
        return jsonify({"error": str(e)}), 404

@app.route("/history/<model_name>")
def model_history(model_name):
    try:
        from blockchain_utils import get_all_versions
        import datetime
        versions = get_all_versions(model_name)
        for v in versions:
            v["timestamp"] = datetime.datetime.fromtimestamp(v["timestamp"]).strftime("%Y-%m-%d %H:%M:%S")
        return render_template("history.html", model_name=model_name, versions=versions)
    except Exception as e:
        return render_template("result.html", status="error", message=str(e))

@app.route("/verify-hash", methods=["GET", "POST"])
def verify_hash():
    if request.method == "GET":
        return render_template("verify_hash.html")
    try:
        model_name = request.form.get("model_name")
        model_hash = request.form.get("model_hash")

        if not model_name or not model_hash:
            return render_template("verify_hash.html", error="Both model name and hash are required.")

        if len(model_hash) != 64:
            return render_template("verify_hash.html", error="Invalid hash format. SHA-256 hash must be exactly 64 characters.")

        if not all(c in "0123456789abcdefABCDEF" for c in model_hash):
            return render_template("verify_hash.html", error="Invalid hash format. Hash must contain only hexadecimal characters.")

        if not is_model_registered(model_name):
            return render_template("verify_hash.html", error=f"Model '{model_name}' is not registered on the blockchain.")

        import datetime
        is_valid = verify_model(model_name, model_hash)
        info = get_model_info(model_name)
        registered_time = datetime.datetime.fromtimestamp(info["timestamp"]).strftime("%Y-%m-%d %H:%M:%S")

        return render_template("result.html",
            status="verified" if is_valid else "tampered",
            model_name=model_name,
            current_hash=model_hash,
            stored_hash=info["hash"],
            registered_by=info["registered_by"],
            registered_time=registered_time,
            message="Model is VERIFIED - Hash matches blockchain record!" if is_valid else "Model is TAMPERED - Hash does not match blockchain record!"
        )
    except Exception as e:
        return render_template("verify_hash.html", error=str(e))

if __name__ == "__main__":
    print("Blockchain connected:", is_connected())
    app.run(debug=True, port=5000)