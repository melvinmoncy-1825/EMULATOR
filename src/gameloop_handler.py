"""
BGMI Emulator Bypass Tool - GameLoop Handler Module

This module handles integration with GameLoop emulator, including:
- Process detection
- ADB communication
- Emulator configuration
- BGMI package management

⚠️ EDUCATIONAL PURPOSE ONLY - DO NOT USE FOR ACTUAL GAMEPLAY
"""

import os
import subprocess
import time
from typing import Optional, List, Dict
from loguru import logger
import psutil


class GameLoopHandler:
    """
    Manages interaction with GameLoop emulator for BGMI bypass.

    This class provides utilities for:
    - Detecting GameLoop process
    - Communicating via ADB
    - Managing BGMI app lifecycle
    - Configuring emulator settings
    """

    def __init__(self, config: Dict):
        """
        Initialize GameLoop handler.

        Args:
            config: Configuration dictionary with GameLoop settings
        """
        self.config = config
        self.gameloop_settings = config.get("gameloop_settings", {})
        self.package_name = self.gameloop_settings.get("package_name", "com.pubg.imobile")
        self.emulator_path = self.gameloop_settings.get("emulator_path", "")
        self.adb_port = 5555
        self.device_id: Optional[str] = None

        logger.info("GameLoopHandler initialized")

    def is_gameloop_running(self) -> bool:
        """
        Check if GameLoop emulator is running.

        Returns:
            True if GameLoop is running, False otherwise
        """
        for proc in psutil.process_iter(['name']):
            try:
                process_name = proc.info['name'].lower()
                # GameLoop processes
                if any(name in process_name for name in ['gameloop', 'aow_exe', 'androidemulator']):
                    logger.info(f"Found GameLoop process: {proc.info['name']}")
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

        logger.warning("GameLoop emulator not detected")
        return False

    def start_gameloop(self) -> bool:
        """
        Start GameLoop emulator if not running.

        Returns:
            True if successfully started or already running
        """
        if self.is_gameloop_running():
            logger.info("GameLoop is already running")
            return True

        if not os.path.exists(self.emulator_path):
            logger.error(f"GameLoop executable not found at: {self.emulator_path}")
            logger.info("Please update the emulator_path in config/bgmi_config.json")
            return False

        try:
            logger.info(f"Starting GameLoop from: {self.emulator_path}")
            subprocess.Popen([self.emulator_path], shell=True)
            time.sleep(10)  # Wait for emulator to initialize

            if self.is_gameloop_running():
                logger.success("GameLoop started successfully")
                return True
            else:
                logger.error("Failed to start GameLoop")
                return False

        except Exception as e:
            logger.error(f"Error starting GameLoop: {e}")
            return False

    def get_adb_devices(self) -> List[str]:
        """
        Get list of connected ADB devices.

        Returns:
            List of device IDs
        """
        try:
            result = subprocess.run(
                ['adb', 'devices'],
                capture_output=True,
                text=True,
                timeout=5
            )

            devices = []
            for line in result.stdout.split('\n')[1:]:  # Skip header
                if line.strip() and 'device' in line:
                    device_id = line.split()[0]
                    devices.append(device_id)

            logger.info(f"Found {len(devices)} ADB device(s)")
            return devices

        except FileNotFoundError:
            logger.error("ADB not found. Please install Android SDK Platform Tools")
            return []
        except Exception as e:
            logger.error(f"Error getting ADB devices: {e}")
            return []

    def connect_adb(self) -> bool:
        """
        Connect to GameLoop via ADB.

        Returns:
            True if connected successfully
        """
        # GameLoop typically runs on localhost:5555
        adb_address = f"127.0.0.1:{self.adb_port}"

        try:
            # Try to connect
            logger.info(f"Connecting to ADB at {adb_address}")
            result = subprocess.run(
                ['adb', 'connect', adb_address],
                capture_output=True,
                text=True,
                timeout=10
            )

            if 'connected' in result.stdout.lower():
                logger.success(f"Connected to ADB: {adb_address}")
                self.device_id = adb_address
                return True
            else:
                logger.warning(f"ADB connection failed: {result.stdout}")
                return False

        except Exception as e:
            logger.error(f"Error connecting to ADB: {e}")
            return False

    def is_bgmi_installed(self) -> bool:
        """
        Check if BGMI is installed on the emulator.

        Returns:
            True if BGMI is installed
        """
        if not self.device_id:
            logger.error("Not connected to ADB device")
            return False

        try:
            result = subprocess.run(
                ['adb', '-s', self.device_id, 'shell', 'pm', 'list', 'packages'],
                capture_output=True,
                text=True,
                timeout=10
            )

            if self.package_name in result.stdout:
                logger.info(f"BGMI ({self.package_name}) is installed")
                return True
            else:
                logger.warning(f"BGMI ({self.package_name}) not found")
                return False

        except Exception as e:
            logger.error(f"Error checking BGMI installation: {e}")
            return False

    def get_bgmi_version(self) -> Optional[str]:
        """
        Get installed BGMI version.

        Returns:
            Version string or None
        """
        if not self.device_id:
            return None

        try:
            result = subprocess.run(
                ['adb', '-s', self.device_id, 'shell', 'dumpsys', 'package', self.package_name],
                capture_output=True,
                text=True,
                timeout=10
            )

            for line in result.stdout.split('\n'):
                if 'versionName' in line:
                    version = line.split('=')[1].strip()
                    logger.info(f"BGMI version: {version}")
                    return version

            return None

        except Exception as e:
            logger.error(f"Error getting BGMI version: {e}")
            return None

    def start_bgmi(self) -> bool:
        """
        Launch BGMI on GameLoop.

        Returns:
            True if launched successfully
        """
        if not self.device_id:
            logger.error("Not connected to ADB device")
            return False

        activity = self.gameloop_settings.get("activity", "com.epicgames.ue4.SplashActivity")
        full_activity = f"{self.package_name}/{activity}"

        try:
            logger.info(f"Starting BGMI: {full_activity}")
            result = subprocess.run(
                ['adb', '-s', self.device_id, 'shell', 'am', 'start', '-n', full_activity],
                capture_output=True,
                text=True,
                timeout=10
            )

            if 'Error' not in result.stdout:
                logger.success("BGMI started successfully")
                time.sleep(5)  # Wait for app to initialize
                return True
            else:
                logger.error(f"Failed to start BGMI: {result.stdout}")
                return False

        except Exception as e:
            logger.error(f"Error starting BGMI: {e}")
            return False

    def stop_bgmi(self) -> bool:
        """
        Stop BGMI process.

        Returns:
            True if stopped successfully
        """
        if not self.device_id:
            return False

        try:
            logger.info("Stopping BGMI...")
            subprocess.run(
                ['adb', '-s', self.device_id, 'shell', 'am', 'force-stop', self.package_name],
                timeout=5
            )
            logger.success("BGMI stopped")
            return True

        except Exception as e:
            logger.error(f"Error stopping BGMI: {e}")
            return False

    def get_bgmi_pid(self) -> Optional[int]:
        """
        Get BGMI process ID.

        Returns:
            Process ID or None
        """
        if not self.device_id:
            return None

        try:
            result = subprocess.run(
                ['adb', '-s', self.device_id, 'shell', 'pidof', self.package_name],
                capture_output=True,
                text=True,
                timeout=5
            )

            if result.stdout.strip():
                pid = int(result.stdout.strip())
                logger.info(f"BGMI PID: {pid}")
                return pid

            return None

        except Exception as e:
            logger.error(f"Error getting BGMI PID: {e}")
            return None

    def setup_frida_server(self) -> bool:
        """
        Setup and start Frida server on the emulator.

        Returns:
            True if Frida server is running
        """
        if not self.device_id:
            logger.error("Not connected to ADB device")
            return False

        try:
            # Check if frida-server is already running
            result = subprocess.run(
                ['adb', '-s', self.device_id, 'shell', 'pidof', 'frida-server'],
                capture_output=True,
                text=True,
                timeout=5
            )

            if result.stdout.strip():
                logger.info("Frida server is already running")
                return True

            # Start frida-server
            logger.info("Starting Frida server on emulator...")
            logger.info("Note: You need to manually push frida-server binary to /data/local/tmp/")
            logger.info("Command: adb push frida-server-*-android-arm64 /data/local/tmp/frida-server")

            # This is a placeholder - user needs to set this up manually
            subprocess.Popen(
                ['adb', '-s', self.device_id, 'shell', 'su -c "/data/local/tmp/frida-server &"'],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

            time.sleep(2)
            logger.success("Frida server start command issued")
            return True

        except Exception as e:
            logger.error(f"Error setting up Frida server: {e}")
            return False

    def configure_emulator_for_bypass(self) -> bool:
        """
        Configure GameLoop emulator settings for better bypass success.

        Returns:
            True if configuration applied
        """
        logger.info("Configuring emulator for bypass...")

        configurations = [
            "Recommended GameLoop Settings:",
            "1. Enable Root access (Settings > Advanced)",
            "2. Set Device Model to: Samsung Galaxy S10",
            "3. Set Android Version to: 9.0 or 11.0",
            "4. Disable Location Services",
            "5. Enable Developer Options",
            "6. Set GPU rendering to: Hardware",
            "7. Allocate at least 4GB RAM",
            "8. Use 64-bit architecture (ARM64-v8a)"
        ]

        for config in configurations:
            logger.info(f"  {config}")

        logger.info("\nThese settings need to be configured manually in GameLoop settings")
        return True

    def validate_setup(self) -> Dict[str, bool]:
        """
        Validate the complete setup for bypass.

        Returns:
            Dictionary with validation results
        """
        logger.info("Validating GameLoop setup...")

        results = {
            "gameloop_running": self.is_gameloop_running(),
            "adb_connected": self.device_id is not None,
            "bgmi_installed": False,
            "correct_version": False,
            "frida_ready": False
        }

        if results["adb_connected"]:
            results["bgmi_installed"] = self.is_bgmi_installed()

            if results["bgmi_installed"]:
                version = self.get_bgmi_version()
                target_version = self.config.get("bgmi_version", "4.2")
                results["correct_version"] = version and target_version in version

        # Log results
        logger.info("Validation Results:")
        for key, value in results.items():
            status = "✓" if value else "✗"
            logger.info(f"  {status} {key.replace('_', ' ').title()}: {value}")

        return results


if __name__ == "__main__":
    logger.info("GameLoopHandler module loaded")
    logger.warning("This is for educational purposes only!")
