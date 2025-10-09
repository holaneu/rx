# Debug Scripts for PythonAnywhere Workflow Issues

This folder contains debugging scripts to help troubleshoot workflow loading issues on PythonAnywhere.

## Quick Start

1. **Upload this debug folder** to your PythonAnywhere project directory
2. **Open a bash console** on PythonAnywhere
3. **Navigate to your project directory**: `cd ~/your-project-name`
4. **Run the complete test suite**: `python debug/run_all_tests.py`

## Individual Scripts

### 1. Path Verification (`test_path_verification.py`)
Tests basic path existence and permissions.

```bash
python debug/test_path_verification.py
```

**What it checks:**
- Environment information (Python version, working directory)
- Critical file and directory paths
- File permissions and access rights
- Python import paths

### 2. Workflow Discovery (`test_workflow_discovery.py`)
Tests if workflow files are being found correctly.

```bash
python debug/test_workflow_discovery.py
```

**What it checks:**
- Workflow directories exist
- Workflow files (m_*.py) are found
- Module manager configuration
- Registry state

### 3. Module Loading (`test_module_loading.py`)
Tests if individual workflow modules can be loaded.

```bash
python debug/test_module_loading.py
```

**What it checks:**
- Individual workflow file loading
- Function discovery within modules
- Workflow decorator detection
- Registry updates after loading

### 4. Complete Registry Test (`test_workflow_registry.py`)
Tests the complete workflow registration process.

```bash
python debug/test_workflow_registry.py
```

**What it checks:**
- Registry state before/after loading
- Module manager full reload process
- Manual workflow loading
- Workflow decorator functionality
- Complete registration pipeline

## Troubleshooting Guide

### Common Issues and Solutions

#### 1. **Empty Workflow Registry**
**Symptoms:** Workflows dropdown is empty in UI
**Debug:** Run `test_workflow_registry.py`
**Likely causes:**
- Python 3.10 vs 3.12 compatibility issues
- File path differences (Windows vs Linux)
- Import path problems

#### 2. **Modules Not Found**
**Symptoms:** Import errors in logs
**Debug:** Run `test_path_verification.py`
**Likely causes:**
- Missing files during deployment
- Incorrect working directory
- Permission issues

#### 3. **Workflow Files Not Discovered**
**Symptoms:** Scripts find files but registry is empty
**Debug:** Run `test_module_loading.py`
**Likely causes:**
- Decorator not executing
- Module loading failures
- Registry import issues

## Example Usage on PythonAnywhere

```bash
# 1. SSH into your PythonAnywhere account
# 2. Navigate to your project
cd ~/rx  # or whatever your project folder is named

# 3. Run all tests
python debug/run_all_tests.py

# 4. Or run individual tests
python debug/test_path_verification.py
python debug/test_workflow_discovery.py
python debug/test_module_loading.py
python debug/test_workflow_registry.py
```

## Reading the Output

### Success Indicators
- `✓ OK` - Path/file exists and is accessible
- `✓ Successfully` - Operation completed
- `✓ PASS` - Test passed

### Failure Indicators  
- `✗ MISSING` - File/directory not found
- `✗ Error` - Exception occurred
- `✗ FAIL` - Test failed

### Key Things to Look For

1. **All critical paths exist** (especially workflow directories)
2. **Workflow files are found** (m_*.py files)
3. **Modules can be loaded** without errors
4. **Registry gets populated** after module loading
5. **No permission errors** when accessing files

## Quick Fix Checklist

If tests reveal issues:

1. **File not found errors** → Check deployment, ensure all files uploaded
2. **Permission errors** → Check file permissions on PythonAnywhere
3. **Import errors** → Check Python path, working directory
4. **Empty registry after loading** → Check Python 3.10 compatibility
5. **Module loading fails** → Check individual workflow file syntax

## Contact Information

After running these tests, you'll have detailed information about what's working and what's not. This makes it much easier to identify the root cause and find a solution.