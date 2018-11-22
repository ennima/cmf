from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
	print("Que pex")
	return 'Hola, mundote.'
@app.route("/hi/<uname>")
def hi(uname):
	return "Hi "+uname

if __name__ == '__main__':
	app.run()