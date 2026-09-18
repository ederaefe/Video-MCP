# Video-MCP: Agent-Supervised Video Editing Deck

This workspace serves as the primary hub for agent-assisted video editing using `mcp-video`, `kinocut`, and FFmpeg. Every editing project lives in its own dedicated subfolder to keep raw assets, intermediate renders, visual previews, and final deliverables isolated, deterministic, and organized.

- **Primary Backup Repository**: [https://github.com/ederaefe/Video-MCP](https://github.com/ederaefe/Video-MCP) (Synchronized weekly)
- **Upstream Skill Source**: [https://github.com/mfortne/mcp-video-editing](https://github.com/mfortne/mcp-video-editing)

---

## 1. System Readiness Status

- **FFmpeg Engine**: Installed and verified (v8.1.2 full build with libx264, libx265, libdav1d, whisper, and audio filters).
- **Video Editing Server (`mcp-video`)**: Installs via `pip install mcp-video` or runs on-demand via `uvx --from mcp-video mcp-video`.
- **Operating Model**: Agent-supervised pipeline with automated guardrails, visual storyboards, and quality checkpoints.

---

## 2. Directory Structure and Project Organization

Each video editing task begins by creating a distinct folder inside this workspace:

```text
mcp-video/
├── README.md                          # Workspace operations and workflow manual
├── documentation.md                   # Permanent technical architecture reference
└── <project_name>/                    # Dedicated folder for a specific video project
    ├── raw/                           # Original footage, background music, assets
    ├── previews/                      # Storyboard grids, frame grabs, waveforms
    ├── output/                        # Exported final clips, platform cuts
    └── metadata/                      # Captions (.srt), quality logs, checkpoints
```

---

## 3. The 4-Stage Agent Workflow

The editing process follows a closed feedback loop:

```text
[1. Inspect] ----> [2. Edit & Guardrail] ----> [3. Visual Verification] ----> [4. Release Checkpoint]
     |                      |                            |                              |
 Probe metadata,     Apply trims, audio,         Generate 3x3 storyboards,       Check audio levels,
 audio tracks,       resizing, captions,         inspect keyframes, verify       verify codecs,
 and dimensions      and color filters           text safe zones                 export final video
```

### Stage 1: Inspection
- Before editing, the media file is analyzed for resolution, duration, audio channels, and framerate using `info`.
- This ensures downstream transforms (such as crop dimensions or filter parameters) stay within safe boundaries.

### Stage 2: Guardrailed Editing
- Edits can be single targeted adjustments or multi-step chained operations:
  - **Trimming & Cutting**: Snipping exact time ranges without audio drift.
  - **Reframing & Resizing**: Adapting 16:9 landscape to 9:16 vertical for Shorts, TikTok, and Instagram Reels.
  - **Audio Normalization**: Calibrating speech and background tracks to industry standards (-14 LUFS).
  - **Captions & Subtitles**: Transcribing speech to `.srt` and burning styled captions onto the video.
  - **Visual Styling**: Applying subtle grading, vignettes, blur backgrounds, or title cards.
- Preflight guardrails intercept improper aspect ratio combinations, audio clipping, and text overflow before FFmpeg processes the media.

### Stage 3: Live Visual Verification
- Because video files cannot be inspected as plain text, visual feedback is generated during each step:
  - **Frame Snapshots**: Single-frame captures at critical timestamps to check alignment and color.
  - **Storyboard Grids (3x3)**: Nine evenly spaced frame captures across the video timeline compiled into an image.
  - **Waveform Inspection**: Visual representation of audio levels to confirm speech clarity and silence cuts.

### Stage 4: Release Checkpoints
- Automated validation checks:
  - Validates container and stream integrity.
  - Verifies audio normalization compliance.
  - Generates final thumbnail image and release manifest.
  - Flags any discrepancies for review before publishing.

---

## 4. How to Request Edits

When initiating a new project, place the footage into a new folder and provide instructions in natural language:

### Example Prompts:

- **Quick Single Edit**:
  > "In folder `interview-01`, trim `raw/source.mp4` from 00:01:10 to 00:01:45, normalize the audio, and show me a frame grab."

- **Social Media Repurposing**:
  > "Take `podcast-ep4/raw/recording.mp4`, find the segment from 05:20 to 06:05, turn it into a 9:16 vertical Short, add burned-in captions, and generate a storyboard."

- **Quality and Loudness Correction**:
  > "Check `promo/raw/draft.mp4` for audio loudness issues, apply -14 LUFS normalization, and run a release checkpoint."

---

## 5. Quick CLI Reference

For manual checks from the terminal:

- Probe video information:
  ```powershell
  mcp-video info input.mp4
  ```
- Generate a 3x3 storyboard for inspection:
  ```powershell
  mcp-video storyboard input.mp4 --output preview.jpg --grid 3x3
  ```
- Trim footage:
  ```powershell
  mcp-video trim input.mp4 -s 00:00:15 -d 30 -o trimmed.mp4
  ```
- Resize aspect ratio:
  ```powershell
  mcp-video resize input.mp4 --aspect-ratio 9:16 -o vertical.mp4
  ```
- Normalize audio:
  ```powershell
  mcp-video normalize-audio input.mp4 -o normalized.mp4
  ```
- Run full quality checkpoint:
  ```powershell
  mcp-video video-quality-check input.mp4
  ```

---

## 6. Backup & Synchronization Strategy

Progress in this repository is synchronized weekly to the remote backup vault:
- **Remote**: `origin` -> `https://github.com/ederaefe/Video-MCP`
- **Cadence**: Weekly checkpoint push (every 7 days) capturing updated skills, pipeline scripts, documentation, and metadata receipts.
- **Excluded**: Volatile intermediate cache files and multi-gigabyte temporary render artifacts (managed via `.gitignore`).

