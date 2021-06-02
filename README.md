# Calcolatori
### *Features*

# *Reti_Di_Calcolatori.md*

---

**Table of Contents**

[TOCM]

[TOC]

#*Libraries*

---

###*Referal Links*

`<link>` :<https://github.com/MatteoFasulo/Calcolatori/blob/main/server_lastest.py>

| Name | Description |
| ------------- | ------------------------------ |
| [OS] | Used for miscellaneous operating system operations
| [Time] | Time is a package that implements time in python script
| [Tqdm]| Instantly make your loops show a smart progress meter - just wrap any iterable with tqdm(iterable)
| [Socket] | This module provides access to the BSD socket interface
| [Subprocess] | The subprocess module allows you to spawn new processes, connect to their input/output/error pipes, and obtain their return codes
| [Threading] | This module constructs higher-level threading interfaces on top of the lower level _thread module
| [Json] | Json exposes an API familiar to users of the standard library marshal and pickle modules
| [Tkinter] | The tkinter package (“Tk interface”) is the standard Python interface to the Tk GUI toolkit
| [Configparser] | Use this to write Python programs which can be customized by end users easily

---
#*Dependencies*

---

[Python 3.9.X]
- OS
| import os  |

- Time
| import time  |

- Tdqm
| import tqdm |

- Socket
| import socket |

- Subprocess
| import subprocess |

- Threading
| import threading |

- Json
| import json  |

- Argparse
| import argparse  |

- Tkinter
| import TK from tkinter  |

- Tkinter.filedialog
| import askopenfilename from tkinter.filedialog  |

- Configparser
| import configparser  |

- Client_latest
| import client_latest  |

#*Installation*

---

####*Python*

```
def main():
    """
    Function main that execute the program
    :return:
    """
    # CONNESSIONE AL SERVER E LOGIN
    
    conn = backend.connect_to_server(port=13000)
    try:
        done = loop = False
        user = pwd = None
        while not done:
            backend.print_welcome()
            choice = backend.handle_choice_menu(2)
            if choice == 1:
                chk, user, pwd = backend.login(conn)
                if chk:
                    loop = True
                    done = True
    
            elif choice == 2:
                backend.register_user(conn)
                conn = backend.connect_to_server(port=13000)
    
            elif (choice.lower())[0] == 'e':
                print("[i] Bye bye! See you soon.")
                conn.close()
                print("Closed manually")
                done = True
                loop = False
                break
    except KeyboardInterrupt:
        conn.close()
        return
    try:
        while loop:
            backend.print_menu()
            choice = backend.handle_choice_menu(5)

            if choice == 1:  # Compressor Settings
                done = False
                while not done:
                    backend.print_submenu1_1()
                    choice = backend.handle_choice_menu(6)

                    # Inspect preset
                    # Edit preset
                    # Delete preset
                    
                    if choice == 1 or choice == 2:
                        correct = False
                        while not correct:
                            bitrate = input("Insert bitrate value: ")
                            try:
                                bitrate = int(bitrate)
                                correct = True
                            except ValueError:
                                print("[i] Please insert a integer number.")

                        if choice == 1:
                            ...
                        elif choice == 2:
                            ...
                        elif choice == 3:
                            ...
                        elif choice == 4:
                            ...
                        elif choice == 5:
                            ...
                        else:
                            print("[i] Going back to Main Menu")
                            done = True


                    elif choice == 3 or choice == 4:
                        bitrate = input("Insert Codec name: ")
                        if choice == 3:
                            # Verifica se il codec video è corretto
                            ...

                        else:
                            # Verifica se il codec audio è corretto
                            ...

                    elif choice == 5:  # DOWNSCALING
                        c = input("[i] ")

                    elif choice == 6:
                        print("[i] Going back to Main Menu")
                        done = True
                        break

                else:
                    print("[i] Invalid assignment, please pay attention")

            elif choice == 2:
                backend.send_file(conn)
                # conn.close()
                conn = backend.connect_to_server(port=13000)
                chk, user, pwd = backend.login(conn, user, pwd)
                if not chk:
                    loop = False
                    break

            elif choice == 3:
                done = False
                while not done:
                    backend.print_submenu_streaming()
                    choice = backend.handle_choice_menu(3)

                    if choice == 1:
                        backend.list_files(conn)

                    elif choice == 2:
                        backend.stream_specific(conn)
                        # conn.close()
                        conn = backend.connect_to_server(port=13000)
                        chk, user, pwd = backend.login(conn, user, pwd)
                        if not chk:
                            loop = False
                            break

                    else:
                        print("[i] Going back to Main Menu")
                        break

            elif choice == 4:
                backend.download_my_file(conn)
                conn = backend.connect_to_server(port=13000)
                chk, user, pwd = backend.login(conn, user, pwd)
                if not chk:
                    loop = False
                    break

            elif choice == 5:
                # Delete compressed file
                backend.delete_my_file(conn)
                ...

            elif (choice.lower())[0] == 'e':
                conn.close()
                print("[i] Bye bye! See you soon.")
                break

            else:
                print("[i] Invalid assignment, please pay attention")
    except KeyboardInterrupt:
        conn.close()
        return


if __name__ == '__main__':
    main()
    
    
def register_user(conn):
    print(mk_title("registration menù", 74))
    user = input("[i] Enter username: ")
    pwd = input("[i] Enter password: ")
    if user == '' and pwd == '':
        print("[i]" + center_title("Empty field, coming back to menu.", 74, 3))
        return False

    conn.send(str("register" + SEP + f"{user}" + SEP + f"{pwd}").encode(encoding=encoding))
    back_msg = int(conn.recv(BUFFER_SIZE).decode())

    while back_msg != 0:
        if back_msg == -2:
            msg = "EMPTY FIELD"
        else:
            msg = "username already in use"

        print('[!] ' + center_title(msg.capitalize(), 74, 3) + '\n')
        user = input("[i] Enter username: ")
        pwd = input("[i] Enter password: ")
        if user == '' and pwd == '':
            print("[i]" + center_title("Empty field, coming back to menu.", 74, 3))
            return False
        conn.send(str("register" + SEP + f"{user}" + SEP + f"{pwd}").encode(encoding=encoding))
        back_msg = int(conn.recv(BUFFER_SIZE).decode())
    print('[i]', center_title("successfully registered".capitalize(), 74, 3))
    return True


def login(conn, user=None, pwd=None):
    wrong_password = True
    print(mk_title("login menù", 74))

    while wrong_password:
        if user==None and pwd==None:
            user = input("[i] Enter username: ")
            pwd = input("[i] Enter password: ")

        if user == '' or pwd == '':
            print("[i]"+center_title("Empty field, coming back to menu.", 74, 3))
            return (False, None, None)
        conn.send(str("login" + SEP + f"{user}" + SEP + f"{pwd}").encode(encoding=encoding))
        login_success = int(conn.recv(BUFFER_SIZE).decode())  # PROTOCOLLO - RICEVO RISPOSTA

        if login_success == -1:
            print("[i]"+center_title("Welcome! You're the first user in this server", 74, 3) + "\n" + center_title("So please first register your user", 74))
            # "PLEASE FIRST REGISTER YOUR USER" ERROR CODE -1
            register_user(conn)
            return (None, None, None)

        elif login_success == -2:
            # "WRONG USER" ERROR CODE -2
            print("[!]"+center_title("WRONG USER", 74, 3))
            user = pwd = None
        elif login_success == -3:
            # "WRONG PASSWORD" ERROR CODE -3
            print("[!]"+center_title("WRONG PASSWORD", 74,3))
            user = pwd = None

        elif login_success == 0:
            wrong_password = False
    return (True, user, pwd)


def fetch_port(conn):
    # conn.send((f"{addr}" + SEP + f"{server_port}").encode(encoding=encoding))
    cmd, server_port = conn.recv(BUFFER_SIZE).decode().split(SEP)
    conn.close()
    if cmd == "new_port":
        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.connect((serverName, int(server_port)))
    else:
        raise ValueError
    return clientSocket


def connect_to_server(port):
    # TODO Deve comunicare con assign socket
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName, port))
    conn = fetch_port(clientSocket)
    return conn


def send_file(conn):
    Tk().withdraw()
    filename = askopenfilename()

    path, filename = os.path.split(filename)
    if path != '':
        os.chdir(path)
    conn.send(("encode" + SEP + "None" + SEP + "None").encode(encoding=encoding))
    time.sleep(threshold)

    conn.send(f"{filename}".encode(encoding=encoding))
    filesize = os.path.getsize(filename)

    # print("test", f"{path}", filename, sep="\t")

    total = 0
    progress = tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    time.sleep(threshold)
    with open(filename, "rb") as video:
        for _ in progress:
            while total != filesize:
                frame = video.read(BUFFER_SIZE)
                if total == filesize:
                    break
                conn.send(frame)
                progress.update(len(frame))
                total += len(frame)
    video.close()
    conn.shutdown(SHUT_WR)

    # INIZIO RICEZIONE
    time.sleep(threshold)

    filename, filesize = conn.recv(BUFFER_SIZE).decode().split(SEP)
    filesize = int(filesize)

    if not os.path.isdir("Download"):
        os.mkdir("Download")

    time.sleep(threshold)

    total = 0
    progress.update(0)
    progress = tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)

    with open("." + os.sep + "Download" + os.sep + filename, 'wb') as f:
        for _ in progress:
            while total != filesize:
                data = conn.recv(BUFFER_SIZE)
                f.write(data)
                if total == filesize:
                    break
                progress.update(len(data))
                total += len(data)
    f.close()
    print(center_title('Successfully get the file',74))
    #conn.shutdown(SHUT_RDWR)
    conn.close()


def list_files(conn):
    conn.send(str("list_dir" + SEP + "None" + SEP + "None").encode(encoding=encoding))
    list_f = conn.recv(BUFFER_SIZE).decode().split(SEP_ADG)
    files = {k: v for k, v in enumerate(list_f, start=1)}
    for key in files:
        print(str(key)+'\t'+files[key])
    return files


def stream_specific(conn):
    files = list_files(conn)
    chosen = files[handle_choice_menu(len(files))]
    conn.send(str("streaming" + SEP + f'"{chosen}"' + SEP + "None").encode(encoding=encoding))
    return


def delete_my_file(conn):
    files = list_files(conn)
    chosen = files[handle_choice_menu(len(files))]
    conn.send(str("delete_file" + SEP + f"{chosen}" + SEP + "None").encode(encoding=encoding))
    cmd, back_msg = conn.recv(BUFFER_SIZE).decode().split(SEP)
    if cmd == 'delete_file':
        print('[i]', center_title(back_msg.capitalize(), 74, 3))
    return


def download_my_file(conn):
    files = list_files(conn)
    chosen = files[handle_choice_menu(len(files))]
    conn.send(str("download_my_file" + SEP + f"{chosen}" + SEP + "None").encode(encoding=encoding))
    time.sleep(0.5)
    filename, filesize = conn.recv(BUFFER_SIZE).decode().split(SEP)
    filesize = int(filesize)

    if not os.path.isdir("Download"):
        os.mkdir("Download")
    time.sleep(1)

    total = 0
    progress = tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)

    with open("." + os.sep + "Download" + os.sep + filename, 'wb') as f:
        for _ in progress:
            while total != filesize:
                data = conn.recv(BUFFER_SIZE)
                f.write(data)
                if total == filesize:
                    break
                progress.update(len(data))
                total += len(data)
    f.close()
    print(center_title('Successfully get the file', 74))
    conn.close()
    return


def edit_cfg(conn, preset: str, param: str, value: str):
    if not os.path.isdir("TEMP"):
        os.mkdir("TEMP")
    cfg_path = (".{}TEMP{}{}".format(os.sep, os.sep, "user_config.cfg"))
    try:
        f_cfg = open(cfg_path, 'r', encoding='UTF-8')
        f_cfg.close()
    except FileNotFoundError:
        conn.send(str("get_cfg" + SEP + "None" + SEP + "None").encode(encoding=encoding))
        time.sleep(2)
        with open(cfg_path, 'wb') as f:
            data = conn.recv(BUFFER_SIZE)
            while data:
                f.write(data)
                data = conn.recv(BUFFER_SIZE)
        f.close()
    cfg.read(cfg_path, encoding="UTF-8")

    cfg.set(preset, param, value)


def print_welcome():
    """
    Function that prints the first menu
    don't :return:
    """
    print(mk_title('welcome', 74))
    print("1. Login")
    print("2. Register")
    print("Type 'exit' to stop")
    print(74 * "-")


def print_menu():
    print(mk_title('menu', 74))
    print("1. Compressor settings")
    print("2. Send file")  # --> -rm after compress or no
    print("3. Stream RTMP")  # --> YouTube/Twitch
    print("4. Download compressed file")
    print("5. Remove compressed file")
    print("Type 'exit' to stop")
    print(74 * "-")


def print_submenu1_1():
    print(mk_title('config settings', 74))
    print("1. Inspect preset")
    print("2. Edit preset")
    print("3. Remove preset")
    print("4. Save & Go back to Main Menu")
    print(74 * "-")


def print_submenu1_2(preset_name: str):
    print(mk_title(f'config {preset_name}', 74))
    print("1. Video bitrate")
    print("2. Audio bitrate")
    print("3. Video Codec")
    print("4. Audio Codec")
        #presets = {9: "ultrafast", 8: "superfast", 7: "veryfast", 6: "faster", 5: "fast", 4: "medium", 3: "slow", 2: "slower", 1: "veryslow", 0: "placebo"}
    print("5. Video Preset") # TODO choose from diz
    print("6. Video downscaling")
    print("6. Go back to Config settings")
    print(74 * "-")


def print_submenu_streaming():
    print(mk_title('streaming settings', 74))
    print("1. List files")
    print("2. Stream file")
    print("3. Go back to Main Menu")
    print(74 * "-")


def center_title(string: str, length: int, offset: int = 0):
    title = string.capitalize()
    f_length = (length - len(title))//2
    title = ((f_length - offset) * ' ') + title
    return title


def mk_title(string: str, length: int):
    if (length - 2) < len(string):
        raise ValueError

    string = string.upper().strip()
    title = ' '
    for i in range(0, len(string)):
        title += string[i] + ' '
        """if i < len(string)-1:
            title += ' '"""
    f_length = length - len(title) - 2
    if f_length % 2 == 0:
        title = ((f_length // 2) * '-') + ' ' + title + ' ' + ((f_length // 2) * '-')
    else:
        title = str((f_length // 2) * '-') + ' ' + title + ' ' + (((f_length // 2) + 1) * '-')

    return str('\n' + title)


def handle_choice_menu(numberOfChoiches):
    """
    function to handle n menu choices
    :return: the choice made by user
    """
    done = False
    while not done:
        choice = input("Enter your choice [1-%d]: " % numberOfChoiches)
        try:
            choice = int(choice)
            done = choice >= 1 or choice <= numberOfChoiches
        except ValueError:
            try:
                done = choice[0].lower() == 'e'
            except IndexError:
                pass
    return choice
    
def main():
    serverSocket = socket(AF_INET, SOCK_STREAM)
    default_port = 13000
    serverSocket.bind((IP, default_port))
    serverSocket.listen()
    print(f"[LISTENING] Server is listening on {IP}:{default_port}")
    while True:
        conn, addr = serverSocket.accept()
        thread = threading.Thread(target=assign_socket, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

def assign_socket(conn, addr):
    print("\t\t open assign_socket")
    serverSocket = socket(AF_INET, SOCK_STREAM)
    server_port = availablePorts[0]

    # TODO SEND TO CLIENT
    conn.send(("new_port" + SEP + f"{server_port}").encode(encoding=encoding))
    # TODO CLOSE OLD CONNECTION
    conn.close()

    availablePorts.remove(server_port)

    serverSocket.bind((IP, server_port))
    serverSocket.listen(1)
    print(f"[LISTENING] Server is listening on {IP}:{server_port} for {addr}")
    conn, addr = serverSocket.accept()

    tcp_socket(conn, addr, server_port)
    print("\t\t close assign_socket")
    # conn.setsockopt(SOL_SOCKET, SO_KEEPALIVE, 1)


def release_socket(conn, port):
    conn.close()
    availablePorts.append(port)
    print("\t\t close assign_socket")
    return port


def tcp_socket(conn, addr, server_port):
    print(f"[NEW CONNECTION] {addr} connected.")
    print("\t\t open tcp_socket")
    os.chdir(HOME)
    user = None

    done = False
    # LISTENER and HANDLING/RESOLVE REQUEST From client
    while not done:
        args = conn.recv(BUFFER_SIZE).decode()  # PROTOCOLLO - RICEVO COMANDO ED ARGS
        print(f"\t{args}")
        # user, pwd = args.split("SEPARATOR")
        try:
            func_handled, arg1, arg2 = map(str, args.split(SEP))
        except ValueError:
            release_socket(conn, server_port)
            return
        if func_handled.lower() == "login":
            login_status = login(user=arg1, pwd=arg2)
            conn.send(f"{login_status}".encode(encoding=encoding))
            if login_status == 0:
                user = arg1
                done = True

        elif func_handled.lower() == "register":
            register_status = register_user(user=arg1, pwd=arg2)
            conn.send(f"{register_status}".encode(encoding=encoding))

    while done:
        print("SUCCESSFULLY LOGGED IN: {}".format(user))
        args = conn.recv(BUFFER_SIZE).decode()  # PROTOCOLLO - RICEVO COMANDO ED ARGS
        try:
            func_handled, arg1, arg2 = map(str, args.split(SEP))
            print(f"AFTER LOGIN: {args}")
        except ValueError:
            release_socket(conn, server_port)
            return

        if func_handled.lower() == "get_cfg":
            ...

        elif func_handled.lower() == "encode":
            # thread = threading.Thread(target=encode, args=(conn, addr, user))
            # thread.start()
            print(f"[ACTIVE THREADS ENCODING] {threading.activeCount() - 1}")
            encode(conn, addr, user=user)
            done = False
            release_socket(conn, server_port)

        elif func_handled.lower() == "list_dir":
            list_file = glob.glob(HOME + "encoded" + os.sep + f"{user}" + os.sep + "*")
            files = str()
            for i in range(len(list_file)):
                files += str(list_file[i][(list_file[i].rfind(os.sep) + 1):])
                if i < len(list_file) - 1:
                    files += SEP_ADG

            conn.send(f"{files}".encode(encoding=encoding))
            print("Lista inviata")

        elif func_handled.lower() == "streaming":
            # TODO parametri da leggere dal config file
            release_socket(conn, server_port)
            try:
                print("\t\tENTER TRY STREAMING")
                """streamingSocket = socket(AF_INET, SOCK_STREAM)
                streaming_port = streamingPorts[0]
                streamingPorts.remove(streaming_port)
                streamingSocket.bind((IP, streaming_port))
                streamingSocket.listen(2)
                print(f"[LISTENING] Server is listening for streaming on {server_port}")
                stream_conn, addr = streamingSocket.accept()"""
                # thread = threading.Thread(target=stream.streaming, args=(f"{user}", f"{arg1}"))
                # thread.start()
                # print(f"[ACTIVE THREADS] {threading.activeCount() - 1}")
                finished = stream.streaming(user=f"{user}", filename=f"{arg1}")
                return
            except KeyError:
                print("Chiave non trovata")
                # TODO ADVERTISE CLIENT OF MISSING KEY
                return

        elif func_handled.lower() == "delete_file":
            try:
                clear_shadows(str(arg1), str(user), f"{HOME}encoded")
                conn.send(str("delete_file" + SEP + "Correctly deleted").encode(encoding=encoding))
            except FileNotFoundError:
                conn.send(str("delete_file" + SEP + "FileNotFoundError").encode(encoding=encoding))
                # TODO invia messaggio al client FileNotFoundError
                pass

        elif func_handled.lower() == "download_my_file":
            filename = arg1
            filesize = calc_filesize(filename, user)
            print(f"\t\t{filename} {filesize}")
            time.sleep(0.5)
            conn.send((f"{filename}" + SEP + f"{filesize}").encode(encoding=encoding))
            os.chdir(f"{HOME}encoded" + os.sep + user)
            with open(f"{filename}",'rb') as f:
                frames = f.read(BUFFER_SIZE)
                while frames:
                    conn.send(frames)
                    frames = f.read(BUFFER_SIZE)
            f.close()
            os.chdir(HOME)
            print(f"[DONE WITH] {user}")
            release_socket(conn, server_port)
            return

        elif func_handled.lower() == "close":
            loop = False
            release_socket(conn, server_port)


def encode(conn, addr, user):
    if not os.path.isdir("received"):
        os.mkdir("received")
    if not os.path.isdir(
            "received" + os.sep + f"{user}"):  # Creazione di una cartella dove mettere tutti i file inviati da un IP
        os.mkdir(
            "received" + os.sep + f"{user}")  # TODO: aggiornarlo per user e non per IP, chiedendo il login al client

    connected = True
    while connected:
        filename = conn.recv(BUFFER_SIZE).decode()
        print(f"\tJUST ARRIVED {filename}")
        path_file = f"{HOME}received{os.sep}{user}{os.sep}{filename}"
        with open(path_file, "wb") as f:
            data = conn.recv(BUFFER_SIZE)
            while data:
                f.write(data)
                data = conn.recv(BUFFER_SIZE)
                if not data:
                    break
        f.close()
        if not os.path.isdir("encoded"):
            os.mkdir("encoded")
        if not os.path.isdir(
                "encoded" + os.sep + f"{user}"):  # Creazione di una cartella dove mettere i file elaborati di un IP
            os.mkdir("encoded" + os.sep + f"{user}")  # TODO: aggiornarlo per user e non per IP

        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(compress_video, f"{filename}", str(user), conn)
            filesize = future.result()
        # filesize = compress_video(filename, str(user), conn)
        conn.send((f"{filename}" + SEP + f"{filesize}").encode(encoding=encoding))
        path_file = f"{HOME}encoded{os.sep}{user}{os.sep}{filename}"
        with open(path_file, 'rb') as f:
            frames = f.read(BUFFER_SIZE)
            while frames:
                conn.send(frames)
                frames = f.read(BUFFER_SIZE)
            f.close()
            print(f"[DONE WITH] {addr}")
            clear_shadows(filename, str(user))
            connected = False
    # conn.close()


def clear_shadows(filename, user, folder=f"{HOME}received"):
    folder = folder + os.sep + user
    print(f"\t\t{folder}\t {filename}")
    os.chdir(folder)
    os.remove(os.path.join(folder, filename))
    if len(os.listdir(folder)) == 0:
        os.rmdir(folder)
    os.chdir(HOME)
    return True


def calc_filesize(filename, user, folder=f"{HOME}encoded"):
    folder = folder + os.sep + user
    print(f"\t\t{folder}\t {filename}")
    os.chdir(folder)
    filesize = os.path.getsize(os.path.join(folder, filename))
    os.chdir(HOME)
    return filesize

# TODO v_bitrate, preset, v_codec, a_bitrate, a_codec
def compress_video(filename: str, user: str, conn, bitrate: int = 1800, threads: int = 0, preset: int = 9):
    print(f"\tTo compress: {filename}")
    cfg = configparser.ConfigParser()  ### Setting parser for language selection
    cfg_path = ('"{}received/{}/{}"'.format(HOME, user, "user_config.cfg"))
    cfg.read(cfg_path, encoding="UTF-8")
    # TODO Finire cfg parser

    presets = {9: "ultrafast", 8: "superfast", 7: "veryfast",
               6: "faster", 5: "fast", 4: "medium", 3: "slow",
               2: "slower", 1: "veryslow", 0: "placebo"}
    preset = presets[preset]
    path = ('"{}received/{}/{}"'.format(HOME, user, filename))
    output = ('"{}encoded/{}/{}"'.format(HOME, user, filename))
    print(f"\n\t{path}\n\t{filename}")
    cmd = f"ffmpeg -i {path} -b:v {bitrate}k -c:v libx264 -threads {threads} -preset {preset} {output}"
    print(f"{cmd}")
    result = subprocess.Popen(cmd, shell=True)
    # print("\n\n\n\n",result.poll(),"\n\n\n\n")
    while result.poll() is None:
        # print("Processing:", f"{result.poll()}")
        time.sleep(10)
        conn.setsockopt(SOL_SOCKET, SO_KEEPALIVE, 1)
        # TODO Keep alive non funziona
    filesize = os.path.getsize(os.path.join('%sencoded/%s', '%s'.replace(" ", "\\")) % (HOME, str(user), str(filename)))
    return filesize


########################## L O G I N   F U N C T I O N S #############################
def register_user(user, pwd):
    try:
        js_file = open("auth.json", 'r', encoding=encoding)
        users = json.load(js_file)
        js_file.close()
    except FileNotFoundError:
        users = dict()

    if user == '' or pwd == '':
        # "EMPTY FIELD" ERROR CODE -2
        return -2

    if user not in users.keys():
        users[user] = dict()
        users[user]['pwd'] = pwd
    else:
        # "ALREADY IN USE" ERROR CODE -1
        # UTENTE GIÀ ESISTENTE
        return -1

    js_file = open("auth.json", 'w', encoding=encoding)
    json.dump(obj=users, fp=js_file, indent=2)
    js_file.close()
    return 0


def login(user, pwd):
    try:
        js_file = open("auth.json", 'r', encoding=encoding)
        users = json.load(js_file)
        js_file.close()
    except FileNotFoundError:
        # "PLEASE FIRST REGISTER YOUR USER" ERROR CODE -1
        return -1

    if user not in users.keys():
        # "WRONG USER" ERROR CODE -2
        return -2
    elif users[user]['pwd'] == pwd:
        return 0
    else:
        # "WRONG PASSWORD" ERROR CODE -3
        return -3


if __name__ == '__main__':
    main()

```
----
                    
###*Tables*
- Principal Function:
                    

| Function name | Description                    |
| ------------- | ------------------------------ |
| `def main()`      | **funzione cardine che esegue il programma **|
| `def main()`   | **mette in ascolto il server sulla porta di defeault; attiva la connessione**|
| `def assign_socket()`      | **richiesta al client di una nuova porta; mette in ascolto il server con l'IP e chiude l'assign**|
| `def release_socket()`   | **chiude la connessione e restituisce la porta**|
| `def tcp_socket()`      | **instaura una connessione tcp; fa un controllo sullo status della registrazione; scarica il file e chiude la connessione**|
| `def encode()`   | **crea una cartella dove mettere tutti i file inviati da un IP e li aggiorna per utente non per user previa registrazione client; crea una cartella dove mettere i file elaborati di un IP e li aggiorna per utente non per IP**|
| `def clear_shadow()`      | **stampa la cartella con il nome del file**|
| `def calc_filesize()`   | **preso in input il filename e la cartella, restituisce la grandezza del file**|
| `def compress_video()`      | **presa in input la stringa del filename, la comprime e restituisce il filesize**|
| `def register_user()`   | **fase di registrazione**|
| `def login()`      | **login dell'utente tramite user e password**|
| `def fetch_port()`   | **è l'equivalente di assign però lato server**|
| `def connect_to_server()`      | **comunica con assign al fine di connettersi al server**|
| `def send_file()`   | **ricezione filename, lo scarica e printa un messaggio di avvenuta ricezione del file**|
| `def list_files()`      | **prende in input la conn. , invia una lista di file e restituisce quest'ultimo**|
| `def stream_specific()`   | ****|
| `def delete_my_file()`      | **preso un file da quelli scaricati, elimina il mio file**|
| `def download_my_file()`   | **il file dopo essere stato inviato e ricevuto, viene scaricato**|
| `def edit_cfg()`   | ****|
| `def print_welcome()`   | **printa welcome + im menù inziale**|
| `def print_menu()`   | **printa il menù nel quale l'utente sceglie quale azione esguire**|
| `def print_submenu_1()`   | **sottomenù relativo al menù precedente nel quale vengono illustrate le azioni**|
| `def print_submenu_2()`   | **scegliere cosa comprimere e in che modo comprimere un file audio o video("ultrafast",...,"placebo")**|
| `def print_submenu_streaming()`   | **streamma il sottomenù**|
| `def center_title()`   | **restituisce il titolo**|
| `def handle_choice_menu()`   | **restituisce la scelta fatta dall'utente**|

----

###*End*


[Python 3.9.X]: <https://www.python.org/downloads/release/python-390/>
[OS]: <https://docs.python.org/3/library/os.html>
[Time]: <https://docs.python.org/3/library/time.html> 
[Tqdm]: <https://pypi.org/project/tqdm/>
[Socket]: <https://docs.python.org/3/library/socket.html> 
[Subprocess]: <https://docs.python.org/3/library/subprocess.html>
[Threading]: <https://docs.python.org/3/library/threading.html>
[Json]: <https://docs.python.org/3/library/json.html>
[Tkinter]: <https://docs.python.org/3/library/tkinter.html> 
[Configparser]: <https://docs.python.org/3/library/configparser.html>
