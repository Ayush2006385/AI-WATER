import sys
import database
import models

def print_menu():
    print("\n" + "="*55)
    print(" DATA CENTER WATER & AI WORKLOAD MANAGER ")
    print("="*55)
    print(" 1. Manage Data Centers")
    print(" 2. Manage AI Workloads")
    print(" 3. Manage Water Consumption")
    print(" 4. Manage Cooling Systems")
    print(" 5. Manage Optimization Logs")
    print(" 6. Manage Roles & Users")
    print(" 7. Manage Monitoring Assignments")
    print(" 8. View Reports & Analytics")
    print(" 9. Initialize/Reset Database (Run schema)")
    print(" 0. Exit")
    print("="*55)

def manage_datacenters():
    while True:
        print("\n--- Manage Data Centers ---")
        print("1. View Data Centers")
        print("2. Add Data Center")
        print("3. Update Data Center")
        print("4. Delete Data Center")
        print("0. Back")
        
        choice = input("Enter choice: ")
        if choice == '1':
            models.view_datacenters()
        elif choice == '2':
            name = input("Enter name: ")
            loc = input("Enter location: ")
            models.add_datacenter(name, loc)
        elif choice == '3':
            models.view_datacenters()
            dc_id = input("Enter Data Center ID to update: ")
            name = input("Enter new name: ")
            loc = input("Enter new location: ")
            models.update_datacenter(dc_id, name, loc)
        elif choice == '4':
            models.view_datacenters()
            dc_id = input("Enter Data Center ID to delete: ")
            models.delete_datacenter(dc_id)
        elif choice == '0':
            break

def manage_workloads():
    while True:
        print("\n--- Manage AI Workloads ---")
        print("1. View Workloads")
        print("2. Add Workload")
        print("3. Update Workload")
        print("4. Delete Workload")
        print("0. Back")
        choice = input("Enter choice: ")
        if choice == '1':
            models.view_workloads()
        elif choice == '2':
            name = input("Enter workload name: ")
            wl_type = input("Enter type (e.g., Training, Inference): ")
            models.view_datacenters()
            dc_id = input("Enter Data Center ID to host this workload (or skip by pressing Enter): ")
            dc_id = dc_id if dc_id.strip() != "" else None
            models.add_workload(name, wl_type, dc_id)
        elif choice == '3':
            models.view_workloads()
            wl_id = input("Enter Workload ID to update: ")
            name = input("Enter new name: ")
            wl_type = input("Enter new type: ")
            dc_id = input("Enter new Data Center ID: ")
            models.update_workload(wl_id, name, wl_type, dc_id)
        elif choice == '4':
            models.view_workloads()
            wl_id = input("Enter Workload ID to delete: ")
            models.delete_workload(wl_id)
        elif choice == '0':
            break

def manage_water():
    while True:
        print("\n--- Manage Water Consumption ---")
        print("1. View Records")
        print("2. Add Record")
        print("3. Delete Record")
        print("0. Back")
        choice = input("Enter choice: ")
        if choice == '1':
            models.view_water_consumptions()
        elif choice == '2':
            try:
                liters = float(input("Enter water used (liters): "))
                if liters < 0:
                    print("Water usage cannot be negative.")
                    continue
                date = input("Enter date (YYYY-MM-DD): ")
                dc_id = input("Enter Data Center ID: ")
                wl_id = input("Enter Workload ID: ")
                models.add_water_consumption(liters, date, dc_id, wl_id)
            except ValueError:
                print("Invalid input for liters.")
        elif choice == '3':
            models.view_water_consumptions()
            wc_id = input("Enter Record ID to delete: ")
            models.delete_water_consumption(wc_id)
        elif choice == '0':
            break

def manage_cooling():
    while True:
        print("\n--- Manage Cooling Systems ---")
        print("1. View Cooling Systems")
        print("2. Add Cooling System")
        print("3. Delete Cooling System")
        print("0. Back")
        choice = input("Enter choice: ")
        if choice == '1':
            models.view_cooling_systems()
        elif choice == '2':
            try:
                c_type = input("Enter cooling system type: ")
                efficiency = float(input("Enter efficiency percentage: "))
                dc_id = input("Enter Data Center ID: ")
                models.add_cooling_system(c_type, efficiency, dc_id)
            except ValueError:
                print("Invalid input.")
        elif choice == '3':
            models.view_cooling_systems()
            cs_id = input("Enter Cooling System ID to delete: ")
            models.delete_cooling_system(cs_id)
        elif choice == '0':
            break

def manage_logs():
    while True:
        print("\n--- Manage Optimization Logs ---")
        print("1. View Logs")
        print("2. Add Log")
        print("3. Delete Log")
        print("0. Back")
        choice = input("Enter choice: ")
        if choice == '1':
            models.view_logs()
        elif choice == '2':
            description = input("Enter description: ")
            date = input("Enter date (YYYY-MM-DD): ")
            dc_id = input("Enter Data Center ID: ")
            models.add_log(description, date, dc_id)
        elif choice == '3':
            models.view_logs()
            log_id = input("Enter Log ID to delete: ")
            models.delete_log(log_id)
        elif choice == '0':
            break

def manage_users():
    while True:
        print("\n--- Manage Roles & Users ---")
        print("1. View Roles")
        print("2. View Users")
        print("3. Add Role")
        print("4. Add User")
        print("0. Back")
        choice = input("Enter choice: ")
        if choice == '1':
            models.view_roles()
        elif choice == '2':
            models.view_users()
        elif choice == '3':
            role = input("Enter Role Name: ")
            models.add_role(role)
        elif choice == '4':
            name = input("Enter User Name: ")
            email = input("Enter User Email: ")
            if "@" not in email:
                print("Invalid email format.")
                continue
            models.view_roles()
            role_id = input("Enter Role ID: ")
            models.add_user(name, email, role_id)
        elif choice == '0':
            break

def manage_monitoring():
    while True:
        print("\n--- Manage Monitoring Assignments ---")
        print("1. View Assignments")
        print("2. Assign User to Data Center")
        print("3. Remove Assignment")
        print("0. Back")
        choice = input("Enter choice: ")
        if choice == '1':
            models.view_monitoring()
        elif choice == '2':
            u_id = input("Enter User ID: ")
            dc_id = input("Enter Data Center ID: ")
            models.add_monitoring(u_id, dc_id)
        elif choice == '3':
            u_id = input("Enter User ID: ")
            dc_id = input("Enter Data Center ID: ")
            models.delete_monitoring(u_id, dc_id)
        elif choice == '0':
            break

def view_reports():
    while True:
        print("\n--- Reports & Analytics ---")
        print("1. Total Water Consumption per Data Center")
        print("2. Water Usage per AI Workload")
        print("3. Most Efficient Cooling Systems (Top 3)")
        print("4. View Logs for a Specific Data Center")
        print("5. View Users Monitoring a Specific Data Center")
        print("0. Back")
        
        choice = input("Enter choice: ")
        if choice == '1':
            models.total_water_per_datacenter()
        elif choice == '2':
            models.water_usage_per_workload()
        elif choice == '3':
            models.most_efficient_cooling()
        elif choice == '4':
            models.view_datacenters()
            dc_id = input("Enter Data Center ID: ")
            if dc_id.isdigit():
                models.logs_for_datacenter(dc_id)
        elif choice == '5':
            models.view_datacenters()
            dc_id = input("Enter Data Center ID: ")
            if dc_id.isdigit():
                models.users_monitoring_datacenter(dc_id)
        elif choice == '0':
            break

def main():
    print("Welcome to Data Center Water & AI Workload Manager")
    
    # Try connecting to verify configuration
    conn = database.get_connection()
    if not conn:
        print("\nWARN: Could not connect to the database. Make sure MySQL is running and configured correctly in .env.")
    else:
        conn.close()

    while True:
        print_menu()
        choice = input("Select an option: ")
        
        if choice == '1':
            manage_datacenters()
        elif choice == '2':
            manage_workloads()
        elif choice == '3':
            manage_water()
        elif choice == '4':
            manage_cooling()
        elif choice == '5':
            manage_logs()
        elif choice == '6':
            manage_users()
        elif choice == '7':
            manage_monitoring()
        elif choice == '8':
            view_reports()
        elif choice == '9':
            database.initialize_database()
        elif choice == '0':
            print("Exiting application. Goodbye!")
            sys.exit(0)
        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    main()
