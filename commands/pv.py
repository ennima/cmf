clients = 'pablo,ricardo,'

def create_clients(client_name):
	global clients
	clients += client_name
	_add_coma()

def _add_coma():
	global clients
	clients += ','

def main():
	create_clients("lou")

	print(clients)

if __name__ == '__main__':
	main()




