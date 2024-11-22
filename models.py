from extensions import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
  id= db.Column(db.Integer, primary_key=True)
  email= db.Column(db.String(50), nullable=False, unique=True)
  first_name= db.Column(db.String(50), nullable=False)
  middle_name= db.Column(db.String(50), nullable=True)
  last_name= db.Column(db.String(50), nullable=False)
  instrument= db.Column(db.String(50), nullable=False)
  password= db.Column(db.String(100), nullable=False)

  songs= db.relationship('UserSong', back_populates='user')

class Song(db.Model):
  id= db.Column(db.Integer, primary_key=True)
  title= db.Column(db.String(100), nullable=False)
  author= db.Column(db.String(100), nullable=False)
  song_path= db.Column(db.String(100), nullable=False)
  structure= db.Column(db.Text, nullable=False)

  user_songs= db.relationship('UserSong', back_populates='song')

class UserSong(db.Model):
  id= db.Column(db.Integer, primary_key= True)
  user_id= db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  song_id= db.Column(db.Integer, db.ForeignKey('song.id'), nullable=False)

  user = db.relationship('User', back_populates='songs')
  song = db.relationship('Song', back_populates='user_songs')
