---
applyTo: '**/*.py'
---

# Python Coding Instructions

- Make code portable and easier to manage across different environments (especially compatible among local environment (windows) and hosting environment (Linux, Python 3.10.5)), but only in a way that is secure and does not expose the application to path traversal vulnerabilities. See some hints further/bellow.

- When working with file paths and file operations in Python, always use `pathlib.Path` instead of `os.path`. Do not use functions from `os.path` unless explicitly requested otherwise. Path concatenation, existence checks, reading and writing files, retrieving file names and extensions, etc., should be performed exclusively using the objects and methods of `pathlib.Path`.

- Always use `with` statements when working with file I/O to ensure proper resource management and to avoid potential file corruption or memory leaks.

- Make code compatible with the PythonAnywhere.com python hosting (Linux, python 3.10.5) environment. Some common issues to avoid:
    - PythonAnywhere.com has working directory set to /home/username/ instead of /home/username/project/. Historically, this has caused issues with relative paths. Solution: Always use absolute paths based on Path(__file__).resolve().parent
    - Path Resolution Best Practices:
        - ✅ DO: Path(__file__).resolve().parent.parent / "some_subdir" / "file.txt"
        - ❌ AVOID: Path("plugins") or os.path.join(".", "some_subdir", "file.txt")
        - ✅ DO: Use .resolve() to get absolute paths
        - ❌ AVOID: Relative paths that depend on current working directory

- Prefer using `raise Exception(...)` for error handling instead of defining or using special error types. Clearly mention the type of error and all other useful information in the error message text rather than expressing it through a custom or specific exception class.

Follow also  [General Coding Instruction](../copilot_instructions.md)