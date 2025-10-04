# API Documentation for Frontend

## API Endpoint
```
http://localhost:8080/api/data
```

## Data Structure
```json
{
  "total": 36078,
  "sources": {"urlhaus": 36078},
  "types": {"url": 36074},
  "threats": [
    {
      "indicator": "http://malicious.com/payload.exe",
      "type": "url",
      "source": "urlhaus",
      "description": "Malicious URL"
    }
  ]
}
```

## How to Use
1. Backend must be running: `.\PowerShell Scripts\server.ps1`
2. Call API from frontend:
```javascript
fetch('http://localhost:8080/api/data')
  .then(response => response.json())
  .then(data => {
    // Use these properties:
    console.log(data.total);        // Total threats: 36078
    console.log(data.sources);      // {urlhaus: 36078}
    console.log(data.types);        // {url: 36074}
    console.log(data.threats[0]);   // First threat object
  });
```