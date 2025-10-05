# 🛡️ Threat Intelligence Dashboard

Real-time OSINT threat monitoring with live dashboard and admin panel.

## 🚀 Quick Start

```bash
git clone https://github.com/Mathewsunil24/osint_8.git
cd osint_8
pip install -r requirements.txt
python src/app.py
🌐 Access URLs
Dashboard: http://localhost:8080/dashboard

Admin Panel: http://localhost:8080/admin

API: http://localhost:8080/api/data

⚡ Features
📊 Live threat statistics

🎯 Risk severity tracking

➕ Add custom threats

🔄 Auto-refresh every 10s

🎨 Professional dark UI

📁 Project Structure
text
osint_8/
├── src/
│   └── app.py
├── data/
│   └── processed/
│       └── threats.json
├── frontend/
│   ├── lovable-integration.js
│   └── integration-readme.md
├── PowerShell Scripts/
│   ├── collect.ps1
│   ├── normalize.ps1
│   ├── run-all.ps1
│   └── server.ps1
├── requirements.txt
└── README.md
Start the server and open the dashboard! 🚀

text

## Update on GitHub:

```powershell
# Create the clean README
@"
# 🛡️ Threat Intelligence Dashboard

Real-time OSINT threat monitoring with live dashboard and admin panel.

## 🚀 Quick Start

\`\`\`bash
git clone https://github.com/Mathewsunil24/osint_8.git
cd osint_8
pip install -r requirements.txt
python src/app.py
\`\`\`

## 🌐 Access URLs

- **Dashboard**: \`http://localhost:8080/dashboard\`
- **Admin Panel**: \`http://localhost:8080/admin\`
- **API**: \`http://localhost:8080/api/data\`

## ⚡ Features

- 📊 Live threat statistics
- 🎯 Risk severity tracking  
- ➕ Add custom threats
- 🔄 Auto-refresh every 10s
- 🎨 Professional dark UI

## 📁 Project Structure

\`\`\`
osint_8/
├── src/
│   └── app.py
├── data/
│   └── processed/
│       └── threats.json
├── frontend/
│   ├── lovable-integration.js
│   └── integration-readme.md
├── PowerShell Scripts/
│   ├── collect.ps1
│   ├── normalize.ps1
│   ├── run-all.ps1
│   └── server.ps1
├── requirements.txt
└── README.md
\`\`\`

**Start the server and open the dashboard!** 🚀
"@ | Out-File -FilePath "README.md" -Encoding utf8

# Commit and push
git add README.md
git commit -m "docs: Clean README with proper structure and spacing"
git push origin main
