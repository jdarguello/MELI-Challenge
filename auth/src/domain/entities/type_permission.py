from src.root import db

# Association Table
type_permission = db.Table('type_permission',
    db.Column('typeid', db.Integer, db.ForeignKey('type.typeid'), primary_key=True),
    db.Column('permissionid', db.Integer, db.ForeignKey('permission.permissionid'), primary_key=True)
)