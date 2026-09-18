# Technical Documentation: Video Editing Architecture & Specifications

## 1. System Overview

This system provides a programmatic, guardrailed media editing interface for local autonomous agents and developers. It unifies low-level multimedia processing tools (FFmpeg) with structured schema validation, programmatic composition engines (Hyperframes), and agent-oriented verification primitives (storyboard grids, frame inspection, quality checkpoints).

---

## 2. Core Architecture & Components

```text
+-------------------------------------------------------------------------+
|                              Agent Host                                 |
|         (Natural language instructions, multi-step pipeline plans)      |
+------------------------------------+------------------------------------+
                                     |
                                     v
+------------------------------------+------------------------------------+
|                         MCP Video Server Layer                          |
|  - Parameter validation and bounding guardrails                         |
|  - Aspect ratio and merge compatibility preflight                       |
|  - Loudness and audio timing analysis                                   |
+-------------------+--------------------------------+--------------------+
                    |                                |
                    v                                v
+-------------------+--------------+   +-------------+--------------------+
|           FFmpeg Engine          |   |       Hyperframes Engine         |
|  - Stream demuxing and decoding  |   |  - Programmatic DOM/CSS motion   |
|  - Audio/video filter graphs     |   |  - Dynamic canvas rendering      |
|  - Codec transcoding & remuxing  |   |  - Web-based animation compositing|
+-------------------+--------------+   +-------------+--------------------+
                    |                                |
                    +----------------+---------------+
                                     |
                                     v
+------------------------------------+------------------------------------+
|                     Verification & Output Artifacts                     |
|  - Output media streams (.mp4, .mov, .wav)                              |
|  - Storyboard matrices & frame captures (.png, .jpg)                    |
|  - Quality verification manifests (.json)                               |
+-------------------------------------------------------------------------+
```

### 2.1 Guardrail Layer
Direct execution of raw media commands frequently suffers from failure modes such as silent frame drops, audio/video desync, aspect ratio distortion, and volume clipping. The guardrail layer evaluates transformations prior to execution:
- **Spatial Boundaries**: Confirms crop parameters and aspect ratios match target platform conventions without anamorphic stretching.
- **Audio Headroom**: Pre-checks audio gain modifications and normalizes to standard target loudness (-14 to -16 LUFS integrated).
- **Text & Overlay Safe Zones**: Verifies subtitle positioning and title overlays respect safe-title margins for mobile vertical viewing (avoiding interface button zones on platforms like TikTok and Instagram Reels).

### 2.2 Verification Primitives
Autonomous execution requires intermediate feedback mechanisms to prevent cascading errors across multi-step pipelines:
- **Frame Sampler**: Extracts single frames at designated fractional timestamps (start, quarter, midpoint, end).
- **Storyboard Matrix**: Assembles an N x M contact sheet to enable rapid visual confirmation of scene transitions, color balance, and text placement.
- **Quality Checkpoint**: Emits a machine-readable JSON receipt containing stream metadata, bitrates, audio loudness profiles, and file integrity flags.

---

## 3. Storage & Project Isolation Standard

To maintain determinism and avoid collision across editing sessions, the workspace mandates isolated sub-directories per project:

```text
<workspace_root>/
└── projects/
    └── <project_identifier>/
        ├── raw/              # Immutable source assets
        ├── previews/         # Visual contact sheets and inspectable frames
        ├── intermediate/     # Transitory processing files (transcriptions, stems)
        ├── output/           # Validated target deliverables
        └── metadata/         # Receipts, quality logs, and subtitle files
```

---

## 4. Integration Interfaces

The workspace supports three primary invocation paradigms:
1. **MCP Tool RPC**: Model Context Protocol integration exposing high-level operations (`trim`, `resize`, `normalize_audio`, `add_text`, `release_checkpoint`) over stdio.
2. **Python Client API**: Synchronous Python module interface for scripting batch transformations or complex pipelines.
3. **Command Line Interface (CLI)**: Direct terminal execution for rapid manual inspection and isolated operations.

---

## 5. System Deployment & Setup Verification

### 5.1 Verified Runtimes and Engines
- **FFmpeg / FFprobe**: Gyan FFmpeg 8.1.2 Full Build (`libx264`, `libx265`, `libdav1d`, `aac`, EBU R128 `loudnorm` filter).
- **Python Runtime**: Python 3.12.10 (x86_64).
- **Core Video Suite**: `mcp-video` v1.6.12 and `kinocut` v1.15.1.
- **Supporting Media Libraries**: OpenCV (`opencv-python`), Pillow, Pydantic, and Rich.

### 5.2 Active Directory Scaffolding
The standard project structure has been initialized under `projects/default/`:
- `projects/default/raw/`: Dedicated incoming storage for raw source assets.
- `projects/default/previews/`: Destination for contact sheets and frame grabs.
- `projects/default/intermediate/`: Working area for isolated audio stems, proxy cuts, and temporary files.
- `projects/default/output/`: Master delivery destination for exported renders.
- `projects/default/metadata/`: Log destination for receipts, SRT subtitle files, and quality checkpoints.

---

## 6. Repository Analysis & Skills Architecture

### 6.1 Antigravity Customization Architecture
Agent skills provide reusable, progressive-disclosure runbooks for the autonomous development workflow:
- **Workspace Discovery**: Skills are discovered automatically from `.agent/skills/<skill-name>/SKILL.md` (or `.agents/`).
- **Community Registry**: Packages from the Antigravity community vault (`@rmyndharis/antigravity-skills`) are queryable and installable directly into the workspace skill hierarchy.
- **Progressive Context Disclosure**: Only skill names and trigger descriptions are loaded initially; full procedures are read on-demand to protect context window efficiency.

### 6.2 Repository Analyzer Engine
The workspace provides a dedicated static repository analysis tool (`.agent/skills/repository-analyzer/scripts/analyze_repo.py`):
- **Topology & Language Profiling**: Recursively traverses file trees, ignores dependency caches (`node_modules`, `venv`), and computes line counts, file distributions, and storage density.
- **Manifest Detection**: Automatically detects language runtimes, package definitions (`pyproject.toml`, `package.json`, `Cargo.toml`), and container configurations.
- **Remote Inspection Workflow**: Supports zero-clone remote repository audits via git tree APIs, examining upstream architectures, ADRs, and module graphs without polluting the local filesystem.

---

## 7. Video Editing Skill & MCP Server Integration

### 7.1 MCP Server Registration
- **Config Path**: `.agents/mcp_config.json` (mirrored in `.agent/mcp_config.json`).
- **Engine**: `mcp-video` stdio server exposing programmatic media editing tools.

### 7.2 Workspace Skill Specification
- **Skill Path**: `.agents/skills/mcp-video/SKILL.md` (mirrored in `.agent/skills/mcp-video/SKILL.md`).
- **Scope**: Interprets natural English video editing directives and translates them into deterministically bounded operations (`trim`, `resize`, `normalize-audio`, `storyboard`, `subtitles`, `mix`).
- **Preflight & Verification**: Enforces visual inspection grids and audio compliance before final asset release.

### 7.3 Upstream Repository Synchronization
- **Source**: `https://github.com/mfortne/mcp-video-editing`
- **Installed Assets**:
  - `skills/mcp-video/SKILL.md`: Authoritative workflow contract and CLI/MCP mapping.
  - `skills/mcp-video/agents/openai.yaml`: Agent invocation policy and interface definition.

---

## 8. Backup & Version Control Lineage

### 8.1 Primary Vault Integration
- **Remote Endpoint**: `https://github.com/ederaefe/Video-MCP.git`
- **Active Branch**: `main` (tracking `origin/main`).
- **Backup Policy**: Weekly progress commits capturing updated skills, scaffolding configurations, pipeline scripts, documentation, and metadata receipts.
- **Exclusion Filters**: Defined in `.gitignore` to prevent committing transitory processing files, local virtual environments, OS metadata, and intermediate rendering scratchpads.

---

## 9. VEDIT Subsystem Integration & Dual-Track Backup Lineage

### 9.1 Architectural Role
`vedit` serves as the non-linear timeline editor and deterministic composition backend within the Video-MCP ecosystem. Unlike purely prompt-driven video toolsets, VEDIT maintains a strictly typed JSON state model compiled into single-pass FFmpeg filtergraphs with transactional undo/redo and an embedded React/Vite timeline UI.

### 9.2 Dual-Track Synchronization Architecture
To achieve optimal resilience, zero-breakage cloning, and pristine history preservation without the pitfalls of Git Submodules:
1. **Track 1: Integrated Monorepo Subfolder (`vedit/`)**:
   - Committed directly to `main` branch under `vedit/`.
   - Contains all backend engines, graph compilers, React timeline frontends, test suites, and operational scripts.
   - Stripped of runtime caches (`.venv`, `node_modules`, `dist`, `__pycache__`) to maintain a clean git footprint.
2. **Track 2: Dedicated Upstream Mirror Branch (`vedit`)**:
   - Maintained at `https://github.com/ederaefe/Video-MCP/tree/vedit`.
   - Preserves 100% of the granular commit history, commit authorship, and branch pointers from the active VEDIT workspace.
3. **Automated Weekly Script (`scripts/sync-to-backup.ps1`)**:
   - Single-command execution (`powershell scripts/sync-to-backup.ps1 -AutoCommit`) that synchronizes both Track 1 and Track 2 in sequence, generating an atomic weekly backup checkpoint.





