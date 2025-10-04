# normalize.ps1 
Write-Host "Normalizing threat data..." -ForegroundColor Yellow

if (Test-Path "data\raw\threats-raw.json") {
    $rawData = Get-Content "data\raw\threats-raw.json" | ConvertFrom-Json
    $normalizedData = @()
    
    foreach ($item in $rawData) {
        # FIX: Use the 'threat' field as the indicator, not 'indicator'
        if ($item.threat) {
            $normalizedData += @{
                indicator = $item.threat  # THIS IS THE URL!
                type = "url"
                source = "urlhaus"
                first_seen = $item.first_seen
                confidence = $item.confidence
                description = "Malicious URL"
            }
        }
        elseif ($item.indicator -and $item.indicator -notmatch "^\d{4}-\d{2}-\d{2}") {
            # Only use indicator if it's not a date
            $normalizedData += @{
                indicator = $item.indicator
                type = $item.type
                source = $item.source
                first_seen = $item.first_seen
                confidence = $item.confidence
            }
        }
    }
    
    if (!(Test-Path "data\processed")) {
        New-Item -ItemType Directory -Path "data\processed" -Force | Out-Null
    }
    
    $normalizedData | ConvertTo-Json -Depth 3 | Out-File "data\processed\threats.json" -Encoding UTF8
    Write-Host "Normalized $($normalizedData.Count) indicators" -ForegroundColor Green
    
    # Show sample
    Write-Host "Sample threats:" -ForegroundColor Magenta
    $normalizedData | Select-Object -First 3 | ForEach-Object {
        Write-Host "  $($_.indicator)" -ForegroundColor Gray
    }
} else {
    Write-Host "No raw data found. Run collect.ps1 first." -ForegroundColor Red
}