import argparse

def get_arguments():
	# return_val = False
	return_data = {}
	""" Read arguments from cmd"""
	parser = argparse.ArgumentParser()
	
	#Required
	parser.add_argument("req", help="echo the string you use here")
	# parser.add_argument("pop")
	# parser.add_argument("square", help="display a square of a given number",
	#                     type=int)

	parser.add_argument("--required", help="required argument")

	# Optional
	parser.add_argument("--verbosity", help="increase output verbosity")
	

	args = parser.parse_args()

	# Validating arguments

	### Required
	if args.required:
		print("Yeah!")
		return_data["required"] = args.required
	elif args.req:
		return_data["required"] = args.req
	else:
		print("######################### --required is necesary")
		

	### Optional
	if args.verbosity:
		print("verbosity turned on")

	return return_data

dic = get_arguments()

print(dic)