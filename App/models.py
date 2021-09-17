from flask_sqlalchemy import SQLAlchemy


def initialize_models(db: SQLAlchemy):
    class User(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(80), unique=True, nullable=False)
        email = db.Column(db.String(120), unique=True, nullable=False)

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
        data = db.Column(db.BINARY)


    db.create_all()
