import platform
import shutil
import subprocess
import sys


def check_admin():
    try:
        if platform.system() == "Windows":
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        else:
            return hasattr(__import__("os"), "geteuid") and __import__("os").geteuid() == 0
    except Exception:
        return False


def check_firewall():
    system = platform.system()

    try:
        if system == "Windows":
            result = subprocess.run(
                ["netsh", "advfirewall", "show", "allprofiles"],
                capture_output=True,
                text=True,
                timeout=5
            )

            output = result.stdout.lower()

            if "state" in output and "on" in output:
                return "Enabled"
            return "Disabled or unavailable"

        elif system == "Linux":
            if shutil.which("ufw"):
                result = subprocess.run(
                    ["ufw", "status"],
                    capture_output=True,
                    text=True,
                    timeout=5
                )

                return result.stdout.strip().splitlines()[0] if result.stdout else "Unknown"

            if shutil.which("firewall-cmd"):
                result = subprocess.run(
                    ["firewall-cmd", "--state"],
                    capture_output=True,
                    text=True,
                    timeout=5
                )

                return result.stdout.strip() or "Unknown"

            return "Firewall tool not detected"

        elif system == "Darwin":
            result = subprocess.run(
                ["/usr/libexec/ApplicationFirewall/socketfilterfw", "--getglobalstate"],
                capture_output=True,
                text=True,
                timeout=5
            )

            return result.stdout.strip() or "Unknown"

        return "Unsupported operating system"

    except Exception as error:
        return f"Unable to check: {error}"


def run_audit():
    print("=" * 45)
    print("        SYSTEM SECURITY AUDITOR")
    print("=" * 45)

    print(f"Operating System : {platform.system()}")
    print(f"System Version   : {platform.release()}")
    print(f"Machine          : {platform.machine()}")
    print(f"Python Version   : {sys.version.split()[0]}")

    admin_status = check_admin()
    print(f"Administrator    : {'Yes' if admin_status else 'No'}")

    firewall_status = check_firewall()
    print(f"Firewall Status  : {firewall_status}")

    print("\nSecurity Notes:")

    if admin_status:
        print("- The program is running with administrator/root privileges.")
    else:
        print("- The program is running without administrator/root privileges.")

    if "disabled" in firewall_status.lower():
        print("- Firewall may be disabled. Check your system settings.")
    elif "enabled" in firewall_status.lower() or "on" in firewall_status.lower():
        print("- Firewall appears to be enabled.")
    else:
        print("- Firewall status could not be confirmed automatically.")

    print("\nAudit completed.")


if __name__ == "__main__":
    run_audit()
