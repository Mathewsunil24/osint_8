# 🛡️ OSINT Threat Intelligence Backend

A comprehensive threat intelligence platform that collects, processes, and visualizes OSINT (Open Source Intelligence) data from multiple security feeds. Features a real-time dashboard and admin panel for threat management.

![Threat Intelligence](https://img.shields.io/badge/Threat-Intelligence-red)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/Flask-2.3%2B-green)
![Real-time](https://img.shields.io/badge/Real--time-Dashboard-orange)

## 🚀 Features

### 🔍 Threat Collection
- **Multiple Data Sources**: AlienVault OTX, URLhaus, ThreatCrowd, Abuse.ch
- **Automated Collection**: PowerShell scripts for scheduled data gathering
- **Data Normalization**: Consistent threat indicator formatting
- **Real-time Updates**: Live data processing and enrichment

### 📊 Dashboard & Visualization
- **Real-time Dashboard**: Live threat statistics and metrics
- **Risk Analysis**: Severity-based threat categorization (High/Medium/Low)
- **Source Tracking**: Threat origin and confidence scoring
- **Interactive UI**: Modern, responsive design with dark theme
- **Auto-refresh**: Automatic updates every 10 seconds

### ⚙️ Administration & Management
- **Admin Panel**: Web-based threat management interface
- **Manual Threat Input**: Add custom threats in real-time
- **Bulk Operations**: Clear all threats with one click
- **API Access**: RESTful endpoints for integration

### 🛡️ Security Features
- **CORS Enabled**: Cross-origin resource sharing for web apps
- **Data Validation**: Input sanitization and threat verification
- **Error Handling**: Comprehensive error management and fallbacks
- **Logging**: Detailed operation logs and audit trails

## 🏗️ Architecture
ThreatIntel-Backend/
├── 📁 data/
│ ├── 📁 raw/ # Raw collected threat data
│ │ └── threats-raw.json
│ └── 📁 processed/ # Normalized threat data
│ └── threats.json
├── 📁 frontend/ # Integration files
│ ├── lovable-integration.js
│ └── integration-readme.md
├── 📁 PowerShell Scripts/ # Automation scripts
│ ├── collect.ps1 # Data collection
│ ├── normalize.ps1 # Data processing
│ ├── run-all.ps1 # Full pipeline
│ └── server.ps1 # Server management
├── 📁 src/ # Python source code
│ └── app.py # Main Flask application
├── requirements.txt # Python dependencies
├── API_DOCUMENTATION.md # API reference
└── README.md # This file

text

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- PowerShell 5.0+
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Mathewsunil24/osint_8.git
   cd osint_8
Install Python dependencies

bash
pip install -r requirements.txt
Run the application

bash
python src/app.py
Alternative: Use PowerShell Script
powershell
.\PowerShell Scripts\server.ps1
🌐 Access Points
Once running, access these endpoints:

Endpoint	Description	Purpose
http://localhost:8080/	Home Page	Overview and navigation
http://localhost:8080/dashboard	Main Dashboard	Real-time threat visualization
http://localhost:8080/admin	Admin Panel	Threat management interface
http://localhost:8080/api/data	Data API	JSON threat data endpoint
📊 Dashboard Features
Real-time Statistics
Total Threat Indicators: Overall threat count

High Risk Threats: Critical severity threats

Medium Risk Threats: Moderate severity threats

Active Sources: Number of intelligence sources

Threat Visualization
Recent Threat Indicators: Latest detected threats

Severity Badges: Color-coded risk levels

Source Analysis: Threat origin breakdown

Confidence Scoring: Reliability indicators

Interactive Elements
Auto-refresh: Updates every 10 seconds

Manual Refresh: On-demand data updates

Hover Effects: Detailed threat information

Responsive Design: Mobile-friendly interface

⚙️ Admin Panel Usage
Adding Threats
Navigate to http://localhost:8080/admin

Fill in threat details:

Indicator: IP, domain, or URL

Type: Malware


