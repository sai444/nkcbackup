from flask_apscheduler import APScheduler #pip install APScheduler
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from main.preventiveMaintenance.preventiveMaintenanceResource import preventiveMaintenanceScheduler

from app import app,db

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

scheduler = APScheduler()

if __name__ == '__main__':
    db.create_all()
    scheduler.add_job(id='preventive maintenance', func=preventiveMaintenanceScheduler, trigger="interval", hours=24,
                      start_date='00:00:00')
    scheduler.start()
    manager.run()
