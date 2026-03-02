from app import app, db
from flask import render_template, redirect, url_for, request, flash
import formularios
from models import Tarea
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', subtitulo="Actividad en grupo TAI")
@app.route('/sobrenosotros', methods=['GET', 'POST'])
def sobrenosotros():
    formulario = formularios.FormAgregarTareas()
    if formulario.validate_on_submit():
        nueva_tarea = Tarea(titulo=formulario.titulo.data)
        db.session.add(nueva_tarea)
        db.session.commit()
        flash(f"Tarea '{formulario.titulo.data}' agregada correctamente.", 'success')
        return redirect(url_for('mostrar_tareas'))
    return render_template('sobrenosotros.html', form=formulario)
@app.route('/saludo')
def saludo():
    return 'Hola, bienvenido a Taller Apps'
@app.route('/usuario/<nombre>')
def usuario(nombre):
    return f'Hola {nombre}, bienvenido a Taller Apps'
@app.route('/tareas')
def mostrar_tareas():
    tareas = Tarea.query.all()
    return render_template('tareas.html', tareas=tareas)
@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_tarea(id):
    tarea = Tarea.query.get_or_404(id)
    formulario = formularios.FormAgregarTareas(obj=tarea)
    if formulario.validate_on_submit():
        tarea.titulo = formulario.titulo.data
        db.session.commit()
        flash(f"Tarea '{tarea.titulo}' actualizada correctamente.", 'success')
        return redirect(url_for('mostrar_tareas'))
    return render_template('editar.html', form=formulario, tarea=tarea)
@app.route('/eliminar/<int:id>', methods=['POST'])
def eliminar_tarea(id):
    tarea = Tarea.query.get_or_404(id)
    db.session.delete(tarea)
    db.session.commit()
    flash(f"Tarea '{tarea.titulo}' eliminada correctamente.", 'success')
    return redirect(url_for('mostrar_tareas'))