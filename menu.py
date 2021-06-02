import configparser
import os

import backend

HOME = os.getcwd()


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
