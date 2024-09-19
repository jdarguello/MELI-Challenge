from src.root import db

class Role(db.Model):
    roleId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)

    # Foreign key to Type
    typeId = db.Column(db.Integer, db.ForeignKey('type.typeId'), nullable=False)

    # Relationship to Type
    type = db.relationship('Type', back_populates='roles')
