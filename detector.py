import subprocess
import requests
import signal
from threading import Thread
import sys

def send_file(filename, url):
    with open(filename, 'rb') as file:
        response = requests.post(url, files={'file': file})
        print(response.text)
        return response.text

def run_script():
    api_url = sys.argv[1]
    flag = True
    while flag:
        # Run the command
        command = f"sudo cicflowmeter -i enp0s8 -c -d 1  output.csv"
        process = subprocess.Popen(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        process.wait()

        # Start a thread for the POST request
        print('sending to url')
        thread = Thread(target=send_file, args=('output.csv', api_url))
        thread.start()

        #repeat for output2
        command = f"sudo cicflowmeter -i enp0s8 -c -d 1 output2.csv"
        process = subprocess.Popen(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        process.wait()

        # Start a thread for the POST request
        print('sending to url')
        thread = Thread(target=send_file, args=('output2.csv', api_url))
        thread.start()

if __name__ == '__main__':
    run_script()
