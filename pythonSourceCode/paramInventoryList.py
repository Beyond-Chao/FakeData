#!flask/bin/python
from flask import Flask, jsonify, abort, make_response

app = Flask(__name__)

tasks = [
         {
             'id': 1000,
             'title': u'Inventroy List',
             'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
             'done': False
         },
         {
             'id': 2000,
             'title': u'Learn Python',
             'description': u'Need to find a good Python tutorial on the web',
             'done': False
         }
         ]

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = filter(lambda t: t['id'] == task_id, tasks)
    
    if len(task) == 0:
        abort(404)
    return jsonify({'task': tasks[0]})

# handle 404 error , defaultt Flask return HTML page instead of json
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)
if __name__ == '__main__':
    app.run(debug=True)