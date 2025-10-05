from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

THREATS_FILE = 'data/processed/threats.json'

def load_threat_data():
    """Load threat data from JSON file"""
    try:
        with open(THREATS_FILE, 'r') as f:
            content = f.read().strip()
            if not content:
                return get_fallback_data()
            data = json.loads(content)
            
            if isinstance(data, list):
                return {
                    "total": len(data),
                    "types": count_threat_types(data),
                    "sources": count_threat_sources(data),
                    "threats": data[:10]
                }
            return data
            
    except Exception as e:
        print(f"Error loading data: {e}")
        return get_fallback_data()

def save_threat_data(threats):
    """Save threats to JSON file"""
    try:
        with open(THREATS_FILE, 'w') as f:
            json.dump(threats, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving data: {e}")
        return False

def count_threat_types(threats):
    types = {}
    for threat in threats:
        threat_type = threat.get('type', 'unknown')
        types[threat_type] = types.get(threat_type, 0) + 1
    return types

def count_threat_sources(threats):
    sources = {}
    for threat in threats:
        source = threat.get('source', 'unknown')
        sources[source] = sources.get(source, 0) + 1
    return sources

def get_fallback_data():
    return {
        "total": 156,
        "types": {"malware": 67, "phishing": 45, "botnet": 28, "exploit": 16},
        "sources": {"alienvault": 72, "threatcrowd": 48, "abuse_ch": 36},
        "threats": [
            {
                "indicator": "malicious-domain.com", "type": "phishing", "source": "alienvault",
                "severity": "high", "confidence": 92, "description": "Phishing campaign"
            }
        ]
    }

@app.route('/api/data')
def api_data():
    data = load_threat_data()
    return jsonify(data)

@app.route('/api/add_threat', methods=['POST'])
def add_threat():
    try:
        new_threat = request.get_json()
        
        # Validate required fields
        if not new_threat or not new_threat.get('indicator'):
            return jsonify({"error": "Indicator is required"}), 400
        
        # Load existing threats
        with open(THREATS_FILE, 'r') as f:
            threats = json.load(f)
        
        # Add new threat with timestamp
        new_threat['timestamp'] = datetime.now().isoformat()
        threats.append(new_threat)
        
        # Save updated threats
        if save_threat_data(threats):
            return jsonify({"success": True, "message": "Threat added successfully"})
        else:
            return jsonify({"error": "Failed to save threat"}), 500
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/clear_threats', methods=['POST'])
def clear_threats():
    try:
        # Reset to empty array
        save_threat_data([])
        return jsonify({"success": True, "message": "All threats cleared"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def home():
    return """
    <h1>Threat Intelligence Backend</h1>
    <p>Available endpoints:</p>
    <ul>
        <li><a href="/api/data">/api/data</a> - Threat data API</li>
        <li><a href="/dashboard">/dashboard</a> - Main Dashboard</li>
        <li><a href="/admin">/admin</a> - Admin Panel (Add threats)</li>
    </ul>
    """

@app.route('/dashboard')
def dashboard():
    return """
<!DOCTYPE html>
<html>
<head>
    <title>OSINT Threat Intelligence Dashboard</title>
    <style>
        :root { --primary: #6366f1; --danger: #ef4444; --warning: #f59e0b; --success: #10b981; --dark: #0f172a; --darker: #020617; --card-bg: #1e293b; --text: #f8fafc; --text-muted: #94a3b8; }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { background: linear-gradient(135deg, var(--darker) 0%, var(--dark) 100%); color: var(--text); font-family: 'Segoe UI', sans-serif; min-height: 100vh; line-height: 1.6; }
        .dashboard { max-width: 1400px; margin: 0 auto; padding: 20px; }
        .header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; padding-bottom: 20px; border-bottom: 1px solid rgba(255,255,255,0.1); }
        .logo { display: flex; align-items: center; gap: 12px; }
        .logo-icon { width: 40px; height: 40px; background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%); border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 20px; }
        .logo-text h1 { font-size: 24px; font-weight: 700; background: linear-gradient(135deg, var(--text) 0%, var(--text-muted) 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .logo-text p { color: var(--text-muted); font-size: 14px; }
        .last-updated { color: var(--text-muted); font-size: 14px; }
        .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 30px; }
        .stat-card { background: var(--card-bg); padding: 25px; border-radius: 16px; border: 1px solid rgba(255,255,255,0.1); position: relative; overflow: hidden; transition: transform 0.3s ease, box-shadow 0.3s ease; }
        .stat-card:hover { transform: translateY(-5px); box-shadow: 0 20px 40px rgba(0,0,0,0.3); }
        .stat-card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 4px; background: linear-gradient(90deg, var(--primary), var(--success)); }
        .stat-card.danger::before { background: linear-gradient(90deg, var(--danger), var(--warning)); }
        .stat-card.warning::before { background: linear-gradient(90deg, var(--warning), var(--success)); }
        .stat-icon { width: 50px; height: 50px; border-radius: 12px; display: flex; align-items: center; justify-content: center; margin-bottom: 15px; font-size: 20px; background: rgba(99, 102, 241, 0.1); color: var(--primary); }
        .stat-card.danger .stat-icon { background: rgba(239, 68, 68, 0.1); color: var(--danger); }
        .stat-card.warning .stat-icon { background: rgba(245, 158, 11, 0.1); color: var(--warning); }
        .stat-value { font-size: 32px; font-weight: 700; margin-bottom: 5px; }
        .stat-label { color: var(--text-muted); font-size: 14px; font-weight: 500; }
        .content-grid { display: grid; grid-template-columns: 2fr 1fr; gap: 25px; }
        .threats-section, .sources-section { background: var(--card-bg); border-radius: 16px; padding: 25px; border: 1px solid rgba(255,255,255,0.1); }
        .section-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
        .section-title { font-size: 18px; font-weight: 600; }
        .refresh-btn { background: var(--primary); color: white; border: none; padding: 8px 16px; border-radius: 8px; cursor: pointer; font-size: 14px; display: flex; align-items: center; gap: 6px; transition: background 0.3s ease; }
        .refresh-btn:hover { background: var(--primary-dark); }
        .threat-list { display: flex; flex-direction: column; gap: 12px; }
        .threat-item { background: rgba(255,255,255,0.05); padding: 16px; border-radius: 12px; border-left: 4px solid var(--primary); transition: background 0.3s ease; }
        .threat-item:hover { background: rgba(255,255,255,0.08); }
        .threat-item.high { border-left-color: var(--danger); }
        .threat-item.medium { border-left-color: var(--warning); }
        .threat-item.low { border-left-color: var(--success); }
        .threat-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px; }
        .threat-indicator { font-weight: 600; font-family: 'Courier New', monospace; color: var(--text); }
        .threat-badge { padding: 4px 8px; border-radius: 6px; font-size: 11px; font-weight: 600; text-transform: uppercase; }
        .badge-high { background: var(--danger); color: white; }
        .badge-medium { background: var(--warning); color: black; }
        .badge-low { background: var(--success); color: white; }
        .threat-meta { display: flex; gap: 15px; color: var(--text-muted); font-size: 13px; margin-bottom: 6px; }
        .threat-description { color: var(--text-muted); font-size: 13px; line-height: 1.4; }
        .sources-grid { display: grid; grid-template-columns: 1fr; gap: 12px; }
        .source-item { display: flex; justify-content: space-between; align-items: center; padding: 12px; background: rgba(255,255,255,0.05); border-radius: 10px; transition: background 0.3s ease; }
        .source-item:hover { background: rgba(255,255,255,0.08); }
        .source-info { display: flex; align-items: center; gap: 10px; }
        .source-icon { width: 32px; height: 32px; border-radius: 8px; background: var(--primary); display: flex; align-items: center; justify-content: center; font-size: 14px; }
        .source-name { font-weight: 500; }
        .source-count { background: var(--primary); color: white; padding: 4px 8px; border-radius: 6px; font-size: 12px; font-weight: 600; }
        .admin-link { position: fixed; bottom: 20px; right: 20px; background: var(--primary); color: white; padding: 12px 16px; border-radius: 8px; text-decoration: none; font-size: 14px; }
    </style>
</head>
<body>
    <div class="dashboard">
        <div class="header">
            <div class="logo">
                <div class="logo-icon">🛡️</div>
                <div class="logo-text">
                    <h1>OSINT Threat Intelligence</h1>
                    <p>Real-time threat analysis from multiple intelligence sources</p>
                </div>
            </div>
            <div class="last-updated" id="lastUpdated">Last updated: <span id="updateTime">Just now</span></div>
        </div>
        
        <div class="stats-grid">
            <div class="stat-card"><div class="stat-icon">📊</div><div class="stat-value" id="totalThreats">0</div><div class="stat-label">Total Indicators</div></div>
            <div class="stat-card danger"><div class="stat-icon">🚨</div><div class="stat-value" id="highRisk">0</div><div class="stat-label">High Risk Threats</div></div>
            <div class="stat-card warning"><div class="stat-icon">⚠️</div><div class="stat-value" id="mediumRisk">0</div><div class="stat-label">Medium Risk Threats</div></div>
            <div class="stat-card"><div class="stat-icon">🔍</div><div class="stat-value" id="sourcesCount">0</div><div class="stat-label">Active Sources</div></div>
        </div>
        
        <div class="content-grid">
            <div class="threats-section">
                <div class="section-header">
                    <div class="section-title">Recent Threat Indicators</div>
                    <button class="refresh-btn" onclick="refreshData()"><span>🔄</span> Refresh</button>
                </div>
                <div class="threat-list" id="threatList"><div>Loading threat data...</div></div>
            </div>
            
            <div class="sources-section">
                <div class="section-header">
                    <div class="section-title">Threat Sources</div>
                    <div class="section-subtitle" id="sourcesSubtitle">0 sources active</div>
                </div>
                <div class="sources-grid" id="sourcesGrid"><div>Loading sources...</div></div>
            </div>
        </div>
    </div>

    <a href="/admin" class="admin-link">⚙️ Admin Panel</a>

    <script>
        async function loadThreatData() {
            try {
                const response = await fetch('/api/data');
                const data = await response.json();
                updateDashboard(data);
                updateLastUpdated();
            } catch (error) {
                document.getElementById('threatList').innerHTML = '<div style="text-align: center; padding: 40px; color: #ef4444;">❌ Connection failed</div>';
            }
        }

        function updateDashboard(data) {
            document.getElementById('totalThreats').textContent = data.total || 0;
            document.getElementById('sourcesCount').textContent = Object.keys(data.sources || {}).length;
            
            const threats = data.threats || [];
            const highRisk = threats.filter(t => t.severity === 'high').length;
            const mediumRisk = threats.filter(t => t.severity === 'medium').length;
            
            document.getElementById('highRisk').textContent = highRisk;
            document.getElementById('mediumRisk').textContent = mediumRisk;
            
            updateThreatList(threats);
            updateSources(data.sources);
        }

        function updateThreatList(threats) {
            const threatList = document.getElementById('threatList');
            if (threats.length === 0) {
                threatList.innerHTML = '<div style="text-align: center; padding: 40px; color: #94a3b8;">No threats detected</div>';
                return;
            }
            
            threatList.innerHTML = threats.slice(0, 8).map(threat => {
                const severity = threat.severity || 'medium';
                return `
                    <div class="threat-item ${severity}">
                        <div class="threat-header">
                            <div class="threat-indicator">${threat.indicator || 'Unknown'}</div>
                            <div class="threat-badge badge-${severity}">${severity.toUpperCase()}</div>
                        </div>
                        <div class="threat-meta">
                            <span>Type: ${threat.type || 'Unknown'}</span>
                            <span>Source: ${threat.source || 'Unknown'}</span>
                            ${threat.confidence ? `<span>Confidence: ${threat.confidence}%</span>` : ''}
                        </div>
                        ${threat.description ? `<div class="threat-description">${threat.description}</div>` : ''}
                    </div>
                `;
            }).join('');
        }

        function updateSources(sources) {
            const sourcesGrid = document.getElementById('sourcesGrid');
            const sourcesSubtitle = document.getElementById('sourcesSubtitle');
            
            if (!sources) {
                sourcesGrid.innerHTML = '<div style="text-align: center; padding: 20px; color: #94a3b8;">No sources available</div>';
                sourcesSubtitle.textContent = '0 sources active';
                return;
            }
            
            const sourceEntries = Object.entries(sources).sort((a, b) => b[1] - a[1]);
            sourcesSubtitle.textContent = `${sourceEntries.length} sources active`;
            
            sourcesGrid.innerHTML = sourceEntries.map(([source, count]) => `
                <div class="source-item">
                    <div class="source-info">
                        <div class="source-icon">🔍</div>
                        <div class="source-name">${source.charAt(0).toUpperCase() + source.slice(1)}</div>
                    </div>
                    <div class="source-count">${count}</div>
                </div>
            `).join('');
        }

        function updateLastUpdated() {
            document.getElementById('updateTime').textContent = new Date().toLocaleTimeString();
        }

        function refreshData() {
            loadThreatData();
        }

        loadThreatData();
        setInterval(loadThreatData, 10000);
    </script>
</body>
</html>
    """

@app.route('/admin')
def admin_panel():
    return """
<!DOCTYPE html>
<html>
<head>
    <title>Threat Admin Panel</title>
    <style>
        :root { --primary: #6366f1; --danger: #ef4444; --warning: #f59e0b; --success: #10b981; --dark: #0f172a; --card-bg: #1e293b; --text: #f8fafc; }
        body { background: var(--dark); color: var(--text); font-family: 'Segoe UI', sans-serif; margin: 0; padding: 20px; min-height: 100vh; }
        .container { max-width: 800px; margin: 0 auto; }
        .header { text-align: center; margin-bottom: 30px; }
        .form-container { background: var(--card-bg); padding: 30px; border-radius: 16px; border: 1px solid rgba(255,255,255,0.1); margin-bottom: 30px; }
        .form-group { margin-bottom: 20px; }
        label { display: block; margin-bottom: 8px; font-weight: 600; }
        input, select, textarea { width: 100%; padding: 12px; border: 1px solid rgba(255,255,255,0.2); border-radius: 8px; background: rgba(0,0,0,0.3); color: var(--text); font-size: 16px; }
        button { background: var(--primary); color: white; border: none; padding: 12px 24px; border-radius: 8px; cursor: pointer; font-size: 16px; margin-right: 10px; }
        button.danger { background: var(--danger); }
        .dashboard-link { display: inline-block; margin-top: 20px; color: var(--primary); text-decoration: none; }
        .message { padding: 12px; border-radius: 8px; margin: 10px 0; }
        .success { background: var(--success); color: white; }
        .error { background: var(--danger); color: white; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🛡️ Threat Admin Panel</h1>
            <p>Add and manage threat intelligence data</p>
        </div>
        
        <div class="form-container">
            <h2>Add New Threat</h2>
            <div id="message"></div>
            
            <div class="form-group">
                <label>Threat Indicator *</label>
                <input type="text" id="indicator" placeholder="e.g., malicious-domain.com, 192.168.1.100" required>
            </div>
            
            <div class="form-group">
                <label>Threat Type</label>
                <select id="type">
                    <option value="malware">Malware</option>
                    <option value="phishing">Phishing</option>
                    <option value="botnet">Botnet</option>
                    <option value="exploit">Exploit</option>
                    <option value="ransomware">Ransomware</option>
                    <option value="c2">Command & Control</option>
                </select>
            </div>
            
            <div class="form-group">
                <label>Source</label>
                <input type="text" id="source" placeholder="e.g., alienvault, custom" value="custom">
            </div>
            
            <div class="form-group">
                <label>Severity</label>
                <select id="severity">
                    <option value="low">Low</option>
                    <option value="medium" selected>Medium</option>
                    <option value="high">High</option>
                </select>
            </div>
            
            <div class="form-group">
                <label>Confidence (0-100)</label>
                <input type="number" id="confidence" min="0" max="100" value="75">
            </div>
            
            <div class="form-group">
                <label>Description</label>
                <textarea id="description" rows="3" placeholder="Threat description..."></textarea>
            </div>
            
            <button onclick="addThreat()">➕ Add Threat</button>
            <button class="danger" onclick="clearThreats()">🗑️ Clear All Threats</button>
            
            <a href="/dashboard" class="dashboard-link">📊 View Dashboard</a>
        </div>
    </div>

    <script>
        function showMessage(text, type) {
            const messageDiv = document.getElementById('message');
            messageDiv.innerHTML = `<div class="message ${type}">${text}</div>`;
            setTimeout(() => messageDiv.innerHTML = '', 5000);
        }

        async function addThreat() {
            const threat = {
                indicator: document.getElementById('indicator').value,
                type: document.getElementById('type').value,
                source: document.getElementById('source').value,
                severity: document.getElementById('severity').value,
                confidence: parseInt(document.getElementById('confidence').value),
                description: document.getElementById('description').value
            };

            if (!threat.indicator) {
                showMessage('Threat indicator is required!', 'error');
                return;
            }

            try {
                const response = await fetch('/api/add_threat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(threat)
                });

                const result = await response.json();
                
                if (response.ok) {
                    showMessage('✅ Threat added successfully! It will appear in the dashboard.', 'success');
                    // Clear form
                    document.getElementById('indicator').value = '';
                    document.getElementById('description').value = '';
                } else {
                    showMessage('❌ Error: ' + result.error, 'error');
                }
            } catch (error) {
                showMessage('❌ Network error: ' + error, 'error');
            }
        }

        async function clearThreats() {
            if (!confirm('Are you sure you want to clear ALL threats?')) return;
            
            try {
                const response = await fetch('/api/clear_threats', { method: 'POST' });
                const result = await response.json();
                
                if (response.ok) {
                    showMessage('✅ All threats cleared!', 'success');
                } else {
                    showMessage('❌ Error: ' + result.error, 'error');
                }
            } catch (error) {
                showMessage('❌ Network error: ' + error, 'error');
            }
        }
    </script>
</body>
</html>
    """

if __name__ == '__main__':
    print("🚀 Starting Threat Intelligence Backend...")
    print("📍 http://localhost:8080")
    print("📊 API: http://localhost:8080/api/data")
    print("📈 Dashboard: http://localhost:8080/dashboard")
    print("⚙️  Admin Panel: http://localhost:8080/admin")
    app.run(host='0.0.0.0', port=8080, debug=True)