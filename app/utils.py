import subprocess


#-Base objects-#
error_message = """
Error connecting. Try:
- Check the given phone IP.
- Connecting the device with USB for the first connect.
""".strip()


#-Function to connect to the given device ip-#
def connect(device_ip: str) -> tuple:

    #-Executing the initial commands-#
    subprocess.run(["adb", "kill-server"], stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)
    subprocess.run(["adb", "start-server"], stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)
    subprocess.run(["adb", "tcpip", "5555"], stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)

    #-Getting the output of the final command-#
    process = subprocess.run(["adb", "connect", device_ip], capture_output = True, text = True)

    #-Output and error objects-#
    output = process.stdout.strip()

    #-Giving output message if get output-#
    if "connected" in output:
        return True

    # Check for any error in stderr and handle it
    else:
        return False
