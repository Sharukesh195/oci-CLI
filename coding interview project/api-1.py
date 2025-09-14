from flask import Flask, jsonify, request, render_template
import oci

app = Flask(__name__)

# Load OCI config
config = oci.config.from_file(r"C:\Users\Sharukesh\.oci\config")
mysql_client = oci.mysql.DbSystemClient(config)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/db-systems')
def get_db_systems():
    compartment_id = "ocid1.compartment.oc1..aaaaaaaaryaa7o57ojwvca5msfujolafp5vnhdkp62lj4ti46qb7m5bi5xda"
    try:
        response = mysql_client.list_db_systems(compartment_id=compartment_id)
        dbs = []
        if response and hasattr(response, "data"):
            for db in response.data:
                dbs.append({
                    "id": db.id,
                    "db_name": db.display_name,
                    "status": db.lifecycle_state,
                    "crash_recovery": getattr(db, 'crash_recovery', 'N/A'),
                    "delete_protected": getattr(db, 'is_delete_protected', 'N/A'),
                    "heatwave_cluster": getattr(db, 'is_heat_wave_cluster_enabled', 'N/A'), 
                    "created": str(getattr(db, 'time_created', 'N/A')),
                    "compartment_id": db.compartment_id
                })
            print("Fetched MySQL DB Systems:")
            for db in dbs:
                print(f"db_name: {db['db_name']}, Status: {db['status']}, Crash Recovery: {db['crash_recovery']}, Delete Protected: {db['delete_protected']}, HeatWave Cluster: {db['heatwave_cluster']}, Created: {db['created']}")
            return jsonify(dbs)
        else:
            print("No data returned from list_db_systems")
            return jsonify({"error": "No data returned from list_db_systems"}), 500
    except Exception as e:
        print("Error fetching MySQL DB systems:", str(e))
        return jsonify({"error": "Failed to fetch MySQL DB systems", "details": str(e)}), 500

@app.route('/api/db-systems/encryption-status')
def get_encryption_status():
    compartment_id = "ocid1.compartment.oc1..aaaaaaaaryaa7o57ojwvca5msfujolafp5vnhdkp62lj4ti46qb7m5bi5xda"
    response = mysql_client.list_db_systems(compartment_id=compartment_id)
    dbs = []
    if response and hasattr(response, "data"):
        for db in response.data:
            encryption_status = "Oracle-managed key"
            dbs.append({
                "id": db.id,
                "display_name": db.display_name,
                "lifecycle_state": db.lifecycle_state,
                "hostname": getattr(db, 'hostname', ''),
                "compartment_id": db.compartment_id,
                "connection_encryption_status": encryption_status
            })
        return jsonify(dbs)
    else:
        print("No data returned from list_db_systems")
        return jsonify({"error": "No data returned from list_db_systems"}), 500

@app.route('/db-systems')
def db_systems_page():
    return render_template('db_systems.html')

@app.route('/encryption-status')
def encryption_status_page():
    return render_template('encryption_status.html')

if __name__ == '__main__':
    app.run(port=5000, debug=True)