from app import create_app

application = create_app("prod")


if __name__ == "__main__":	
	app = create_app("dev")
	app.run(debug=True)
