# BGMI Emulator Bypass Tool - Usage Examples

## Quick Start Guide

### Prerequisites Check

Before using the tool, ensure you have:

1. **GameLoop Emulator** installed and running
2. **BGMI 4.2** (64-bit) installed in GameLoop
3. **Python 3.8+** installed
4. **ADB** (Android Debug Bridge) in PATH
5. **Frida** and dependencies installed

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd EMULATOR

# Install Python dependencies
pip install -r requirements.txt

# Verify installation
python src/main.py --help
```

## Usage Examples

### Example 1: Setup and Validation Only

Run this first to verify your environment is configured correctly:

```bash
python src/main.py --setup-only
```

**Expected Output:**
```
╔═══════════════════════════════════════════════════════════╗
║        BGMI EMULATOR BYPASS TOOL v1.0                    ║
║        Educational & Research Purpose Only                ║
╚═══════════════════════════════════════════════════════════╝

[*] Running setup and validation...
[*] [1/5] Checking GameLoop emulator...
[+] Found GameLoop process: gameloop.exe
[*] [2/5] Connecting to ADB...
[+] Connected to ADB: 127.0.0.1:5555
[*] [3/5] Verifying BGMI installation...
[+] BGMI (com.pubg.imobile) is installed
[*] [4/5] Setting up Frida server...
[+] Frida server is already running
[*] [5/5] Validating complete setup...
[+] Setup completed successfully!
```

### Example 2: Analyze libUE4.so

Analyze a libUE4.so file to identify detection mechanisms:

```bash
# Extract libUE4.so from BGMI APK first
python src/main.py --analyze-only --lib-path /path/to/libUE4.so
```

**Expected Output:**
```
[*] Running libUE4.so analysis...
[*] NOTE: For full analysis, use IDA Pro or Ghidra

============================================================
ANALYSIS RESULTS:
============================================================
File: /path/to/libUE4.so
Architecture: arm64-v8a

Detection Methods Found:
  • System property checks (ro.kernel.qemu)
  • Build fingerprint validation
  • CPU feature detection
  • OpenGL renderer checks
  • Sensor availability checks

Recommended Patches:
  • Function: IsEmulatorEnvironment
    Offset: 0x123456
    Action: Returns 0 (false) instead of detection result
  • Function: CheckSystemProps
    Offset: 0x234567
    Action: Skip system property validation
============================================================

For detailed analysis, use IDA Pro or Ghidra
Update config/bgmi_config.json with actual offsets
```

### Example 3: Full Bypass Mode (Educational)

Run the complete bypass process:

```bash
python src/main.py --version 4.2 --arch 64
```

**Interactive Prompt:**
```
Do you understand and agree to the terms above?
This tool is for EDUCATIONAL purposes only.

Type 'I UNDERSTAND' to proceed: I UNDERSTAND
```

**Expected Output:**
```
[*] User consent obtained
[*] BGMI Version: 4.2
[*] Architecture: 64-bit
[*] Config: config/bgmi_config.json

[*] Running setup and validation...
[+] Setup completed successfully!

⚠️  Running full bypass mode...
⚠️  This is for EDUCATIONAL purposes only!

============================================================
⚠️  STARTING BGMI EMULATOR BYPASS - EDUCATIONAL MODE
⚠️  DO NOT USE FOR ACTUAL GAMEPLAY
============================================================

[*] [1/3] Starting BGMI...
[+] BGMI started successfully
[*] Waiting for BGMI to initialize...

[*] [2/3] Injecting bypass hooks...
[*] Attempting to attach to process: com.pubg.imobile
[+] Attached to com.pubg.imobile
[Frida] [*] BGMI Bypass Script Loaded
[Frida] [!] WARNING: Educational use only!
[Frida] [+] Found libUE4.so at: 0x7f8a000000
[Frida] [*] Hooking detection functions...
[Frida] [+] Hooked __system_property_get
[Frida] [+] Hooked glGetString
[Frida] [*] Hook installation complete!
[+] Hooks injected successfully!

[*] Applying 1 memory patches...
[+] Memory patches applied (educational mode)
[+] Device properties spoofed (educational mode)

[+] Bypass process complete!

[*] [3/3] Bypass active - Monitoring...
[*] Monitoring logs for detection attempts...
Press Ctrl+C to stop
```

### Example 4: Skip Consent (For Automation)

Skip the interactive consent prompt:

```bash
python src/main.py --no-consent --setup-only
```

### Example 5: Debug Mode

Enable detailed debug logging:

```bash
python src/main.py --log-level DEBUG
```

**Debug Output Example:**
```
2024-03-28 10:30:15 | DEBUG    | Loading config from config/bgmi_config.json
2024-03-28 10:30:15 | DEBUG    | Config loaded: {'bgmi_version': '4.2', ...}
2024-03-28 10:30:16 | DEBUG    | Searching for process: com.pubg.imobile
2024-03-28 10:30:16 | DEBUG    | Found PID: 12345
2024-03-28 10:30:17 | DEBUG    | Creating Frida script...
2024-03-28 10:30:17 | DEBUG    | Script length: 3421 bytes
```

## Advanced Usage

### Custom Configuration

Edit `config/bgmi_config.json` to customize behavior:

```json
{
  "bgmi_version": "4.2",
  "architecture": "arm64-v8a",
  "bypass_methods": {
    "property_spoofing": {
      "enabled": true,
      "properties": {
        "ro.build.fingerprint": "your-custom-fingerprint"
      }
    }
  }
}
```

Then run:
```bash
python src/main.py --config config/bgmi_config.json
```

### Using with IDA Pro Workflow

1. **Extract libUE4.so from BGMI:**
   ```bash
   # Pull from device
   adb pull /data/app/com.pubg.imobile-*/lib/arm64/libUE4.so
   ```

2. **Analyze in IDA Pro:**
   - Open libUE4.so in IDA Pro 64-bit
   - Follow the guide in `docs/IDA_ANALYSIS.md`
   - Document function offsets

3. **Update configuration:**
   ```json
   {
     "bypass_methods": {
       "library_hooks": {
         "enabled": true,
         "libUE4_offsets": {
           "emulator_check_1": "0xABCD1234",
           "emulator_check_2": "0xEF567890"
         }
       }
     }
   }
   ```

4. **Test bypasses:**
   ```bash
   python src/main.py
   ```

### Monitoring Detection Attempts

While the tool is running, watch for these log messages:

```
[Frida] [*] Intercepted property check: ro.kernel.qemu
[Frida] [+] Spoofed ro.kernel.qemu to 0
[Frida] [*] Intercepted property check: ro.hardware
[Frida] [+] Spoofed ro.hardware to qcom
[Frida] [+] Spoofed GPU renderer
```

These indicate that detection attempts were caught and bypassed.

## Troubleshooting Examples

### Problem: ADB Connection Failed

```bash
# Check if GameLoop is running
python src/main.py --setup-only

# If fails, manually test ADB
adb devices

# If no devices, try connecting manually
adb connect 127.0.0.1:5555

# Then retry
python src/main.py --setup-only
```

### Problem: BGMI Not Found

```bash
# Check if BGMI is installed
adb shell pm list packages | grep pubg

# If not found, install BGMI in GameLoop first
# Then verify
python src/main.py --setup-only
```

### Problem: Frida Server Not Running

```bash
# Push frida-server to emulator
adb push frida-server-16.1.4-android-arm64 /data/local/tmp/frida-server

# Set permissions
adb shell chmod 755 /data/local/tmp/frida-server

# Run frida-server
adb shell su -c "/data/local/tmp/frida-server &"

# Verify it's running
adb shell pidof frida-server
```

### Problem: Hooks Not Working

Enable debug logging to see what's happening:

```bash
python src/main.py --log-level DEBUG
```

Check if:
- libUE4.so is loaded
- Function names are correct
- Architecture matches (ARM64)

## Integration Examples

### Using as a Library

```python
from src.lib_bypass import LibraryBypass
from src.gameloop_handler import GameLoopHandler
from src.utils import setup_logging

# Setup
setup_logging(log_level="INFO")

# Initialize
bypass = LibraryBypass("config/bgmi_config.json")
gameloop = GameLoopHandler(bypass.config)

# Connect
if gameloop.connect_adb():
    print("Connected!")

# Start BGMI
if gameloop.start_bgmi():
    print("BGMI started!")

# Run bypass
if bypass.start_bypass():
    print("Bypass active!")
```

### Custom Frida Script

Create your own Frida script:

```javascript
// custom_hook.js
console.log("Custom hook loaded");

var targetFunc = Module.findExportByName("libUE4.so", "YourFunction");
Interceptor.attach(targetFunc, {
    onEnter: function(args) {
        console.log("Function called!");
    }
});
```

Load it:
```python
bypass = LibraryBypass()
bypass.attach_to_process()

with open("custom_hook.js") as f:
    script_code = f.read()

script = bypass.frida_session.create_script(script_code)
script.load()
```

## Best Practices

1. **Always start with --setup-only** to verify environment
2. **Use debug logging** when troubleshooting
3. **Update offsets** after BGMI updates
4. **Monitor logs** for new detection methods
5. **Test in stages** (setup → analysis → bypass)

## Educational Goals

This tool demonstrates:
- Frida-based dynamic instrumentation
- Android emulator detection mechanisms
- Reverse engineering workflows
- Security research methodologies

**Remember:** Use only for learning and research, never for actual gameplay!

## Next Steps

1. Read `docs/TECHNICAL_GUIDE.md` for implementation details
2. Study `docs/IDA_ANALYSIS.md` for analysis techniques
3. Experiment with different hooks and patches
4. Document your findings for educational purposes

## Support and Resources

- For Frida help: https://frida.re/docs/
- For IDA Pro: https://hex-rays.com/ida-pro/support/
- For Android internals: https://source.android.com/

---

**⚠️ Final Reminder: Educational Use Only!**

Do not use this tool to cheat in games or violate Terms of Service.
