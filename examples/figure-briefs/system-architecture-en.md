# System Architecture Figure Brief (EN)

## Use Case
A method or platform paper that needs a top-level architecture diagram.

## Figure Goal
Show the complete module hierarchy and the main data flow from input to final output.

## Figure Type / Mode
- type: system architecture
- mode: image
- language: en

## Core Modules
- input or acquisition layer
- preprocessing
- retrieval or memory module
- model or inference core
- controller or orchestration
- output and feedback

## Must-Keep Terms
- keep standard English abbreviations
- keep model names exactly as written in the paper
- keep variables or protocol names if they matter to the diagram

## Visual Constraints
- white background
- publication-style spacing
- concise labels
- clear arrows and reading order
- avoid decorative gradients

## Recommended Command
```powershell
python "$HOME/.codex/skills/engineering-figure-agent/scripts/generate_image.py" `
  --figure-template system-architecture `
  --lang en `
  "[paste your technical background here]"
```
