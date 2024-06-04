import psutil
import time
import threading

def monitor_usage():
    while True:
        memory_info = psutil.virtual_memory()
        cpu_info = psutil.cpu_percent(interval=1)
        disk_info = psutil.disk_usage('/')

        # Print usage information
        print(f"Memory Usage: {memory_info.percent}%")
        print(f"CPU Usage: {cpu_info}%")
        print('-' * 30)

        time.sleep(1)

def start_monitor():
    monitor_thread = threading.Thread(target=monitor_usage)
    monitor_thread.start()
