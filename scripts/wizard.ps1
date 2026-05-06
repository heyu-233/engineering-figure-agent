param(
    [string]$SkillDir = "$HOME/.codex/skills/engineering-figure-agent",
    [string]$DefaultOutDir = "./output/engineering-figure"
)

$ErrorActionPreference = "Stop"

function Ask-Choice($title, $options, $defaultIndex) {
    Write-Host ""
    Write-Host $title -ForegroundColor Cyan
    for ($i = 0; $i -lt $options.Count; $i++) {
        Write-Host ("[{0}] {1}" -f ($i + 1), $options[$i])
    }
    $raw = Read-Host ("Select 1-{0} (default {1})" -f $options.Count, ($defaultIndex + 1))
    if (-not $raw) { return $defaultIndex }
    $parsed = 0
    if (-not [int]::TryParse($raw, [ref]$parsed)) {
        return $defaultIndex
    }
    $value = $parsed - 1
    if ($value -lt 0 -or $value -ge $options.Count) { return $defaultIndex }
    return $value
}

function Read-MultilineInput($prompt) {
    Write-Host ""
    Write-Host $prompt -ForegroundColor Cyan
    Write-Host "Finish with a single line containing only END"
    $lines = @()
    while ($true) {
        $line = Read-Host
        if ($line -eq 'END') { break }
        $lines += $line
    }
    return ($lines -join "`n").Trim()
}

$mode = @("image", "plot")[(Ask-Choice "Select workflow mode" @("image - conceptual figure or schematic", "plot - exact quantitative figure") 0)]
$lang = @("en", "zh")[(Ask-Choice "Select figure language" @("English", "Chinese") 0)]
$highres = (Ask-Choice "Request high-resolution output?" @("No - normal routine generation", "Yes - high-res / final-export") 0) -eq 1

if ($highres) {
    Write-Host ""
    Write-Host "High-res reminder: if this path fails, the workflow should stop and ask for human confirmation. It must not silently downgrade." -ForegroundColor Yellow
}

if ($mode -eq "image") {
    $provider = @("gemini", "openai")[(Ask-Choice "Select image provider" @("gemini - Google Gemini / Banana-compatible", "openai - OpenAI Image API") 0)]
    $templateOptions = @("system-architecture", "algorithm-workflow", "graphical-abstract", "electronic-schematic")
    $template = $templateOptions[(Ask-Choice "Select engineering figure template" $templateOptions 0)]
    $inputSource = @("direct", "file")[(Ask-Choice "Background source" @("Paste technical background directly", "Read from a text or markdown file") 0)]

    $promptArg = ""
    $extraArgs = @("--provider $provider", "--figure-template $template", "--lang $lang", "--out-dir `"$DefaultOutDir`"")

    if ($highres) {
        $extraArgs += "--highres"
    }

    if ($inputSource -eq "file") {
        $filePath = Read-Host "Enter the background file path"
        $extraArgs += "--prompt-file `"$filePath`""
    } else {
        $background = Read-MultilineInput "Paste the technical background for the figure"
        $escaped = $background.Replace('"', '`"')
        $promptArg = "`"$escaped`""
    }

    $styleNote = Read-Host "Optional style note (press Enter to skip)"
    if ($styleNote) {
        $extraArgs += "--style-note `"$($styleNote.Replace('"', '`"'))`""
    }

    $command = "python `"$SkillDir\scripts\generate_image.py`" {0} {1}" -f ($extraArgs -join " "), $promptArg
} else {
    $requestSource = @("file", "draft")[(Ask-Choice "Plot input source" @("Use an existing concise request JSON file", "Show me the starter workflow only") 0)]
    if ($requestSource -eq "file") {
        $requestFile = Read-Host "Enter the concise request JSON path"
        $specOut = Read-Host "Output full spec path (default: ./output/plot-spec.json)"
        if (-not $specOut) { $specOut = "./output/plot-spec.json" }
        $figureOut = Read-Host "Output figure prefix (default: ./output/publication-figure)"
        if (-not $figureOut) { $figureOut = "./output/publication-figure" }
        $command = @(
            "python `"$SkillDir\scripts\build_plot_spec.py`" `"$requestFile`" --out `"$specOut`"",
            "python `"$SkillDir\scripts\plot_publication_figure.py`" `"$specOut`" --out-path `"$figureOut`" --formats png pdf svg"
        ) -join "`n"
    } else {
        $command = @(
            "1. Create or copy a concise request JSON from examples/figure-briefs/benchmark-plot-request.md",
            "2. Run:",
            "python `"$SkillDir\scripts\build_plot_spec.py`" `"./your-request.json`" --out `"./output/plot-spec.json`"",
            "python `"$SkillDir\scripts\plot_publication_figure.py`" `"./output/plot-spec.json`" --out-path `"./output/publication-figure`" --formats png pdf svg"
        ) -join "`n"
    }
}

Write-Host ""
Write-Host "Recommended command / workflow" -ForegroundColor Green
Write-Host $command

$execute = (Ask-Choice "Do you want to execute it now?" @("No - just show the command", "Yes - execute in this shell") 0) -eq 1
if ($execute) {
    Write-Host ""
    Write-Host "Running..." -ForegroundColor Cyan
    Invoke-Expression $command
} else {
    Write-Host ""
    Write-Host "No command executed. Copy the command above after loading env with load_nanobanana_env.ps1 if needed." -ForegroundColor Yellow
}
