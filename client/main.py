import configparser
import os
import time

import backend

HOME = os.getcwd()


def main(user=None, pwd=None):
    """
    Function main that execute the program
    :return:
    """
    # CONNESSIONE AL SERVER E LOGIN
    try:
        conn = backend.connect_to_server(port=13000)
    except ConnectionRefusedError:
        time.sleep(1)
        return main()

    try:
        done = loop = False
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
                try:
                    conn = backend.connect_to_server(port=13000)
                except ConnectionRefusedError:
                    time.sleep(1)
                    main()

            elif (choice.lower())[0] == 'e':
                print("[i] Bye bye! See you soon.")
                conn.close()
                print("Closed manually")
                done = True
                loop = False
                break
    except KeyboardInterrupt:
        conn.close()
        raise KeyboardInterrupt
    try:
        while loop:
            backend.print_menu()
            choice = backend.handle_choice_menu(5)

            if choice == 1:  # Compressor Settings
                done = False
                while not done:
                    backend.print_submenu1_1()
                    choice = backend.handle_choice_menu(4)

                    if choice == 1:
                        backend.alter_config(conn, cmd="insert_cfg")

                    elif choice == 2:
                        backend.print_minimenu()
                        choice = backend.handle_choice_menu(4)

                        if choice == 1:
                            backend.alter_config(conn, cmd="edit_cfg")

                        elif choice == 2:
                            backend.alter_config(conn, cmd="delete_cfg")
                        elif choice == 3:
                            backend.alter_config(conn, cmd="delete_val")
                        else:
                            print("[i] Going back to Main Menu")
                            break

                    elif choice == 3:
                        backend.alter_config(conn, cmd="restore_def_config")

                    else:
                        print("[i] Going back to Main Menu")
                        break

                try:
                    conn = backend.connect_to_server(port=13000)
                except ConnectionRefusedError:
                    time.sleep(1)
                    return main(user, pwd)
                chk, user, pwd = backend.login(conn, user, pwd)
                if not chk:
                    loop = False
                    break

            elif choice == 2:
                backend.send_file(conn)
                # conn.close()
                try:
                    conn = backend.connect_to_server(port=13000)
                except ConnectionRefusedError:
                    time.sleep(1)
                    main(user, pwd)
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
                        try:
                            conn = backend.connect_to_server(port=13000)
                        except ConnectionRefusedError:
                            time.sleep(1)
                            main(user, pwd)
                        chk, user, pwd = backend.login(conn, user, pwd)
                        if not chk:
                            loop = False
                            break

                    else:
                        print("[i] Going back to Main Menu")
                        break

            elif choice == 4:
                backend.download_my_file(conn)
                try:
                    conn = backend.connect_to_server(port=13000)
                except ConnectionRefusedError:
                    time.sleep(1)
                    main(user, pwd)
                chk, user, pwd = backend.login(conn, user, pwd)
                if not chk:
                    loop = False
                    break

            elif choice == 5:
                # Delete compressed file
                backend.delete_my_file(conn)

            elif (choice.lower())[0] == 'e':
                conn.close()
                print("[i] Bye bye! See you soon.")
                break

            else:
                print("[i] Invalid assignment, please pay attention")
    except KeyboardInterrupt:
        conn.close()
        raise KeyboardInterrupt


if __name__ == '__main__':
    main()
