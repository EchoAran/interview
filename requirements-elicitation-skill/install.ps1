param(
  [switch]$DryRun,
  [switch]$Uninstall
)

$ErrorActionPreference = "Stop"

$RootDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$SkillFile = Join-Path $RootDir "SKILL.md"
if (-not (Test-Path $SkillFile)) {
  throw "SKILL.md not found in $RootDir"
}

$SkillName = $null
Get-Content $SkillFile | ForEach-Object {
  if ($_ -match "^name:\s*(.+)$" -and -not $SkillName) {
    $SkillName = $Matches[1].Trim()
  }
}
if (-not $SkillName) {
  throw "Could not parse skill name from SKILL.md frontmatter."
}

function Invoke-Step {
  param([string]$Message, [scriptblock]$Action)
  if ($DryRun) {
    Write-Host "[dry-run] $Message"
  } else {
    & $Action
  }
}

function Install-LinkOrCopy {
  param([string]$Source, [string]$Destination)
  $Parent = Split-Path -Parent $Destination
  Invoke-Step "Ensure directory $Parent" { New-Item -ItemType Directory -Path $Parent -Force | Out-Null }
  Invoke-Step "Remove existing $Destination" {
    if (Test-Path $Destination) { Remove-Item -Recurse -Force $Destination }
  }
  if ($DryRun) {
    Write-Host "[dry-run] Create symlink $Destination -> $Source (fallback to copy)"
    return
  }
  try {
    New-Item -ItemType SymbolicLink -Path $Destination -Target $Source -Force | Out-Null
  } catch {
    Copy-Item -Recurse -Force $Source $Destination
  }
}

function Remove-PathSafe {
  param([string]$PathToRemove)
  Invoke-Step "Remove $PathToRemove" {
    if (Test-Path $PathToRemove) { Remove-Item -Recurse -Force $PathToRemove }
  }
}

$HomeDir = [Environment]::GetFolderPath("UserProfile")
$Destinations = @(
  (Join-Path $HomeDir ".claude\skills\$SkillName"),
  (Join-Path $HomeDir ".agents\skills\$SkillName"),
  (Join-Path $HomeDir ".codex\skills\$SkillName"),
  (Join-Path $HomeDir ".gemini\skills\$SkillName"),
  (Join-Path $HomeDir ".kiro\skills\$SkillName")
)

$CursorRulesDir = if ($env:CURSOR_RULES_DIR) { $env:CURSOR_RULES_DIR } else { Join-Path (Get-Location) ".cursor\rules" }
$WindsurfRulesDir = if ($env:WINDSURF_RULES_DIR) { $env:WINDSURF_RULES_DIR } else { Join-Path (Get-Location) ".windsurf\rules" }
$CursorRuleFile = Join-Path $CursorRulesDir "$SkillName.mdc"
$WindsurfRuleFile = Join-Path $WindsurfRulesDir "$SkillName.md"

if ($Uninstall) {
  Write-Host "Uninstalling skill '$SkillName'..."
  $Destinations | ForEach-Object { Remove-PathSafe $_ }
  Remove-PathSafe $CursorRuleFile
  Remove-PathSafe $WindsurfRuleFile
  Write-Host "Done."
  exit 0
}

Write-Host "Installing skill '$SkillName' from $RootDir"
$Destinations | ForEach-Object {
  Install-LinkOrCopy -Source $RootDir -Destination $_
  Write-Host "Installed: $_"
}

$CursorRule = @"
---
description: requirements elicitation workflow guidance
globs:
  - "**/*"
alwaysApply: false
---
# $SkillName

Use the `$SkillName` skill from:
`$RootDir`

When users ask for requirements clarification, follow the runtime loop defined in `SKILL.md` and related `references/` files.
"@

$WindsurfRule = @"
# $SkillName

Use the skill content at:
`$RootDir`

Trigger this rule for tasks about product requirements interviews, scope clarification, contradiction resolution, and requirements summarization.
"@

Invoke-Step "Write Cursor rule $CursorRuleFile" {
  New-Item -ItemType Directory -Path $CursorRulesDir -Force | Out-Null
  Set-Content -Path $CursorRuleFile -Value $CursorRule -Encoding UTF8
}

Invoke-Step "Write Windsurf rule $WindsurfRuleFile" {
  New-Item -ItemType Directory -Path $WindsurfRulesDir -Force | Out-Null
  Set-Content -Path $WindsurfRuleFile -Value $WindsurfRule -Encoding UTF8
}

Write-Host "Installed Cursor adapter: $CursorRuleFile"
Write-Host "Installed Windsurf adapter: $WindsurfRuleFile"
Write-Host "Done."
