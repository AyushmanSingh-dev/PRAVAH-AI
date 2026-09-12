"""
PRAVAH AI - Production Web Application Server
Serves the interactive disaster prediction dashboard and provides physical simulation REST APIs.
"""

from flask import Flask, render_template, request, jsonify
from engine.physics import PravahPhysicsEngine
from engine.catchment_data import SCENARIOS, SETTLEMENTS
import datetime
import xml.etree.ElementTree as ET

app = Flask(__name__)
engine = PravahPhysicsEngine()

from engine.catchment_data import SCENARIOS, SETTLEMENTS, HIMALAYAN_REGIONS
from engine.historical_validation import run_historical_hindcast_suite, HISTORICAL_DISASTERS
from engine.iot_manager import get_iot_manager
from engine.ml_model import predict_hybrid_risk

iot_mgr = get_iot_manager()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/region/<region_id>")
def region_redirect(region_id):
    return render_template("index.html")

@app.route("/api/regions", methods=["GET"])
def get_regions():
    return jsonify(HIMALAYAN_REGIONS)

@app.route("/api/region/<region_id>", methods=["GET"])
def get_region_detail(region_id):
    region = HIMALAYAN_REGIONS.get(region_id)
    if not region:
        return jsonify({"error": "Region not found"}), 404
    return jsonify(region)

@app.route("/api/regions-overview", methods=["GET"])
def get_regions_overview():
    """Returns real-time risk overview across all Himalayan basins for multi-regional monitoring."""
    overview = []
    for reg_id, reg in HIMALAYAN_REGIONS.items():
        base_scen = reg["scenarios"].get("normal_baseline", {})
        res = engine.run_full_pipeline(
            rainfall_rate_mm_hr=base_scen.get("rainfall_rate_mm_hr", 4.0),
            duration_hr=base_scen.get("duration_hr", 1.0),
            initial_soil_moisture=base_scen.get("initial_soil_moisture", 0.20),
            custom_params=reg["geotechnical"],
            settlements=reg["settlements"]
        )
        overview.append({
            "id": reg["id"],
            "name": reg["name"],
            "short_name": reg["short_name"],
            "district": reg["district"],
            "state": reg["state"],
            "elevation_range": reg["elevation_range"],
            "dominant_geology": reg["dominant_geology"],
            "catchment_area_km2": reg["catchment_area_km2"],
            "critical_settlement": reg["settlements"][0]["name"] if reg["settlements"] else "N/A",
            "hazard_level": res.get("overall_hazard_level", "SAFE"),
            "compound_risk_pct": res.get("compound_risk_pct", 5.0),
            "primary_driver": res.get("explainable_attribution", {}).get("primary_driver", "Normal baseflow"),
            "center": [reg["center_lat"], reg["center_lon"]],
            "authority": reg.get("authority", {})
        })
    return jsonify(overview)

@app.route("/api/status", methods=["GET"])
def get_status():
    region_id = request.args.get("region", "alaknanda")
    region_cfg = HIMALAYAN_REGIONS.get(region_id, HIMALAYAN_REGIONS["alaknanda"])
    default_scenario = region_cfg["scenarios"].get("normal_baseline", list(region_cfg["scenarios"].values())[0])

    result = engine.run_full_pipeline(
        rainfall_rate_mm_hr=default_scenario["rainfall_rate_mm_hr"],
        duration_hr=default_scenario["duration_hr"],
        initial_soil_moisture=default_scenario["initial_soil_moisture"],
        custom_params=region_cfg["geotechnical"],
        settlements=region_cfg["settlements"]
    )
    result["active_scenario"] = "normal_baseline"
    result["active_region"] = region_id
    
    # Attach Physics-Guided ML Guidance & Live IoT Telemetry
    result["ml_guidance"] = predict_hybrid_risk(
        result["inputs"],
        result["compound_probability"]["compound_flash_flood_probability_pct"]
    )
    result["iot_telemetry"] = iot_mgr.get_latest_basin_telemetry(region_id)
    return jsonify(result)

@app.route("/api/simulate", methods=["POST"])
def simulate():
    data = request.get_json() or {}
    region_id = data.get("region_id", "alaknanda")
    region_cfg = HIMALAYAN_REGIONS.get(region_id, HIMALAYAN_REGIONS["alaknanda"])

    rainfall = float(data.get("rainfall_rate_mm_hr", 45.0))
    duration = float(data.get("duration_hr", 2.0))
    moisture = float(data.get("initial_soil_moisture", 0.25))

    # Clamp basic bounds
    rainfall = max(0.0, min(300.0, rainfall))
    duration = max(0.2, min(72.0, duration))
    moisture = max(0.05, min(0.44, moisture))

    result = engine.run_full_pipeline(
        rainfall_rate_mm_hr=rainfall,
        duration_hr=duration,
        initial_soil_moisture=moisture,
        custom_params=data,
        settlements=region_cfg["settlements"]
    )
    result["active_region"] = region_id

    # Attach Physics-Guided ML Guidance & Live IoT Telemetry
    result["ml_guidance"] = predict_hybrid_risk(
        result["inputs"],
        result["compound_probability"]["compound_flash_flood_probability_pct"]
    )
    result["iot_telemetry"] = iot_mgr.get_latest_basin_telemetry(region_id)
    return jsonify(result)

@app.route("/api/iot/status", methods=["GET"])
def get_iot_status():
    region_id = request.args.get("region", "alaknanda")
    return jsonify(iot_mgr.get_latest_basin_telemetry(region_id))

@app.route("/api/iot/telemetry", methods=["POST"])
def post_iot_telemetry():
    packet = request.get_json() or {}
    verified = iot_mgr.ingest_packet(packet)
    return jsonify({"status": "SUCCESS", "packet": verified})

@app.route("/api/iot/stream/step", methods=["POST", "GET"])
def step_iot_stream():
    region_id = request.args.get("region") or (request.get_json() or {}).get("region_id", "alaknanda")
    telemetry = iot_mgr.step_stream(region_id)

    # Drive full physics and ML simulation directly from the live IoT stream
    region_cfg = HIMALAYAN_REGIONS.get(region_id, HIMALAYAN_REGIONS["alaknanda"])
    agg = telemetry["aggregated_telemetry"]

    rainfall_rate = max(2.0, agg.get("peak_station_rainfall_mm_hr", 4.0))
    moisture_pct = agg.get("mean_soil_moisture_pct", 25.0)
    moisture_ratio = min(0.44, max(0.08, moisture_pct / 100.0))

    sim_res = engine.run_full_pipeline(
        rainfall_rate_mm_hr=rainfall_rate,
        duration_hr=1.5,
        initial_soil_moisture=moisture_ratio,
        custom_params=region_cfg["geotechnical"],
        settlements=region_cfg["settlements"]
    )
    sim_res["active_region"] = region_id
    sim_res["active_scenario"] = "live_iot_stream"
    sim_res["ml_guidance"] = predict_hybrid_risk(
        sim_res["inputs"],
        sim_res["compound_probability"]["compound_flash_flood_probability_pct"]
    )
    sim_res["iot_telemetry"] = telemetry

    return jsonify(sim_res)

@app.route("/api/historical-validation", methods=["GET"])
def get_historical_validation():
    suite_results = run_historical_hindcast_suite()
    return jsonify(suite_results)

@app.route("/api/presets", methods=["GET"])
def get_presets():
    # Combine standard scenarios with historical disaster benchmark cases
    presets = dict(SCENARIOS)
    for h in HISTORICAL_DISASTERS:
        presets[h["id"]] = {
            "name": h["name"],
            "location": h["location"],
            "date": h["date"],
            "rainfall_rate_mm_hr": h["inputs"]["rainfall_rate_mm_hr"],
            "duration_hr": h["inputs"]["duration_hr"],
            "initial_soil_moisture": h["inputs"]["initial_soil_moisture"],
            "description": f"{h['terrain_type']} - Observed Q: {h['observed_ground_truth']['peak_discharge_m3s']} m³/s, Stage: {h['observed_ground_truth']['stage_depth_m']}m.",
            "is_historical": True,
            "full_inputs": h["inputs"],
            "observed": h["observed_ground_truth"]
        }
    return jsonify(presets)

@app.route("/api/settlements", methods=["GET"])
def get_settlements():
    return jsonify(SETTLEMENTS)

@app.route("/api/export-cap", methods=["POST"])
def export_cap_alert():
    """
    Generates an official Common Alerting Protocol (CAP v1.2) XML payload
    for NDRF / State Disaster Management Authority (USDMA) dissemination.
    """
    data = request.get_json() or {}
    settlement_id = data.get("settlement_id", "raini")
    
    # Find settlement across all Himalayan regions
    settlement = None
    target_region = HIMALAYAN_REGIONS["alaknanda"]
    for reg in HIMALAYAN_REGIONS.values():
        for s in reg["settlements"]:
            if s["id"] == settlement_id:
                settlement = s
                target_region = reg
                break
        if settlement:
            break

    if not settlement:
        settlement = target_region["settlements"][0]

    lead_time = data.get("lead_time_min", 45)
    depth = data.get("stage_depth_m", 5.2)
    urgency = "Immediate" if data.get("hazard_level") == "RED" else "Expected"
    authority = target_region.get("authority", {})
    ddma_name = authority.get("ddma_name", f"{target_region['district']} Emergency Authority")
    siren_freq = authority.get("siren_freq", "144.50 MHz VHF")

    now_iso = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+00:00")
    expires_iso = (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=4)).strftime("%Y-%m-%dT%H:%M:%S+00:00")

    # Construct CAP XML
    root = ET.Element("alert", xmlns="urn:oasis:names:tc:emergency:cap:1.2")
    ET.SubElement(root, "identifier").text = f"IN-NDRF-PRAVAH-{int(datetime.datetime.now().timestamp())}"
    ET.SubElement(root, "sender").text = "pravah-ai@ndrf.gov.in"
    ET.SubElement(root, "sent").text = now_iso
    ET.SubElement(root, "status").text = "Actual"
    ET.SubElement(root, "msgType").text = "Alert"
    ET.SubElement(root, "scope").text = "Public"

    info = ET.SubElement(root, "info")
    ET.SubElement(info, "category").text = "Met"
    ET.SubElement(info, "event").text = f"Himalayan Flash Flood & Debris Surge ({target_region['short_name']})"
    ET.SubElement(info, "urgency").text = urgency
    ET.SubElement(info, "severity").text = "Extreme" if urgency == "Immediate" else "Severe"
    ET.SubElement(info, "certainty").text = "Observed"
    ET.SubElement(info, "eventCode").text = "FLW"
    ET.SubElement(info, "expires").text = expires_iso
    ET.SubElement(info, "headline").text = f"FLASH FLOOD WARNING: {settlement['name']} ({target_region['district']}) - Evacuation Lead Time: {lead_time} Minutes"
    ET.SubElement(info, "description").text = (
        f"PRAVAH AI multi-stage physical modeling has detected catastrophic discharge at upstream {target_region['name']} reaches. "
        f"Predicted river stage is {depth}m (exceeding {settlement['danger_depth_m']}m danger mark). "
        f"Expected inundation crest in {lead_time} minutes. Immediate evacuation of low-lying floodplains is ordered by {ddma_name}."
    )
    ET.SubElement(info, "instruction").text = (
        f"1. Move to designated high ground above {round(depth * 1.5, 1)}m contour immediately.\n"
        f"2. Keep emergency sirens and VHF radio frequency {siren_freq} active.\n"
        f"3. Do not attempt bridge or culvert crossings until clearance is broadcasted by {ddma_name}."
    )
    area = ET.SubElement(info, "area")
    ET.SubElement(area, "areaDesc").text = f"{settlement['name']}, {target_region['district']}"
    ET.SubElement(area, "circle").text = f"{settlement['lat']},{settlement['lon']},5.0"

    xml_str = ET.tostring(root, encoding="utf-8").decode("utf-8")
    return jsonify({
        "cap_xml": xml_str,
        "headline": f"FLASH FLOOD WARNING: {settlement['name']} ({target_region['district']})",
        "lead_time_min": lead_time,
        "authority_name": ddma_name,
        "siren_freq": siren_freq,
        "audio_script_hindi": f"सावधान! प्रवाह एआई एवं {ddma_name} आपातकालीन चेतावनी: {settlement['name']} में {target_region['short_name']} का जलस्तर खतरे के निशान को पार कर गया है। आपके पास {lead_time} मिनट का समय है। वीएचएफ आवृत्ति {siren_freq} पर बने रहें और तुरंत ऊंचे स्थानों पर जाएं।",
        "audio_script_english": f"Attention! Pravah AI and {ddma_name} Alert: River stage at {settlement['name']} ({target_region['short_name']}) has crossed danger mark. Estimated evacuation lead time is {lead_time} minutes. Monitor {siren_freq} and move to high ground immediately."
    })

if __name__ == "__main__":
    print("Starting PRAVAH AI Web Application on http://127.0.0.1:5000")
    app.run(host="127.0.0.1", port=5000, debug=False)
