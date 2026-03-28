# IDA Pro Analysis Guide for BGMI libUE4.so

## Overview

This guide explains how to use IDA Pro to analyze the libUE4.so library from BGMI to identify emulator detection mechanisms.

## Prerequisites

- IDA Pro (Version 7.5+ recommended)
- libUE4.so from BGMI 4.2 (64-bit version)
- Basic understanding of ARM64 assembly
- Familiarity with Unreal Engine 4 structure

## Step 1: Loading libUE4.so in IDA Pro

1. Open IDA Pro 64-bit (ida64.exe)
2. File → Open → Select your libUE4.so file
3. IDA will auto-detect the file type as ELF64 ARM (AArch64)
4. Click OK and wait for initial analysis to complete (this may take 10-30 minutes for large files)

## Step 2: Finding Emulator Detection Functions

### Method 1: String Search

Emulator detection often relies on checking for specific strings. Search for:

```
Common emulator detection strings:
- "qemu"
- "goldfish"
- "vbox"
- "generic"
- "sdk"
- "emulator"
- "android_x86"
- "ro.kernel.qemu"
- "ro.product.model"
- "ro.build.fingerprint"
```

**How to search in IDA:**
1. View → Open subviews → Strings (Shift+F12)
2. Ctrl+F to search within strings window
3. Search for each detection string
4. Double-click on found strings to jump to references

### Method 2: Function Name Analysis

Look for suspicious function names:
- Functions with "Check", "Verify", "Detect", "Validate" in their names
- Functions related to system properties
- Functions dealing with build information

**How to search functions:**
1. View → Open subviews → Functions (Shift+F3)
2. Ctrl+F to search function names

### Method 3: Cross-Reference Analysis

When you find a detection string:
1. Double-click the string to go to the data section
2. Press 'X' to see cross-references (where this string is used)
3. Follow the xrefs to find the detection function

## Step 3: Analyzing Detection Functions

### Example: System Property Check Function

```assembly
; Typical system property check pattern
LDR     X0, =aRoKernelQemu  ; "ro.kernel.qemu"
BL      __system_property_get
CMP     W0, #0
B.NE    detection_positive   ; Branch if property exists
```

**What to look for:**
- Calls to `__system_property_get`
- String comparisons (strcmp, strstr)
- Conditional branches based on results
- Return values indicating detection

### Example: Build Fingerprint Check

```assembly
; Build fingerprint validation
LDR     X0, =aRoBuildFingerprint
BL      __system_property_get
LDR     X1, =expected_fingerprint
BL      strcmp
CBZ     W0, validation_passed  ; If match, continue
B       validation_failed       ; Else, detected emulator
```

## Step 4: Identifying Patch Points

For each detection function, identify:

1. **Function offset**: Note the address (e.g., `0x123456`)
2. **Detection logic**: Understand what triggers detection
3. **Return value**: What value indicates "not emulator"

### Common Patch Strategies

#### Strategy 1: NOP the Detection
Replace detection code with NOP instructions

```assembly
Before:
BL      check_emulator_function

After:
NOP                           ; 0xD503201F in ARM64
```

#### Strategy 2: Force Return Value
Make function always return "not emulator"

```assembly
Before:
check_emulator_function:
    ; ... detection code ...
    MOV     W0, #1            ; Return 1 (detected)
    RET

After:
check_emulator_function:
    MOV     W0, #0            ; Always return 0 (not detected)
    RET
```

#### Strategy 3: Skip Conditional Branch
Change conditional branch to unconditional

```assembly
Before:
CMP     W0, #1
B.NE    not_emulator

After:
CMP     W0, #1
B       not_emulator          ; Always branch
```

## Step 5: Documenting Offsets

Create a patch list in the format:

```json
{
  "patches": [
    {
      "name": "Disable qemu property check",
      "offset": "0x123456",
      "original": "00 00 00 94",  // BL instruction
      "patch": "1F 20 03 D5",     // NOP
      "description": "NOPs the call to check ro.kernel.qemu"
    }
  ]
}
```

## Step 6: Common Detection Mechanisms in BGMI

### 1. System Properties
- `ro.kernel.qemu` - QEMU emulator indicator
- `ro.product.model` - Should match real device
- `ro.build.fingerprint` - Build signature verification
- `ro.hardware` - Hardware platform check

### 2. File System Checks
- `/system/bin/qemu-props`
- `/sys/devices/virtual/`
- Specific emulator files

### 3. CPU Features
- ARM NEON support
- Hardware floating point
- CPU model strings

### 4. OpenGL Renderer
- `glGetString(GL_RENDERER)`
- Looking for "llvmpipe", "SwiftShader"
- GPU vendor checks

### 5. Sensor Checks
- Accelerometer presence
- Gyroscope presence
- Specific sensor values

## Step 7: Testing Your Findings

1. Note all offsets in config/bgmi_config.json
2. Use the Python tool to apply patches
3. Monitor behavior in GameLoop
4. Refine patches as needed

## Advanced Techniques

### Dynamic Analysis with IDA Debugger

1. Attach IDA debugger to running BGMI process
2. Set breakpoints on detection functions
3. Step through code to understand runtime behavior
4. Modify registers/memory in real-time to test bypasses

### Using IDA Python Scripts

```python
import idaapi
import idc

# Find all calls to __system_property_get
for func_ea in Functions():
    for ref in XrefsTo(func_ea):
        if "system_property_get" in get_func_name(func_ea):
            print(f"Found at: {hex(ref.frm)}")
```

## Important Notes

⚠️ **Legal Warning**:
- Reverse engineering may violate BGMI Terms of Service
- This is for educational purposes only
- Do not distribute modified game files
- Use only for security research

## Resources

- [ARM64 Instruction Set](https://developer.arm.com/documentation/ddi0487/latest)
- [IDA Pro Documentation](https://hex-rays.com/products/ida/support/idadoc/)
- [Android System Properties](https://source.android.com/docs/core/architecture/configuration/add-system-properties)

## Next Steps

After completing analysis:
1. Update `config/bgmi_config.json` with found offsets
2. Test bypasses using the Python tool
3. Iterate and refine as needed
4. Document your findings for educational purposes
