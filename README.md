# Windows Parental Control

[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![Windows](https://img.shields.io/badge/OS-Windows%2010%20%7C%2011-blue)](https://www.microsoft.com/windows)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Package: pywin32](https://img.shields.io/badge/pywin32-305-blue)](https://pypi.org/project/pywin32/)
[![Python Package: psutil](https://img.shields.io/badge/psutil-5.9.6-lightgrey)](https://pypi.org/project/psutil/)

A comprehensive parental control solution for Windows 10/11 that helps parents manage their children's computer usage by blocking inappropriate websites, restricting applications, enforcing time limits, and monitoring activity—all while respecting privacy boundaries.

## ⚠️ Privacy & Ethical Use Notice

**This software is designed exclusively for legitimate parental supervision on devices you own or have explicit authority to manage.** 

- 🔒 **Respect Privacy**: Only use on devices belonging to minor children under your guardianship
- 📋 **Transparency**: Inform children that monitoring is in place (age-appropriate disclosure)
- 🚫 **Prohibited Use**: Never use for surveillance of spouses, employees, or others without explicit consent
- 📜 **Legal Compliance**: Ensure compliance with local laws regarding digital monitoring and child safety

Misuse of monitoring software may violate privacy laws and damage trust. Use responsibly.

## ✨ Features

- **Web Filtering**: Blocks access to inappropriate websites via Windows Hosts file modification
- **Application Control**: Prevents launch of specified applications (e.g., torrent clients, games)
- **Time-based Access Control**: Allows computer use only during specified hours
- **Activity Monitoring**: Tracks browser history (Chrome/Firefox) for accountability
- **Download Prevention**: Blocks file downloads from browsers (optional)
- **USB Monitoring**: Optional USB device connection alerts
- **Stealth Mode**: Runs silently in background via Windows Service/Startup
- **Password Protection**: Secure parental configuration with password
- **Logging & bulletproofing**: Comprehensive logging with configurable retention
- **Email Alerts** (optional): Email notifications for blocked access attempts
- **Easy Installation**: Automated installer creates Windows service/startup entry

## 📋 Requirements

- Windows 10 or Windows 11 (64-bit recommended)
- Python 3.8+
- Administrator privileges (required for installation and operation)
- Python packages: `pywin32`, `psutil`, `pyyaml`, `requests`

## 🚀 Installation

### Option 1: Automated Installation (Recommended)

1. **Download** the repository as ZIP or clone:
   ```bash
   git clone https://github.com/Obed-Ojingwa/Parental-Control-Windows.git
   cd Parental-Control-Windows
   ```

2. **Run installer as Administrator**:
   - Right-click `setup_install.py` → "Run as administrator"
   - OR open Command Prompt/PowerShell as Admin and run:
     ```bash
     python setup_install.py
     ```

3. **Follow the prompts** – the installer will:
   - Create installation directory (`C:\Program Files\ParentalControl\`)
   - Copy all required files
   - Install Python dependencies
   - Configure startup via Windows Scheduled Task
   - Set appropriate file permissions

4. **Configure** the software:
   - Edit `C:\Program Files\ParentalControl\parental_config.yaml`
   - Set your parental password (change the default immediately!)
   - Customize blocked websites, applications, and allowed hours
   - Adjust monitoring preferences

5. **Reboot** or run the startup script manually to begin protection:
   ```bash
   "C:\Program Files\ParentalControl\start_parental_control.bat"
   ```

### Option 2: Manual Installation

1. Install Python 3.8+ from [python.org](https://www.python.org/downloads/)
2. Clone/download this repository
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy files to desired location (e.g., `C:\ParentalControl\`)
5. Edit `parental_config.yaml` with your preferences
6. Run `parental_control.py` as Administrator
7. Configure Windows Task Scheduler to run at startup (optional)

## ⚙️ Configuration

Edit `parental_config.yaml` to customize behavior:

```yaml
# Website blocking (add domains without protocol)
blocked_urls:
  - facebook.com
  - youtube.com
  - instagram.com
  - tiktok.com

# Application blocking (case-insensitive substrings)
blocked_apps:
  - torrent
  - bitcoinminer
  - malware

# Time-based access (24-hour format)
allowed_hours:
  start: 7   # 7:00 AM
  end: 23    # 11:00 PM

# Feature toggles
monitoring_enabled: true
block_downloads: true
enforce_time_limits: true
monitor_usb: false

# Security (CHANGE THESE!)
parent_password: hihi@1234  # ← CHANGE IMMEDIATELY AFTER FIRST RUN

# Logging & notifications
logging:
  level: INFO
  keep_days: 30
notifications:
  email: your-email@example.com
  alert_on_blocked_access: true
```

### Important Configuration Notes:
- **Change the default password** immediately after first installation
- Use complete domain names for website blocking (no `http://` or `www.`)
- Application blocking uses substring matching (e.g., `steam` blocks Steam)
- Time restrictions apply to overall system access when enabled
- Email notifications require proper SMTP configuration in the code (advanced)

## 🖥️ Usage

After installation and configuration:

1. **Automatic Start**: The software runs automatically at Windows startup via scheduled task
2. **Manual Start**: Run the batch file as Administrator:
   ```bash
   "C:\Program Files\ParentalControl\start_parental_control.bat"
   ```
3. **Verification**: Check the log file at `C:\Program Files\ParentalControl\parental_control.log`
4. **Testing**: Attempt to access a blocked website or launch a blocked application
5. **Stopping**: To temporarily disable, end the `parental_control.py` process via Task Manager (requires admin)

## 🛡️ How It Works

### Web Filtering
Modifies Windows `C:\Windows\System32\drivers\etc\hosts` file to redirect blocked domains to `127.0.0.1` (localhost), preventing DNS resolution.

### Application Monitoring
Uses `psutil` to monitor running processes and terminate those matching blocked application names.

### Time Enforcement
Checks system time against allowed hours and can enforce logoff/restriction outside permitted windows.

### Browser Monitoring
Periodically checks Chrome/Firefox history databases for visits to blocked sites (read-only access).

### Stealth Operation
Runs without console window via VBScript wrapper when installed via the setup script.

## 🔒 Security Considerations

- **Password Protection**: Configuration is password-protected (change default password!)
- **File Permissions**: Config file set to read-only for standard users after installation
- **Administrator Requirement**: Requires admin rights to modify system files and monitor processes
- **Log Security**: Logs stored in protectedProgram Files directory
- **Open Source**: Code is transparent – review for any privacy concerns

## 📝 Privacy Best Practices

When using this software for legitimate parental supervision:

1. **Open Communication**: Discuss internet safety and monitoring with your child
2. **Age-Appropriate Limits**: Adjust restrictions based on age and maturity
3. **Data Minimization**: Only collect necessary data; regularly review/delete logs
4. **Transparency**: Consider showing children what is being monitored
5. **Respect Boundaries**: Avoid monitoring private communications (email, chats) unless safety concerns exist
6. **Regular Review**: Periodically review and adjust settings as child demonstrates responsibility
7. **Educate**: Use monitoring as a teaching opportunity about responsible internet use

## ❓ Troubleshooting

### Common Issues

**Problem**: Software not blocking websites  
**Solution**: 
- Verify running as Administrator
- Check anti-virus isn't blocking hosts file changes
- Confirm entries in `C:\Windows\System32\drivers\etc\hosts`
- Ensure website domains are correctly formatted (no `http://`)

**Problem**: Application blocking not working  
**Solution**:
- Check process names in Task Manager match blocked list
- Verify monitoring is enabled in config
- Ensure script is running (check system tray/process list)

**Problem**: Cannot access configuration file  
**Solution**:
- Navigate to `C:\Program Files\ParentalControl\parental_config.yaml`
- Take ownership if needed (right-click → Properties → Security)
- Or run notepad as administrator to edit

**Problem**: Service not starting at boot  
**Solution**:
- Check Task Scheduler for "ParentalControl" task
- Ensure it's set to run with highest privileges
- Verify the batch file path is correct

### Log Files
Main log: `C:\Program Files\ParentalControl\parental_control.log`  
Increase logging level in config for detailed debugging.

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup
```bash
git clone https://github.com/Obed-Ojingwa/Parental-Control-Windows.git
cd Parental-Control-Windows
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Coding Standards
- Follow PEP 8 where applicable
- Add type hints for new functions
- Update documentation for new features
- Include unit tests for critical logic

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by various open-source parental control solutions
- Thanks to the developers of `pywin32`, `psutil`, and `pyyaml` for excellent Windows integration libraries
- Built for concerned parents seeking to protect children in the digital age

---

*Copyright © 2026 Obed-Ojingwa. Licensed under MIT.*

## 📞 Support & Contact

For questions, issues, or contributions:

- **Issue Tracker**: [GitHub Issues](https://github.com/Obed-Ojingwa/Parental-Control-Windows/issues)
- **Email**: obedchukwunenye@gmail.com (as listed in config)
- **Documentation**: See this README and code comments

---


**Remember**: The best parental control combines technology with open communication, trust, and education. Use this tool as part of a comprehensive approach to digital safety and responsibility.

*Copyright © 2023 PC-Parental-Control Contributors. Licensed under MIT.*