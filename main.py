import subprocess
import re

# Get all saved wifi profiles
profiles = subprocess.check_output(["netsh", "wlan", "show", "profiles"]).decode("utf-8").split("\n")
names = [re.search("All User Profile     : (.*)\r", profile) for profile in profiles]
names = [name.group(1) for name in names if name]

# Get passwords for each profile
passwords = {}
for name in names:
    # Get metadata for each profile
    meta_data = subprocess.check_output(["netsh", "wlan", "show", "profile", name]).decode("utf-8").split("\n")
    # Check if password is present
    security = [line for line in meta_data if "Security key" in line]
    if "Present" in security[0]:
        # Get password for each profile
        password = subprocess.check_output(["netsh", "wlan", "show", "profile", name, "key=clear"]).decode("utf-8").split("\n")
        password = [line for line in password if "Key Content" in line]
        # Store password as key-value pair
        passwords[name] = password[0].split(":")[1].strip()

# Print passwords
for key, value in passwords.items():
    print(f"{key} : {value}")