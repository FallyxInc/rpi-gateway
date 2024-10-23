import subprocess
import time
import threading

# Define the two scripts you want to run
SCRIPT_1 = "python logger_single2.py"
SCRIPT_2 = "python logger_single2.py"
SCRIPT_3 = "python logger_single2.py"

# Function to run a script, poll its status, and restart it if it exits
def monitor_script(command, script_name):
    while True:
        print(f"Starting {script_name}...")
        process = subprocess.Popen(command, shell=True)

        # Poll the process to check if it's still running
        while True:
            ret_code = process.poll()
            if ret_code is None:
                # Script is still running
               pass 
            else:
                # Script has exited, restart it
                print(f"{script_name} has exited with return code {ret_code}. Restarting in 3 seconds...")
                break
            time.sleep(3)  # Poll every 5 seconds to check if the script has exited

        # Wait for 3 seconds before restarting
        time.sleep(1)

# Run both scripts in parallel using threading
if __name__ == "__main__":
    thread1 = threading.Thread(target=monitor_script, args=(SCRIPT_1, "Script 1"))
    thread2 = threading.Thread(target=monitor_script, args=(SCRIPT_2, "Script 2"))
    thread3 = threading.Thread(target=monitor_script, args=(SCRIPT_3, "Script 3"))

    # Start both threads
    thread1.start()
    thread2.start()
    thread3.start()

    # Wait for both threads to finish (this never happens because of the infinite while loop)
    thread1.join()
    thread2.join()
    thread3.join()
 
