# TODO Add docs 
import os
import configparser

# TODO: .ini полное говно, проще, удобнее использовать .py

DEFAULT_CONFIG = '''
[config]
; Дважды вводить мастер ключ, чтобы избежать ошибки в написании
double_entry_master_key = true

; Если тут введён хэш (по умолчанию None), то он сравниваеться с хэшом масер ключа, при его вводею.
; Хэш является результатом работы функции hashlib.sha256(master_key.encode('utf-8')).hexdigest()
master_key_hash = None 

; Путь к фалу базы паролей
password_base_path = "~/passes.json"

; Длинна пароля по умолчанию
defautl_password_lenght = 16

; Использовать ли специальные символы по умалчанию
use_special_symbols_by_default = false

'''


class Config:
    config_dir_name = "passgen"
    config_file_name = "config.ini"

    def __init__(self):
        self.double_entry_master_key = True
        self.master_key_hash = None
        self.password_base_path = "~/passes.json"
        self.default_password_lenght = 16
        self.use_special_symbols_by_default = False

        if not self.is_config_exists():
            self.generate_default_config()
        else:
            self.load_config()

    def generate_default_config(self):
        with open(f"{os.path.expanduser('~')}/.config/{self.config_dir_name}/{self.config_file_name}", "x") as f:
           f.write(DEFAULT_CONFIG)

    def is_config_exists(self):
        # Config directory check
        if os.path.isdir(f"{os.path.expanduser('~')}/.config/{self.config_dir_name}"):
            # Config file check
            if os.path.isfile(f"{os.path.expanduser('~')}/.config/{self.config_dir_name}/{self.config_file_name}"):
                return True
        else:
            os.mkdir(f"{os.path.expanduser('~')}/.config/{self.config_dir_name}")

        return False

    def load_config(self):
        parser = configparser.ConfigParser()
        parser.read(f"{os.path.expanduser('~')}/.config/{self.config_dir_name}/{self.config_file_name}")
        
        self.double_entry_master_key = parser.getboolean("config", 'double_entry_master_key')
        self.master_key_hash = parser.get('config', 'master_key_hash')
        self.password_base_path = parser.get('config', 'password_base_path')
        self.password_base_path = self.password_base_path.replace('~', os.path.expanduser('~'))
        self.password_base_path = self.password_base_path[1:-1]
        self.default_password_lenght = parser.getint('config', 'default_password_lenght')
        self.use_special_symbols_by_default = parser.getboolean('config', 'use_special_symbols_by_default')

