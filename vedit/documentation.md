# Architecture and Technical Reference: vedit-mcp (editorvideo-ai)

## 1. System Overview
`vedit` (distributed on PyPI as `vedit-mcp`) is a local-first, non-linear video editor (NLE) providing full parity between human manual editing and autonomous AI agent operations. It pairs a React web timeline interface with an MCP (Model Context Protocol) server exposing 77 atomic editing and analysis tools running deterministically on a local `ffmpeg` engine.

## 2. Core Architecture
- **State Model (`model.py`)**: The entire project state is represented as a serializable JSON document (tracks, clips, transitions, keyframed transforms, audio gains, and effect chains).
- **Single Source of Truth (`store.py`)**: All project mutations (from web UI, CLI, or MCP agents) must execute through the `Store` class. This provides:
  - Atomic undo/redo history.
  - Transactional safety and auto-saving.
  - Live change event propagation (`on_change`) to connected clients via WebSockets.
- **Graph Compiler (`graph.py`)**: Compiles the JSON project model into a single `filter_complex` pipeline in ffmpeg:
  - Base canvas (`color=black`) onto which clips are composited using `overlay`.
  - Transparent temporal padding (`tpad`) avoids PTS manipulation issues.
  - Reverse draw order within tracks allows automatic cross-dissolves without dedicated transition nodes.
  - Long filtergraphs are written to temporary script files to bypass Windows 32,767-character command-line limits.
- **Dual-Mode Preview (`App.jsx`, `Preview.jsx`, `LivePlayer.jsx`)**:
  - *Diretta* (Direct): Browser-native HTML5 Canvas/Video preview for real-time scrub and playback.
  - *Fedele* (Faithful): Frame-accurate on-demand rendering using the local ffmpeg binary.
- **Hardware Acceleration (`hw.py`)**: Actively probes and verifies GPU encoders (NVENC, Intel QSV, AMD AMF, Apple VideoToolbox) before rendering.

## 3. Intelligent Capabilities
- **Rhythmic Editing (`analyze.py`)**: Computes audio envelopes, beat detection, and bar grids (`music_beats`), allowing cuts precisely timed to music.
- **Automated Shot Curation (`story.py`)**: Subdivides long raw takes (>12s) into candidates, grading them on focus, motion, lighting, and dialogue to assemble rough cuts according to predefined narrative styles (`shortform`, `vlog`, `documentary`, `cinematic`).
- **Speech Tightening & Captions (`captions.py`, `cleanup.py`)**: Utilizes `faster-whisper` for timestamped transcription, subtitle burning, and dead-air / pause cutting.
- **Subject Tracking & Auto-Reframing (`vision.py`)**: Employs YOLO (`ultralytics`) to track human subjects and generate animated crop keyframes for aspect ratio conversions (e.g., 16:9 to 9:16 Shorts/Reels).
- **Color Grading & Matching (`colormatch.py`, `effects.py`)**: Histogram-based color transfer across different cameras or lighting conditions.

## 4. Agent MCP Interface
- Exposes 77 tools covering project management, clip manipulation, keyframing, analysis, and rendering.
- Includes `open_ui` to mount the web editor within the MCP server process, attaching directly to the active `Store` instance without IPC or disk lock conflicts.
- Visual feedback tools (`preview_frame`, `preview_grid`) allow agents to visually inspect frame and sequence outputs before committing renders.
