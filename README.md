# System Security Auditor

A small Python utility for checking a few basic security-related settings on a computer.

## Features

- Detects the operating system
- Shows system version and machine architecture
- Displays the Python version
- Checks whether the program is running with administrator/root privileges
- Attempts to detect the current firewall status
- Provides simple security notes after the audit

## Technologies

- Python
- Standard Python libraries
- `subprocess`
- `platform`
- `shutil`

## Usage

Run the program with:

```bash
python system_security_auditor.py
