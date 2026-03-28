CREATE DATABASE IF NOT EXISTS water_ai_db;
USE water_ai_db;

-- 1. DataCenter (data_center_id PK, name, location)
CREATE TABLE IF NOT EXISTS DataCenter (
    data_center_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    location VARCHAR(255) NOT NULL
);

-- 2. AI_Workload (workload_id PK, name, type, data_center_id FK)
CREATE TABLE IF NOT EXISTS AI_Workload (
    workload_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    type VARCHAR(50) NOT NULL,
    data_center_id INT,
    FOREIGN KEY (data_center_id) REFERENCES DataCenter(data_center_id) ON DELETE SET NULL
);

-- 3. Water_Consumption (water_id PK, water_used_liters, date, data_center_id FK, workload_id FK)
CREATE TABLE IF NOT EXISTS Water_Consumption (
    water_id INT AUTO_INCREMENT PRIMARY KEY,
    water_used_liters DECIMAL(15,2) NOT NULL CHECK (water_used_liters >= 0),
    date DATE NOT NULL,
    data_center_id INT,
    workload_id INT,
    FOREIGN KEY (data_center_id) REFERENCES DataCenter(data_center_id) ON DELETE CASCADE,
    FOREIGN KEY (workload_id) REFERENCES AI_Workload(workload_id) ON DELETE CASCADE
);

-- 4. Cooling_System (cooling_id PK, type, efficiency, data_center_id FK)
CREATE TABLE IF NOT EXISTS Cooling_System (
    cooling_id INT AUTO_INCREMENT PRIMARY KEY,
    type VARCHAR(100) NOT NULL,
    efficiency DECIMAL(5,2) NOT NULL,
    data_center_id INT UNIQUE,
    FOREIGN KEY (data_center_id) REFERENCES DataCenter(data_center_id) ON DELETE CASCADE
);

-- 5. Optimization_Log (log_id PK, description, date, data_center_id FK)
CREATE TABLE IF NOT EXISTS Optimization_Log (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    description TEXT NOT NULL,
    date DATE NOT NULL,
    data_center_id INT,
    FOREIGN KEY (data_center_id) REFERENCES DataCenter(data_center_id) ON DELETE CASCADE
);

-- 6. Role (role_id PK, role_name)
CREATE TABLE IF NOT EXISTS Role (
    role_id INT AUTO_INCREMENT PRIMARY KEY,
    role_name VARCHAR(50) NOT NULL UNIQUE
);

-- 7. User (user_id PK, name, email, role_id FK)
CREATE TABLE IF NOT EXISTS User (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    role_id INT,
    FOREIGN KEY (role_id) REFERENCES Role(role_id) ON DELETE SET NULL
);

-- 8. Monitoring (user_id FK, data_center_id FK, PRIMARY KEY(user_id, data_center_id))
CREATE TABLE IF NOT EXISTS Monitoring (
    user_id INT,
    data_center_id INT,
    PRIMARY KEY (user_id, data_center_id),
    FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE,
    FOREIGN KEY (data_center_id) REFERENCES DataCenter(data_center_id) ON DELETE CASCADE
);

-- INSERT SAMPLE DATA

INSERT INTO Role (role_name) VALUES 
('Admin'), ('Operator'), ('Analyst'), ('Site Engineer'), ('General Manager');

INSERT INTO User (name, email, role_id) VALUES 
('Alice Smith', 'alice@example.com', 1),
('Bob Johnson', 'bob@example.com', 2),
('Charlie Brown', 'charlie@example.com', 3),
('David Miller', 'david@example.com', 4),
('Eve Davis', 'eve@example.com', 5),
('Frank Wilson', 'frank@example.com', 2);

INSERT INTO DataCenter (name, location) VALUES 
('US-East-1', 'Virginia, USA'),
('EU-West-1', 'Dublin, Ireland'),
('AP-South-1', 'Mumbai, India'),
('AP-East-1', 'Tokyo, Japan'),
('SA-East-1', 'Sao Paulo, Brazil');

INSERT INTO AI_Workload (name, type, data_center_id) VALUES 
('LLM Training GPT-4', 'Training', 1),
('Image Inference Node', 'Inference', 2),
('Recommendation Engine', 'Data Processing', 3),
('Customer Support Bot', 'Inference', 1),
('Real-time NLP Processor', 'Inference', 4),
('Video Rendering Pipeline', 'Data Processing', 5);

INSERT INTO Water_Consumption (water_used_liters, date, data_center_id, workload_id) VALUES 
(54000.50, '2023-10-01', 1, 1),
(12000.00, '2023-10-01', 2, 2),
(8500.25, '2023-10-02', 3, 3),
(4500.00, '2023-10-02', 1, 4),
(15200.75, '2023-10-03', 4, 5),
(28500.00, '2023-10-03', 5, 6);

INSERT INTO Cooling_System (type, efficiency, data_center_id) VALUES 
('Chilled Water System', 85.5, 1),
('Direct Expansion', 78.0, 2),
('Evaporative Cooling', 92.0, 3),
('Liquid Immersion Cooling', 97.5, 4),
('Air-side Free Cooling', 89.0, 5);

INSERT INTO Optimization_Log (description, date, data_center_id) VALUES 
('Upgraded pump efficiency in Chilled Water System', '2023-09-15', 1),
('Replaced faulty compressor in DX unit', '2023-09-20', 2),
('Scheduled maintenance for Evaporative Cooling', '2023-10-05', 3),
('Installed advanced immersion fluid monitoring', '2023-10-10', 4),
('Calibrated external air intake sensors', '2023-10-12', 5);

INSERT INTO Monitoring (user_id, data_center_id) VALUES 
(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), -- Admin Alice monitors all
(2, 2), (6, 5),                         -- Operators Bob and Frank
(3, 1), (3, 3),                         -- Analyst Charlie monitors US and India
(4, 4), (4, 5),                         -- Engineer David monitors AP-East and SA-East
(5, 1);                                 -- Manager Eve watches US-East
