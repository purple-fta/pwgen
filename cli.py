import click
import pwinput
import pyperclip

from lib.generator import generate_password


@click.command()
# TODO: Add help
@click.option('-n', default=16, help='/')
@click.option('-s', is_flag=True, help='.')
@click.option('-i', default=1, help='.')
def main(n: int, s: bool, i: int):
    master_key = pwinput.pwinput("Master Key: ")
    service_name = input("Service Name: ")

    password = generate_password(master_key, service_name, n, s, i)

    pyperclip.copy(password)
    print("Password copied")


if __name__ == '__main__':
    main()
