import elgamal
import utils

menu_options = {
    1: 'Show users with their public keys',
    2: 'Send an encrypted message to a user.',
    3: 'Sign a message.',
    4: 'Exit.'
}

usernames = ["Me", "Alice", "Bob"]


# Call in a loop to create terminal progress bar
# @params:
#  iteration   - Required  : current iteration (Int)
#  total       - Required  : total iterations (Int)
#  prefix      - Optional  : prefix string (Str)
#  suffix      - Optional  : suffix string (Str)
#  decimals    - Optional  : number of decimals in percent complete (Int)
#  length      - Optional  : character length of bar (Int)
#  fill        - Optional  : bar fill character (Str)
#  printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
def printProgressBar(iteration, total, prefix='', suffix='', decimals=1,
                     length=100, fill='█', printEnd="\r"):

    percent = ("{0:." + str(decimals) + "f}").format(100 *
                                                     (iteration / float(total))
                                                     )
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()


def print_menu():
    print(" Menu:")
    for key in menu_options.keys():
        print(" ", key, menu_options[key])
    print()


def show_users(users: list):
    print("\n User information:")
    for u in users:
        print()
        username = u["user"]
        p, g, ga = u["public"]
        print(f"  {username}")
        print(f"    Prime: {p}")
        print(f"    Generator: {g}")
        print(f"    g^a mod p: {ga}")
    print()


def send_encrypted_message(users: list):
    print("\n Who do you want to send the message to? ")
    i: int = 1
    while True:
        for user in users:
            username = user["user"]
            print(f"  {i} {username} ")
            i = i + 1
        print()
        option = int(input(" Option: "))

        if option <= len(users) and option > 0:
            public_dest = users[option - 1]["public"]
            break
        else:
            print(
                f""" Invalid option. Please introduce a number
                between 1 and {len(users)}""")

    message = input(" Enter the message: ")

    # Divide the message into ascii blocks
    msg = utils.message_to_ascii_blocks(message, 2)

    # Encrypt each block
    encrypted_msg = list()
    for b in msg:
        encrypted_msg.append(elgamal.encrypt(b, public_dest))

    print(f" The encrypted message is:\n {encrypted_msg}\n")
    print(" All users will try to decrypt the message\n")

    for user in users:
        decrypt_msg = list()
        username = user["user"]
        public = user["public"]
        private = user["private"]
        for b in encrypted_msg:
            x, y = b
            decrypt_msg.append(elgamal.decrypt(x, y, public, private))
        print(f" User {username} sees:")
        print(utils.ascii_blocks_to_message(decrypt_msg, 2))
        print()


def sign_message(me):
    message = input(" Enter the message you want to sign: ")
    H = hash

    private, public = me["private"], me["public"]

    p, _, _ = public
    m = H(message)
    print(f"\n Hash(message) = {m}\n")

    signature = elgamal.sign(public, private, m)
    r, s = signature

    print(f" Signature = (r, s)\n    r = {r}\n    s = {s}\n")

    if elgamal.verify(public, signature, m):
        print(" Signature verified.")
    return


def generate_users(n_bits: int):
    users = list()
    n_users = len(usernames)
    i: int = 0
    print()
    printProgressBar(i, n_users, prefix=' Generating users:',
                     suffix='Complete', length=30)
    for name in usernames:
        i = i + 1
        public, private = elgamal.generate_keys(n_bits)
        users.append({"user": name,
                     "public": public, "private": private})
        printProgressBar(i, n_users, prefix=' Generating users:',
                         suffix='Complete', length=30)
    return users


def header():
    print("                                                             ")
    print(" ███████╗██╗      ██████╗  █████╗ ███╗   ███╗ █████╗ ██╗     ")
    print(" ██╔════╝██║     ██╔════╝ ██╔══██╗████╗ ████║██╔══██╗██║     ")
    print(" █████╗  ██║     ██║  ███╗███████║██╔████╔██║███████║██║     ")
    print(" ██╔══╝  ██║     ██║   ██║██╔══██║██║╚██╔╝██║██╔══██║██║     ")
    print(" ███████╗███████╗╚██████╔╝██║  ██║██║ ╚═╝ ██║██║  ██║███████╗")
    print(" ╚══════╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝")
    print("                    Signature Scheme                         ")
    print("      Sergio Domínguez   Javier Lobillo   Marina Musse       ")
    print("                                                             ")
    print("                     2022  /  2023                           ")
    print("                                                             ")
    print("                                                             ")
    print("                                                             ")


def main():
    header()
    n_bits: int = int(input(" Enter the key length: "))
    users = generate_users(n_bits)
    me = users.pop(0)

    while (True):
        print_menu()
        option: int = int(input(" Option: "))
        if option == 1:
            show_users(users)
        elif option == 2:
            send_encrypted_message(users)
        elif option == 3:
            sign_message(me)
        elif option == 4:
            break
        else:
            print("Invalid option. Please introduce a number between 1 and 4")


main()
