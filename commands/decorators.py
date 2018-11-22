
def protected(func):
	def wrapper(password):
		if(password == 'platzi'):
			return func()
		else:
			print('El pass es incorrecto. :(')

	return wrapper

@protected
def protected_func():
	print('Tu pass es correcto.')


def main():
	password = "platzi"
	protected_func(password)

if __name__ == '__main__':
	main()