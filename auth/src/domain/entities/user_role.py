from src.root import db

user_role = db.Table('user_role',
    db.Column('userid', db.BigInteger, db.ForeignKey('app_user.userid'), primary_key=True),
    db.Column('roleid', db.Integer, db.ForeignKey('role.roleid'), primary_key=True)
)
