import threading
import subprocess
import time

#code from 
def run_script(script_name):
    subprocess.run(["python", script_name])

if __name__ == "__main__":
    data_thread = threading.Thread(target=run_script, args=("MPU6050_Data.py",))
    cleaning_thread = threading.Thread(target=run_script, args=("cleaning.py",))
    flask_api_thread = threading.Thread(target=run_script, args=("mpu6050_api.py",))
    daily_api_thread = threading.Thread(target=run_script, args=("daily_api.py",))
    averages_thread = threading.Thread(target=run_script, args=("averages.py",))

    print("Scripts are currently executing.")

    data_thread.start()
    cleaning_thread.start()
    flask_api_thread.start()
    daily_api_thread.start()
    averages_thread.start()
    
    data_thread.join()
    cleaning_thread.join()
    flask_api_thread.start()
    daily_api_thread.join()
    averages_thread.start()
    
    
