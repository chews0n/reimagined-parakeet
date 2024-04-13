import sys
from model.train import train
from utils.constants import START_YEAR, END_YEAR


def main() -> int:
	retcode = train(START_YEAR, END_YEAR, 'model.bin')

	return retcode


if __name__ == '__main__':
	sys.exit(main())  # next section explains the use of sys.exit
