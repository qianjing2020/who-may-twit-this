from flask import Flask
import os

app = Flask(__name__)
env_configuration = os.environ['CONFIGURATION_SETUP']


app.config.from_object(env_configuration)


print(f"Environment: {app.config['ENV']}")
print(f"Debug: {app.config['DEBUG']}")
print(f"Secret key: {app.config['TWITTER_API_KEY']}")

if __name__ == "__main__":
	app.run()