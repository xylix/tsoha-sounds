from flask_sqlalchemy import SQLAlchemy

from werkzeug.security import generate_password_hash

def initialize_models(db: SQLAlchemy):
    # TODO: In future either stop changing database and remove this or implement proper migrations
    db.drop_all()

    class User(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(80), unique=True, nullable=False)
        email = db.Column(db.String(120), unique=True, nullable=False)
        password = db.Column(db.String(1024), unique=True, nullable=False)

        def __repr__(self):
            return '<User %r>' % self.username

    class Project(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        owner = db.Column(db.ForeignKey('user.id'))

        def __repr__(self):
            return '<Project %r>' % self.username

    class File(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        owner = db.Column(db.ForeignKey('user.id'))
        containing_project = db.Column(db.ForeignKey('project.id'))
        data = db.Column(db.LargeBinary)


    db.create_all()
    
    if (not User.query.filter_by(username="admin").first()):

        admin_user = User(username='admin', email='admin@/dev/null', password=generate_password_hash('root'))
        db.session.add(admin_user)
    db.session.commit()
    return (User, Project, File)
