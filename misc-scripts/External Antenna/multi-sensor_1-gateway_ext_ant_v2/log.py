import subprocess
import time
import os

def run_script(script_name):
    """Run a script and return the subprocess object."""
    return subprocess.Popen(['python', script_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def monitor_scripts(scripts):
    """Monitor the given scripts, restart them if they exit or hang."""
    processes = {script: run_script(script) for script in scripts}

    while True:
        for script in scripts:
            proc = processes[script]

            # Read the output of the script
            output = proc.stdout.readline()
            if output:
                print(f"{script}: {output.decode().strip()}")

            # Check if the process has exited
            ret_code = proc.poll()
            if ret_code is not None:  # Process has exited
                print(f"{script} has exited with code {ret_code}. Restarting...")
                processes[script] = run_script(script)

            # Check for hanging process (for example, if no output in 10 seconds)
            if proc.stdout.readable():
                if not output and time.time() - proc.start_time > 10:  # Modify timeout as needed
                    print(f"{script} seems to be hanging. Restarting...")
                    proc.terminate()  # or proc.kill() if needed
                    processes[script] = run_script(script)

        time.sleep(1)  # Sleep for a short duration before checking again

if __name__ == "__main__":
    scripts_to_run = ["logger_single2_ant.py", "logger_single2_ant.py"]  # Replace with your script names
    monitor_scripts(scripts_to_run)

