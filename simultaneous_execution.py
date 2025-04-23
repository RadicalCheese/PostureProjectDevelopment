import threading
import subprocess
import time

#running this script
def run_script(script_name):
    subprocess.run(["python", script_name])

#ensuring the code runs when executed directly, not imported as a module
#uses threading to run different scripts
if __name__ == "__main__":
    data_thread = threading.Thread(target=run_script, args=("acc_gyro.py",))
    cleaning_thread = threading.Thread(target=run_script, args=("cleaning.py",))
    averages_thread = threading.Thread(target=run_script, args=("averages.py",))
    flask_api_thread = threading.Thread(target=run_script, args=("sensor_api.py",))
    daily_api_thread = threading.Thread(target=run_script, args=("daily_api.py",))
    
    #printing to console that the scripts are all currently running
    print("Scripts are currently executing.")

    #starts running each thread in parallel
    #execution begins almost simultaneously
    data_thread.start()
    cleaning_thread.start()
    averages_thread.start()
    flask_api_thread.start()
    daily_api_thread.start()

    #all threads must be finished executing before the code stops executing
    data_thread.join()
    cleaning_thread.join()
    averages_thread.join()
    flask_api_thread.join()
    daily_api_thread.join()
