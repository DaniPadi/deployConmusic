from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask import send_from_directory, jsonify
from flask_login import login_required, current_user
from models import Song, UserSong
from extensions import db
import os

music_bp= Blueprint('music', __name__, url_prefix='/music')

@music_bp.route('/manage', methods= ['GET', 'POST'])
@login_required
def manage_music():
  
  def is_json_request():
        # Verifica si el cliente solicita JSON basado en el encabezado o un parámetro.
        return (
            request.headers.get("Accept") == "application/json"
            or request.args.get("response_type") == "json"
        )
  if request.method== 'POST':
    title= request.form.get('title')
    author= request.form.get('author')
    song_file= request.files.get('song')
    structure= request.form.get('structure')

    print(f'El archivo de canción {song_file}')
    if song_file is None:
      if is_json_request():
        
        return jsonify({"error": f"El archivo de canción no se subió {song_file}"}), 400
      return redirect(url_for('music.manage_music'))
    print(f'El archivo de canción {song_file.name}')
    upload_folder = os.path.join(current_app.instance_path, 'uploads')
    
    song_path= song_file.filename
    song_file.save(os.path.join(upload_folder, song_file.filename))
    

    newSong= Song(title= title, author= author, song_path= song_path, structure= structure)
    db.session.add(newSong)
    db.session.commit()

    new_user_song = UserSong(user_id=current_user.id, song_id=newSong.id)  # Asegúrate de que current_user está disponible
    db.session.add(new_user_song)
    db.session.commit()
    if is_json_request():
            return jsonify({
                "message": "Canción subida exitosamente",
                "song": {
                    "id": newSong.id,
                    "title": newSong.title,
                    "author": newSong.author,
                    "path": newSong.song_path,
                    "structure": newSong.structure,
                }
            }), 201

    return redirect(url_for('music.manage_music'))
    
  user_songs = UserSong.query.filter_by(user_id=current_user.id).all()
  songs = [user_song.song for user_song in user_songs]
  
  return render_template('songs.html', songs= songs)

@music_bp.route('/edit/<int:id>', methods= ['GET', 'POST'])
@login_required
def edit_song(id):
  song= Song.query.get_or_404(id)
  if request.method== 'POST':
    song.title= request.form.get('title')
    song.author= request.form.get('author')
    song.structure= request.form.get('structure')
    db.session.commit()
    return redirect(url_for('music.manage_music'))
  return render_template('edit_song.html', song= song)

@music_bp.route('/delete/<int:id>', methods= ['GET', 'POST'])
@login_required
def delete_song(id):
  song= Song.query.get_or_404(id)
  user_song = UserSong.query.filter_by(user_id=current_user.id,song_id=song.id).first()

  if user_song:
    db.session.delete(user_song)
    db.session.commit()

  return redirect(url_for('music.manage_music'))

@music_bp.route('/play/<int:id>', methods= ['GET', 'POST'])
@login_required
def play_song(id):
  song= Song.query.get_or_404(id)
  return render_template('play_song.html', song= song)

# Ruta para servir los archivos de la carpeta 'uploads' en 'instance'
@music_bp.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(os.path.join(current_app.instance_path, 'uploads'), filename)

@music_bp.route('/search', methods=['GET', 'POST'])
@login_required
def search_song():
  if request.method == 'POST' and request.form.get('searching_song')!= '':
    searching_song= request.form.get('searching_song')
    songs= Song.query.filter(Song.title.like(f'%{searching_song}%')).all()
    return render_template('search_song.html', songs= songs)

  songs = Song.query.all()
  return render_template('search_song.html', songs= songs)  

@music_bp.route('/add/<int:song_id>', methods=['GET', 'POST'])
@login_required
def add_song(song_id):
  new_user_song = UserSong(user_id=current_user.id, song_id=song_id)  
  db.session.add(new_user_song)
  db.session.commit()
  return redirect(url_for('music.search_song'))
