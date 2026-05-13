param(
    [string]$SecretsDir = "$HOME/.codex/secrets",
    [string]$SkillDir = "$HOME/.codex/skills/engineering-figure-agent"
)

$ErrorActionPreference = "Continue"

function Write-Status($status, $message) {
    switch ($status) {
        "PASS" { Write-Host "[PASS] $message" -ForegroundColor Green }
        "WARN" { Write-Host "[WARN] $message" -ForegroundColor Yellow }
        "FAIL" { Write-Host "[FAIL] $message" -ForegroundColor Red }
        default { Write-Host "[$status] $message" }
    }
}

function Write-NextStep($message) {
    Write-Host "       Next: $message" -ForegroundColor Cyan
}

function Add-Result($status, $message, $nextStep) {
    $script:results += [pscustomobject]@{ Status = $status; Message = $message; NextStep = $nextStep }
    Write-Status $status $message
    if ($nextStep) {
        Write-NextStep $nextStep
    }
}

$results = @()
$failed = $false
$warned = $false
$readyForPromptOnly = $false

Write-Host "Engineering Figure Agent setup check"
Write-Host "SkillDir   : $SkillDir"
Write-Host "SecretsDir : $SecretsDir"
Write-Host ""

if (Get-Command python -ErrorAction SilentlyContinue) {
    $pythonVersion = python --version 2>&1
    Add-Result "PASS" "Python detected: $pythonVersion" $null
} else {
    Add-Result "FAIL" "Python not found in PATH" "Install Python 3.10+ and reopen PowerShell so the `python` command is available."
    $failed = $true
}

if (Test-Path $SkillDir) {
    Add-Result "PASS" "Skill directory exists" $null
} else {
    Add-Result "FAIL" "Skill directory missing: $SkillDir" "Run `& `"$HOME/.codex/skills/engineering-figure-agent/scripts/install_and_test.ps1`"` from the repo root or copy this skill into `$HOME/.codex/skills/engineering-figure-agent`."
    $failed = $true
}

$requiredFiles = @(
    "SKILL.md",
    "agents/openai.yaml",
    "scripts/generate_image.py",
    "scripts/load_nanobanana_env.ps1",
    "assets/prompt-templates/engineering-figure-templates.json"
)

foreach ($rel in $requiredFiles) {
    $path = Join-Path $SkillDir $rel
    if (Test-Path $path) {
        Add-Result "PASS" "Found $rel" $null
    } else {
        Add-Result "FAIL" "Missing $rel" "Reinstall or re-copy the skill so all required files exist under `$HOME/.codex/skills/engineering-figure-agent`."
        $failed = $true
    }
}

$envFile = Join-Path $SecretsDir "nanobanana.env"
$keyFile = Join-Path $SecretsDir "nanobanana_api_key.txt"
$openaiKeyFile = Join-Path $SecretsDir "openai_api_key.txt"
$envMap = @{}

if (Test-Path $envFile) {
    Add-Result "PASS" "Found nanobanana.env" $null
    Get-Content -Path $envFile | ForEach-Object {
        $line = $_.Trim()
        if (-not $line -or $line.StartsWith("#")) { return }
        $parts = $line -split "=", 2
        if ($parts.Count -eq 2) {
            $envMap[$parts[0].Trim()] = $parts[1].Trim()
        }
    }

    foreach ($name in @("NANOBANANA_BASE_URL", "NANOBANANA_DEFAULT_MODEL", "NANOBANANA_AUTH_MODE")) {
        if ($envMap.ContainsKey($name) -and $envMap[$name]) {
            Add-Result "PASS" "$name is set" $null
        } else {
            Add-Result "WARN" "$name is not set in nanobanana.env" "Edit $envFile and add `$name=...`, then rerun this setup check."
            $warned = $true
        }
    }

    if ($envMap.ContainsKey("NANOBANANA_BASE_URL") -and $envMap["NANOBANANA_BASE_URL"]) {
        $baseUrl = $envMap["NANOBANANA_BASE_URL"]
        if ($baseUrl -eq "https://generativelanguage.googleapis.com") {
            Add-Result "PASS" "Official Google endpoint configured" $null
        } else {
            Add-Result "WARN" "Third-party or custom endpoint configured: $baseUrl" "Keep using this only if you trust the provider and make sure the provider's model names and auth mode are correct."
            $warned = $true
            if (($envMap["NANOBANANA_ALLOW_THIRD_PARTY"] -ne "1")) {
                Add-Result "WARN" "NANOBANANA_ALLOW_THIRD_PARTY is not set to 1" "If you intentionally use a relay, add `NANOBANANA_ALLOW_THIRD_PARTY=1` to $envFile or pass `--allow-third-party` when generating."
                $warned = $true
            }
        }
    }

    if (-not ($envMap.ContainsKey("NANOBANANA_HIGHRES_MODEL") -and $envMap["NANOBANANA_HIGHRES_MODEL"])) {
        Add-Result "WARN" "NANOBANANA_HIGHRES_MODEL is not configured" "Routine generation can still work, but `pro-2k` or final-export requests will stop instead of silently downgrading. Add the provider's high-res model name if you want that path available."
        $warned = $true
    } else {
        Add-Result "PASS" "NANOBANANA_HIGHRES_MODEL is set" $null
    }
}
else {
    Add-Result "FAIL" "Missing nanobanana.env: $envFile" "Copy `secrets/nanobanana.env.example` to $envFile, fill in your provider values, then rerun this setup check."
    $failed = $true
}

if (Test-Path $keyFile) {
    $key = (Get-Content -Raw -Path $keyFile).Trim()
    if (-not $key) {
        Add-Result "FAIL" "nanobanana_api_key.txt is empty" "Paste your real API key into $keyFile. Do not keep it blank."
        $failed = $true
    } elseif ($key -eq "REPLACE_WITH_YOUR_CURRENT_VALID_NANOBANANA_API_KEY") {
        Add-Result "FAIL" "nanobanana_api_key.txt still contains the placeholder value" "Replace the placeholder in $keyFile with your current valid API key."
        $failed = $true
    } else {
        Add-Result "PASS" "Found non-placeholder API key file" $null
    }
} else {
    Add-Result "FAIL" "Missing nanobanana_api_key.txt: $keyFile" "Copy `secrets/nanobanana_api_key.txt.example` to $keyFile and paste your real API key into it."
    $failed = $true
}

if (($envMap["ENGINEERING_FIGURE_IMAGE_PROVIDER"] -eq "openai") -or $envMap.ContainsKey("OPENAI_IMAGE_MODEL") -or (Test-Path $openaiKeyFile)) {
    if ($envMap.ContainsKey("OPENAI_IMAGE_MODEL") -and $envMap["OPENAI_IMAGE_MODEL"]) {
        Add-Result "PASS" "OPENAI_IMAGE_MODEL is set" $null
    } else {
        Add-Result "WARN" "OPENAI_IMAGE_MODEL is not set" "Add `OPENAI_IMAGE_MODEL=gpt-image-1.5` to $envFile or pass `--model` when using `--provider openai`."
        $warned = $true
    }

    $configuredOpenAIKeyFile = $envMap["OPENAI_API_KEY_FILE"]
    if (-not $configuredOpenAIKeyFile) { $configuredOpenAIKeyFile = $openaiKeyFile }
    if (Test-Path $configuredOpenAIKeyFile) {
        $openaiKey = (Get-Content -Raw -Path $configuredOpenAIKeyFile).Trim()
        if (-not $openaiKey -or $openaiKey -eq "REPLACE_WITH_YOUR_CURRENT_VALID_OPENAI_API_KEY") {
            Add-Result "WARN" "OpenAI API key file is missing a real key" "Paste your real OpenAI API key into $configuredOpenAIKeyFile before using `--provider openai`."
            $warned = $true
        } else {
            Add-Result "PASS" "Found non-placeholder OpenAI API key file" $null
        }
    } else {
        Add-Result "WARN" "OpenAI key file not found: $configuredOpenAIKeyFile" "Create this file only if you want to use `--provider openai`; Gemini/Banana generation is unaffected."
        $warned = $true
    }
}

if ($env:NANOBANANA_BASE_URL) {
    Add-Result "PASS" "Current shell already has NANOBANANA_* values loaded" $null
} else {
    Add-Result "WARN" "Current shell does not appear to have NANOBANANA_* values loaded yet" "Run `. `"$HOME/.codex/skills/engineering-figure-agent/scripts/load_nanobanana_env.ps1`"` in this PowerShell session before generating."
    $warned = $true
    $readyForPromptOnly = $true
}

Write-Host ""
Write-Host "Readiness summary" -ForegroundColor Cyan
if ($failed) {
    Write-Host "Blocked until fixed" -ForegroundColor Red
    Write-Host "Fix the FAIL items above first, then rerun:`n  & `"$HOME/.codex/skills/engineering-figure-agent/scripts/check_setup.ps1`"" -ForegroundColor Cyan
    exit 1
}

if ($warned -and $readyForPromptOnly) {
    Write-Host "Ready for prompt-only testing" -ForegroundColor Yellow
    Write-Host "Next recommended commands:" -ForegroundColor Cyan
    Write-Host "  . `"$HOME/.codex/skills/engineering-figure-agent/scripts/load_nanobanana_env.ps1`""
    Write-Host "  & `"$HOME/.codex/skills/engineering-figure-agent/scripts/wizard.ps1`""
    exit 0
}

if ($warned) {
    Write-Host "Ready for minimal generation, but review the WARN items above" -ForegroundColor Yellow
    Write-Host "Next recommended commands:" -ForegroundColor Cyan
    Write-Host "  & `"$HOME/.codex/skills/engineering-figure-agent/scripts/wizard.ps1`""
    Write-Host "  or run the minimal command from README.md"
    exit 0
}

Write-Host "Ready for minimal generation" -ForegroundColor Green
Write-Host "Next recommended commands:" -ForegroundColor Cyan
Write-Host "  & `"$HOME/.codex/skills/engineering-figure-agent/scripts/wizard.ps1`""
Write-Host "  or run the minimal command from README.md"
exit 0
