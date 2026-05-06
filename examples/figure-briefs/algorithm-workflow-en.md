# Algorithm Workflow Figure Brief (EN)

## Use Case
A methods section that needs a stepwise workflow figure.

## Figure Goal
Explain the full algorithm path, decision points, loopbacks, and outputs.

## Figure Type / Mode
- type: algorithm workflow
- mode: image
- language: en

## Required Stages
- input acquisition
- preprocessing or feature extraction
- model inference or optimization
- post-processing
- evaluation or final output

## Must-Keep Terms
- preserve standard variables and abbreviations
- preserve training/inference split when it exists

## Visual Constraints
- top-to-bottom or left-to-right flow
- short labels
- distinct main path
- readable at paper-column size

## Recommended Command
```powershell
python "$HOME/.codex/skills/engineering-figure-agent/scripts/generate_image.py" `
  --figure-template algorithm-workflow `
  --lang en `
  "[paste your method workflow background here]"
```
