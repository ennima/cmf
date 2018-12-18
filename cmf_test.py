# -*- coding: utf-8 -*-
from cmf import *
def main():
	cmf = "V:\\media\\PlayToAir\\VOZ NINA MIGRANTE FT.cmf"	
	my_cmf = Cmf(cmf)
	print(my_cmf.get_source_id())
	print(my_cmf.get_audio_format())

if __name__ == '__main__':
	main()


