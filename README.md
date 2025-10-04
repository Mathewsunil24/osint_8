# 🛡️ Threat Intelligence Backend

PowerShell backend for OSINT Lab 8 - Threat Intelligence Pipeline

## 🚀 Quick Start
```powershell
# Run complete pipeline
.\collect.ps1
.\normalize.ps1
.\server.ps1

# Test API
Invoke-RestMethod "http://localhost:8080/api/data"