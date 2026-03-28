import mysql.connector
from tabulate import tabulate
from database import get_connection

def print_table(cursor, results):
    if not results:
        print("\nNo records found.")
        return
    columns = [desc[0] for desc in cursor.description]
    print("\n" + tabulate(results, headers=columns, tablefmt="grid"))

def execute_commit(query, params=None):
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            print("\n[+] Operation successful.")
            return True
        except mysql.connector.Error as err:
            print(f"\n[-] Error: {err}")
            return False
        finally:
            cursor.close()
            conn.close()

def execute_fetch(query, params=None):
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            results = cursor.fetchall()
            print_table(cursor, results)
        except mysql.connector.Error as err:
            print(f"\n[-] Error: {err}")
        finally:
            cursor.close()
            conn.close()

# --- DataCenter CRUD ---
def add_datacenter(name, location):
    query = "INSERT INTO DataCenter (name, location) VALUES (%s, %s)"
    execute_commit(query, (name, location))

def view_datacenters():
    query = "SELECT * FROM DataCenter"
    execute_fetch(query)

def update_datacenter(dc_id, name, location):
    query = "UPDATE DataCenter SET name=%s, location=%s WHERE data_center_id=%s"
    execute_commit(query, (name, location, dc_id))

def delete_datacenter(dc_id):
    query = "DELETE FROM DataCenter WHERE data_center_id=%s"
    execute_commit(query, (dc_id,))

# --- AI Workload CRUD ---
def add_workload(name, wl_type, dc_id):
    query = "INSERT INTO AI_Workload (name, type, data_center_id) VALUES (%s, %s, %s)"
    execute_commit(query, (name, wl_type, dc_id))

def view_workloads():
    query = """
    SELECT w.workload_id, w.name, w.type, d.name AS datacenter
    FROM AI_Workload w
    LEFT JOIN DataCenter d ON w.data_center_id = d.data_center_id
    """
    execute_fetch(query)

def update_workload(wl_id, name, wl_type, dc_id):
    query = "UPDATE AI_Workload SET name=%s, type=%s, data_center_id=%s WHERE workload_id=%s"
    execute_commit(query, (name, wl_type, dc_id, wl_id))

def delete_workload(wl_id):
    query = "DELETE FROM AI_Workload WHERE workload_id=%s"
    execute_commit(query, (wl_id,))

# --- Water Consumption CRUD ---
def add_water_consumption(liters, date, dc_id, wl_id):
    query = "INSERT INTO Water_Consumption (water_used_liters, date, data_center_id, workload_id) VALUES (%s, %s, %s, %s)"
    execute_commit(query, (liters, date, dc_id, wl_id))

def view_water_consumptions():
    query = """
    SELECT wc.water_id, wc.water_used_liters, wc.date, d.name AS datacenter, w.name AS workload
    FROM Water_Consumption wc
    LEFT JOIN DataCenter d ON wc.data_center_id = d.data_center_id
    LEFT JOIN AI_Workload w ON wc.workload_id = w.workload_id
    """
    execute_fetch(query)

def update_water_consumption(wc_id, liters, date, dc_id, wl_id):
    query = "UPDATE Water_Consumption SET water_used_liters=%s, date=%s, data_center_id=%s, workload_id=%s WHERE water_id=%s"
    execute_commit(query, (liters, date, dc_id, wl_id, wc_id))

def delete_water_consumption(wc_id):
    query = "DELETE FROM Water_Consumption WHERE water_id=%s"
    execute_commit(query, (wc_id,))

# --- Cooling System CRUD ---
def add_cooling_system(c_type, efficiency, dc_id):
    query = "INSERT INTO Cooling_System (type, efficiency, data_center_id) VALUES (%s, %s, %s)"
    execute_commit(query, (c_type, efficiency, dc_id))

def view_cooling_systems():
    query = """
    SELECT cs.cooling_id, cs.type, cs.efficiency, d.name AS datacenter
    FROM Cooling_System cs
    LEFT JOIN DataCenter d ON cs.data_center_id = d.data_center_id
    """
    execute_fetch(query)

def delete_cooling_system(cs_id):
    query = "DELETE FROM Cooling_System WHERE cooling_id=%s"
    execute_commit(query, (cs_id,))

# --- Optimization Log CRUD ---
def add_log(description, date, dc_id):
    query = "INSERT INTO Optimization_Log (description, date, data_center_id) VALUES (%s, %s, %s)"
    execute_commit(query, (description, date, dc_id))

def view_logs():
    query = """
    SELECT ol.log_id, ol.description, ol.date, d.name AS datacenter
    FROM Optimization_Log ol
    LEFT JOIN DataCenter d ON ol.data_center_id = d.data_center_id
    """
    execute_fetch(query)

def delete_log(log_id):
    query = "DELETE FROM Optimization_Log WHERE log_id=%s"
    execute_commit(query, (log_id,))

# --- Roles CRUD ---
def add_role(role_name):
    query = "INSERT INTO Role (role_name) VALUES (%s)"
    execute_commit(query, (role_name,))

def view_roles():
    query = "SELECT * FROM Role"
    execute_fetch(query)

def delete_role(role_id):
    query = "DELETE FROM Role WHERE role_id=%s"
    execute_commit(query, (role_id,))

# --- Users CRUD ---
def add_user(name, email, role_id):
    query = "INSERT INTO User (name, email, role_id) VALUES (%s, %s, %s)"
    execute_commit(query, (name, email, role_id))

def view_users():
    query = """
    SELECT u.user_id, u.name, u.email, r.role_name
    FROM User u
    LEFT JOIN Role r ON u.role_id = r.role_id
    """
    execute_fetch(query)

def delete_user(user_id):
    query = "DELETE FROM User WHERE user_id=%s"
    execute_commit(query, (user_id,))

# --- Monitoring CRUD ---
def add_monitoring(user_id, dc_id):
    query = "INSERT INTO Monitoring (user_id, data_center_id) VALUES (%s, %s)"
    execute_commit(query, (user_id, dc_id))

def view_monitoring():
    query = """
    SELECT m.user_id, u.name AS user_name, m.data_center_id, d.name AS datacenter_name
    FROM Monitoring m
    JOIN User u ON m.user_id = u.user_id
    JOIN DataCenter d ON m.data_center_id = d.data_center_id
    """
    execute_fetch(query)

def delete_monitoring(user_id, dc_id):
    query = "DELETE FROM Monitoring WHERE user_id=%s AND data_center_id=%s"
    execute_commit(query, (user_id, dc_id))


# --- Special Analytical Queries ---
def total_water_per_datacenter():
    query = """
    SELECT d.name AS 'Data Center', SUM(wc.water_used_liters) AS 'Total Water (Liters)'
    FROM DataCenter d
    LEFT JOIN Water_Consumption wc ON d.data_center_id = wc.data_center_id
    GROUP BY d.data_center_id, d.name
    ORDER BY SUM(wc.water_used_liters) DESC
    """
    execute_fetch(query)

def water_usage_per_workload():
    query = """
    SELECT w.name AS 'AI Workload', SUM(wc.water_used_liters) AS 'Total Water (Liters)'
    FROM AI_Workload w
    LEFT JOIN Water_Consumption wc ON w.workload_id = wc.workload_id
    GROUP BY w.workload_id, w.name
    ORDER BY SUM(wc.water_used_liters) DESC
    """
    execute_fetch(query)

def most_efficient_cooling():
    query = """
    SELECT c.type AS 'Cooling System', c.efficiency, d.name AS 'Data Center'
    FROM Cooling_System c
    JOIN DataCenter d ON c.data_center_id = d.data_center_id
    ORDER BY c.efficiency DESC LIMIT 3
    """
    execute_fetch(query)

def logs_for_datacenter(dc_id):
    query = """
    SELECT ol.date, ol.description, d.name AS 'Data Center'
    FROM Optimization_Log ol
    JOIN DataCenter d ON ol.data_center_id = d.data_center_id
    WHERE d.data_center_id = %s
    ORDER BY ol.date DESC
    """
    execute_fetch(query, (dc_id,))

def users_monitoring_datacenter(dc_id):
    query = """
    SELECT u.name AS 'User', u.email, r.role_name
    FROM User u
    JOIN Monitoring m ON u.user_id = m.user_id
    JOIN Role r ON u.role_id = r.role_id
    WHERE m.data_center_id = %s
    """
    execute_fetch(query, (dc_id,))
