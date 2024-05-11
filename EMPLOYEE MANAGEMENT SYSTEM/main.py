from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

con = mysql.connector.connect(
    host="localhost", user="root", password="admin1234", database="emp")

def check_employee(employee_id):
    sql = 'select * from empd where id=%s'
    c = con.cursor(buffered=True)
    data = (employee_id,)
    c.execute(sql, data)
    r = c.rowcount
    if r == 1:
        return True
    else:
        return False

def add_employee():
    if request.method == 'POST':
        Name = request.form['name']
        ID = request.form['id']
        Post = request.form['post']
        Salary = request.form['salary']
        if (check_employee(ID) == True):
            return("Employee already exists\nTry Again\n")
        else:
            data = ( ID , Name, Post, Salary)
            sql = 'insert into empd values(%s,%s,%s,%s)'
            c = con.cursor()
            c.execute(sql, (ID,Name,Post,Salary))
            con.commit()    
        return ("EMPLOYEE ADDED TO DATABASE")
    
def remove_employee():
    if request.method == 'POST':
        ID = request.form['id']
        if (check_employee(ID) == False):
            return("Employee does not exists in database \nTry Again\n")
        else:
            sql = 'delete from empd where id=%s'
            data = (ID,)
            c = con.cursor()
            c.execute(sql,data)
            con.commit()
    return "Employee has been removed successfully from the database"

def promote_employee():
    if request.method == 'POST':
        ID = request.form['id']
        if (check_employee(ID) == False):
            print("Employee does not  exists\nTry Again\n")
        else:
            Amount = int(request.form['incriment'])

            sql = 'select salary from empd where id=%s'
            data = (ID,)
            c = con.cursor()
            c.execute(sql, data)
            r = c.fetchone()
            t = r[0] + Amount
            sql = 'update empd set salary=%s where id=%s'
            d = (t, ID)
            c.execute(sql, d)
            con.commit()
        return "Salary is incrimented , THANK YOU !"

# Function to display employees
def display_employees():
    sql = 'SELECT * FROM empd'
    c = con.cursor(dictionary=True)  # Fetch rows as dictionaries
    c.execute(sql)
    employees = c.fetchall()
    # Fetch column names
    column_names = [i[0] for i in c.description]
    # Pass both column names and employee details to the HTML template
    return render_template('display.html', employees=employees, column_names=column_names)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_employee', methods=['POST'])
def add_employee_form():
    result = add_employee()
    return result

@app.route('/remove_employee', methods=['POST'])
def remove_employee_form():
    result = remove_employee()
    return result

@app.route('/promote_employee', methods=['POST'])
def promote_employee_form():
    result = promote_employee()
    return result

# Route to handle display_employees form submission
@app.route('/display_employees', methods=['POST'])
def display_employees_form():
    result = display_employees()
    return result


@app.route('/add_employee_page', methods=['POST'])
def pytadding_emp():
    return render_template('add_employee.html')


@app.route('/remove_employee_page',methods=['POST'])
def removing_emp():
    return render_template('remove_employee.html')


@app.route('/promote_employee_page',methods=['POST'])
def incriment():
    return render_template('incriment.html')


@app.route('/display_employees_page',methods=['POST'])
def display():
    return display_employees()


if __name__ == '__main__':
    app.run(debug=True)
