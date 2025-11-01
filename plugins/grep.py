import os
import re

def handle(args, logger):
    if len(args) < 2:
        print("Использование: grep <pattern> <path> [-r] [-i]")
        return

    pattern = args[0]
    path = args[1]
    recursive = "-r" in args
    ignore_case = "-i" in args
    flags = re.IGNORECASE if ignore_case else 0

    try:
        for root, dirs, files in os.walk(path):
            for file in files:
                full_path = os.path.join(root, file)
                try:
                    with open(full_path, "r", encoding="utf-8") as f:
                        for i, line in enumerate(f, 1):
                            if re.search(pattern, line, flags):
                                print(f"{full_path}:{i}: {line.strip()}")
                except Exception:
                    continue
            if not recursive:
                break
        logger.info(f"grep {pattern} {path} OK")
    except Exception as e:
        print(f"Ошибка: {e}")
        logger.error(f"grep {pattern} {path} ERROR: {e}")
