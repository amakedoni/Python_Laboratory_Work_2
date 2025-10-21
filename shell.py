import os
import logging
from datetime import datetime
from commands import basic, archive, grep

LOG_FILE = 'logs/shell.log'
HISTORY_FILE = 'history.txt'

os.makedirs('logs', exist_ok=True)
os.makedirs('trash', exist_ok=True)

logging.basicConfig(
	filename=LOG_FILE,
	level=logging.INFO,
	format="[%(asctime)s] %(message)s",
	datefmt="%Y-%m-%d %H:%M:%S"
)
def log(massage):
	logging.info(massage)
	print(f"Логи: {massage}")


def save_history(command):
	with open(HISTORY_FILE, 'a', encoding='uft-8') as f:
		f.write(command + '\n')

def main():
	print('Мини-shell: Введите команду, для выхода ведите exit')
	while True:
		try:
			cmd = input(f"{os.getcwd()}$ ").strip()
			if not cmd:
				continue
			if cmd == 'exit':
				break
		save_history(cmd)
