from app import create_app,db
from flask_script import Manager, Server
from flask_migrate import Migrate
from app.models import User,Comment,Blog,Subscriber

app=create_app("development")
manager=Manager(app)
manager.add_command("run",Server(use_debugger=True))
@manager.shell
def make_shell_context():
    return dict(app=app, db=db)
    
if __name__=="__main__":
    manager.run()

    
