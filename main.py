import subprocess
import os

def run_command(command):
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error while executing '{command}': {e}")

def main():
    cnc_script = "cnc.py"
    bot_script = "bot.py"
    apiddos_script = "api.py"
    update_script = "auto.py"
    plan = "123.py"

    run_command(f"screen python {cnc_script}")
    run_command(f"screen python {bot_script}")
    run_command(f"screen python {apiddos_script}")
    run_command(f"screen python {update_script}")  
    run_command(f"screen python {plan}")
    
if __name__ == "__main__":
    main()
