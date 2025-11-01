import os
import shutil
from datetime import datetime
from colorama import Fore, Style
from plugins.history import register_undo_action

def parse_args(args: list, valid_options: list):
    options, paths = [], []
    for arg in args:
        if arg in valid_options:
            options.append(arg)
        else:
            paths.append(arg)
    return options, paths

class ShellCommands:
    def __init__(self, logger):
        self.logger = logger

    def ls(self, args):
        options, paths = parse_args(args, ["-l"])
        detailed = "-l" in options
        path = paths[0] if paths else "."
        try:
            entries = os.listdir(path)
            for entry in entries:
                full_path = os.path.join(path, entry)
                if detailed:
                    stat = os.stat(full_path)
                    size = stat.st_size
                    mtime = datetime.fromtimestamp(stat.st_mtime)
                    mode = oct(stat.st_mode)[-3:]
                    print(f"{entry:30} {size:10} bytes  {mtime}  {mode}")
                else:
                    print(entry)
            self.logger.info(f"ls {' '.join(args)} OK")
        except Exception as e:
            print(f"{Fore.RED}Ошибка: {e}{Style.RESET_ALL}")
            self.logger.error(f"ls {' '.join(args)} ERROR: {e}")

    def cd(self, args):
        path = args[0] if args else os.path.expanduser("~")
        try:
            os.chdir(path)
            self.logger.info(f"cd {path} OK")
        except Exception as e:
            print(f"{Fore.RED}Ошибка: {e}{Style.RESET_ALL}")
            self.logger.error(f"cd {path} ERROR: {e}")

    def cat(self, args):
        if not args:
            print("Укажите файл.")
            return
        filename = args[0]
        try:
            with open(filename, "r", encoding="utf-8") as f:
                print(f.read())
            self.logger.info(f"cat {filename} OK")
        except Exception as e:
            print(f"{Fore.RED}Ошибка: {e}{Style.RESET_ALL}")
            self.logger.error(f"cat {filename} ERROR: {e}")

    def cp(self, args):
        options, paths = parse_args(args, ["-r"])
        recursive = "-r" in options
        if len(paths) < 2:
            print("Использование: cp [-r] <источник> <назначение>")
            return
        src, dst = paths[:2]
        try:
            if recursive and os.path.isdir(src):
                shutil.copytree(src, dst, dirs_exist_ok=True)
            else:
                shutil.copy2(src, dst)
            register_undo_action("cp", src, dst)
            print("Копирование успешно.")
            self.logger.info(f"cp {src} -> {dst} OK")
        except Exception as e:
            print(f"{Fore.RED}Ошибка: {e}{Style.RESET_ALL}")
            self.logger.error(f"cp {src} -> {dst} ERROR: {e}")

    def mv(self, args):
        if len(args) < 2:
            print("Использование: mv <источник> <назначение>")
            return
        src, dst = args[:2]
        try:
            shutil.move(src, dst)
            register_undo_action("mv", src, dst)
            print("Перемещение успешно.")
            self.logger.info(f"mv {src} -> {dst} OK")
        except Exception as e:
            print(f"{Fore.RED}Ошибка: {e}{Style.RESET_ALL}")
            self.logger.error(f"mv {src} -> {dst} ERROR: {e}")

    def rm(self, args):
        options, paths = parse_args(args, ["-r"])
        recursive = "-r" in options
        if not paths:
            print("Использование: rm [-r] <файл/каталог>")
            return
        target = paths[0]
        if target in ("/", ".."):
            print("Удаление запрещено.")
            return

        try:
            trash_dir = os.path.join("data", ".trash")
            os.makedirs(trash_dir, exist_ok=True)
            backup = os.path.join(trash_dir, os.path.basename(target))

            if recursive and os.path.isdir(target):
                confirm = input(f"Удалить каталог {target}? (y/n): ")
                if confirm.lower() != "y":
                    print("Отмена.")
                    return
                shutil.copytree(target, backup, dirs_exist_ok=True)
                shutil.rmtree(target)
            else:
                shutil.copy2(target, backup)
                os.remove(target)

            register_undo_action("rm", target, backup)
            print("Удаление успешно.")
            self.logger.info(f"rm {target} OK")
        except Exception as e:
            print(f"{Fore.RED}Ошибка: {e}{Style.RESET_ALL}")
            self.logger.error(f"rm {target} ERROR: {e}")
