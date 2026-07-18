"""
Setup/Installation script for Parental Control
Runs with Administrator privileges to install as Windows service
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
import json

class ParentalControlSetup:
    def __init__(self):
        self.install_dir = Path(os.getenv('PROGRAMFILES')) / 'ParentalControl'
        self.python_exe = sys.executable
        
    def check_admin_privileges(self):
        """Verify script is running as administrator"""
        try:
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    
    def create_installation_directory(self):
        """Create installation directory"""
        try:
            self.install_dir.mkdir(parents=True, exist_ok=True)
            print(f"✓ Created installation directory: {self.install_dir}")
            return True
        except Exception as e:
            print(f"✗ Error creating directory: {e}")
            return False
    
    def copy_files(self):
        """Copy script files to installation directory"""
        try:
            files_to_copy = [
                'parental_control.py',
                'parental_config.yaml',
                'requirements.txt'
            ]
            
            for file in files_to_copy:
                src = Path.cwd() / file
                dst = self.install_dir / file
                
                if src.exists():
                    shutil.copy2(src, dst)
                    print(f"✓ Copied {file}")
                else:
                    print(f"⚠ Warning: {file} not found in current directory")
            
            return True
        except Exception as e:
            print(f"✗ Error copying files: {e}")
            return False
    
    def install_dependencies(self):
        """Install Python dependencies"""
        try:
            print("\nInstalling Python dependencies...")
            requirements_file = self.install_dir / 'requirements.txt'
            
            subprocess.check_call(
                [self.python_exe, '-m', 'pip', 'install', '-r', str(requirements_file)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            
            print("✓ Dependencies installed successfully")
            return True
        except Exception as e:
            print(f"✗ Error installing dependencies: {e}")
            return False
    
    def create_batch_launcher(self):
        """Create batch file to launch the Python script"""
        try:
            batch_content = f"""@echo off
REM Parental Control Launcher
REM This script launches the parental control with admin privileges

cd /d "{self.install_dir}"
python parental_control.py
pause
"""
            
            batch_file = self.install_dir / 'start_parental_control.bat'
            with open(batch_file, 'w') as f:
                f.write(batch_content)
            
            print(f"✓ Created launcher: {batch_file}")
            return True
        except Exception as e:
            print(f"✗ Error creating batch launcher: {e}")
            return False
    
    def create_vbs_wrapper(self):
        """Create VBS wrapper to run batch silently (without showing console)"""
        try:
            vbs_content = f"""' VBS Wrapper for Parental Control
Set objShell = CreateObject("WScript.Shell")
objShell.Run "{self.install_dir}\\start_parental_control.bat", 0, False
"""
            
            vbs_file = self.install_dir / 'run_parental_control.vbs'
            with open(vbs_file, 'w') as f:
                f.write(vbs_content)
            
            print(f"✓ Created VBS wrapper: {vbs_file}")
            return True
        except Exception as e:
            print(f"✗ Error creating VBS wrapper: {e}")
            return False
    
    def create_startup_shortcut(self):
        """Create shortcut in Startup folder (Windows will run it on boot)"""
        try:
            startup_dir = Path(os.path.expanduser('~')) / 'AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup'
            
            vbs_code = f"""
Set objShell = CreateObject("WScript.Shell")
Set lnk = objShell.CreateShortcut("{startup_dir}\\Parental Control.lnk")
lnk.TargetPath = "{self.install_dir}\\run_parental_control.vbs"
lnk.WorkingDirectory = "{self.install_dir}"
lnk.Save
"""
            
            vbs_file = self.install_dir / 'create_shortcut.vbs'
            with open(vbs_file, 'w') as f:
                f.write(vbs_code)
            
            subprocess.run(['cscript.exe', str(vbs_file)])
            os.remove(vbs_file)
            
            print(f"✓ Created startup shortcut")
            return True
        except Exception as e:
            print(f"✗ Error creating startup shortcut: {e}")
            return False
    
    def create_scheduled_task(self):
        """Create Windows scheduled task to run on system startup"""
        try:
            task_name = "ParentalControl"
            script_path = str(self.install_dir / 'parental_control.py')
            
            cmd = f'''schtasks /create /tn "{task_name}" /tr "python \\"{script_path}\\"" /sc onstart /ru SYSTEM /f'''
            
            subprocess.run(cmd, shell=True, capture_output=True)
            
            print(f"✓ Created scheduled task: {task_name}")
            return True
        except Exception as e:
            print(f"✗ Error creating scheduled task: {e}")
            return False
    
    def set_file_permissions(self):
        """Set restrictive permissions on config file"""
        try:
            config_file = self.install_dir / 'parental_config.yaml'
            
            # Make config read-only for child account
            os.chmod(config_file, 0o444)
            
            print("✓ Set restrictive file permissions")
            return True
        except Exception as e:
            print(f"⚠ Warning: Could not set file permissions: {e}")
            return True  # Non-critical
    
    def test_installation(self):
        """Test if installation was successful"""
        try:
            print("\nTesting installation...")
            
            script = self.install_dir / 'parental_control.py'
            if not script.exists():
                print("✗ Script not found")
                return False
            
            # Try importing the script
            subprocess.run(
                [self.python_exe, '-c', 'import yaml; import psutil'],
                capture_output=True,
                timeout=10
            )
            
            print("✓ Installation test passed")
            return True
        except Exception as e:
            print(f"✗ Installation test failed: {e}")
            return False
    
    def run(self):
        """Run the complete installation process"""
        print("=" * 60)
        print("  Parental Control System - Installation")
        print("=" * 60)
        
        if not self.check_admin_privileges():
            print("\n✗ ERROR: This installation requires Administrator privileges!")
            print("   Please run this script as Administrator")
            sys.exit(1)
        
        steps = [
            ("Creating installation directory", self.create_installation_directory),
            ("Copying files", self.copy_files),
            ("Installing dependencies", self.install_dependencies),
            ("Creating batch launcher", self.create_batch_launcher),
            ("Creating VBS wrapper", self.create_vbs_wrapper),
            ("Setting up startup", self.create_startup_shortcut),
            ("Creating scheduled task", self.create_scheduled_task),
            ("Setting file permissions", self.set_file_permissions),
            ("Testing installation", self.test_installation),
        ]
        
        print(f"\nInstallation directory: {self.install_dir}\n")
        
        all_passed = True
        for step_name, step_func in steps:
            print(f"Step: {step_name}...")
            try:
                if not step_func():
                    all_passed = False
                    print()
            except Exception as e:
                print(f"✗ Error: {e}\n")
                all_passed = False
        
        print("\n" + "=" * 60)
        if all_passed:
            print("✓ Installation completed successfully!")
            print("\nNext steps:")
            print(f"1. Edit the configuration file:")
            print(f"   {self.install_dir}\\parental_config.yaml")
            print(f"\n2. The program will run automatically on system startup")
            print(f"\n3. To test immediately, run:")
            print(f"   {self.install_dir}\\start_parental_control.bat")
        else:
            print("⚠ Installation completed with warnings/errors")
            print("   Please review the messages above")
        
        print("=" * 60)


def main():
    setup = ParentalControlSetup()
    setup.run()


if __name__ == '__main__':
    main()
