---
applyTo: '**/*.py'
---

# Python Coding Instructions

- When working with file paths and file operations in Python, always use `pathlib.Path` instead of `os.path`. Do not use functions from `os.path` unless explicitly requested otherwise. Path concatenation, existence checks, reading and writing files, retrieving file names and extensions, etc., should be performed exclusively using the objects and methods of `pathlib.Path`.

- Always use `with` statements when working with file I/O to ensure proper resource management and to avoid potential file corruption or memory leaks.

- Use relative paths or configuration settings to define file locations to make the code portable and easier to manage across different environments, but only in a way that is secure and does not expose the application to path traversal vulnerabilities.

- Prefer using `raise Exception(...)` for error handling instead of defining or using special error types. Clearly mention the type of error and all other useful information in the error message text rather than expressing it through a custom or specific exception class.

Follow also  [General Coding Instruction](../copilot_instructions.md)