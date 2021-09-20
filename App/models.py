from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    func,
    DateTime,
    String,
    Boolean,
    LargeBinary,
)
from sqlalchemy.schema import CreateTable
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash


def initialize_models(db: SQLAlchemy):
    file_project_association_table = db.Table(
        "FileProject",
        db.metadata,
        Column("file_id", ForeignKey("Files.id"), primary_key=True),
        Column("project_id", ForeignKey("Projects.id"), primary_key=True),
    )

    class AppUser(db.Model):
        __tablename__ = "AppUsers"
        id = Column(Integer, primary_key=True)
        username = Column(String(80), unique=True, nullable=False)
        email = Column(String(120), nullable=False)
        password = Column(String(1024), unique=True, nullable=False)
        is_admin = Column(Boolean, default=False)

        def __repr__(self):
            return "<User %r>" % self.username

    class Project(db.Model):
        __tablename__ = "Projects"
        id = Column(Integer, primary_key=True)
        owner = Column(ForeignKey("AppUsers.id"))
        name = Column(String(80), unique=True)
        published = Column(Boolean, default=False)
        files = db.relationship("File", secondary=file_project_association_table)

    class File(db.Model):
        __tablename__ = "Files"
        id = Column(Integer, primary_key=True)
        owner = Column(ForeignKey("AppUsers.id"))
        data = Column(LargeBinary)
        name = Column(String(80))

    class Comment(db.Model):
        __tablename__ = "Comments"
        id = Column(Integer, primary_key=True)
        sender = Column(ForeignKey("AppUsers.id"))
        containing_project = Column(ForeignKey("Projects.id"))
        content = Column(String(1024), nullable=False)
        sent = Column(
            DateTime(timezone=True), server_default=func.now(), nullable=False
        )

    db.create_all()

    if AppUser.query.filter_by(username="admin").first() is None:
        admin_user = AppUser(
            username="admin",
            email="admin@/dev/null",
            password=generate_password_hash("root"),
            is_admin=True,
        )
        db.session.add(admin_user)
        db.session.commit()
        sample_project = Project(
            owner=admin_user.id, name="First public project", published=True
        )
        sample_file = File(owner=admin_user.id, name="Test file")
        sample_project.files.append(sample_file)
        db.session.add(sample_project)
        db.session.commit()
        sample_comment = Comment(
            sender=admin_user.id,
            containing_project=sample_project.id,
            content="First test comment",
        )
        db.session.add(sample_comment)
        db.session.commit()

    print(db.engine.table_names())
    models = AppUser, Project, File, Comment
    print(CreateTable(file_project_association_table))
    [print(CreateTable(item.__table__)) for item in models]
    return models
