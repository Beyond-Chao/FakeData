from flask import Flask, request, abort, jsonify

app = Flask(__name__)

tasks = [
         {
             'id': 1000,
             'title': u'Post Request Tool',
             'description': u'Post Man, Unix Curl Command, Advance REST client',
             'done': False
         },
         {
             'id': 2000,
             'title': u'Learn Python',
             'description': u'Need to find a good Python tutorial on the web',
             'done': False
         }
         ]

# GET Request
@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})


# POST Request
@app.route('/todo/api/v1.0/tasks', methods=['POST'])
def create_task():
    # request.json include Request Data
    # if request.json is not a json format or `title` field is not in request.json
    # will report `400` error
    if not request.json or not 'title' in request.json:
        aborb(400)

    # parse the parameter and create a task
    task = {
        'id': tasks[-1]['id'] + 1, # the last task`s id plus 1
        'title': request.json['title'],
        'description': request.json.get('description',""),
        'done': False
    }

    tasks.append(task)
    return jsonify({'task': task}), 201



if __name__ == '__main__':
    app.run(debug=True)