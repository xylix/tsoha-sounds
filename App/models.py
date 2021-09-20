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


def initialize_models(database: SQLAlchemy):
    file_project_association_table = database.Table(
        "fileproject",
        database.metadata,
        Column("file_id", ForeignKey("files.id"), primary_key=True),
        Column("project_id", ForeignKey("projects.id"), primary_key=True),
    )

    class AppUser(database.Model):
        __tablename__ = "appusers"
        id = Column(Integer, primary_key=True)
        username = Column(String(80), unique=True, nullable=False)
        email = Column(String(120), nullable=False)
        password = Column(String(1024), unique=True, nullable=False)
        is_admin = Column(Boolean, default=False)

    class Project(database.Model):
        __tablename__ = "projects"
        id = Column(Integer, primary_key=True)
        owner = Column(ForeignKey("appusers.id"))
        name = Column(String(80), unique=True)
        published = Column(Boolean, default=False)
        files = database.relationship("File", secondary=file_project_association_table)

    class File(database.Model):
        __tablename__ = "files"
        id = Column(Integer, primary_key=True)
        owner = Column(ForeignKey("appusers.id"))
        data = Column(LargeBinary, nullable=False)
        name = Column(String(80))

    class Comment(database.Model):
        __tablename__ = "comments"
        id = Column(Integer, primary_key=True)
        sender = Column(ForeignKey("appusers.id"))
        containing_project = Column(ForeignKey("projects.id"))
        content = Column(String(1024), nullable=False)
        sent = Column(
            DateTime(timezone=True), server_default=func.now(), nullable=False
        )

    database.create_all()

    if AppUser.query.filter_by(username="admin").first() is None:
        admin_user = AppUser(
            username="admin",
            email="admin@/dev/null",
            password=generate_password_hash("root"),
            is_admin=True,
        )
        database.session.add(admin_user)
        database.session.commit()
        sample_project = Project(
            owner=admin_user.id, name="First public project", published=True
        )
        sample_file = File(
            owner=admin_user.id, name="Broken test file", data=b"1010101010"
        )
        sample_project.files.append(sample_file)
        database.session.add(sample_project)
        database.session.commit()
        sample_comment = Comment(
            sender=admin_user.id,
            containing_project=sample_project.id,
            content="First test comment",
        )
        database.session.add(sample_comment)
        database.session.commit()

    print(database.engine.table_names())
    models = AppUser, Project, File, Comment
    print(CreateTable(file_project_association_table).compile(database.engine))
    [print(CreateTable(item.__table__).compile(database.engine)) for item in models]
    return models
