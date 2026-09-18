#!/usr/bin/env python3
"""
Repository Analyzer Engine
Zero-dependency static analysis tool for inspecting project topology, language distributions,
dependency manifests, and file metrics for autonomous agents and developers.
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, Any, List

IGNORED_DIRS = {
    ".git", ".svn", ".hg", "node_modules", "venv", ".venv", "env",
    "__pycache__", ".pytest_cache", ".mypy_cache", ".idea", ".vscode",
    "dist", "build", "target", "out", ".next", ".nuxt", ".cache"
}

EXTENSION_MAP = {
    # Programming Languages
    ".py": "Python",
    ".js": "JavaScript",
    ".mjs": "JavaScript",
    ".cjs": "JavaScript",
    ".ts": "TypeScript",
    ".tsx": "TypeScript (React)",
    ".jsx": "JavaScript (React)",
    ".go": "Go",
    ".rs": "Rust",
    ".java": "Java",
    ".c": "C",
    ".cpp": "C++",
    ".cc": "C++",
    ".h": "C/C++ Header",
    ".hpp": "C++ Header",
    ".cs": "C#",
    ".rb": "Ruby",
    ".php": "PHP",
    ".swift": "Swift",
    ".kt": "Kotlin",
    ".scala": "Scala",
    ".sh": "Shell",
    ".bash": "Shell",
    ".ps1": "PowerShell",
    # Markup / Config
    ".html": "HTML",
    ".css": "CSS",
    ".scss": "SCSS",
    ".sass": "SASS",
    ".json": "JSON",
    ".yaml": "YAML",
    ".yml": "YAML",
    ".toml": "TOML",
    ".xml": "XML",
    ".md": "Markdown",
    ".txt": "Plain Text",
    ".sql": "SQL",
    ".dockerfile": "Dockerfile",
    # Media / Binaries
    ".mp4": "Video (MP4)",
    ".mov": "Video (MOV)",
    ".mkv": "Video (MKV)",
    ".mp3": "Audio (MP3)",
    ".wav": "Audio (WAV)",
    ".srt": "Subtitles (SRT)",
    ".vtt": "Subtitles (VTT)",
    ".png": "Image (PNG)",
    ".jpg": "Image (JPEG)",
    ".jpeg": "Image (JPEG)",
    ".svg": "Vector Image (SVG)",
}

MANIFEST_FILES = {
    "package.json": "Node.js / npm",
    "pyproject.toml": "Python (PEP 518/621)",
    "requirements.txt": "Python pip",
    "setup.py": "Python setuptools",
    "Pipfile": "Pipenv",
    "Cargo.toml": "Rust Cargo",
    "go.mod": "Go Modules",
    "pom.xml": "Java Maven",
    "build.gradle": "Java Gradle",
    "composer.json": "PHP Composer",
    "Gemfile": "Ruby Bundler",
    "Dockerfile": "Docker Container",
    "docker-compose.yml": "Docker Compose",
    "Makefile": "Make",
}


def analyze_repository(repo_path: str) -> Dict[str, Any]:
    root = Path(repo_path).resolve()
    if not root.is_dir():
        raise ValueError(f"Target path does not exist or is not a directory: {repo_path}")

    stats = {
        "root": str(root),
        "total_files": 0,
        "total_bytes": 0,
        "total_lines": 0,
        "languages": {},
        "file_types": {},
        "manifests_detected": [],
        "large_files": [],
        "directory_summary": {},
    }

    lang_counts: Dict[str, Dict[str, int]] = {}
    type_counts: Dict[str, int] = {}
    large_files: List[Dict[str, Any]] = []

    for dirpath, dirnames, filenames in os.walk(root):
        # Exclude ignored directories in-place
        dirnames[:] = [d for d in dirnames if d not in IGNORED_DIRS and not d.startswith(".agent")]

        rel_dir = os.path.relpath(dirpath, root)
        if rel_dir == ".":
            rel_dir = "root"

        stats["directory_summary"][rel_dir] = len(filenames)

        for fname in filenames:
            fpath = Path(dirpath) / fname
            rel_path = fpath.relative_to(root).as_posix()

            try:
                size = fpath.stat().st_size
            except OSError:
                continue

            stats["total_files"] += 1
            stats["total_bytes"] += size

            if fname in MANIFEST_FILES:
                stats["manifests_detected"].append({
                    "file": rel_path,
                    "ecosystem": MANIFEST_FILES[fname],
                    "size_bytes": size
                })

            ext = fpath.suffix.lower()
            lang = EXTENSION_MAP.get(ext, "Other" if ext else "No Extension")
            type_counts[ext or "none"] = type_counts.get(ext or "none", 0) + 1

            # Count lines if text
            lines = 0
            if size < 5 * 1024 * 1024 and ext in EXTENSION_MAP and "Video" not in lang and "Audio" not in lang and "Image" not in lang:
                try:
                    with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                        lines = sum(1 for _ in f)
                    stats["total_lines"] += lines
                except Exception:
                    pass

            if lang not in lang_counts:
                lang_counts[lang] = {"files": 0, "bytes": 0, "lines": 0}
            lang_counts[lang]["files"] += 1
            lang_counts[lang]["bytes"] += size
            lang_counts[lang]["lines"] += lines

            # Track files larger than 10MB
            if size > 10 * 1024 * 1024:
                large_files.append({
                    "path": rel_path,
                    "size_bytes": size,
                    "size_mb": round(size / (1024 * 1024), 2)
                })

    # Sort distributions
    stats["languages"] = dict(sorted(lang_counts.items(), key=lambda item: item[1]["bytes"], reverse=True))
    stats["file_types"] = dict(sorted(type_counts.items(), key=lambda item: item[1], reverse=True))
    stats["large_files"] = sorted(large_files, key=lambda item: item["size_bytes"], reverse=True)

    return stats


def main():
    parser = argparse.ArgumentParser(description="Analyze codebase structure and topology.")
    parser.add_argument("path", nargs="?", default=".", help="Root path of repository to analyze")
    parser.add_argument("--json", action="store_true", help="Output results in raw JSON format")
    args = parser.parse_args()

    try:
        report = analyze_repository(args.path)
    except Exception as exc:
        sys.stderr.write(f"Error during repository analysis: {exc}\n")
        sys.exit(1)

    if args.json:
        print(json.dumps(report, indent=2))
        return

    # Text summary output
    print("=" * 60)
    print(f"Repository Analysis Report: {report['root']}")
    print("=" * 60)
    print(f"Total Files: {report['total_files']}")
    print(f"Total Lines of Code/Text: {report['total_lines']}")
    print(f"Total Size: {round(report['total_bytes'] / (1024 * 1024), 2)} MB")
    print()

    print("Detected Ecosystem Manifests:")
    if report["manifests_detected"]:
        for m in report["manifests_detected"]:
            print(f"  - {m['file']} ({m['ecosystem']})")
    else:
        print("  - None detected")
    print()

    print("Language / Content Breakdown:")
    for lang, metrics in report["languages"].items():
        mb = round(metrics["bytes"] / (1024 * 1024), 2)
        print(f"  - {lang:20} : {metrics['files']:4} files | {metrics['lines']:6} lines | {mb:6.2f} MB")
    print()

    if report["large_files"]:
        print("Large Files (>10MB):")
        for lf in report["large_files"]:
            print(f"  - {lf['path']} ({lf['size_mb']} MB)")
        print()


if __name__ == "__main__":
    main()
