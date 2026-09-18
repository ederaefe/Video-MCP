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



