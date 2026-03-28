"""
BGMI Emulator Bypass Tool - Main Entry Point

This is the main script that orchestrates the bypass process.

⚠️ EDUCATIONAL PURPOSE ONLY - DO NOT USE FOR ACTUAL GAMEPLAY

Usage:
    python main.py --version 4.2 --arch 64
    python main.py --analyze-only
    python main.py --setup-only
"""

import sys
import argparse
import time
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from loguru import logger
from lib_bypass import LibraryBypass
from gameloop_handler import GameLoopHandler
from utils import (
    setup_logging,
    display_banner,
    display_disclaimer,
    get_user_consent,
    print_setup_instructions
)


class BGMIBypassTool:
    """
    Main class that coordinates the BGMI emulator bypass process.
    """

    def __init__(self, config_path: str = "config/bgmi_config.json"):
        """
        Initialize the bypass tool.

        Args:
            config_path: Path to configuration file
        """
        self.lib_bypass = LibraryBypass(config_path)
        self.gameloop_handler = GameLoopHandler(self.lib_bypass.config)
        self.config = self.lib_bypass.config

    def run_setup(self) -> bool:
        """
        Run initial setup and validation.

        Returns:
            True if setup is successful
        """
        logger.info("Running setup and validation...")

        # Step 1: Check GameLoop
        logger.info("[1/5] Checking GameLoop emulator...")
        if not self.gameloop_handler.is_gameloop_running():
            logger.warning("GameLoop is not running. Starting...")
            if not self.gameloop_handler.start_gameloop():
                logger.error("Failed to start GameLoop")
                return False

        # Step 2: Connect ADB
        logger.info("[2/5] Connecting to ADB...")
        if not self.gameloop_handler.connect_adb():
            logger.error("Failed to connect to ADB")
            return False

        # Step 3: Verify BGMI installation
        logger.info("[3/5] Verifying BGMI installation...")
        if not self.gameloop_handler.is_bgmi_installed():
            logger.error("BGMI is not installed on the emulator")
            return False

        # Step 4: Setup Frida
        logger.info("[4/5] Setting up Frida server...")
        self.gameloop_handler.setup_frida_server()

        # Step 5: Validate complete setup
        logger.info("[5/5] Validating complete setup...")
        validation = self.gameloop_handler.validate_setup()

        all_valid = all(validation.values())
        if all_valid:
            logger.success("Setup completed successfully!")
        else:
            logger.warning("Some setup steps failed. Please review the validation results.")

        return True

    def run_analysis(self, lib_path: str) -> bool:
        """
        Run analysis on libUE4.so.

        Args:
            lib_path: Path to libUE4.so file

        Returns:
            True if analysis completed
        """
        logger.info("Running libUE4.so analysis...")

        analysis = self.lib_bypass.analyze_libue4(lib_path)

        logger.info("\n" + "=" * 60)
        logger.info("ANALYSIS RESULTS:")
        logger.info("=" * 60)
        logger.info(f"File: {analysis['file']}")
        logger.info(f"Architecture: {analysis['architecture']}")

        logger.info("\nDetection Methods Found:")
        for method in analysis['detection_methods']:
            logger.info(f"  • {method}")

        logger.info("\nRecommended Patches:")
        for patch in analysis['recommended_patches']:
            logger.info(f"  • Function: {patch['function']}")
            logger.info(f"    Offset: {patch['offset']}")
            logger.info(f"    Action: {patch['description']}")

        logger.info("=" * 60)
        logger.info("\nFor detailed analysis, use IDA Pro or Ghidra")
        logger.info("Update config/bgmi_config.json with actual offsets")

        return True

    def run_bypass(self) -> bool:
        """
        Run the complete bypass process.

        Returns:
            True if bypass executed successfully
        """
        logger.info("Starting BGMI emulator bypass process...")

        # Step 1: Ensure BGMI is running
        logger.info("[1/3] Starting BGMI...")
        if not self.gameloop_handler.start_bgmi():
            logger.error("Failed to start BGMI")
            return False

        # Give BGMI time to fully load
        logger.info("Waiting for BGMI to initialize...")
        time.sleep(10)

        # Step 2: Run bypass
        logger.info("[2/3] Injecting bypass hooks...")
        if not self.lib_bypass.start_bypass():
            logger.error("Failed to start bypass")
            return False

        # Step 3: Monitor
        logger.info("[3/3] Bypass active - Monitoring...")
        logger.success("Bypass process complete!")
        logger.info("\nMonitoring logs for detection attempts...")
        logger.info("Press Ctrl+C to stop")

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("\nStopping bypass...")
            self.cleanup()

        return True

    def cleanup(self):
        """Clean up resources."""
        logger.info("Cleaning up resources...")
        self.lib_bypass.cleanup()
        logger.info("Cleanup complete")


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="BGMI Emulator Bypass Tool - Educational Purpose Only",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        '--version',
        type=str,
        default='4.2',
        help='BGMI version (default: 4.2)'
    )

    parser.add_argument(
        '--arch',
        type=str,
        choices=['32', '64'],
        default='64',
        help='Architecture: 32 or 64 bit (default: 64)'
    )

    parser.add_argument(
        '--config',
        type=str,
        default='config/bgmi_config.json',
        help='Path to configuration file'
    )

    parser.add_argument(
        '--analyze-only',
        action='store_true',
        help='Only analyze libUE4.so without running bypass'
    )

    parser.add_argument(
        '--lib-path',
        type=str,
        help='Path to libUE4.so for analysis'
    )

    parser.add_argument(
        '--setup-only',
        action='store_true',
        help='Only run setup and validation'
    )

    parser.add_argument(
        '--no-consent',
        action='store_true',
        help='Skip consent prompt (automatic acceptance for educational purposes)'
    )

    parser.add_argument(
        '--log-level',
        type=str,
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        default='INFO',
        help='Logging level (default: INFO)'
    )

    return parser.parse_args()


def main():
    """Main entry point."""
    args = parse_arguments()

    # Setup logging
    setup_logging(log_level=args.log_level)

    # Display banner and disclaimer
    display_banner()

    if args.arch == '32':
        logger.error("32-bit architecture is not supported due to increased risk")
        logger.error("Please use 64-bit BGMI version")
        sys.exit(1)

    if not args.no_consent:
        display_disclaimer()
        if not get_user_consent():
            logger.error("User consent required. Exiting.")
            sys.exit(1)

    logger.info(f"BGMI Version: {args.version}")
    logger.info(f"Architecture: {args.arch}-bit")
    logger.info(f"Config: {args.config}")

    # Initialize tool
    tool = BGMIBypassTool(config_path=args.config)

    try:
        # Analysis only mode
        if args.analyze_only:
            if not args.lib_path:
                logger.error("--lib-path required for analysis mode")
                print_setup_instructions()
                sys.exit(1)

            success = tool.run_analysis(args.lib_path)
            sys.exit(0 if success else 1)

        # Setup only mode
        if args.setup_only:
            print_setup_instructions()
            success = tool.run_setup()
            sys.exit(0 if success else 1)

        # Full bypass mode
        logger.warning("Running full bypass mode...")
        logger.warning("⚠️  This is for EDUCATIONAL purposes only!")

        # Run setup first
        if not tool.run_setup():
            logger.error("Setup failed. Please review errors and try again.")
            sys.exit(1)

        # Run bypass
        success = tool.run_bypass()
        sys.exit(0 if success else 1)

    except KeyboardInterrupt:
        logger.info("\n\nInterrupted by user")
        tool.cleanup()
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        logger.exception("Full traceback:")
        tool.cleanup()
        sys.exit(1)


if __name__ == "__main__":
    main()
