from flask import render_template, redirect, request, session, flash
from flask_app import app

#importamos los modelos
from flask_app.models.users import User
from flask_app.models.grades import Grade


@app.route('/new/grade')
def new_grade():
    if 'user_id' not in session:
        return redirect('/')

    #Yo sé que en sesión tengo el id de mi usuario (session['user_id'])
    #Queremos una función que en base a ese id me regrese una instancia del usuario
    formulario = {"id": session['user_id']}

    user = User.get_by_id(formulario) #Recibo la instancia de usuario en base a su ID

    return render_template('new_grade.html', user=user)


    #ruta 
@app.route('/create/grade', methods=['POST'])
def create_grade():
    if 'user_id' not in session:
        return redirect('/')

    #Validar calificacion
    if not Grade.valida_calificacion(request.form):
        return redirect('/new/grade')

    #gurdar calificacion
    Grade.save(request.form)

    return redirect('/dashboard')



    #ruta 
@app.route('/edit/grade/<int:id>')
def edit_grade(id):
    if 'user_id' not in session:
        return redirect('')

    #Yo sé que en sesión tengo el id de mi usuario (session['user_id'])
        #Queremos una función que en base a ese id me regrese una instancia del usuario
    formulario = {"id": session['user_id']}

    user = User.get_by_id(formulario) #Recibo la instancia de usuario en base a su ID


        #cual es la calificacion q se va a editar
    formulario_calificacion = {"id": id}
    grade = Grade.get_by_id(formulario_calificacion)

    return render_template('edit_grade.html', user=user, grade=grade)


#ruta editar
@app.route('/update/grade', methods=['POST'])
def update_grade():
    if 'user_id' not in session:
        return redirect('/')
        
    #Validación de Calificación
    if not Grade.valida_calificacion(request.form):
        return redirect('/edit/grade/'+request.form['id']) #/edit/grade/1
        
    Grade.update(request.form)

    return redirect('/dashboard')



#ruta borrar
@app.route('/delete/grade/<int:id>')
def delete_grade(id):
    if 'user_id' not in session:
        return redirect('/')

    formulario = {"id": id}
    Grade.delete(formulario)

    return redirect('/dashboard')