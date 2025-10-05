// Loveable AI OSINT Dashboard Integration for Threat Intelligence Backend
// Add this to your Loveable AI project's Custom Code section

class OSINTDashboard {
    constructor() {
        this.apiBaseUrl = 'http://localhost:8080/api';
        this.init();
    }

    async init() {
        console.log('🛡️ OSINT Threat Dashboard Initializing...');
        await this.loadThreatData();
        
        // Auto-refresh every 30 seconds
        setInterval(() => this.loadThreatData(), 30000);
        
        // Add refresh button if not exists
        this.addRefreshButton();
    }

    async loadThreatData() {
        try {
            console.log('📡 Fetching OSINT data from backend...');
            const response = await fetch(`${this.apiBaseUrl}/data`);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            console.log('✅ OSINT Data received:', data);
            this.updateDashboard(data);
            
        } catch (error) {
            console.error('❌ Failed to load OSINT data:', error);
            this.showFallbackData();
        }
    }

    updateDashboard(data) {
        // Update total threats
        this.updateElement('.total-threats, [data-total], #total', data.total?.toLocaleString() || '0');
        
        // Update threat types
        this.updateElement('.threat-types, [data-types]', Object.keys(data.types || {}).length);
        
        // Update sources count
        this.updateElement('.sources, [data-sources]', Object.keys(data.sources || {}).length);
        
        // Update threat list
        this.updateThreatList(data.threats || []);
        
        // Update charts if any
        this.updateCharts(data);
    }

    updateElement(selector, value) {
        if (!value) return;
        
        const elements = document.querySelectorAll(selector);
        elements.forEach(element => {
            if (element.textContent !== value.toString()) {
                element.textContent = value;
                // Add update animation
                element.style.animation = 'pulse 0.5s ease-in-out';
                setTimeout(() => element.style.animation = '', 500);
            }
        });
    }

    updateThreatList(threats) {
        const containers = [
            '.threat-list', '[data-threat-list]', '#threatList',
            '.recent-threats', '.threats-container'
        ];
        
        let threatList = null;
        for (const selector of containers) {
            threatList = document.querySelector(selector);
            if (threatList) break;
        }
        
        if (threatList && threats.length > 0) {
            threatList.innerHTML = threats.slice(0, 10).map((threat, index) => `
                <div class="threat-item" style="
                    border-left: 3px solid ${this.getThreatColor(threat.severity)};
                    padding: 12px;
                    margin: 8px 0;
                    background: rgba(255,255,255,0.05);
                    border-radius: 4px;
                    transition: transform 0.2s;
                " onmouseover="this.style.transform='translateX(5px)'" 
                   onmouseout="this.style.transform='translateX(0)'">
                    <div style="font-weight: bold; color: #e74c3c; font-size: 14px;">
                        ${threat.indicator || 'Unknown'}
                    </div>
                    <div style="font-size: 0.8em; color: #95a5a6; margin-top: 4px;">
                        Type: ${threat.type || 'Unknown'} | 
                        Source: ${threat.source || 'Unknown'} |
                        Confidence: ${threat.confidence || 'N/A'}%
                    </div>
                    ${threat.description ? `<div style="font-size: 0.75em; color: #7f8c8d; margin-top: 2px;">${threat.description}</div>` : ''}
                </div>
            `).join('');
        }
    }

    getThreatColor(severity) {
        const colors = {
            'high': '#e74c3c',
            'medium': '#f39c12', 
            'low': '#f1c40f',
            'info': '#3498db'
        };
        return colors[severity?.toLowerCase()] || '#95a5a6';
    }

    updateCharts(data) {
        // Placeholder for chart updates
        if (window.updateOSINTCharts) {
            window.updateOSINTCharts(data);
        }
    }

    showFallbackData() {
        const demoData = {
            total: 127,
            types: { malware: 45, phishing: 32, botnet: 28, exploit: 22 },
            sources: { alienvault: 50, threatcrowd: 35, abuse_ch: 25, other: 17 },
            threats: [
                { 
                    indicator: "malicious-domain.com", 
                    type: "phishing", 
                    source: "alienvault",
                    severity: "high",
                    confidence: 85
                },
                { 
                    indicator: "192.168.1.100", 
                    type: "botnet", 
                    source: "threatcrowd",
                    severity: "medium",
                    confidence: 72
                }
            ]
        };
        this.updateDashboard(demoData);
        
        this.showError('Using demo data - Backend connection failed. Make sure server is running.');
    }

    showError(message) {
        // Remove existing errors
        const existingError = document.querySelector('.osint-error');
        if (existingError) existingError.remove();
        
        const errorDiv = document.createElement('div');
        errorDiv.className = 'osint-error';
        errorDiv.style.cssText = `
            background: #e74c3c; 
            color: white; 
            padding: 12px; 
            margin: 10px; 
            border-radius: 5px;
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 1000;
            max-width: 300px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        `;
        errorDiv.innerHTML = `
            <strong>⚠️ OSINT Dashboard Error</strong>
            <div style="font-size: 0.9em; margin-top: 5px;">${message}</div>
        `;
        document.body.appendChild(errorDiv);
        
        setTimeout(() => errorDiv.remove(), 8000);
    }

    addRefreshButton() {
        if (document.querySelector('#osint-refresh-btn')) return;
        
        const btn = document.createElement('button');
        btn.id = 'osint-refresh-btn';
        btn.innerHTML = '🔄 Refresh OSINT Data';
        btn.style.cssText = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            padding: 12px 16px;
            background: #3498db;
            color: white;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            z-index: 1000;
            font-size: 14px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
            transition: background 0.3s;
        `;
        btn.onmouseover = () => btn.style.background = '#2980b9';
        btn.onmouseout = () => btn.style.background = '#3498db';
        btn.onclick = () => this.loadThreatData();
        
        document.body.appendChild(btn);
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    window.osintDashboard = new OSINTDashboard();
});

// Manual refresh function
window.refreshOSINTData = function() {
    if (window.osintDashboard) {
        window.osintDashboard.loadThreatData();
    }
};

// Test connection function
window.testOSINTConnection = function() {
    fetch('http://localhost:8080/api/data')
        .then(response => response.json())
        .then(data => {
            alert(`✅ OSINT Backend Connected!\nTotal Threats: ${data.total}\nSources: ${Object.keys(data.sources || {}).length}`);
        })
        .catch(error => {
            alert('❌ OSINT Connection Failed: ' + error.message);
        });
};

// Add some basic styles for animations
const style = document.createElement('style');
style.textContent = `
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.7; }
        100% { opacity: 1; }
    }
`;
document.head.appendChild(style);