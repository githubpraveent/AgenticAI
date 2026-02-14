# Fix: "command not found: python"

## Problem

On macOS, you tried to run:
```bash
python test_basic.py
```

But got:
```
zsh: command not found: python
```

## Solution

**Use `python3` instead of `python` on macOS.**

## Quick Fix

```bash
# Instead of: python test_basic.py
python3 test_basic.py
```

## Complete Setup Steps

1. **First, install dependencies:**
   ```bash
   # Run the setup script
   ./setup.sh
   
   # OR manually:
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Then run tests:**
   ```bash
   python3 test_basic.py
   ```

## Why This Happens

- macOS doesn't include `python` by default
- Python 3 is installed as `python3`
- The scripts are already configured to use `python3` (see the `#!/usr/bin/env python3` at the top)

## All Correct Commands

```bash
# Setup
./setup.sh
# OR
python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt

# Tests
python3 test_basic.py
python3 test_scenarios.py
python3 test_mcp_server.py

# Examples
python3 example_usage.py

# MCP Server
python3 mcp_server.py

# Verification
python3 verify_setup.py
```

## Alternative: Use Virtual Environment

After activating the virtual environment, `python` will work:

```bash
source venv/bin/activate
python test_basic.py  # Now works!
```

## See Also

- [RUN_COMMANDS.md](RUN_COMMANDS.md) - Complete command reference
- [QUICKSTART.md](QUICKSTART.md) - Quick start guide

