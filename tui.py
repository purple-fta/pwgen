import pwinput
import hashlib
import pyperclip
from colorama import Fore, init

from lib.repository import Repository
from lib.config import Config
from lib.generator import generate_password
from lib.input_lib import input_lib

# TODO: Docs


def main():
    init()

    config = Config()

    master_key = pwinput.pwinput(Fore.LIGHTMAGENTA_EX + "Master Key: " + Fore.YELLOW)
    print(Fore.RESET + "\n" + "\x1B[A", end='')

    if config.double_entry_master_key:
        second_master_key = pwinput.pwinput(Fore.LIGHTMAGENTA_EX + "     Again: " + Fore.YELLOW)
        print(Fore.RESET + "\n" + "\x1B[A", end='')

        if second_master_key != master_key:
            print(Fore.LIGHTRED_EX + "Master passwords do not match")
            return

    if config.master_key_hash != "None":
        if hashlib.sha256(master_key.encode('utf-8')).hexdigest() != config.master_key_hash:
            print(Fore.LIGHTRED_EX + "The hash of the entered master password does not match the hash in the config")
            return

    repo = Repository.load(config.password_base_path)
    services = [i for i in repo]

    service_name = input_lib.search_input("Service name: ", services)

    if service_name in services:
        n = repo[service_name]["n"]
        s = repo[service_name]["s"]
        i = repo[service_name]["i"]
    else:
        n = input_lib.counter("Lenght: ", config.default_password_lenght, 1, 256) 
        s = input_lib.checker("Special Symbols: ", config.use_special_symbols_by_default)
        i = input_lib.counter("Iteration: ", 1, 1, 256) 

    Repository.save(config.password_base_path, service_name, n, s, i)

    password = generate_password(master_key, service_name, n, s, i)

    pyperclip.copy(password)
    print(Fore.GREEN + "Password copied")
    print()


main()

