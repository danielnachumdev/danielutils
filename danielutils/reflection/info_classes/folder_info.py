#!/usr/bin/env python3
"""
Folder Information Analyzer
Provides comprehensive information about folders and their contents recursively.
"""

import os
import fnmatch
from pathlib import Path
from collections import defaultdict, Counter
import statistics
from typing import Dict, List, Tuple, Any, Set, Optional, Union
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class FileInfo:
    """Information about a single file."""
    name: str
    path: str
    size: int
    extension: str
    is_python: bool = False
    line_count: int = 0
    code_lines: int = 0
    comment_lines: int = 0
    empty_lines: int = 0
    classes: int = 0
    functions: int = 0
    docstrings: int = 0
    imports: List[str] = field(default_factory=list)
    created_time: Optional[datetime] = None
    modified_time: Optional[datetime] = None
    accessed_time: Optional[datetime] = None

    def __post_init__(self):
        """Set file type and analyze Python files."""
        self.is_python = self.extension.lower() == '.py'
        if self.is_python:
            self._analyze_python_file()

    def _analyze_python_file(self):
        """Analyze Python file content for detailed statistics."""
        try:
            with open(self.path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
                self.line_count = len(lines)

                for line in lines:
                    stripped = line.strip()
                    if not stripped:
                        self.empty_lines += 1
                    elif stripped.startswith('#'):
                        self.comment_lines += 1
                    else:
                        self.code_lines += 1

                    # Count imports, classes, functions, docstrings
                    if stripped.startswith('import ') or stripped.startswith('from '):
                        import_part = stripped.split()[1]
                        if ' as ' in stripped:
                            import_part = import_part.split(' as ')[0]
                        self.imports.append(import_part)
                    elif stripped.startswith('class '):
                        self.classes += 1
                    elif stripped.startswith('def '):
                        self.functions += 1
                    elif '"""' in line or "'''" in line:
                        self.docstrings += 1
        except (OSError, UnicodeDecodeError):
            pass

    def to_dict(self) -> Dict[str, Any]:
        """Convert FileInfo to dictionary."""
        return {
            'name': self.name,
            'path': self.path,
            'size': self.size,
            'extension': self.extension,
            'is_python': self.is_python,
            'line_count': self.line_count,
            'code_lines': self.code_lines,
            'comment_lines': self.comment_lines,
            'empty_lines': self.empty_lines,
            'classes': self.classes,
            'functions': self.functions,
            'docstrings': self.docstrings,
            'imports': self.imports,
            'created_time': self.created_time.isoformat() if self.created_time else None,
            'modified_time': self.modified_time.isoformat() if self.modified_time else None,
            'accessed_time': self.accessed_time.isoformat() if self.accessed_time else None
        }


@dataclass
class FolderInfo:
    """Information about a folder and its contents."""
    name: str
    path: str
    total_files: int = 0
    total_folders: int = 0
    python_files: int = 0
    total_lines: int = 0
    code_lines: int = 0
    comment_lines: int = 0
    empty_lines: int = 0
    total_size: int = 0
    file_extensions: Counter = field(default_factory=Counter)
    files: List[FileInfo] = field(default_factory=list)
    subfolders: List['FolderInfo'] = field(default_factory=list)
    depth: int = 0
    excluded_files: int = 0
    excluded_folders: int = 0
    created_time: Optional[datetime] = None
    modified_time: Optional[datetime] = None
    accessed_time: Optional[datetime] = None

    # Computed properties
    _stats_computed: bool = False
    _file_stats: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Initialize computed properties."""
        self._file_stats = {}

    def add_file(self, file_info: FileInfo):
        """Add a file to this folder."""
        self.files.append(file_info)
        self.total_files += 1
        self.total_size += file_info.size
        self.file_extensions[file_info.extension] += 1

        if file_info.is_python:
            self.python_files += 1
            self.total_lines += file_info.line_count
            self.code_lines += file_info.code_lines
            self.comment_lines += file_info.comment_lines
            self.empty_lines += file_info.empty_lines

    def add_subfolder(self, folder_info: 'FolderInfo'):
        """Add a subfolder to this folder."""
        self.subfolders.append(folder_info)
        self.total_folders += 1

    def compute_statistics(self):
        """Compute comprehensive statistics for this folder."""
        if self._stats_computed:
            return self._file_stats

        # Aggregate statistics from files
        line_counts = [
            f.line_count for f in self.files if f.is_python and f.line_count > 0]
        file_sizes = [f.size for f in self.files]

        # Aggregate statistics from subfolders
        for subfolder in self.subfolders:
            subfolder.compute_statistics()
            self.total_files += subfolder.total_files
            self.total_folders += subfolder.total_folders
            self.python_files += subfolder.python_files
            self.total_lines += subfolder.total_lines
            self.code_lines += subfolder.code_lines
            self.comment_lines += subfolder.comment_lines
            self.empty_lines += subfolder.empty_lines
            self.total_size += subfolder.total_size

            # Merge file extensions
            for ext, count in subfolder.file_extensions.items():
                self.file_extensions[ext] += count

        # Calculate computed statistics
        self._file_stats = {
            'avg_lines_per_file': statistics.mean(line_counts) if line_counts else 0,
            'median_lines_per_file': statistics.median(line_counts) if line_counts else 0,
            'min_lines': min(line_counts) if line_counts else 0,
            'max_lines': max(line_counts) if line_counts else 0,
            'avg_file_size': statistics.mean(file_sizes) if file_sizes else 0,
            'comment_percentage': (self.comment_lines / self.total_lines * 100) if self.total_lines > 0 else 0,
            'empty_percentage': (self.empty_lines / self.total_lines * 100) if self.total_lines > 0 else 0,
            'code_percentage': (self.code_lines / self.total_lines * 100) if self.total_lines > 0 else 0,
        }

        self._stats_computed = True
        return self._file_stats

    def get_largest_file(self) -> Optional[FileInfo]:
        """Get the largest file in this folder (recursively)."""
        largest_file = None
        largest_size = 0

        for file_info in self.files:
            if file_info.size > largest_size:
                largest_size = file_info.size
                largest_file = file_info

        for subfolder in self.subfolders:
            sub_largest = subfolder.get_largest_file()
            if sub_largest and sub_largest.size > largest_size:
                largest_size = sub_largest.size
                largest_file = sub_largest

        return largest_file

    def get_smallest_file(self) -> Optional[FileInfo]:
        """Get the smallest file in this folder (recursively)."""
        smallest_file = None
        smallest_size = float('inf')

        for file_info in self.files:
            if file_info.size < smallest_size:
                smallest_size = file_info.size
                smallest_file = file_info

        for subfolder in self.subfolders:
            sub_smallest = subfolder.get_smallest_file()
            if sub_smallest and sub_smallest.size < smallest_size:
                smallest_size = sub_smallest.size
                smallest_file = sub_smallest

        return smallest_file

    def get_files_by_extension(self, extension: str) -> List[FileInfo]:
        """Get all files with a specific extension (recursively)."""
        files = [f for f in self.files if f.extension.lower() ==
                 extension.lower()]

        for subfolder in self.subfolders:
            files.extend(subfolder.get_files_by_extension(extension))

        return files

    def get_python_files(self) -> List[FileInfo]:
        """Get all Python files (recursively)."""
        return self.get_files_by_extension('.py')

    def get_folder_structure(self) -> Dict[str, int]:
        """Get folder structure by depth."""
        structure: Dict[str, int] = defaultdict(int)
        structure[f"depth_{self.depth}"] += 1

        for subfolder in self.subfolders:
            sub_structure = subfolder.get_folder_structure()
            for depth, count in sub_structure.items():
                structure[depth] += count

        return structure

    def get_imports_summary(self) -> Counter:
        """Get summary of all imports (recursively)."""
        imports: Counter[str] = Counter()

        for file_info in self.files:
            if file_info.is_python:
                imports.update(file_info.imports)

        for subfolder in self.subfolders:
            imports.update(subfolder.get_imports_summary())

        return imports

    def to_dict(self) -> Dict[str, Any]:
        """Convert FolderInfo to dictionary."""
        stats = self.compute_statistics()

        return {
            'name': self.name,
            'path': self.path,
            'depth': self.depth,
            'total_files': self.total_files,
            'total_folders': self.total_folders,
            'python_files': self.python_files,
            'total_lines': self.total_lines,
            'code_lines': self.code_lines,
            'comment_lines': self.comment_lines,
            'empty_lines': self.empty_lines,
            'total_size': self.total_size,
            'file_extensions': dict(self.file_extensions),
            'excluded_files': self.excluded_files,
            'excluded_folders': self.excluded_folders,
            'created_time': self.created_time.isoformat() if self.created_time else None,
            'modified_time': self.modified_time.isoformat() if self.modified_time else None,
            'accessed_time': self.accessed_time.isoformat() if self.accessed_time else None,
            'statistics': stats,
            'files': [f.to_dict() for f in self.files],
            'subfolders': [sf.to_dict() for sf in self.subfolders]
        }

    def print_summary(self, indent: int = 0):
        """Print a summary of this folder."""
        prefix = "  " * indent
        stats = self.compute_statistics()

        print(f"{prefix}📁 {self.name}/")
        print(f"{prefix}   📊 Files: {self.total_files}, Folders: {self.total_folders}")
        print(
            f"{prefix}   🐍 Python: {self.python_files} files, {self.total_lines} lines")
        print(
            f"{prefix}   💾 Size: {self.total_size:,} bytes ({self.total_size/1024:.1f} KB)")

        if self.python_files > 0:
            print(f"{prefix}   📈 Avg lines: {stats['avg_lines_per_file']:.1f}")
            print(
                f"{prefix}   💻 Code: {stats['code_percentage']:.1f}%, Comments: {stats['comment_percentage']:.1f}%")

        # Print top file extensions
        if self.file_extensions:
            top_extensions = self.file_extensions.most_common(3)
            ext_str = ", ".join(
                [f"{ext}: {count}" for ext, count in top_extensions])
            print(f"{prefix}   📄 Extensions: {ext_str}")

        # Print subfolders
        for subfolder in self.subfolders:
            subfolder.print_summary(indent + 1)


class FolderAnalyzer:
    """Analyzer for creating FolderInfo instances recursively."""

    def __init__(self, blacklist: Optional[Set[str]] = None):
        """Initialize the analyzer with optional blacklist."""
        self.blacklist = blacklist or self._get_default_blacklist()

    def _get_default_blacklist(self) -> Set[str]:
        """Get default blacklist patterns."""
        return {
            # Node.js
            "node_modules", "npm-debug.log*", "yarn-debug.log*", "yarn-error.log*",

            # Python
            "__pycache__", "*.pyc", "*.pyo", "*.pyd", ".Python", "venv", "env",
            ".env", ".venv", "ENV", "env.bak", "venv.bak",

            # Build and distribution
            "build", "develop-eggs", "dist", "downloads", "eggs", ".eggs", "lib",
            "lib64", "parts", "sdist", "var", "wheels", "*.egg-info",
            ".installed.cfg", "*.egg",

            # IDE and editor files
            ".vscode", ".idea", "*.swp", "*.swo", "*~", ".DS_Store", "Thumbs.db",

            # Git and version control
            ".git", ".gitignore", ".gitattributes", ".svn", ".hg",

            # OS generated files
            ".DS_Store?", "._*", ".Spotlight-V100", ".Trashes", "ehthumbs.db",

            # Logs and temporary files
            "*.log", "*.tmp", "*.temp", "temp", "tmp",

            # Archive and backup
            "*.zip", "*.tar.gz", "*.rar", "*.7z", "*.bak", "*.backup",
        }

    def is_blacklisted(self, path: Path) -> bool:
        """Check if a path matches any blacklist pattern."""
        path_str = str(path)

        for pattern in self.blacklist:
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

    def analyze_folder(self, folder_path: Union[str, Path], max_depth: Optional[int] = None) -> FolderInfo:
        """Analyze a folder and return a FolderInfo instance."""
        folder = Path(folder_path)

        if not folder.exists() or not folder.is_dir():
            raise ValueError(
                f"Folder {folder_path} does not exist or is not a directory")

        return self._analyze_folder_recursive(folder, depth=0, max_depth=max_depth)

    def _analyze_folder_recursive(self, folder: Path, depth: int = 0, max_depth: Optional[int] = None) -> FolderInfo:
        """Recursively analyze a folder."""
        if max_depth is not None and depth > max_depth:
            return FolderInfo(
                name=folder.name,
                path=str(folder),
                depth=depth
            )

        # Create FolderInfo instance
        folder_info = FolderInfo(
            name=folder.name,
            path=str(folder.absolute()),
            depth=depth
        )

        # Get folder timestamps
        try:
            stat = folder.stat()
            folder_info.created_time = datetime.fromtimestamp(stat.st_ctime)
            folder_info.modified_time = datetime.fromtimestamp(stat.st_mtime)
            folder_info.accessed_time = datetime.fromtimestamp(stat.st_atime)
        except OSError:
            pass

        # Analyze files in current folder
        for file_path in folder.iterdir():
            if file_path.is_file():
                if self.is_blacklisted(file_path):
                    folder_info.excluded_files += 1
                    continue

                # Create FileInfo instance
                file_info = self._create_file_info(file_path)
                folder_info.add_file(file_info)

            elif file_path.is_dir():
                if self.is_blacklisted(file_path):
                    folder_info.excluded_folders += 1
                    continue

                # Recursively analyze subfolder
                subfolder_info = self._analyze_folder_recursive(
                    file_path, depth + 1, max_depth
                )
                folder_info.add_subfolder(subfolder_info)

        return folder_info

    def _create_file_info(self, file_path: Path) -> FileInfo:
        """Create a FileInfo instance for a file."""
        try:
            stat = file_path.stat()
            file_info = FileInfo(
                name=file_path.name,
                path=str(file_path),
                size=stat.st_size,
                extension=file_path.suffix,
                created_time=datetime.fromtimestamp(stat.st_ctime),
                modified_time=datetime.fromtimestamp(stat.st_mtime),
                accessed_time=datetime.fromtimestamp(stat.st_atime)
            )
            return file_info
        except OSError:
            # Fallback for files we can't stat
            return FileInfo(
                name=file_path.name,
                path=str(file_path),
                size=0,
                extension=file_path.suffix
            )


def analyze_folder(folder_path: Union[str, Path], blacklist: Optional[Set[str]] = None,
                   max_depth: Optional[int] = None) -> FolderInfo:
    """Convenience function to analyze a folder."""
    analyzer = FolderAnalyzer(blacklist)
    return analyzer.analyze_folder(folder_path, max_depth)


def print_folder_info(folder_info: FolderInfo, show_files: bool = False, show_subfolders: bool = True):
    """Print comprehensive information about a folder."""
    print(f"\n{'='*80}")
    print(f"📁 FOLDER ANALYSIS: {folder_info.name}")
    print(f"{'='*80}")

    # Print basic statistics
    stats = folder_info.compute_statistics()

    print(f"\n📊 BASIC STATISTICS:")
    print(f"   Total Files: {folder_info.total_files:,}")
    print(f"   Total Folders: {folder_info.total_folders:,}")
    print(f"   Python Files: {folder_info.python_files:,}")
    print(f"   Total Lines: {folder_info.total_lines:,}")
    print(
        f"   Total Size: {folder_info.total_size:,} bytes ({folder_info.total_size/1024:.1f} KB)")

    if folder_info.excluded_files > 0 or folder_info.excluded_folders > 0:
        print(f"   Excluded Files: {folder_info.excluded_files:,}")
        print(f"   Excluded Folders: {folder_info.excluded_folders:,}")

    # Print line analysis if Python files exist
    if folder_info.python_files > 0:
        print(f"\n📈 LINE ANALYSIS:")
        print(f"   Average Lines per File: {stats['avg_lines_per_file']:.1f}")
        print(
            f"   Median Lines per File: {stats['median_lines_per_file']:.1f}")
        print(f"   Min Lines: {stats['min_lines']:,}")
        print(f"   Max Lines: {stats['max_lines']:,}")

        print(f"\n💻 CODE COMPOSITION:")
        print(
            f"   Code Lines: {folder_info.code_lines:,} ({stats['code_percentage']:.1f}%)")
        print(
            f"   Comment Lines: {folder_info.comment_lines:,} ({stats['comment_percentage']:.1f}%)")
        print(
            f"   Empty Lines: {folder_info.empty_lines:,} ({stats['empty_percentage']:.1f}%)")

    # Print file extensions
    print(f"\n📁 FILE EXTENSIONS (Top 10):")
    for ext, count in folder_info.file_extensions.most_common(10):
        print(f"   {ext}: {count:,}")

    # Print largest and smallest files
    largest_file = folder_info.get_largest_file()
    smallest_file = folder_info.get_smallest_file()

    if largest_file:
        print(f"\n🏆 EXTREMES:")
        print(
            f"   Largest File: {largest_file.name} ({largest_file.size:,} bytes)")
        if largest_file.is_python:
            print(
                f"              {largest_file.path} ({largest_file.line_count:,} lines)")

    if smallest_file and smallest_file.size > 0:
        print(
            f"   Smallest File: {smallest_file.name} ({smallest_file.size:,} bytes)")

    # Print imports summary
    imports = folder_info.get_imports_summary()
    if imports:
        print(f"\n📦 TOP IMPORTS (Top 10):")
        for module, count in imports.most_common(10):
            print(f"   {module}: {count:,}")

    # Print folder structure
    structure = folder_info.get_folder_structure()
    if structure:
        print(f"\n📂 FOLDER STRUCTURE:")
        for depth, count in sorted(structure.items()):
            print(f"   {depth}: {count:,} folders")

    # Print files if requested
    if show_files and folder_info.files:
        print(f"\n📄 FILES IN THIS FOLDER:")
        for file_info in sorted(folder_info.files, key=lambda x: x.name.lower()):
            print(f"   {file_info.name} ({file_info.size:,} bytes)")
            if file_info.is_python and file_info.line_count > 0:
                print(
                    f"     Lines: {file_info.line_count}, Classes: {file_info.classes}, Functions: {file_info.functions}")

    # Print subfolders if requested
    if show_subfolders and folder_info.subfolders:
        print(f"\n📁 SUBFOLDERS:")
        for subfolder in sorted(folder_info.subfolders, key=lambda x: x.name.lower()):
            subfolder.print_summary(indent=1)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print(
            "Usage: python folder_info.py <folder_path> [--max-depth N] [--show-files] [--no-subfolders]")
        print("Example: python folder_info.py danielutils --max-depth 3 --show-files")
        sys.exit(1)

    folder_path = sys.argv[1]
    max_depth = None
    show_files = False
    show_subfolders = True

    # Parse arguments
    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == "--max-depth" and i + 1 < len(sys.argv):
            max_depth = int(sys.argv[i + 1])
            i += 2
        elif sys.argv[i] == "--show-files":
            show_files = True
            i += 1
        elif sys.argv[i] == "--no-subfolders":
            show_subfolders = False
            i += 1
        else:
            i += 1

    try:
        folder_info = analyze_folder(folder_path, max_depth=max_depth)
        print_folder_info(folder_info, show_files=show_files,
                          show_subfolders=show_subfolders)
    except Exception as e:
        print(f"❌ Error analyzing folder: {e}")
        sys.exit(1)
