import configparser
import math
import os
import time
from socket import *
from tkinter import Tk
from tkinter.filedialog import askopenfilename

from tqdm import tqdm

########################## STATIC INT #############################
serverName = "128.116.135.192" #"128.116.135.192"
BUFFER_SIZE = 1024 * 4
encoding = 'utf-8'
SEP = "<SEPARATOR>"
SEP_ADG = "><SEP><"
threshold = math.log2(6)
cfg = configparser.ConfigParser()  #parser for config file


########################## L O G I N   F U N C T I O N S #############################
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
