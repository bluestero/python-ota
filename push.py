import subprocess


def create_backup(file_path: str) -> str:

    #-Define the backup file path by appending ".bak"-#
    backup_path = file_path + ".bak"
    
    #-Use adb shell command to copy the file to create a backup-#
    process = subprocess.run(
        ["adb", "shell", "cp", file_path, backup_path],
        capture_output=True,
        text=True
    )

    #-Check for any errors-#
    if process.returncode == 0:
        return f"Backup created: {backup_path}\n"
    else:
        return f"Failed to create backup: {process.stderr.strip()}\n"


#-Base objects-#
filepath = r"C:\Users\Jhumritalaiyya\Desktop\Files\Github\python-ota\testing.txt"
destination = "/sdcard/Download/testing.txt"

#-Using the adb shell command to check if the file exists-#
process = subprocess.run(
    ["adb", "shell", "test", "-f", destination, "&&", "echo", "File exists", "||", "echo", "File does not exist"],
    capture_output=True,
    text=True
)

#-Output of the adb command-#
output = process.stdout.strip()

#-Creating backup of the file if exists, then pushing-#
if "File exists" in output:
    print(f"File {destination} already exists.\n")
    print("Creating a backup.\n")
    print(create_backup(destination))
    process = subprocess.run(["adb", "push", filepath, destination], capture_output = True, text = True)
    print(f"{destination} was pushed successfully.\n")

#-Else pushing it directly if not exists-#
else:
    print("Not existing file found. No backup will be created.")
    process = subprocess.run(["adb", "push", filepath, destination], capture_output = True, text = True)
    print(f"{destination} was pushed successfully.")
