# -*- coding: utf-8 -*-
import cmf_reader
import cmf
def main():
	cmf = "X:\\Recup\\ENTREVISTA REBECA DE ALBA\\ENTREVISTA REBECA DE ALBA(2).cmf\\ENTREVISTA REBECA DE ALBA(2).xml"
	print(cmf_reader.get_audio_format(cmf))

if __name__ == '__main__':
	main()


