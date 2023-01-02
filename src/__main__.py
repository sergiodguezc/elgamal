import elgamal


def main():
    header()
    n_bits: int = int(input(" Enter the key length: "))
    message = input(" Enter the message: ")
    H = hash

    params = elgamal.generate_parameters(n_bits, H)
    private, public = elgamal.generate_keys(params)

    print(f"\n Private key: {private} \n Public key: {public}\n")

    p, _, _ = params
    m = H(message)
    print(f" Hash(message) = {m}\n")

    signature = elgamal.sign(params, private, m)
    r, s = signature

    print(f" Signature = (r, s)\n    r = {r}\n    s = {s}\n")

    if elgamal.verify(params, public, signature, m):
        print(" Signature verified.")

    return


def header() -> None:
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


main()
