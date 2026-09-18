---
name: repository-analyzer
description: >-
  Analyze repository structure, detect frameworks, evaluate dependency trees,
  measure code density, and inspect architecture. Use this skill when asked to
  analyze, audit, inspect, or summarize a repository or codebase.
---

# Repository Analyzer

This skill provides autonomous reconnaissance and holistic static analysis of a software repository. It assesses directory topology, identifies language distributions, inspects dependency manifests, detects build and configuration workflows, and extracts architectural boundaries.

## When to Use

Use this skill whenever:
- Onboarding to an unfamiliar repository or codebase.
- Reviewing high-level project architecture, code density, or language splits.
- Auditing dependencies and runtime configurations.
- Preparing for major refactoring or migration.

---

## Analysis Workflow

### 1. Automated Topological Reconnaissance

Run the built-in analysis script from the repository root:

```powershell
python .agent/skills/repository-analyzer/scripts/analyze_repo.py
```

For programmatic agent consumption, emit raw JSON:

```powershell
python .agent/skills/repository-analyzer/scripts/analyze_repo.py --json
```

This captures:
- Total file count, line counts, and cumulative size in megabytes.
- Language distribution and file extension breakdown.
- Detection of ecosystem manifests (`package.json`, `pyproject.toml`, `requirements.txt`, `Cargo.toml`, etc.).
- Heavy binary assets (>10MB) requiring special attention.

### 2. Dependency & Configuration Inspection

Inspect the identified manifests:
- **Node.js**: Check `dependencies` vs. `devDependencies`, build scripts in `package.json`.
- **Python**: Check dependencies and packaging tools in `pyproject.toml` or `requirements.txt`.
- **Docker / CI**: Examine `Dockerfile`, `docker-compose.yml`, and `.github/workflows` to understand containerization and deployment pipelines.

### 3. Architecture & Entrypoint Mapping

Trace primary execution flows:
1. Locate main entrypoints (`main.py`, `index.ts`, `app.py`, `src/`).
2. Map module boundaries, shared libraries, and utility directories.
3. Identify external interfaces: REST endpoints, CLI parsers, GraphQL schemas, or MCP tool servers.

### 4. Quality, Verification & Documentation Assessment

1. Check for automated test suites (`tests/`, `__tests__/`, `pytest.ini`).
2. Review existing project documentation (`README.md`, `documentation.md`, architecture diagrams).
3. Identify technical debt, dead code, or outdated dependencies.

### 5. Architectural Synthesis

Synthesize findings using the C4 model or structured Markdown summary:
- **Context**: What business problem does this repository solve?
- **Containers/Services**: What runtimes, daemons, or background workers exist?
- **Components**: What are the core modules and how do they interact?
- **Recommendations**: Immediate risks, missing tests, or architectural improvements.
