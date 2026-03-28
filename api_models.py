import mysql.connector
from database import get_connection

def execute_commit(query, params=None):
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return {"success": True, "message": "Operation successful."}
        except mysql.connector.Error as err:
            return {"success": False, "error": str(err)}
        finally:
            cursor.close()
            conn.close()
    return {"success": False, "error": "Database connection failed."}

def execute_fetch(query, params=None):
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, params)
            results = cursor.fetchall()
            return {"success": True, "data": results}
        except mysql.connector.Error as err:
            return {"success": False, "error": str(err)}
        finally:
            cursor.close()
            conn.close()
    return {"success": False, "error": "Database connection failed."}

# DataCenters
def get_datacenters(): return execute_fetch("SELECT * FROM DataCenter")
def add_datacenter(name, loc): return execute_commit("INSERT INTO DataCenter (name, location) VALUES (%s, %s)", (name, loc))
def update_datacenter(dc_id, name, loc): return execute_commit("UPDATE DataCenter SET name=%s, location=%s WHERE data_center_id=%s", (name, loc, dc_id))
def delete_datacenter(dc_id): return execute_commit("DELETE FROM DataCenter WHERE data_center_id=%s", (dc_id,))

# Workloads
def get_workloads(): return execute_fetch("SELECT w.workload_id, w.name, w.type, w.data_center_id, d.name AS datacenter FROM AI_Workload w LEFT JOIN DataCenter d ON w.data_center_id = d.data_center_id")
def add_workload(name, t, dc_id): return execute_commit("INSERT INTO AI_Workload (name, type, data_center_id) VALUES (%s, %s, %s)", (name, t, dc_id))
def delete_workload(wl_id): return execute_commit("DELETE FROM AI_Workload WHERE workload_id=%s", (wl_id,))

# Water
def get_water(): return execute_fetch("SELECT wc.water_id, CAST(wc.water_used_liters AS CHAR) AS water_used_liters, DATE_FORMAT(wc.date, '%Y-%m-%d') AS date, d.name AS datacenter, w.name AS workload FROM Water_Consumption wc LEFT JOIN DataCenter d ON wc.data_center_id = d.data_center_id LEFT JOIN AI_Workload w ON wc.workload_id = w.workload_id")
def add_water(liters, date, dc_id, wl_id): return execute_commit("INSERT INTO Water_Consumption (water_used_liters, date, data_center_id, workload_id) VALUES (%s, %s, %s, %s)", (liters, date, dc_id, wl_id))
def delete_water(wc_id): return execute_commit("DELETE FROM Water_Consumption WHERE water_id=%s", (wc_id,))

# Cooling 
def get_cooling(): return execute_fetch("SELECT cs.cooling_id, cs.type, CAST(cs.efficiency AS CHAR) AS efficiency, d.name AS datacenter FROM Cooling_System cs LEFT JOIN DataCenter d ON cs.data_center_id = d.data_center_id")
def add_cooling(t, eff, dc_id): return execute_commit("INSERT INTO Cooling_System (type, efficiency, data_center_id) VALUES (%s, %s, %s)", (t, eff, dc_id))
def delete_cooling(c_id): return execute_commit("DELETE FROM Cooling_System WHERE cooling_id=%s", (c_id,))

# Analytics
def rep_water_per_dc(): return execute_fetch("SELECT d.name AS datacenter, CAST(SUM(wc.water_used_liters) AS CHAR) AS total_water FROM DataCenter d LEFT JOIN Water_Consumption wc ON d.data_center_id = wc.data_center_id GROUP BY d.data_center_id, d.name ORDER BY SUM(wc.water_used_liters) DESC")
def rep_water_per_wl(): return execute_fetch("SELECT w.name AS workload, CAST(SUM(wc.water_used_liters) AS CHAR) AS total_water FROM AI_Workload w LEFT JOIN Water_Consumption wc ON w.workload_id = wc.workload_id GROUP BY w.workload_id, w.name ORDER BY SUM(wc.water_used_liters) DESC")
def rep_cooling(): return execute_fetch("SELECT c.type AS cooling_system, CAST(c.efficiency AS CHAR) AS efficiency, d.name AS datacenter FROM Cooling_System c JOIN DataCenter d ON c.data_center_id = d.data_center_id ORDER BY c.efficiency DESC LIMIT 3")
