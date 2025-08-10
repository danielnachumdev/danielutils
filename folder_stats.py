#!/usr/bin/env python3
"""
Folder Statistics Analyzer
Analyzes Python folders for various statistics including file counts, line counts, and more.
"""

import os
import sys
import fnmatch
from pathlib import Path
from collections import defaultdict, Counter
import statistics
from typing import Dict, List, Tuple, Any, Set


# Default blacklist patterns for common unwanted folders and files
DEFAULT_BLACKLIST = {
    # Node.js
    "node_modules",
    "npm-debug.log*",
    "yarn-debug.log*",
    "yarn-error.log*",

    # Python
    "__pycache__",
    "*.pyc",
    "*.pyo",
    "*.pyd",
    ".Python",
    "venv",
    "env",
    ".env",
    ".venv",
    "ENV",
    "env.bak",
    "venv.bak",

    # Build and distribution
    "build",
    "develop-eggs",
    "dist",
    "downloads",
    "eggs",
    ".eggs",
    "lib",
    "lib64",
    "parts",
    "sdist",
    "var",
    "wheels",
    "*.egg-info",
    ".installed.cfg",
    "*.egg",

    # IDE and editor files
    ".vscode",
    ".idea",
    "*.swp",
    "*.swo",
    "*~",
    ".DS_Store",
    "Thumbs.db",

    # Git and version control
    ".git",
    ".gitignore",
    ".gitattributes",
    ".svn",
    ".hg",

    # OS generated files
    ".DS_Store",
    ".DS_Store?",
    "._*",
    ".Spotlight-V100",
    ".Trashes",
    "ehthumbs.db",
    "Thumbs.db",

    # Logs and temporary files
    "*.log",
    "*.tmp",
    "*.temp",
    "temp",
    "tmp",

    # Archive and backup
    "*.zip",
    "*.tar.gz",
    "*.rar",
    "*.7z",
    "*.bak",
    "*.backup",

    # Media files (optional - uncomment if you want to exclude them)
    # "*.mp3", "*.mp4", "*.avi", "*.mov", "*.wav", "*.flac",
    # "*.jpg", "*.jpeg", "*.png", "*.gif", "*.bmp", "*.tiff",
    # "*.pdf", "*.doc", "*.docx", "*.xls", "*.xlsx",
}


def is_blacklisted(path: Path, blacklist: Set[str]) -> bool:
    """Check if a path matches any blacklist pattern."""
    path_str = str(path)

    for pattern in blacklist:
        # Handle directory patterns
        if pattern.endswith('/') or pattern.endswith('\\'):
            if path_str.endswith(pattern.rstrip('/\\')):
                return True
        # Handle glob patterns
        elif '*' in pattern or '?' in pattern:
            if fnmatch.fnmatch(path.name, pattern):
                return True
        # Handle exact matches
        elif path.name == pattern:
            return True
        # Handle path contains
        elif pattern in path_str:
            return True

    return False


def analyze_folder(folder_path: str, blacklist: Set[str] = None) -> Dict[str, Any]:
    """Analyze a folder and return comprehensive statistics."""
    folder = Path(folder_path)

    if not folder.exists() or not folder.is_dir():
        return {"error": f"Folder {folder_path} does not exist or is not a directory"}

    # Use default blacklist if none provided
    if blacklist is None:
        blacklist = DEFAULT_BLACKLIST

    stats = {
        "folder_path": str(folder.absolute()),
        "total_files": 0,
        "total_folders": 0,
        "python_files": 0,
        "total_lines": 0,
        "code_lines": 0,
        "comment_lines": 0,
        "empty_lines": 0,
        "file_extensions": Counter(),
        "largest_file": {"name": "", "lines": 0, "size": 0},
        "smallest_file": {"name": "", "lines": float('inf'), "size": float('inf')},
        "line_counts": [],
        "file_sizes": [],
        "folder_structure": defaultdict(int),
        "imports": Counter(),
        "classes": 0,
        "functions": 0,
        "docstrings": 0,
        "excluded_files": 0,
        "excluded_folders": 0
    }

    for root, dirs, files in os.walk(folder):
        # Filter out blacklisted directories
        original_dirs = dirs.copy()
        dirs[:] = [d for d in dirs if not is_blacklisted(
            Path(root) / d, blacklist)]
        stats["excluded_folders"] += len(original_dirs) - len(dirs)

        # Count folders
        stats["total_folders"] += len(dirs)

        # Analyze folder depth
        depth = root.replace(str(folder), "").count(os.sep)
        if depth > 0:
            stats["folder_structure"][f"depth_{depth}"] += 1

        for file in files:
            file_path = Path(root) / file

            # Skip blacklisted files
            if is_blacklisted(file_path, blacklist):
                stats["excluded_files"] += 1
                continue

            stats["total_files"] += 1

            # Count file extensions
            ext = file_path.suffix.lower()
            stats["file_extensions"][ext] += 1

            # Get file size
            try:
                file_size = file_path.stat().st_size
                stats["file_sizes"].append(file_size)
            except OSError:
                continue

            # Analyze Python files specifically
            if ext == '.py':
                stats["python_files"] += 1
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        lines = f.readlines()
                        line_count = len(lines)
                        stats["line_counts"].append(line_count)
                        stats["total_lines"] += line_count

                        # Track largest and smallest files
                        if line_count > stats["largest_file"]["lines"]:
                            stats["largest_file"] = {
                                "name": str(file_path.relative_to(folder)),
                                "lines": line_count,
                                "size": file_size
                            }

                        if line_count < stats["smallest_file"]["lines"]:
                            stats["smallest_file"] = {
                                "name": str(file_path.relative_to(folder)),
                                "lines": line_count,
                                "size": file_size
                            }

                        # Analyze line types
                        for line in lines:
                            stripped = line.strip()
                            if not stripped:
                                stats["empty_lines"] += 1
                            elif stripped.startswith('#'):
                                stats["comment_lines"] += 1
                            else:
                                stats["code_lines"] += 1

                        # Count imports, classes, functions, docstrings
                        for line in lines:
                            stripped = line.strip()
                            if stripped.startswith('import ') or stripped.startswith('from '):
                                stats["imports"][stripped.split()[1]] += 1
                            elif stripped.startswith('class '):
                                stats["classes"] += 1
                            elif stripped.startswith('def '):
                                stats["functions"] += 1
                            elif '"""' in line or "'''" in line:
                                stats["docstrings"] += 1

                except (OSError, UnicodeDecodeError):
                    continue

    # Calculate averages and additional statistics
    if stats["line_counts"]:
        stats["avg_lines_per_file"] = statistics.mean(stats["line_counts"])
        stats["median_lines_per_file"] = statistics.median(
            stats["line_counts"])
        stats["min_lines"] = min(stats["line_counts"])
        stats["max_lines"] = max(stats["line_counts"])
    else:
        stats["avg_lines_per_file"] = 0
        stats["median_lines_per_file"] = 0
        stats["min_lines"] = 0
        stats["max_lines"] = 0

    if stats["file_sizes"]:
        stats["avg_file_size"] = statistics.mean(stats["file_sizes"])
        stats["total_size"] = sum(stats["file_sizes"])
    else:
        stats["avg_file_size"] = 0
        stats["total_size"] = 0

    # Calculate percentages
    if stats["total_lines"] > 0:
        stats["comment_percentage"] = (
            stats["comment_lines"] / stats["total_lines"]) * 100
        stats["empty_percentage"] = (
            stats["empty_lines"] / stats["total_lines"]) * 100
        stats["code_percentage"] = (
            stats["code_lines"] / stats["total_lines"]) * 100
    else:
        stats["comment_percentage"] = 0
        stats["empty_percentage"] = 0
        stats["code_percentage"] = 0

    return stats


def print_stats(stats: Dict[str, Any], folder_name: str = ""):
    """Print formatted statistics."""
    if "error" in stats:
        print(f"❌ {stats['error']}")
        return

    print(f"\n{'='*60}")
    print(f"📁 FOLDER ANALYSIS: {folder_name or stats['folder_path']}")
    print(f"{'='*60}")

    print(f"\n📊 BASIC STATISTICS:")
    print(f"   Total Files: {stats['total_files']:,}")
    print(f"   Total Folders: {stats['total_folders']:,}")
    print(f"   Python Files: {stats['python_files']:,}")
    print(f"   Total Lines: {stats['total_lines']:,}")

    if stats['excluded_files'] > 0 or stats['excluded_folders'] > 0:
        print(f"   Excluded Files: {stats['excluded_files']:,}")
        print(f"   Excluded Folders: {stats['excluded_folders']:,}")

    print(f"\n📈 LINE ANALYSIS:")
    print(f"   Average Lines per File: {stats['avg_lines_per_file']:.1f}")
    print(f"   Median Lines per File: {stats['median_lines_per_file']:.1f}")
    print(f"   Min Lines: {stats['min_lines']:,}")
    print(f"   Max Lines: {stats['max_lines']:,}")

    print(f"\n💻 CODE COMPOSITION:")
    print(
        f"   Code Lines: {stats['code_lines']:,} ({stats['code_percentage']:.1f}%)")
    print(
        f"   Comment Lines: {stats['comment_lines']:,} ({stats['comment_percentage']:.1f}%)")
    print(
        f"   Empty Lines: {stats['empty_lines']:,} ({stats['empty_percentage']:.1f}%)")

    print(f"\n📁 FILE EXTENSIONS (Top 10):")
    for ext, count in stats['file_extensions'].most_common(10):
        print(f"   {ext}: {count:,}")

    print(f"\n🔍 PYTHON SPECIFIC:")
    print(f"   Classes: {stats['classes']:,}")
    print(f"   Functions: {stats['functions']:,}")
    print(f"   Docstrings: {stats['docstrings']:,}")

    print(f"\n📏 FILE SIZES:")
    print(
        f"   Total Size: {stats['total_size']:,} bytes ({stats['total_size']/1024:.1f} KB)")
    print(f"   Average File Size: {stats['avg_file_size']:.1f} bytes")

    print(f"\n📂 FOLDER STRUCTURE:")
    for depth, count in sorted(stats['folder_structure'].items()):
        print(f"   {depth}: {count:,} folders")

    print(f"\n🏆 EXTREMES:")
    if stats['largest_file']['name']:
        print(
            f"   Largest File: {stats['largest_file']['name']} ({stats['largest_file']['lines']:,} lines)")
    if stats['smallest_file']['name'] and stats['smallest_file']['lines'] != float('inf'):
        print(
            f"   Smallest File: {stats['smallest_file']['name']} ({stats['smallest_file']['lines']:,} lines)")

    print(f"\n📦 TOP IMPORTS (Top 10):")
    for module, count in stats['imports'].most_common(10):
        print(f"   {module}: {count:,}")


def main():
    """Main function to analyze specified folders."""
    if len(sys.argv) < 2:
        print("Usage: python folder_stats.py <folder1> [folder2] ...")
        print("Example: python folder_stats.py danielmusicil tests")
        print("\nThe script automatically excludes common unwanted folders and files:")
        print("  - node_modules, venv, __pycache__, build, dist, .git, etc.")
        sys.exit(1)

    folders = sys.argv[1:]

    for folder in folders:
        if os.path.exists(folder):
            stats = analyze_folder(folder)
            print_stats(stats, folder)
        else:
            print(f"❌ Folder '{folder}' does not exist!")


if __name__ == "__main__":
    main()
