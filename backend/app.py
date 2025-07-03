from flask import Flask, request, current_app
from . import app, db
from .models import *
from .apis import auth_resource


app.register_blueprint(auth_resource, url_prefix = '/')

if __name__ == '__main__':
    app.run(debug=True)
