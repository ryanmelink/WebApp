from typing import List, Dict
import simplejson as json
from flask import Flask, request, Response, redirect
from flask import render_template
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor

app = Flask(__name__)
mysql = MySQL(cursorclass=DictCursor)

app.config['MYSQL_DATABASE_HOST'] = 'db'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_DB'] = 'gradesData'
mysql.init_app(app)


@app.route('/', methods=['GET'])
def index():
    user = {'username': 'Grades Project'}
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM fldGrade')
    result = cursor.fetchall()
    return render_template('index.html', title='Home', user=user, grades=result)


@app.route('/view/<int:grade_id>', methods=['GET'])
def record_view(grade_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM fldGrade WHERE id=%s', grade_id)
    result = cursor.fetchall()
    return render_template('view.html', title='View Form', grade=result[0])


@app.route('/edit/<int:grade_id>', methods=['GET'])
def form_edit_get(grade_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM fldGrade WHERE id=%s', grade_id)
    result = cursor.fetchall()
    return render_template('edit.html', title='Edit Form', grade=result[0])


@app.route('/edit/<int:grade_id>', methods=['POST'])
def form_update_post(grade_id):
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('fldName'), request.form.get('fldLat'), request.form.get('fldLong'),
                 request.form.get('fldCountry'), request.form.get('fldAbbreviation'),
                 request.form.get('fldCapitalStatus'), request.form.get('fldPopulation'), grade_id)
    sql_update_query = """UPDATE fldGrade t SET t.fldLastName = %s, t.fldFirstName = %s, t.fldSSN = %s, t.fldTest1 = 
    %s, t.fldTest2 = %s, t.fldTest3 = %s, t.fldTest4 = %s WHERE t.id = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)

@app.route('/grades/new', methods=['GET'])
def form_insert_get():
    return render_template('new.html', title='New Grade Form')


@app.route('/grades/new', methods=['POST'])
def form_insert_post():
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('fldName'), request.form.get('fldLat'), request.form.get('fldLong'),
                 request.form.get('fldCountry'), request.form.get('fldAbbreviation'),
                 request.form.get('fldCapitalStatus'), request.form.get('fldPopulation'))
    sql_insert_query = """INSERT INTO fldGrade (fldLastName,fldFirstName,fldSSN,fldTest1,fldTest2,fldTest3,fldTest4) VALUES (%s, %s,%s, %s,%s, %s,%s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)

@app.route('/delete/<int:grade_id>', methods=['POST'])
def form_delete_post(grade_id):
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM fldGrade WHERE id = %s """
    cursor.execute(sql_delete_query, grade_id)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/api/v1/grades', methods=['GET'])
def api_browse() -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM fldGrade')
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/grades/<int:grade_id>', methods=['GET'])
def api_retrieve(grade_id) -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM fldGrade WHERE id=%s', grade_id)
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/grades/<int:grade_id>', methods=['PUT'])
def api_edit(grade_id) -> str:
    cursor = mysql.get_db().cursor()
    content = request.json
    inputData = (content['fldName'], content['fldLat'], content['fldLong'],
                 content['fldCountry'], content['fldAbbreviation'],
                 content['fldCapitalStatus'], content['fldPopulation'],grade_id)
    sql_update_query = """UPDATE fldGrade t SET t.fldLastName = %s, t.fldFirstName = %s, t.fldSSN = %s, t.fldTest1 = 
        %s, t.fldTest2 = %s, t.fldTest3 = %s, t.fldTest4 = %s WHERE t.id = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    resp = Response(status=200, mimetype='application/json')
    return resp

@app.route('/api/v1/grades', methods=['POST'])
def api_add() -> str:

    content = request.json

    cursor = mysql.get_db().cursor()
    inputData = (content['fldName'], content['fldLat'], content['fldLong'],
                 content['fldCountry'], content['fldAbbreviation'],
                 content['fldCapitalStatus'], request.form.get('fldPopulation'))
    sql_insert_query = """INSERT INTO fldGrade (fldLastName,fldFirstName,fldSSN,fldTest1,fldTest2,fldTest3,fldTest4) VALUES (%s, %s,%s, %s,%s, %s,%s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    resp = Response(status=201, mimetype='application/json')
    return resp

@app.route('/api/v1/grades/<int:grade_id>', methods=['DELETE'])
def api_delete(grade_id) -> str:
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM fldGrade WHERE id = %s """
    cursor.execute(sql_delete_query, grade_id)
    mysql.get_db().commit()
    resp = Response(status=200, mimetype='application/json')
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)