import json


########################## L O G I N   F U N C T I O N S #############################
def register_user(user, pwd):
    try:
        js_file = open("auth.json", 'r', encoding="utf-8")
        users = json.load(js_file)
        js_file.close()
    except FileNotFoundError:
        users = dict()

    if user not in users.keys():
        users[user] = dict()
        users[user]['pwd'] = pwd
    else:
        # UTENTE GIÀ ESISTENTE
        return False

    js_file = open("auth.json", 'w', encoding="utf-8")
    json.dump(obj=users, fp=js_file, indent=2)
    js_file.close()
    return True


def login(user, pwd):
    try:
        js_file = open("auth.json", 'r', encoding="utf-8")
        users = json.load(js_file)
        js_file.close()
    except FileNotFoundError:
        # "PLEASE FIRST REGISTER YOUR USER" ERROR CODE -1
        return -1

    if user not in users.keys():
        # "WRONG USER" ERROR CODE -2
        return -2
    elif users[user]['pwd'] == pwd:
        return True
    else:
        # "WRONG PASSWORD" ERROR CODE -3
        return -3


def main():
    finito = False
    while not finito:
        user = input("[i] Enter username: ")
        pwd = input("[i] Enter password: ")
        finito = register_user(user,pwd)

if __name__ == '__main__':
    main()