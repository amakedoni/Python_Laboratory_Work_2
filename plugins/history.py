import os
import json
import shutil

HISTORY_FILE = os.path.join("data", ".history")
UNDO_FILE = os.path.join("data", ".undo.json")
TRASH_DIR = os.path.join("data", ".trash")

os.makedirs("data", exist_ok=True)
os.makedirs(TRASH_DIR, exist_ok=True)


def save_command(cmd: str):
    with open(HISTORY_FILE, "a", encoding="utf-8") as f:
        f.write(cmd + "\n")


def show_history(n: int = 20):
    if not os.path.exists(HISTORY_FILE):
        print("История пуста.")
        return
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
    for i, line in enumerate(lines[-n:], 1):
        print(f"{i:3}: {line.strip()}")


def register_undo_action(action: str, src: str, dst: str = None):
    record = {"action": action, "src": src, "dst": dst}
    with open(UNDO_FILE, "w", encoding="utf-8") as f:
        json.dump(record, f)


def undo(logger):
    if not os.path.exists(UNDO_FILE):
        print("Нет действий для отмены.")
        return
    with open(UNDO_FILE, "r", encoding="utf-8") as f:
        record = json.load(f)

    action, src, dst = record.get("action"), record.get("src"), record.get("dst")

    try:
        if action == "cp":
            if dst and os.path.exists(dst):
                if os.path.isdir(dst):
                    shutil.rmtree(dst)
                else:
                    os.remove(dst)
            print(f"Отменено копирование {dst}.")
        elif action == "mv":
            if dst and os.path.exists(dst):
                shutil.move(dst, src)
                print(f"Отменено перемещение {dst} -> {src}.")
        elif action == "rm":
            if dst and os.path.exists(dst):
                restored_path = src
                if os.path.exists(restored_path):
                    restored_path += "_restored"
                shutil.move(dst, restored_path)
                print(f"Восстановлено {restored_path}.")
        else:
            print(f"Неизвестное действие: {action}")

        os.remove(UNDO_FILE)
        logger.info(f"undo {action} OK")
    except Exception as e:
        print(f"Ошибка undo: {e}")
        logger.error(f"undo ERROR: {e}")
