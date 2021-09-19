from sqlalchemy import func

from flask_sqlalchemy import SQLAlchemy

from werkzeug.security import generate_password_hash

def initialize_models(db: SQLAlchemy):
    class AppUser(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(80), unique=True, nullable=False)
        email = db.Column(db.String(120), unique=True, nullable=False)
        password = db.Column(db.String(1024), unique=True, nullable=False)
        is_admin = db.Column(db.Boolean, default=False)

        def __repr__(self):
            return '<User %r>' % self.username

    class Project(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        owner = db.Column(db.ForeignKey('app_user.id'))
        name = db.Column(db.String(80), unique=True)
        published = db.Column(db.Boolean, default=False)

        def __repr__(self):
            return '<Project %r>' % self.username

    class File(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        owner = db.Column(db.ForeignKey('app_user.id'))
        containing_project = db.Column(db.ForeignKey('project.id'))
        data = db.Column(db.LargeBinary)
        name = db.Column(db.String(80))

    class Comment(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        sender = db.Column(db.ForeignKey('app_user.id'))
        containing_project = db.Column(db.ForeignKey('project.id'))
        content = db.Column(db.String(1024), nullable=False)
        sent = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    db.create_all()

    if AppUser.query.filter_by(username="admin").first() is None:
        admin_user = AppUser(username='admin', email='admin@/dev/null', password=generate_password_hash('root'), is_admin=True)
        db.session.add(admin_user)
        db.session.commit()
        sample_project = Project(owner=admin_user.id, name="First public project", published=True)
        db.session.add(sample_project)
        db.session.commit()
        sample_comment = Comment(sender=admin_user.id, containing_project=sample_project.id, content="First test comment")
        db.session.add(sample_comment)
        db.session.commit()
    
    return (AppUser, Project, File, Comment)
