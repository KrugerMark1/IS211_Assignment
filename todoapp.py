from flask import Flask, render_template, request, Response, redirect
import re
import json
from random import randrange

app = Flask(__name__)

try:
	file_db = open('db.txt', 'r')
	todo_list = json.load(file_db)

except:
	todo_list = []

def generate_id():
	new_id = randrange(99999999999999)
	return(str(new_id))

def save_to_file():
	json_string = json.dumps(todo_list)

	with open('db.txt', 'w') as file:
		file.write(json_string)

def is_valid_email(email):
	regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

	if re.fullmatch(regex, email):
		return(True)
	else:
		return(False)

@app.route('/')
def index():

	return(render_template('index.html', todo_list=todo_list))

@app.route('/clear', methods=['GET'])
def clear():
	todo_list.clear()
	return(redirect('/'))

@app.route('/submit', methods=['GET'])
def submit():
	args = request.args

	new_task = {
	  "id": generate_id(),
	  "task": args.get('task'),
	  "email": args.get('email'),
	  "priority": args.get('priority')
	}

	errors = []

	if args.get('email') is None or not is_valid_email(new_task.get('email')):
		errors.append('Invalid Email Address.')

	if args.get('priority') not in ['Low', 'Medium', 'High']:
		errors.append('Invalid priority level.')

	if len(errors) == 0:
		todo_list.append(new_task)
	else:
		print(errors)

	return(redirect('/'))

@app.route('/save', methods=['GET'])
def save():
	save_to_file()
	return(redirect('/'))

@app.route('/delete', methods=['GET'])
def delete():
	args = request.args
	task_id = args.get('task_id')

	for item in todo_list:
		if item.get('id') == task_id:
			todo_list.remove(item)

	return(redirect('/'))

if __name__ == '__main__':
	app.run()