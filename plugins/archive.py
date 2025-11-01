import shutil
import tarfile
import zipfile

def handle(cmd, args, logger):
    try:
        if cmd == "zip":
            if len(args) < 2:
                print("Использование: zip <folder> <archive.zip>")
                return
            folder, archive = args
            shutil.make_archive(archive.replace(".zip", ""), 'zip', folder)
            print(f"ZIP архив {archive} создан.")
        elif cmd == "unzip":
            if len(args) < 1:
                print("Использование: unzip <archive.zip>")
                return
            archive = args[0]
            with zipfile.ZipFile(archive, 'r') as zf:
                zf.extractall()
            print(f"Архив {archive} распакован.")
        elif cmd == "tar":
            if len(args) < 2:
                print("Использование: tar <folder> <archive.tar.gz>")
                return
            folder, archive = args
            with tarfile.open(archive, "w:gz") as tar:
                tar.add(folder, arcname=".")
            print(f"TAR архив {archive} создан.")
        elif cmd == "untar":
            if len(args) < 1:
                print("Использование: untar <archive.tar.gz>")
                return
            archive = args[0]
            with tarfile.open(archive, "r:gz") as tar:
                tar.extractall()
            print(f"Архив {archive} распакован.")
        logger.info(f"{cmd} {' '.join(args)} OK")
    except Exception as e:
        print(f"Ошибка: {e}")
        logger.error(f"{cmd} {' '.join(args)} ERROR: {e}")
