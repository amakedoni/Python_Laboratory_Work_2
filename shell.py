import os
from core.commands import ShellCommands
from core.logger import setup_logger
from plugins.history import save_command, show_history, undo
from plugins import archive, grep

# Настройка логгера
logger = setup_logger()
shell = ShellCommands(logger)

def main():
    while True:
        try:
            cmd_input = input("MiniShell > ").strip()
            if not cmd_input:
                continue

            # Сохраняем в историю
            save_command(cmd_input)

            parts = cmd_input.split()
            cmd = parts[0]
            args = parts[1:]

            # Основные команды
            if cmd == "ls":
                shell.ls(args)
            elif cmd == "cd":
                shell.cd(args)
            elif cmd == "cat":
                shell.cat(args)
            elif cmd == "cp":
                shell.cp(args)
            elif cmd == "mv":
                shell.mv(args)
            elif cmd == "rm":
                shell.rm(args)
            elif cmd == "history":
                show_history()
            elif cmd == "undo":
                undo(logger)
            # Плагины: архивы
            elif cmd in ("zip", "unzip", "tar", "untar"):
                archive.handle(cmd, args, logger)
            # Плагины: поиск по содержимому
            elif cmd == "grep":
                grep.handle(args, logger)
            elif cmd in ("exit", "quit"):
                print("Выход.")
                break
            else:
                print(f"Неизвестная команда: {cmd}")
                logger.error(f"Неизвестная команда: {cmd_input}")

        except KeyboardInterrupt:
            print("\nВыход.")
            break
        except Exception as e:
            print(f"Ошибка: {e}")
            logger.error(f"shell ERROR: {e}")

if __name__ == "__main__":
    main()
