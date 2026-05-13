param(
    [string]$SourceDir = (Split-Path -Parent $PSScriptRoot),
    [string]$CodexHome = "$HOME/.codex"
)

$ErrorActionPreference = "Stop"

$skillsDir = Join-Path $CodexHome "skills"
$secretsDir = Join-Path $CodexHome "secrets"
$targetSkillDir = Join-Path $skillsDir "engineering-figure-agent"
$envTemplate = Join-Path $SourceDir "secrets/nanobanana.env.example"
$keyTemplate = Join-Path $SourceDir "secrets/nanobanana_api_key.txt.example"
$envTarget = Join-Path $secretsDir "nanobanana.env"
$keyTarget = Join-Path $secretsDir "nanobanana_api_key.txt"
$syncScript = Join-Path $SourceDir "scripts/sync_codex_skill.py"

Write-Host "Installing Engineering Figure Agent"
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

$sourceResolved = (Resolve-Path -LiteralPath $SourceDir).Path
$targetResolved = $null
if (Test-Path $targetSkillDir) {
    $targetResolved = (Resolve-Path -LiteralPath $targetSkillDir).Path
}

if ($targetResolved -and $sourceResolved -eq $targetResolved) {
    Write-Host "Source is already the installed runtime directory. Skipping file sync." -ForegroundColor Yellow
} elseif ((Get-Command python -ErrorAction SilentlyContinue) -and (Test-Path $syncScript)) {
    & python $syncScript --target $targetSkillDir
    if ($LASTEXITCODE -ne 0) {
        throw "Runtime sync failed."
    }
} else {
    New-Item -ItemType Directory -Force -Path $targetSkillDir | Out-Null
    Get-ChildItem -Force -LiteralPath $SourceDir | ForEach-Object {
        Copy-Item -LiteralPath $_.FullName -Destination $targetSkillDir -Recurse -Force
    }
}

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

Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Edit $envTarget"
Write-Host "2. Put your real API key into $keyTarget"
Write-Host "3. Run:"
Write-Host "   . `"$targetSkillDir\\scripts\\load_nanobanana_env.ps1`""
Write-Host "4. Verify setup:"
Write-Host "   & `"$targetSkillDir\\scripts\\check_setup.ps1`""
Write-Host "5. Open a new Codex session or restart Codex if needed"
Write-Host ""
Write-Host "The runtime install is pruned on purpose, so docs/examples/tests are left in the repo instead of the Codex skill folder." -ForegroundColor Yellow
