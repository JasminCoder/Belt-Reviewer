#importamos conexion con BD
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash #flash envia mensajes de error

from datetime import datetime #para manipular fechas


class Grade:

    def __init__(self, data):
        self.id = data['id']
        self.alumno = data['alumno']
        self.stack = data['stack']
        self.fecha = data['fecha']
        self.calificacion = data['calificacion']
        self.cinturon = data['cinturon']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']


    #validaciones
    @staticmethod
    def valida_calificacion(formulario):
        es_valido = True

        if formulario['alumno'] == '':
            flash('Alumno no puede estar vacio', 'grades')
            es_valido = False

        if formulario['calificacion'] == '':
            flash('Ingresa una calificación', 'grades')
            es_valido = False
        else:
            if int(formulario['calificacion']) < 1 or int(formulario['calificacion']) > 10:
                flash('Calificacion debe ser entre 1 y 10', 'grades')
                es_valido = False

        if formulario['fecha'] == '':
            flash('Ingresa una fecha', 'grades')
            es_valido = False
        else:
            fecha_obj = datetime.strptime(formulario['fecha'], '%Y-%m-%d') #transformando texto a formato fecha
            hoy = datetime.now() #Da la fecha de hoy
            if hoy < fecha_obj:
                flash('La fecha debe ser en pasado', 'grades')
                es_valido = False

        return es_valido



    #funcion guardar
    @classmethod
    def save(cls, formulario):
        query = "INSERT INTO grades (alumno, stack, fecha, calificacion, cinturon, user_id) VALUES (%(alumno)s, %(stack)s, %(fecha)s, %(calificacion)s, %(cinturon)s, %(user_id)s)"
        result = connectToMySQL('belt_reviewer').query_db(query, formulario)
        return result



    #funcion para recibir todas la califiaciones
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM grades"
        results = connectToMySQL('belt_reviewer').query_db(query) #recibimos lisata de diccionarios
        grades = []

        for grade in results:
            grades.append(cls(grade)) #1- cls(grade) cre una instancia en base al diccionario / 2.- grades.append() 
            #me agrega esa instancia a mi lista
        
        return grades



    #regresa una instancia en base al id
    @classmethod
    def get_by_id(cls, formulario):
        query = "SELECT * FROM grades WHERE id = %(id)s"
        result = connectToMySQL('belt_reviewer').query_db(query, formulario)
        grade = cls(result[0])
        return grade



    #editar calificaion
    @classmethod
    def update(cls, formulario):
        query = "UPDATE grades SET alumno=%(alumno)s, stack=%(stack)s, fecha=%(fecha)s, calificacion=%(calificacion)s, cinturon=%(cinturon)s, user_id=%(user_id)s WHERE id=%(id)s"
        result = connectToMySQL('belt_reviewer').query_db(query, formulario)
        return result



    #funcion borrar
    @classmethod
    def delete(cls, formulario):
        query = "DELETE FROM grades WHERE id = %(id)s"
        result = connectToMySQL('belt_reviewer').query_db(query, formulario)
        return result
