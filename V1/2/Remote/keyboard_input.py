"""
Depriciated.
Doo doo.
"""
from curtsies import Input
from remote import *


def main():
	# Setup
	r = Remote()
	# "Left" if direction else "Right"
	direction = True

	with Input(keynames='curses') as input_generator:
		for e in input_generator:
			print(repr(e))
			# Quit
			if e == '\x1b':
				print('\nGoodbye')
				break
			elif e in ('7', '.') :
				r.do_input(["A", '0'])
			elif e in ('8', '/'):
				r.do_input(["B", '0'])
			elif e in ('4', ' '):
				r.do_input(["X", '0'])
			elif e == '5':
				r.do_input(["Y", '0'])
			elif e == 'h':
				r.do_input(["H", '0'])
			elif e == '0':
				r.reset()
			elif e == 'a':
				r.do_input(LEFT)
			elif e == 'd':
				r.do_input(RIGHT)
			elif e == 'w':
				r.do_input(UP)
			elif e == 's':
				r.do_input(DOWN)
			elif e == 'KEY_LEFT':
				r.do_input(left_electric)
			elif e == 'KEY_RIGHT':
				r.do_input(right_electric)
			elif e == 'c':
				r.do_input(UP_B)

	r.close_ser()
	return


if __name__ == '__main__':
    main()