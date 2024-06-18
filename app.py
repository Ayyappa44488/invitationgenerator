from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from confidential import mysql_url

app = Flask(__name__)
app.secret_key = 'ayyappa'
app.static_folder = 'static'
app.config['SQLALCHEMY_DATABASE_URI']=mysql_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False


db=SQLAlchemy(app)
migrate=Migrate(app,db)


def register_blueprints(app):
    from blueprints.users import models as user_models
    from blueprints.invitations import models as invitation_models
    from blueprints.users.user import user
    from blueprints.invitations.invitation import invitation
    app.register_blueprint(user, url_prefix='/user')
    app.register_blueprint(invitation, url_prefix='/invitation')

register_blueprints(app)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
