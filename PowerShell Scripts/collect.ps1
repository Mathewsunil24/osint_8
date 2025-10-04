# collect.ps1 - USING PUBLIC FEEDS
Write-Host "Collecting threat data from public feeds..." -ForegroundColor Yellow

function Get-PublicThreats {
    $threats = @()
    
    try {
        # Method 1: Abuse.ch URLhaus (public feed)
        Write-Host "Fetching from URLhaus..." -ForegroundColor Gray
        $urlhaus = Invoke-RestMethod -Uri "https://urlhaus.abuse.ch/downloads/csv_recent/" -TimeoutSec 30
        $urlLines = $urlhaus -split "`n" | Select-Object -Skip 9  # Skip header
        
        foreach ($line in $urlLines) {
            if ($line -match '^"([^"]+)","([^"]+)","([^"]+)","([^"]+)","([^"]+)"') {
                $threats += @{
                    url = $matches[2]
                    threat = $matches[3]
                    date = $matches[5]
                    source = "urlhaus"
                }
            }
        }
        Write-Host "Found $($urlLines.Count) URLs from URLhaus" -ForegroundColor Green
    }
    catch {
        Write-Host "URLhaus failed: $($_.Exception.Message)" -ForegroundColor Red
    }
    
    try {
        # Method 2: AlienVault OTX (sample public pulses)
        Write-Host "Fetching sample threats..." -ForegroundColor Gray
        
        # Add sample threats for demo
        $sampleThreats = @(
            @{ indicator = "malicious-domain.com"; type = "domain"; source = "sample"; confidence = "high" },
            @{ indicator = "192.168.1.100"; type = "ipv4"; source = "sample"; confidence = "medium" },
            @{ indicator = "http://evil.com/payload.exe"; type = "url"; source = "sample"; confidence = "high" },
            @{ indicator = "5d41402abc4b2a76b9719d911017c592"; type = "md5"; source = "sample"; confidence = "medium" },
            @{ indicator = "bad-site.net"; type = "domain"; source = "sample"; confidence = "high" }
        )
        
        $threats += $sampleThreats
        Write-Host "Added $($sampleThreats.Count) sample threats" -ForegroundColor Green
    }
    catch {
        Write-Host "Sample data failed: $($_.Exception.Message)" -ForegroundColor Red
    }
    
    return $threats
}

# Create data directory
if (!(Test-Path "data\raw")) {
    New-Item -ItemType Directory -Path "data\raw" -Force | Out-Null
}

# Collect data
$threats = Get-PublicThreats

if ($threats.Count -gt 0) {
    # Save raw data
    $threats | ConvertTo-Json -Depth 3 | Out-File "data\raw\threats-raw.json" -Encoding UTF8
    Write-Host "Collected $($threats.Count) total threats" -ForegroundColor Green
    Write-Host "Saved to: data\raw\threats-raw.json" -ForegroundColor Cyan
} else {
    Write-Host "No data collected" -ForegroundColor Red
}

return $threats