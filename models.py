from flask_sqlalchemy import SQLAlchemy
from flask import Flask


db = SQLAlchemy()

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    email_user = db.Column(db.String(60), unique=True, nullable=False)
    rol = db.Column(db.String(20), nullable=False)

    def _repr_(self):
        return f"User: {self.username} Email: {self.email_user}"
    
    # Metodos por flask_login
    @property
    def is_authenticated(self):
        return True
    
    @property
    def is_active(self):
        return True
    
    @property
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return str(self.id)

categorias_curso = db.Table('categorias_curso', 
    db.Column('curso_id', db.Integer, db.ForeignKey('curso.id'), primary_key=True),
    db.Column('categoria_id', db.Integer, db.ForeignKey('categoria.id'), primary_key=True)
    )

class Curso(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, default=0.0)
    id_profesor = db.Column(db.Integer, db.ForeignKey('usuario.id'), name='fk_curso_usuario')
    categorias = db.relationship('Categoria', secondary=categorias_curso,
                                 backref=db.backref('cursos', lazy='dynamic'))
    
    # con esta funcion me permitira mostrar los datos en un json
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'categorias': [categoria.serialize() for categoria in self.categorias]
        }

    def _repr_(self):
        return f"Curso: {self.title}"

class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)

    # con esta funcion nos permitira mostrar los datos en formato json
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }

    def _repr_(self):
        return f"Categoria: {self.name}"

class Reseña(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    curso_id = db.Column(db.Integer, db.ForeignKey('curso.id'), nullable=False)
    user = db.relationship('Usuario', backref='review')
    curso = db.relationship('Curso', backref='review')

    def __repr__(self):
        return f"Review: {self.rating} - {self.comment}"
