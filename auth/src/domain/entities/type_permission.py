from src.root import db

# Association Table
type_permission = db.Table('type_permission',
    db.Column('typeId', db.Integer, db.ForeignKey('type.typeId'), primary_key=True),
    db.Column('permissionId', db.Integer, db.ForeignKey('permission.permissionId'), primary_key=True)
)