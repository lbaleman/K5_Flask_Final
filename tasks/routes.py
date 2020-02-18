from tasks import app
from flask import render_template, request, url_for, redirect
from tasks.forms import TaskForm, ProcessTaskForm
from datetime import date
import sqlite3

BASE_DATOS = './data/{}'.format(app.config['DB_FILE'])
cabecera = ['title', 'description', 'date']

def dict_factory(cursor, row):
    d = {}
    for ix, col in enumerate(cursor.description):
        d[col[0]] = row[ix]
    return d

def dbQuery(consulta, *args):
    conn = sqlite3.connect(BASE_DATOS)
    conn.row_factory = dict_factory

    cursor = conn.cursor()

    rows = cursor.execute(consulta, args).fetchall()

    if len(rows) == 1:
        rows = rows[0]
    elif len(rows) == 0:
        rows = None

    conn.commit()
    conn.close()

    print(rows)
    return rows
    

@app.route("/")
def index():
    registros = dbQuery('SELECT titulo, descripción, date, id FROM tareas;')
    
    if registros:
        if isinstance(registros, dict):
            registros = [registros] #Para guardar cada linea en una tupla distinta. Importante este paso.
    else:
        registros = []


    return render_template("index.html", registros=registros)


@app.route("/newTask", methods =('GET', 'POST') )
def newTask():
    form = TaskForm(request.form)

    if request.method == 'GET':
        return render_template("task.html", form=form)
    
    if form.validate():
        title = request.values.get('title')
        desc = request.values.get('description')
        fx = request.values.get('fx')

        dbQuery("""INSERT INTO tareas (titulo, descripción, date) VALUES (?,?,?);""", title, desc, fx)
    
        return redirect(url_for('index'))#Va a redirigir a index.
    else:
        return render_template("task.html", form=form)

@app.route("/processtask", methods=('GET', 'POST'))
def processTask():
    form = ProcessTaskForm(request.form)

    if request.method == 'GET':
        ix = request.values.get('ix')
        if ix:
            registroAct = dbQuery("""SELECT titulo, descripción, date, id FROM tareas WHERE id = ?;""", ix)

            if registroAct:
                if registroAct['date']:
                    fechaTarea = date(int(registroAct['date'][:4]), int(registroAct['date'][5:7]), int(registroAct['date'][8:]))
                else:
                    fechaTarea = None
                
                accion = ''

                if 'btnModificar' in request.values:
                    accion = 'M'
                if 'btnBorrar' in request.values:
                    accion = 'B'
                    
                form = ProcessTaskForm(data={'ix': ix, 'title': registroAct['titulo'], 'description': registroAct['descripción'], 'fx': fechaTarea, 'btn': accion})
            
            return render_template("processtask.html", form=form)
        else:
            return redirect(url_for('index'))

    if form.btn.data == 'B':    
        ix = request.values.get('ix')
        consulta = """
            DELETE FROM tareas WHERE id = ?;
                """
        dbQuery(consulta, ix)

        return redirect(url_for('index'))
                
    if form.btn.data == 'M':
        if form.validate():
            ix = request.values.get('ix')
            consulta = """
            UPDATE tareas SET titulo= ?, descripción=?, date=? 
            WHERE id = ?;
                """
            dbQuery(consulta,request.values.get('title'), request.values.get('description'), request.values.get('fx'), ix)

        return redirect(url_for('index'))

    return render_template("processtask.html", form=form)