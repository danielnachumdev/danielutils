# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.45] - 2024-12-20

### Added
- **Comprehensive Database Abstraction Layer** (`@/db`)
  - Abstract `Database` base class with standardized CRUD operations
  - Multiple database implementations:
    - `InMemoryDatabase`: Fast in-memory database for testing and development
    - `PersistentInMemoryDatabase`: In-memory database with persistence capabilities
    - `SQLiteDatabase`: Full SQLite implementation with SQL query support
    - `RedisDatabase`: Redis-based database implementation
  - `DatabaseFactory` for easy database instance creation and management
  - `DatabaseInitializer` for SQLAlchemy model integration and schema validation
  - Rich type system with `ColumnType` enum supporting all major SQL types
  - Query building system with `SelectQuery`, `UpdateQuery`, and `DeleteQuery`
  - Advanced query features including:
    - Complex WHERE clauses with multiple conditions and operators
    - JOIN operations (INNER, LEFT, RIGHT, FULL)
    - ORDER BY, GROUP BY, HAVING clauses
    - LIMIT and OFFSET support
    - Foreign key relationships and constraints
    - Index management
  - Pydantic integration with `BaseDBModel` for type-safe data models
  - JSON serialization/deserialization support
  - Context manager support for automatic connection management
  - Exception handling with standardized `DBException` types
  - Comprehensive schema validation and migration support

### Changed
- Enhanced project structure with dedicated database abstraction module
- Improved type safety across database operations
- Better separation of concerns between database interface and implementations

## [1.0.39] - 2024-12-19

### Added
- Redis database implementation and tests
- Database abstraction layer with multiple implementations
- Context manager utilities
- Import wrapper for tqdm

### Fixed
- Fixed sleeping time units (seconds to milliseconds)
- Removed unused imports

## [1.0.38] - 2024-12-18

### Added
- Async worker pool improvements
- Better work loop and printing functionality
- Enhanced type hints for queue operations

### Fixed
- JavaInterface implementation issues
- Import compatibility for different Python versions

## [1.0.37] - 2024-12-17

### Added
- Async command execution utilities
- Async layered command functionality
- Improved async worker pool logging

### Fixed
- Test compatibility issues

## [1.0.36] - 2024-12-16

### Added
- Async tools and utilities
- Enhanced async functionality

## [1.0.35] - 2024-12-15

### Added
- Async programming utilities
- Enhanced async support

## [1.0.31] - 2024-12-14

### Added
- Async programming tools

## [1.0.3] - 2024-12-13

### Added
- Logging system with multiple implementations
- Lombok-style builder design pattern
- Enhanced logging functionality

### Changed
- Refactored logging system for better modularity

## [1.0.2] - 2024-12-12

### Added
- Specialized unittest test cases
- ClassInfo functionality

### Changed
- Removed local editor configuration files

## [1.0.1] - 2024-12-11

### Fixed
- Minor bug fixes and improvements

## [1.0.0] - 2024-12-10

### Added
- Singleton decorator implementation
- Enhanced backoff strategies for retry executor
- Better type annotations throughout the codebase
- Topological sorted dependency inspection
- Generic support for data structures (Stack, Heap, Comparer)

### Changed
- Major version bump to 1.0.0
- Improved project structure and organization
- Enhanced type safety with better annotations

## [0.9.94] - 2024-12-09

### Added
- Random number generation utilities
- Interpreter class for code execution
- Enhanced object reflection capabilities
- Configuration management utilities

### Fixed
- Protocol handling in isoftype function
- Type handling improvements
- Import compatibility issues

## [0.9.92] - 2024-12-08

### Added
- Random creator functions
- Enhanced reflection capabilities
- Better type checking utilities

### Changed
- Updated README documentation
- Improved requirements management

## [0.9.91] - 2024-12-07

### Added
- RetryExecutor class with configurable backoff strategies
- AlwaysTeardownTestCase for improved test reliability
- Enhanced unittest classes

### Fixed
- Type annotation improvements
- Minor bug fixes

## [0.9.90] - 2024-12-06

### Added
- ProgressBar iteration support
- Enhanced aliases system
- Better progress tracking utilities

### Changed
- Improved requirements management
- Enhanced development environment setup

## [0.9.84] - 2024-12-05

### Added
- Deterministic Finite Automaton (DFA) implementation
- Matrix, Vector, and Polynomial classes for linear algebra
- Foreach utility functions
- Custom types system
- State context management
- Optional context utilities
- SAT language implementation (sketch)
- CNF (Conjunctive Normal Form) utilities
- Turing Machine implementation (sketch)
- Bellman-Ford algorithm sketch
- Memo generator utilities

### Changed
- Enhanced ProgressBar functionality
- Improved file handling with TemporaryFile
- Better type hints throughout

### Fixed
- TemporaryFile type hints
- Development environment compatibility

## [0.9.83] - 2024-12-04

### Added
- MultiContext utility
- Enhanced ProgressBar family of classes
- Template file utilities
- Image processing skeleton
- Machine learning skeleton
- Run-length encoding implementation
- PNG processing utilities

### Changed
- Improved ProgressBar functionality
- Better file organization

## [0.9.82] - 2024-12-03

### Added
- Parallel for loop utilities
- ProgressBarPool, ProgressBar, and MockProgressBar classes
- Enhanced progress tracking capabilities

### Changed
- Improved file organization and naming conventions

## [0.9.81] - 2024-12-02

### Added
- AttrContext utility
- Enhanced LayeredCommand functionality
- Improved TemporaryFile implementation

## [0.9.80] - 2024-12-01

### Added
- LayeredCommand utility for command execution

## [0.9.78] - 2024-11-30

### Added
- Versioned imports system for better compatibility
- Enhanced import management across Python versions

### Changed
- Improved compatibility with Python 3.8+
- Removed slots from dataclasses for older Python versions

## [0.9.76] - 2024-11-29

### Fixed
- Distribution packaging issues
- Import path corrections

## [0.9.75] - 2024-11-28

### Added
- File reflection utilities
- Final decorator implementation
- Enhanced reflection capabilities

### Changed
- Major code cleanup and reorganization
- Improved project structure

## [0.9.74] - 2024-11-27

### Added
- Protocol handling in isoftype function
- Enhanced type checking capabilities
- Better function declaration handling

### Changed
- Improved type system compatibility

## [0.9.73] - 2024-11-26

### Added
- Abstractions module for better code organization
- Enhanced abstraction patterns

### Changed
- Updated README documentation
- Improved project structure

## [0.9.72] - 2024-11-25

### Added
- University probability module with comprehensive probability theory implementation
- Conditional variable support
- Discrete and continuous probability distributions
- Bernoulli, Binomial, and other probability distributions
- Probability expressions and accumulation expressions
- Expected value, covariance, and other statistical functions
- Total ordering decorator
- Enhanced frange functionality
- OOP design patterns (Observer, Strategy)

### Changed
- Migrated from pytest to unittest
- Improved test organization
- Enhanced type annotations

### Fixed
- TList implementation issues
- Reflection test improvements

## [0.9.71] - 2024-11-24

### Added
- Enhanced reflection capabilities
- Better type annotations

### Fixed
- Code compatibility with Python 3.8.0

## [0.9.70] - 2024-11-23

### Changed
- Improved type annotations throughout the codebase

## [0.9.69] - 2024-11-22

### Added
- Singleton decorator
- Enhanced type annotations
- Topological sorted dependency inspection
- Generic support for Stack, Heap, and Comparer

### Changed
- Improved publish script functionality
- Better project structure

## [0.9.68] - 2024-11-21

### Added
- Enhanced type annotations
- Better return type specifications

## [0.9.67] - 2024-11-20

### Changed
- Minor improvements and bug fixes

## [0.9.66] - 2024-11-19

### Changed
- Minor improvements and bug fixes

## [0.9.65] - 2024-11-18

### Changed
- Minor improvements and bug fixes

## [0.9.64] - 2024-11-17

### Changed
- Minor improvements and bug fixes

## [0.9.63] - 2024-11-16

### Changed
- Minor improvements and bug fixes

## [0.9.62] - 2024-11-15

### Changed
- Minor improvements and bug fixes

## [0.9.61] - 2024-11-14

### Changed
- File naming convention improvements
- Python 3.8.17 compatibility fixes

## [0.9.6] - 2024-11-13

### Added
- ProgressBarPool for managing multiple progress bars
- WorkerPool class and Worker interface
- File time utilities for Windows
- Multiloop and flatten utilities
- Enhanced reflection capabilities

### Changed
- Updated IO file path arguments
- Improved requirements management

## [0.9.5] - 2024-11-12

### Added
- py.typed file for proper mypy support
- Enhanced type annotations
- Better color scheme for info messages

### Changed
- Refactored requirements structure
- Improved Python version compatibility (3.8+)

## [0.9.0] - 2024-11-11

### Added
- Typed builtins system (TList, TDict, TSet, TTuple)
- Factory pattern for typed classes
- Database course implementations
- Enhanced type safety throughout
- Better mypy integration

### Changed
- Major project restructuring
- Improved type annotations
- Enhanced test coverage

### Fixed
- Python 3.8 compatibility issues
- ParamSpec compatibility across Python versions

## [0.8.7] - 2024-11-10

### Added
- Enhanced publish script
- Better typed class creation utilities

### Changed
- Major readme updates
- Improved project documentation

## [0.8.6] - 2024-11-09

### Added
- Join generators utility
- Node, MultiNode, Stack, and Graph implementations
- ImplicitDataDeleterMeta metaclass
- TypedBuiltins folder structure
- InstanceCacheMeta metaclass
- Property, overload decorators

### Fixed
- Join generators implementation
- PriorityQueue inheritance issues
- Queue push_many functionality

## [0.8.5] - 2024-11-08

### Added
- Pylint integration with 9.90+ rating
- GitHub workflows for CI/CD
- CodeQL security analysis
- Gitleaks security scanning
- Enhanced code quality tools

### Changed
- Major code reformatting for pylint compliance
- Improved code style and quality

### Fixed
- Interface edge cases
- Validate decorator improvements

## [0.8.3] - 2024-11-07

### Added
- Enhanced Interface implementation
- Better function declaration handling

### Fixed
- Interface edge cases
- Function declaration issues

## [0.8.2] - 2024-11-06

### Added
- Enhanced Interface testing
- Better test coverage

### Fixed
- Interface edge cases

## [0.8.1] - 2024-11-05

### Added
- CMRT (Context Manager Return Type) utility
- Threadify decorator
- Heap implementations (MinHeap, MaxHeap)
- Comparer utility
- PriorityQueue with weight function support
- Interface class implementation

### Changed
- Enhanced decorator system
- Improved data structure implementations

## [0.7.9] - 2024-11-04

### Added
- Mathematical symbols utilities
- Better printing functions
- Implicit validate decorator

### Changed
- Migrated to newer validate decorator for better performance
- Improved validation system

## [0.7.8] - 2024-11-03

### Added
- Better validation system
- Enhanced decorator functionality

### Changed
- Renamed old validate decorator to validate_explicit
- Improved validation performance

## [0.7.5] - 2024-11-02

### Added
- Enhanced ACM (Atomic Context Manager) functionality
- Better system validation

### Changed
- Improved metadata handling
- Enhanced project structure

## [0.7.4] - 2024-11-01

### Fixed
- Minor bug fixes and improvements

## [0.7.3] - 2024-10-31

### Added
- Sleep method and atomic decorator
- Enhanced timeout functionality

### Fixed
- Typo corrections throughout the codebase

## [0.7.2] - 2024-10-30

### Added
- JSON-dict utilities
- Enhanced data structure support

### Changed
- Pre-validate refactor preparation

## [0.7.0] - 2024-10-29

### Added
- Automatic test file creation
- Enhanced testing utilities
- Better test automation

### Changed
- Major version bump to 0.7.0

## [0.6.5] - 2024-10-28

### Added
- Enhanced testing utilities
- Better test framework

## [0.6.3] - 2024-10-27

### Added
- Color module for terminal output
- Limit recursion decorator
- Sleep method and atomic decorator

### Changed
- Added __all__ exports to non-class modules

## [0.6.2] - 2024-10-26

### Added
- Internet utilities
- Enhanced testing modules

## [0.6.0] - 2024-10-25

### Added
- Time utilities
- Enhanced testing modules
- Better validation system

### Changed
- Major version bump to 0.6.0

### Fixed
- Validate decorator bug fixes

## [0.5.6] - 2024-10-24

### Added
- Text and Conversions utilities
- Enhanced function documentation
- Better overload and validate decorators

### Changed
- Improved class implementations
- Enhanced documentation

## [0.5.5] - 2024-10-23

### Added
- Initial utility functions
- Basic project structure

## [Initial] - 2024-10-22

### Added
- Initial project setup
- Basic utility functions
- Project foundation

---

## Notes

- This changelog is based on git commit history and represents estimated dates
- Major features and breaking changes are highlighted
- Each version includes the most significant additions, changes, and fixes
- The project has evolved from a simple utility library to a comprehensive Python toolkit
- Python version compatibility has been maintained from 3.8+ throughout recent versions 