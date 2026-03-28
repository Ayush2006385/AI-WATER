# Data Center Water & AI Workload Manager

A comprehensive Python-based DBMS project that tracks and manages AI workloads, data centers, and their water consumption. 

## Features Demonstrated
This system models real-world 3NF database architecture.
- **ER to Relational Mapping**
- **1NF, 2NF, 3NF Normalization**
- **Complex Relationships**: 1:1, 1:N, and M:N relationships (e.g., Users Monitoring Data Centers).
- **CRUD Operations**: Comprehensive creation, retrieval, updates, and deletion for 8 entities.
- **Advanced SQL Reporting**: Aggregation, grouping, and filtering using complex JOINs.

## Project Structure
- `schema.sql`: Contains the DDL table definitions, foreign key constraints, and sample data population.
- `database.py`: Handles connection pooling and database initialization logic.
- `models.py`: Centralized CRUD routines and complex analytical SQL queries.
- `main.py`: The CLI application entrypoint.

## Pre-requisites
- **Python 3.8+**
- **MySQL 8.0+**

## Setup Instructions

1. **Install Python Packages**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Database Credentials**
   Create a `.env` file in the root directory (or copy the provided `.env.example`):
   ```ini
   DB_HOST=localhost
   DB_USER=root
   DB_PASSWORD=password
   DB_NAME=water_ai_db
   ```

3. **Run the Application**
   ```bash
   python main.py
   ```

4. **Initialize Database**
   - In the CLI Main Menu, select option `9. Initialize/Reset Database (Run schema)`.
   - This will automatically execute `schema.sql` into your MySQL instance and populate the tables with sample records.

## Analytical Queries included
The application fulfills essential DBMS reporting through:
1. Total water consumption per data center.
2. Water usage per AI workload.
3. Most efficient cooling system.
4. Descriptive optimization logs scoped to a specific data center.
5. Users currently monitoring specific facilities (M:N queries).

## Constraints Implemented
- Referential Integrity via `FOREIGN KEY` constraints (`ON DELETE CASCADE` / `ON DELETE SET NULL`).
- Non-negative value checks using `CHECK (water_used_liters >= 0)`.
- Unique attributes via `UNIQUE` (Email, Role Name).
