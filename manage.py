import os
import unittest
from flask_script import Manager 
from flask_migrate import Migrate, MigrateCommand
from app import create_app
from app.models import db


app = create_app(config_name=os.getenv('APP_SETTINGS'))
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


#Usage : python manage.py test
@manager.command
def test():
    tests = unittest.TestLoader().discover('./tests',pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1



if __name__ == '__main__':
    manager.run()
