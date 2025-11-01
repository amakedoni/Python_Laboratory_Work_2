# MiniShell — Мини-оболочка с файловыми командами

## Описание

MiniShell — минимальная оболочка на Python, позволяющая работать с файловой системой без использования внешних команд.

Поддерживаются:
```
Основные файловые команды (ls, cd, cat, cp, mv, rm)

История команд и возможность отмены последнего действия (undo)

Работа с архивами (zip, unzip, tar, untar)

Поиск по содержимому файлов (grep)

Логирование всех действий
```
Проект кроссплатформенный — работает на Windows, macOS и Linux.

## Структура проекта

```
mini_shell/
│
├── shell.py                     # Точка входа — запуск оболочки
├── core/
│   ├── __init__.py
│   ├── commands.py              # Реализация базовых команд
│   ├── logger.py                # Логирование
│   └── utils.py                 # Вспомогательные функции (опционально)
├── plugins/
│   ├── __init__.py
│   ├── archive.py               # ZIP/TAR архивы
│   ├── grep.py                  # Поиск по содержимому
│   └── history.py               # История команд и undo
├── data/
│   ├── .history                 # История команд
│   └── .trash/                  # Корзина для undo rm
├── logs/
│   └── shell.log                # Лог-файл
├── requirements.txt
└── README.md
```

## Установка

### 1. Клонируйте репозиторий:

```bash
git clone <repo_url>
cd mini_shell
```

### 2. Установите зависимости:

```bash
pip install -r requirements.txt
```

### 3. Запустите оболочку:

```bash
python shell.py
```

## Основные команды

### 1. ls

Список файлов и каталогов:
```bash
ls             # простой список
ls -l          # подробный список (имя, размер, дата, права)
ls path/to/folder
```
### 2. cd

Переход в каталог:
```bash
cd path/to/folder
cd ..          # вверх на уровень
cd             # домашний каталог
```
### 3. cat

Вывод содержимого файла:
```bash
cat filename.txt
```

Ошибка при указании каталога вместо файла.

### 4. cp

Копирование файлов/каталогов:
```bash
cp source.txt dest.txt
cp -r folder/ dest_folder/
```

Поддержка undo для отмены копирования.

### 5. mv

Перемещение или переименование:
```bash
mv old.txt new.txt
mv file.txt folder/
```

Поддержка undo для возврата.

### 6. rm

Удаление файлов/каталогов:
```bash
rm file.txt
rm -r folder/
```

Корзина .trash для восстановления через undo

Нельзя удалять / или ..

### 7. history

Вывод последних 20 команд:
```bash
history
```
### 8. undo

Отмена последнего действия (cp, mv, rm):
```bash
undo
```
### 9. Архивы (archive.py)
```bash
zip folder archive.zip       # создать ZIP
unzip archive.zip            # распаковать ZIP
tar folder archive.tar.gz    # создать TAR.GZ
untar archive.tar.gz         # распаковать TAR.GZ
```
### 10. Поиск по содержимому (grep.py)
```bash
grep "pattern" path          # поиск в файлах
grep "pattern" path -r       # рекурсивно в подкаталогах
grep "pattern" path -i       # игнорировать регистр
grep "pattern" path -r -i    # рекурсивно + игнорировать регистр
```
### 11. Выход
```bash
exit
quit
```

## Логирование

Все действия записываются в logs/shell.log:
```log
[2025-11-01 15:30:12] ls -l /home/user OK
[2025-11-01 15:31:05] rm file.txt ERROR: not found
```
Пример работы
```bash
MiniShell > ls
file1.txt
file2.txt
folder/

MiniShell > cp file1.txt copy.txt
Копирование успешно.

MiniShell > undo
Отменено копирование copy.txt

MiniShell > rm file2.txt
Удаление успешно.

MiniShell > undo
Восстановлено file2.txt

MiniShell > zip folder archive.zip
ZIP архив archive.zip создан.

MiniShell > unzip archive.zip
Архив archive.zip распакован.

MiniShell > grep "Hello" folder -r -i
folder/file1.txt:1: Hello world!
```
## Зависимости
```
Python 3.11+

colorama
```
## Особенности

Поддержка абсолютных и относительных путей

Undo для cp, mv, rm

История команд сохраняется между сессиями

Кроссплатформенный (Windows/macOS/Linux)

Плагины для архивов и поиска