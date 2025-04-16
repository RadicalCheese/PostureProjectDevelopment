import threading
import subprocess
import time

def run_script(script_name):
    subprocess.run(["python", script_name])

if __name__ == "__main__":
    data_thread = threading.Thread(target=run_script, args=("acc_gyro.py",))
    cleaning_thread = threading.Thread(target=run_script, args=("cleaning.py",))

    data_thread.start()
    time.sleep(10)
    cleaning_thread.start()
    
    data_thread.join()
    cleaning_thread.join()

    print("Both scripts have finished executing.")
