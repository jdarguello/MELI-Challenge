from src.root import db

user_role = db.Table('user_role',
    db.Column('userId', db.BigInteger, db.ForeignKey('user.userId'), primary_key=True),
    db.Column('roleId', db.Integer, db.ForeignKey('role.roleId'), primary_key=True)
)
