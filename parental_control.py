"""
Parental Control Script for Windows 10
Controls: URL access blocking, app download prevention, and usage monitoring
Requires: Administrator privileges
"""

import os
import sys
import json
import time
import logging
import subprocess
import threading
from datetime import datetime
from pathlib import Path
import psutil
import yaml

# Configure logging
LOG_DIR = Path(os.getenv('PROGRAMFILES')) / 'ParentalControl'
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / 'parental_control.log'



logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ParentalControl:
    def __init__(self, config_file='parental_config.yaml'):
        """Initialize parental control with configuration"""
        self.config_file = config_file
        self.config = self.load_config()
        self.blocked_urls = self.config.get('blocked_urls', [])
        self.blocked_apps = self.config.get('blocked_apps', [])
        self.allowed_hours = self.config.get('allowed_hours', {'start': 8, 'end': 22})
        self.running = True
        
        logger.info("Parental Control initialized")
        
    def load_config(self):
        """Load configuration from YAML file"""
        try:
            with open(self.config_file, 'r') as f:
                config = yaml.safe_load(f)
                logger.info(f"Configuration loaded from {self.config_file}")
                return config
        except FileNotFoundError:
            logger.warning(f"Config file not found. Using defaults.")
            return self.create_default_config()
    
    def create_default_config(self):
        """Create default configuration"""
        default_config = {
            'blocked_urls': [
                'facebook.com',
                'youtube.com',
                'instagram.com',
                'tiktok.com',
            ],
            'blocked_apps': [
                'torrent',
                'bitcoinminer',
                'malware'
            ],
            'allowed_hours': {
                'start': 8,
                'end': 22
            },
            'monitoring_enabled': True,
            'block_downloads': True,
            'parent_password': 'change_me_immediately'
        }
        
        with open(self.config_file, 'w') as f:
            yaml.dump(default_config, f)
        
        logger.info("Default configuration created")
        return default_config
    
    def is_within_allowed_hours(self):
        """Check if current time is within allowed hours"""
        current_hour = datetime.now().hour
        start_hour = self.allowed_hours['start']
        end_hour = self.allowed_hours['end']
        
        return start_hour <= current_hour < end_hour
    
    def block_url_via_hosts(self, url):
        """Add URL to Windows hosts file to block access"""
        hosts_path = Path('C:\\Windows\\System32\\drivers\\etc\\hosts')
        
        try:
            with open(hosts_path, 'a') as hosts_file:
                hosts_file.write(f'\n127.0.0.1 {url}')
                hosts_file.write(f'\n127.0.0.1 www.{url}')
            logger.info(f"Blocked URL via hosts file: {url}")
            return True
        except PermissionError:
            logger.error(f"Permission denied: Cannot modify hosts file. Run as Administrator.")
            return False
        except Exception as e:
            logger.error(f"Error blocking URL {url}: {e}")
            return False
    
    def setup_hosts_file_blocking(self):
        """Setup blocking via Windows hosts file"""
        logger.info("Setting up hosts file blocking...")
        
        for url in self.blocked_urls:
            self.block_url_via_hosts(url)
    
    def monitor_browser_history(self):
        """Monitor browser access attempts"""
        logger.info("Starting browser history monitoring...")
        
        # Chrome history path
        chrome_history = Path(
            os.path.expanduser('~') + 
            r'\AppData\Local\Google\Chrome\User Data\Default\History'
        )
        
        # Firefox profile path
        firefox_profile = Path(
            os.path.expanduser('~') + 
            r'\AppData\Roaming\Mozilla\Firefox\Profiles'
        )
        
        last_check = time.time()
        
        while self.running:
            try:
                current_time = time.time()
                
                # Check Chrome history periodically
                if chrome_history.exists():
                    self.check_chrome_history(chrome_history, last_check)
                
                last_check = current_time
                time.sleep(30)  # Check every 30 seconds
                
            except Exception as e:
                logger.error(f"Error monitoring browser history: {e}")
                time.sleep(30)
    
    def check_chrome_history(self, history_path, last_check):
        """Check Chrome history for blocked URLs"""
        try:
            # Note: Direct SQLite access requires Chrome to not be running
            # This is a simplified approach - in production, use Chrome DevTools API
            pass
        except Exception as e:
            logger.error(f"Error checking Chrome history: {e}")
    
    def monitor_processes(self):
        """Monitor running processes and block unauthorized apps"""
        logger.info("Starting process monitoring...")
        
        while self.running:
            try:
                for proc in psutil.process_iter(['pid', 'name', 'exe']):
                    try:
                        proc_name = proc.info['name'].lower()
                        
                        # Check if blocked app is running
                        for blocked_app in self.blocked_apps:
                            if blocked_app.lower() in proc_name:
                                logger.warning(f"Blocked application detected: {proc_name}")
                                try:
                                    proc.kill()
                                    logger.info(f"Terminated blocked process: {proc_name}")
                                except (psutil.NoSuchProcess, psutil.AccessDenied):
                                    pass
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        pass
                
                time.sleep(10)  # Check every 10 seconds
                
            except Exception as e:
                logger.error(f"Error in process monitoring: {e}")
                time.sleep(10)
    
    def monitor_downloads(self):
        """Monitor Downloads folder for blocked file types"""
        logger.info("Starting download monitoring...")
        
        downloads_path = Path(os.path.expanduser('~')) / 'Downloads'
        dangerous_extensions = ['.exe', '.msi', '.bat', '.cmd', '.vbs', '.scr']
        dangerous_keywords = ['torrent', 'bitcoinminer', 'crack', 'keygen']
        
        seen_files = set()
        
        while self.running:
            try:
                if downloads_path.exists():
                    for file in downloads_path.iterdir():
                        if file.is_file() and file.name not in seen_files:
                            seen_files.add(file.name)
                            
                            # Check extension
                            if file.suffix.lower() in dangerous_extensions:
                                logger.warning(f"Dangerous file detected: {file.name}")
                                self.handle_dangerous_file(file)
                            
                            # Check filename for dangerous keywords
                            for keyword in dangerous_keywords:
                                if keyword.lower() in file.name.lower():
                                    logger.warning(f"Suspicious file detected: {file.name}")
                                    self.handle_dangerous_file(file)
                
                time.sleep(5)  # Check every 5 seconds
                
            except Exception as e:
                logger.error(f"Error monitoring downloads: {e}")
                time.sleep(5)
    
    def handle_dangerous_file(self, file_path):
        """Handle dangerous files"""
        try:
            quarantine_dir = LOG_DIR / 'Quarantine'
            quarantine_dir.mkdir(exist_ok=True)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            quarantine_path = quarantine_dir / f"{timestamp}_{file_path.name}"
            
            file_path.rename(quarantine_path)
            logger.warning(f"File quarantined: {file_path.name} -> {quarantine_path}")
        except Exception as e:
            logger.error(f"Error quarantining file: {e}")
    
    def check_time_restrictions(self):
        """Enforce time-based access restrictions"""
        logger.info("Starting time restriction checker...")
        
        while self.running:
            try:
                if not self.is_within_allowed_hours():
                    logger.info("Outside allowed hours - enforcing restrictions")
                    self.enforce_restrictions()
                
                time.sleep(60)  # Check every minute
                
            except Exception as e:
                logger.error(f"Error checking time restrictions: {e}")
                time.sleep(60)
    
    def enforce_restrictions(self):
        """Enforce restrictions outside allowed hours"""
        # Close specified browsers/apps
        browser_processes = ['chrome.exe', 'firefox.exe', 'msedge.exe']
        
        for browser in browser_processes:
            for proc in psutil.process_iter(['name']):
                if proc.info['name'].lower() == browser.lower():
                    try:
                        proc.kill()
                        logger.info(f"Closed browser: {browser}")
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        pass
    
    def start(self):
        """Start all monitoring threads"""
        logger.info("Starting Parental Control System...")
        
        # Setup hosts file blocking
        self.setup_hosts_file_blocking()
        
        # Start monitoring threads
        threads = [
            threading.Thread(target=self.monitor_processes, daemon=True),
            threading.Thread(target=self.monitor_downloads, daemon=True),
            threading.Thread(target=self.check_time_restrictions, daemon=True),
            threading.Thread(target=self.monitor_browser_history, daemon=True),
        ]
        
        for thread in threads:
            thread.start()
        
        logger.info("All monitoring systems started")
        
        # Keep main thread alive
        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("Parental Control stopped by user")
            self.stop()
    
    def stop(self):
        """Stop all monitoring"""
        self.running = False
        logger.info("Parental Control system stopped")


def check_admin_privileges():
    """Check if script is running with admin privileges"""
    try:
        return os.getuid() == 0
    except AttributeError:
        # Windows
        import ctypes
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False


def main():
    """Main entry point"""
    if not check_admin_privileges():
        logger.error("This script requires Administrator privileges!")
        print("ERROR: Please run this script as Administrator")
        sys.exit(1)
    
    try:
        pc = ParentalControl()
        pc.start()
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
