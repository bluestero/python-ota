import subprocess

#-Executing the initial commands-#
subprocess.run(["adb", "kill-server"], stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)
subprocess.run(["adb", "start-server"], stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)
subprocess.run(["adb", "tcpip", "5555"], stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)

#-Getting the output of the final command-#
process = subprocess.run(["adb", "connect", "192.168.1.52:5555"], capture_output = True, text = True)

#-Output and error objects-#
output = process.stdout.strip()

#-Giving output message if get output-#
if "connected" in output:
    print(f"Successfully {output}.")

# Check for any error in stderr and handle it
else:
    print("")
    print(output)
    print("Try connecting the device with USB for the first connect.")
    print("Or check the given phone IP.")
