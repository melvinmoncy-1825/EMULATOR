"""
BGMI Emulator Bypass Tool - Utility Functions

Common utility functions used across the bypass tool.

⚠️ EDUCATIONAL PURPOSE ONLY
"""

import os
import sys
import hashlib
from typing import Optional
from loguru import logger


def setup_logging(log_level: str = "INFO", log_file: Optional[str] = None):
    """
    Configure logging with appropriate format and level.

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
        log_file: Optional file path to write logs
    """
    logger.remove()  # Remove default handler

    # Console logging with colors
    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>",
        level=log_level,
        colorize=True
    )

    # File logging if specified
    if log_file:
        logger.add(
            log_file,
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {message}",
            level=log_level,
            rotation="10 MB"
        )


def calculate_file_hash(file_path: str, algorithm: str = "sha256") -> Optional[str]:
    """
    Calculate hash of a file.

    Args:
        file_path: Path to the file
        algorithm: Hash algorithm (md5, sha1, sha256)

    Returns:
        Hex digest of the hash or None if error
    """
    if not os.path.exists(file_path):
        logger.error(f"File not found: {file_path}")
        return None

    try:
        hash_obj = hashlib.new(algorithm)
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                hash_obj.update(chunk)

        file_hash = hash_obj.hexdigest()
        logger.debug(f"{algorithm.upper()} hash of {file_path}: {file_hash}")
        return file_hash

    except Exception as e:
        logger.error(f"Error calculating hash: {e}")
        return None


def verify_libue4_version(lib_path: str) -> bool:
    """
    Verify if the libUE4.so is the expected version for BGMI 4.2.

    Args:
        lib_path: Path to libUE4.so

    Returns:
        True if version matches
    """
    if not os.path.exists(lib_path):
        logger.warning(f"libUE4.so not found at: {lib_path}")
        return False

    # Calculate hash
    file_hash = calculate_file_hash(lib_path)

    # In practice, you would compare against known hashes for BGMI 4.2
    # This is a placeholder
    known_hashes = [
        "example_hash_for_bgmi_4.2_arm64",
        # Add actual hashes after analysis
    ]

    logger.info(f"Verifying libUE4.so version...")
    logger.info(f"File hash: {file_hash}")
    logger.warning("Note: Hash verification is for educational demonstration")

    return True


def display_banner():
    """Display tool banner."""
    banner = """
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║        BGMI EMULATOR BYPASS TOOL v1.0                    ║
    ║        Educational & Research Purpose Only                ║
    ║                                                           ║
    ║        Target: BGMI 4.2 (64-bit)                         ║
    ║        Platform: GameLoop Emulator                        ║
    ║                                                           ║
    ║        ⚠️  WARNING: FOR EDUCATIONAL USE ONLY ⚠️           ║
    ║                                                           ║
    ║        Using this tool may:                               ║
    ║        - Violate BGMI Terms of Service                    ║
    ║        - Result in permanent account bans                 ║
    ║        - Lead to legal consequences                       ║
    ║                                                           ║
    ║        USE AT YOUR OWN RISK                               ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """
    print(banner)


def display_disclaimer():
    """Display legal disclaimer."""
    disclaimer = """
    LEGAL DISCLAIMER:
    ─────────────────────────────────────────────────────────────

    This tool is provided for EDUCATIONAL and RESEARCH purposes only.

    By using this tool, you acknowledge and agree that:

    1. This tool demonstrates concepts of emulator detection bypass
    2. Using this tool in actual gameplay violates BGMI Terms of Service
    3. The authors are not responsible for any consequences of misuse
    4. You will not use this tool for cheating or gaining unfair advantages
    5. You assume all risks associated with using this tool

    This tool is intended for:
    - Security researchers studying anti-cheat mechanisms
    - Developers understanding emulator detection techniques
    - Educational purposes in controlled environments

    DO NOT USE THIS TOOL FOR:
    - Cheating in online games
    - Bypassing legitimate security measures for malicious purposes
    - Violating any Terms of Service or laws

    ─────────────────────────────────────────────────────────────
    """
    print(disclaimer)


def get_user_consent() -> bool:
    """
    Get user consent before proceeding.

    Returns:
        True if user consents
    """
    print("\nDo you understand and agree to the terms above?")
    print("This tool is for EDUCATIONAL purposes only.")

    response = input("\nType 'I UNDERSTAND' to proceed: ").strip()

    if response == "I UNDERSTAND":
        logger.info("User consent obtained")
        return True
    else:
        logger.warning("User consent not obtained")
        return False


def check_root_access() -> bool:
    """
    Check if the script has necessary permissions.

    Returns:
        True if sufficient permissions
    """
    # This is a placeholder
    # In practice, you would check for root/admin access
    logger.info("Checking permissions...")
    return True


def print_setup_instructions():
    """Print setup instructions for users."""
    instructions = """
    SETUP INSTRUCTIONS:
    ═══════════════════════════════════════════════════════════

    1. PREREQUISITES:
       - GameLoop Emulator installed
       - BGMI 4.2 (64-bit) installed in GameLoop
       - Python 3.8+ installed
       - ADB (Android Debug Bridge) installed

    2. INSTALL FRIDA SERVER:
       - Download frida-server for Android ARM64
       - Push to emulator: adb push frida-server /data/local/tmp/
       - Set permissions: adb shell chmod 755 /data/local/tmp/frida-server
       - Run as root: adb shell su -c /data/local/tmp/frida-server &

    3. CONFIGURE GAMELOOP:
       - Enable Root access in settings
       - Set device model to Samsung Galaxy S10
       - Allocate minimum 4GB RAM
       - Enable 64-bit architecture

    4. INSTALL PYTHON DEPENDENCIES:
       - pip install -r requirements.txt

    5. IDA PRO ANALYSIS (Advanced):
       - Load libUE4.so in IDA Pro
       - Search for detection strings
       - Identify function offsets
       - Update config/bgmi_config.json with offsets

    ═══════════════════════════════════════════════════════════
    """
    print(instructions)


if __name__ == "__main__":
    display_banner()
    display_disclaimer()
    print_setup_instructions()
