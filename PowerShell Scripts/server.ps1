Add-Type -AssemblyName System.Web

$listener = New-Object System.Net.HttpListener
$listener.Prefixes.Add("http://localhost:8080/")
$listener.Start()

Write-Host "Server running: http://localhost:8080/api/data" -ForegroundColor Green

while ($listener.IsListening) {
    $context = $listener.GetContext()
    $request = $context.Request
    $response = $context.Response
    
    if ($request.Url.LocalPath -eq "/api/data") {
        if (Test-Path "data\processed\threats.json") {
            $threats = Get-Content "data\processed\threats.json" | ConvertFrom-Json
            $json = @{
                total = $threats.Count
                sources = @{ urlhaus = $threats.Count }
                types = @{ url = ($threats | Where-Object type -eq "url").Count }
                threats = $threats | Select-Object -First 10
            } | ConvertTo-Json
        } else {
            $json = '{"error": "No data available"}'
        }
        
        $buffer = [System.Text.Encoding]::UTF8.GetBytes($json)
        $response.ContentType = "application/json"
        $response.OutputStream.Write($buffer, 0, $buffer.Length)
    }
    
    $response.Close()
}