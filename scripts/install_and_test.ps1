param(
    [string]$SourceDir = (Split-Path -Parent $PSScriptRoot),
    [string]$CodexHome = "$HOME/.codex",
    [switch]$RunSetupCheck
)

$ErrorActionPreference = "Stop"

$skillsDir = Join-Path $CodexHome "skills"
$secretsDir = Join-Path $CodexHome "secrets"
$targetSkillDir = Join-Path $skillsDir "engineering-figure-agent"
$envTemplate = Join-Path $SourceDir "secrets/nanobanana.env.example"
$keyTemplate = Join-Path $SourceDir "secrets/nanobanana_api_key.txt.example"
$openaiKeyTemplate = Join-Path $SourceDir "secrets/openai_api_key.txt.example"
$envTarget = Join-Path $secretsDir "nanobanana.env"
$keyTarget = Join-Path $secretsDir "nanobanana_api_key.txt"
$openaiKeyTarget = Join-Path $secretsDir "openai_api_key.txt"
$checkScript = Join-Path $targetSkillDir "scripts/check_setup.ps1"

Write-Host "Installing Engineering Figure Agent" -ForegroundColor Cyan
Write-Host "Source      : $SourceDir"
Write-Host "Target skill: $targetSkillDir"
Write-Host "Secrets dir : $secretsDir"
Write-Host ""

New-Item -ItemType Directory -Force -Path $skillsDir | Out-Null
New-Item -ItemType Directory -Force -Path $secretsDir | Out-Null

if (Test-Path $targetSkillDir) {
    Write-Host "Skill already exists. Updating files..." -ForegroundColor Yellow
} else {
    Write-Host "Skill not found. Creating target directory..." -ForegroundColor Green
}

Copy-Item -Path $SourceDir -Destination $targetSkillDir -Recurse -Force

if (-not (Test-Path $envTarget) -and (Test-Path $envTemplate)) {
    Copy-Item -Path $envTemplate -Destination $envTarget
    Write-Host "Created nanobanana.env from template" -ForegroundColor Green
} else {
    Write-Host "Kept existing nanobanana.env" -ForegroundColor Yellow
}

if (-not (Test-Path $keyTarget) -and (Test-Path $keyTemplate)) {
    Copy-Item -Path $keyTemplate -Destination $keyTarget
    Write-Host "Created nanobanana_api_key.txt from template" -ForegroundColor Green
} else {
    Write-Host "Kept existing nanobanana_api_key.txt" -ForegroundColor Yellow
}

if (-not (Test-Path $openaiKeyTarget) -and (Test-Path $openaiKeyTemplate)) {
    Copy-Item -Path $openaiKeyTemplate -Destination $openaiKeyTarget
    Write-Host "Created openai_api_key.txt from template" -ForegroundColor Green
} else {
    Write-Host "Kept existing openai_api_key.txt" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Edit $envTarget"
Write-Host "2. Put your real API key into $keyTarget"
Write-Host "   Optional OpenAI key file: $openaiKeyTarget"
Write-Host "3. Load env in the same shell:"
Write-Host "   . `"$targetSkillDir\scripts\load_nanobanana_env.ps1`""
Write-Host "4. Open the interactive wizard or run the minimal README command:"
Write-Host "   & `"$targetSkillDir\scripts\wizard.ps1`""
Write-Host ""
Write-Host "This installer does not automatically call the live image API, so it will not burn tokens by surprise." -ForegroundColor Yellow

if ($RunSetupCheck) {
    Write-Host ""
    Write-Host "Running setup check..." -ForegroundColor Cyan
    & $checkScript -SecretsDir $secretsDir -SkillDir $targetSkillDir
}
