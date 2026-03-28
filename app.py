from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import api_models

app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)

@app.route("/")
def index():
    return render_template("index.html")

# --- Datacenters API ---
@app.route("/api/datacenters", methods=["GET"])
def get_datacenters():
    return jsonify(api_models.get_datacenters())

@app.route("/api/datacenters", methods=["POST"])
def add_datacenter():
    data = request.json
    return jsonify(api_models.add_datacenter(data.get("name"), data.get("location")))

@app.route("/api/datacenters/<dc_id>", methods=["DELETE"])
def delete_datacenter(dc_id):
    return jsonify(api_models.delete_datacenter(dc_id))

# --- Workloads API ---
@app.route("/api/workloads", methods=["GET"])
def get_workloads():
    return jsonify(api_models.get_workloads())

@app.route("/api/workloads", methods=["POST"])
def add_workload():
    data = request.json
    return jsonify(api_models.add_workload(data.get("name"), data.get("type"), data.get("data_center_id")))

@app.route("/api/workloads/<wl_id>", methods=["DELETE"])
def delete_workload(wl_id):
    return jsonify(api_models.delete_workload(wl_id))

# --- Water Consumption API ---
@app.route("/api/water", methods=["GET"])
def get_water():
    return jsonify(api_models.get_water())

@app.route("/api/water", methods=["POST"])
def add_water():
    data = request.json
    return jsonify(api_models.add_water(data.get("water_used_liters"), data.get("date"), data.get("data_center_id"), data.get("workload_id")))

@app.route("/api/water/<wc_id>", methods=["DELETE"])
def delete_water(wc_id):
    return jsonify(api_models.delete_water(wc_id))

# --- Analytics API ---
@app.route("/api/reports/water_per_dc", methods=["GET"])
def rep_water_per_dc():
    return jsonify(api_models.rep_water_per_dc())

@app.route("/api/reports/water_per_wl", methods=["GET"])
def rep_water_per_wl():
    return jsonify(api_models.rep_water_per_wl())

@app.route("/api/reports/top_cooling", methods=["GET"])
def rep_top_cooling():
    return jsonify(api_models.rep_cooling())

if __name__ == "__main__":
    app.run(debug=True, port=5000)
