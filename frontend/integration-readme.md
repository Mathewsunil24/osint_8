# Loveable AI OSINT Dashboard Integration

## Overview
This integration connects your Loveable AI dashboard with the OSINT threat intelligence backend.

## Setup Instructions

### 1. Loveable AI Configuration
1. Open your Loveable AI project
2. Go to **Settings → Custom Code → JavaScript**
3. Paste the entire contents of `lovable-integration.js`
4. Save and publish your project

### 2. Backend Requirements
Ensure your backend is running and provides this endpoint:
- `GET http://localhost:8080/api/data`

**Expected Response Format:**
```json
{
  "total": 127,
  "types": {
    "malware": 45,
    "phishing": 32,
    "botnet": 28,
    "exploit": 22
  },
  "sources": {
    "alienvault": 50,
    "threatcrowd": 35,
    "abuse_ch": 25,
    "other": 17
  },
  "threats": [
    {
      "indicator": "malicious-domain.com",
      "type": "phishing",
      "source": "alienvault",
      "severity": "high",
      "confidence": 85,
      "description": "Phishing campaign targeting financial institutions"
    }
  ]
}