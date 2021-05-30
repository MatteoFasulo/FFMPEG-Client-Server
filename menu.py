import configparser
import client_latest

cfg = configparser.ConfigParser()  ### Setting parser for config file


def main():
    """
    Function main that execute the program
    :return:
    """
    loop = True
    while loop:
        print_menu()
        choice = handle_choice_menu(5)

        if choice == 1:  # Compressor Settings
            done = False
            while not done:
                print_submenu1_1()
                choice = handle_choice_menu(6)

                # create preset
                # edit preset
                #
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
            done = False
            while not done:
                client_latest.main()

        elif choice == 3:
            done = False
            while not done:
                choice = handle_choice_menu()

                if choice == 1:
                    ...

                elif choice == 3:
                    print("[i] Going back to Main Menu")
                    done = True
                    break

                else:
                    print("[i] Invalid assignment, please pay attention")

        elif choice == 4:
            ...

        elif choice == 5:
            ...

        elif (choice.lower())[0] == 'e':
            print("[i] Bye bye! See you soon.")
            break

        else:
            print("[i] Invalid assignment, please pay attention")


def print_menu():
    """
    Function that prints the first menu
    don't :return:
    """
    print("\n" + 32 * "-", "M E N U", 32 * "-")
    print("1. Compressor settings")
    print("2. Send file")  # --> -rm after compress or no
    print("3. Stream HLS/RTMP")  # --> YouTube/Twitch
    print("4. Download compressed file")  # --> if not yet rm
    print("5. Remove compressed file")
    print("Type 'exit' to stop")
    print(73 * "-")


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
            done = choice[0].lower() == 'e'
    return choice


def print_submenu1_1():
    print("\n" + 21 * "-", "C O N F I G   S E T T I N G S", 21 * "-")
    print("1. Video bitrate")
    print("2. Audio bitrate")
    print("3. Video Codec")
    print("4. Audio Codec")
    print("5. Video downscaling")
    print("6. Save & Go back to Main Menu")
    print(73 * "-")


def set_cfg(preset: str, param: str, value: str):
    try:
        f_cfg = open("user_config.cfg", 'r', encoding='UTF-8')
        f_cfg.close()
    except FileNotFoundError:
        f_cfg = open("user_config.cfg", 'w', encoding='UTF-8')
        f_cfg.close()
    cfg_path = ("./TEMP/{}".format("user_config.cfg"))
    cfg.read(cfg_path, encoding="UTF-8")

    cfg.set(preset, param, value)


if __name__ == '__main__':
    main()
