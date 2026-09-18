<#
.SYNOPSIS
    Antigravity CLI helper script for PowerShell.
    Bridges skill registry management and workspace tools.
.EXAMPLE
    .\.agent\scripts\antigravity.ps1 skills search repository
    .\.agent\scripts\antigravity.ps1 skills add core/repository-analyzer
#>

param(
    [Parameter(Position=0)]
    [string]$Command,

    [Parameter(Position=1)]
    [string]$Subcommand,

    [Parameter(Position=2, ValueFromRemainingArguments=$true)]
    [string[]]$ArgsList
)

function Show-Help {
    Write-Host "Antigravity CLI Utility" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Usage:"
    Write-Host "  antigravity skills search <query>       Search the community skills vault"
    Write-Host "  antigravity skills add <skillName>      Install a skill to the workspace"
    Write-Host "  antigravity skills installed            List installed workspace skills"
    Write-Host "  antigravity skills analyze [path]       Run repository analysis on target"
    Write-Host ""
}

if (-not $Command) {
    Show-Help
    exit 0
}

if ($Command -eq "skills") {
    switch ($Subcommand) {
        "search" {
            $query = ($ArgsList -join " ")
            if (-not $query) {
                Write-Host "Please specify a search term." -ForegroundColor Yellow
                exit 1
            }
            Write-Host "Querying skills registry for: $query" -ForegroundColor Cyan
            npx -y @rmyndharis/antigravity-skills search $query
        }
        { $_ -in "add", "install" } {
            $targetSkill = $ArgsList[0]
            if (-not $targetSkill) {
                Write-Host "Please specify a skill name to add." -ForegroundColor Yellow
                exit 1
            }
            if ($targetSkill -in @("core/repository-analyzer", "repository-analyzer")) {
                Write-Host "Skill 'repository-analyzer' is actively configured in .agent/skills/repository-analyzer" -ForegroundColor Green
                exit 0
            }
            Write-Host "Installing $targetSkill from vault..." -ForegroundColor Cyan
            npx -y @rmyndharis/antigravity-skills install $targetSkill
        }
        "installed" {
            Write-Host "Checking installed workspace skills..." -ForegroundColor Cyan
            npx -y @rmyndharis/antigravity-skills installed
            if (Test-Path ".agent/skills/repository-analyzer") {
                Write-Host "  - repository-analyzer (workspace native)" -ForegroundColor Green
            }
        }
        "analyze" {
            $targetPath = if ($ArgsList.Count -gt 0) { $ArgsList[0] } else { "." }
            python ".agent/skills/repository-analyzer/scripts/analyze_repo.py" $targetPath
        }
        default {
            Show-Help
        }
    }
} else {
    Show-Help
}
