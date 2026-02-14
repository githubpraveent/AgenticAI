# Running Commands - Quick Reference

## ⚠️ Important: Use `python3` on macOS

On macOS, Python 3 is typically accessed via `python3`, not `python`.

## ✅ Correct Commands

```bash
# Run tests
python3 test_basic.py
python3 test_scenarios.py
python3 test_mcp_server.py

# Run examples
python3 example_usage.py

# Run MCP server
python3 mcp_server.py

# Verify setup
python3 verify_setup.py
```

## 🔧 Setup Commands

```bash
# Run setup script
./setup.sh

# Or manually:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 💡 Tips

### Option 1: Always use `python3`
Just remember to use `python3` instead of `python` on macOS.

### Option 2: Create an alias (optional)
Add to your `~/.zshrc`:
```bash
alias python=python3
```
Then reload: `source ~/.zshrc`

### Option 3: Use virtual environment
After activating venv, `python` will work:
```bash
source venv/bin/activate
python test_basic.py  # Now works!
```

## 🚀 Quick Test

```bash
# Verify Python is available
python3 --version

# Run a quick test
python3 test_basic.py
```

