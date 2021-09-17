from sqlalchemy import inspect

from flask_sqlalchemy import SQLAlchemy

from werkzeug.security import generate_password_hash

def initialize_models(db: SQLAlchemy):
    class AppUser(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(80), unique=True, nullable=False)
        email = db.Column(db.String(120), unique=True, nullable=False)
        password = db.Column(db.String(1024), unique=True, nullable=False)

        def __repr__(self):
            return '<User %r>' % self.username

    class Project(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        owner = db.Column(db.ForeignKey('app_user.id'))

        def __repr__(self):
            return '<Project %r>' % self.username

    class File(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        owner = db.Column(db.ForeignKey('app_user.id'))
        containing_project = db.Column(db.ForeignKey('project.id'))
        data = db.Column(db.LargeBinary)
    
    # inspector = inspect(db.engine)
    # if not inspector.has_table('app_user'):
    #    db.create_all()

    # if AppUser.query.filter_by(username="admin").first() is not None:
    #    admin_user = AppUser(username='admin', email='admin@/dev/null', password=generate_password_hash('root'))
    #    db.session.add(admin_user)
    #    db.session.commit()
    
    return (AppUser, Project, File)
