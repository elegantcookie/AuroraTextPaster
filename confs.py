import os


class Configurator:
    """ Настраивает конфиг """
    def __init__(self):
        self.flags = {}
        self.config_name = 'config.txt'
        if not self._config_exists():
            self._create_default_config()
        self._load_config()

    def add_flag(self, key, val):
        self.flags[key] = val

    def edit_flag(self, key, new_val):
        self.flags[key] = new_val
        self._refresh_flags()

    def _refresh_flags(self):
        """ Мне было лень что-то делать, поэтому функция просто перезаписывает весь конфиг """
        with open(self.config_name, 'w', encoding='utf8') as file:
            for key in self.flags.keys():
                file.write(f'{key}:{self.flags[key]}')

    def _create_default_config(self):
        """ Создаёт конфиг по умолчанию, если его нет"""
        with open(self.config_name, 'w', encoding='utf8') as file:
            key = "bind_key"
            val = "<ctrl>+P\n"
            self.add_flag(key, val)
            file.write(f"{key}:{val}")

    def _config_exists(self):
        if os.path.exists(self.config_name):
            return True
        return False

    def _load_config(self):
        with open(self.config_name, 'r', encoding='utf8') as file:
            contents = file.readlines()
            self.flags = self._parse_config(contents)

    def _parse_config(self, contents):
        flags = {}
        for i in range(len(contents)):
            key, val = contents[i].split(':')
            flags[key] = val.rstrip('\n')
        return flags
