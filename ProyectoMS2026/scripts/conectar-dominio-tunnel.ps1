# Conecta https://techstor-pro.vercel.app al backend local (gateway :7091) vía Cloudflare Tunnel.
# Requisitos: stack local levantado (levantar-todo-dev.ps1) y Vercel CLI autenticado.
#
# Uso: .\scripts\conectar-dominio-tunnel.ps1

$ErrorActionPreference = "Stop"
$root = Split-Path $PSScriptRoot -Parent
$repoRoot = Split-Path $root -Parent
$cfDir = "$env:TEMP\cloudflared"
$cfExe = Join-Path $cfDir "cloudflared.exe"
$logFile = Join-Path $cfDir "tunnel.log"

function Test-GatewayLocal {
    try {
        $h = Invoke-RestMethod -Uri "http://localhost:7091/actuator/health" -TimeoutSec 5
        return $h.status -eq "UP"
    } catch { return $false }
}

Write-Host ""
Write-Host "=== Conectar dominio Vercel al backend local ===" -ForegroundColor Cyan

if (-not (Test-GatewayLocal)) {
    Write-Host "Gateway local no responde. Ejecuta primero:" -ForegroundColor Red
    Write-Host "  .\scripts\levantar-todo-dev.ps1"
    exit 1
}

if (-not (Test-Path $cfExe)) {
    New-Item -ItemType Directory -Path $cfDir -Force | Out-Null
    Write-Host "Descargando cloudflared..."
    Invoke-WebRequest -Uri "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe" -OutFile $cfExe
}

# Detener tunel anterior si existe
Get-CimInstance Win32_Process -Filter "Name='cloudflared.exe'" -ErrorAction SilentlyContinue |
    Where-Object { $_.CommandLine -like "*localhost:7091*" } |
    ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }

Remove-Item $logFile -ErrorAction SilentlyContinue
Start-Process -FilePath $cfExe -ArgumentList @("tunnel", "--url", "http://localhost:7091", "--no-autoupdate") -RedirectStandardOutput $logFile -RedirectStandardError $logFile -WindowStyle Hidden | Out-Null

$tunnelUrl = $null
$deadline = (Get-Date).AddSeconds(45)
while ((Get-Date) -lt $deadline) {
    if (Test-Path $logFile) {
        $match = Select-String -Path $logFile -Pattern "https://[a-z0-9-]+\.trycloudflare\.com" | Select-Object -First 1
        if ($match) {
            $tunnelUrl = $match.Matches[0].Value
            break
        }
    }
    Start-Sleep -Seconds 2
}

if (-not $tunnelUrl) {
    Write-Host "No se pudo obtener la URL del tunel. Revisa $logFile" -ForegroundColor Red
    exit 1
}

Write-Host "Tunel activo: $tunnelUrl" -ForegroundColor Green

try {
    $health = Invoke-RestMethod -Uri "$tunnelUrl/actuator/health" -TimeoutSec 20
    if ($health.status -ne "UP") { throw "Gateway no UP" }
} catch {
    Write-Host "El tunel no alcanza el gateway: $_" -ForegroundColor Red
    exit 1
}

Push-Location $repoRoot
try {
    $tunnelUrl | npx vercel env add API_URL production --force --yes 2>&1 | Out-Null
    npx vercel deploy --prod --yes 2>&1 | Out-Null
    Write-Host "Vercel actualizado (API_URL + redeploy)" -ForegroundColor Green
} finally {
    Pop-Location
}

Write-Host ""
Write-Host "Listo: https://techstor-pro.vercel.app" -ForegroundColor Cyan
Write-Host "Mantén este PC encendido con el stack local y el tunel activos."
Write-Host "Para backend 24/7 en la nube: agrega tarjeta en Render y aplica render.yaml"
Write-Host ""
