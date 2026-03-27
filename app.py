from flask import Flask 
from flask_smorest import Api, Blueprint
import uuid, datetime
from datetime import timezone, datetime
from flask.views import MethodView
from marshmallow import Schema, fields
from flask_smorest import abort
import enum

server = Flask(__name__)

#Create a Configuration object
class APIConfig:
    API_TITLE = "TODO API"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.3"
    OPEN_API_URL_PREFIX = "/"
    OPENAPI_SWAGGER_UI_PATH = "/docs"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    
server.config.from_object(APIConfig)
api = Api(server)

#A blueprint keeps several URLs in your API together so that way you can make 
# config changes on all of them together or separately for each of them as needed
todo = Blueprint("todo", "todo", url_prefix="/todo", description="TODO API")

#The actual todo list tasks. These should be ideally in a persistent storage like a database in a real world app.
#But here, we will store them as JSON objects in memory
tasks = [{
    "id": uuid.UUID("b3a06237-d966-40bb-9ccb-9175769f7251"),
    "created": datetime.now(timezone.utc),
    "completed": False,
    "task": "Create Flask API tutorial"

}]

#Create a Marshmallow model that represents the post object for each task object
#Note that the user will only provide the "task" name and the rest of the fields are handled on the server side

#for the /tasks/todo POST method
class CreateTask(Schema):
    task = fields.String()

#for the /tasks/todo PUT method
class UpdateTask(CreateTask):
    #so, updateTask will have both task and completed fields
    completed = fields.Boolean()

#for /tasks/todo GET method
class Task(UpdateTask):
    id = fields.UUID()
    created = fields.DateTime()

class SortByEnum(enum.Enum):
    #so, we can sort tasks using the "task" field or the "created" field
    task = "task"
    created = "created"

class SortDirectionEnum(enum.Enum):
    #sort order: asc or desc
    asc = "asc"
    desc = "desc"

class ListTasks(Schema):
    tasks = fields.List(fields.Nested(Task))

class ListTaskParameters(Schema):
    #by default, it will be sorted by the "created" field
    order_by = fields.Enum(SortByEnum, load_default=SortByEnum.created)
    #by default, tasks will e sorted in ascending order
    order = fields.Enum(SortDirectionEnum, load_default=SortDirectionEnum.asc)



#Create the Routes using classes
#Each class can deal with all the HTTP methods(GET, POST, etc., for a route)
#You are writing the API code for /todo/tasks endpoint here:
@todo.route("/tasks")
class TodoCollection(MethodView):
    @todo.arguments(ListTaskParameters, location="query")
    @todo.response(status_code=200, schema=ListTasks)
    #return the list of tasks to the user
    def get(self, parameters):
        return {
            "tasks":sorted(
                            tasks, 
                            key=lambda task: task[parameters["order_by"].value],
                            reverse=parameters["order"] == SortDirectionEnum.desc,
                        )
        }
    
    #Arguments represent input to this endpoint
    @todo.arguments(CreateTask)
    @todo.response(status_code=201, schema=Task)
    def post(self, task):
        task["id"] = uuid.uuid4()
        task["created"] = datetime.now(timezone.utc)
        task["completed"] = False
        tasks.append(task)
        return task

#Singleton API endpoint: singleton endpoint means that we can perform PUT, DELETE, GET actions on a specific task item
#This needs a separate class because the path is different, and will be something like /tasks/task_id
@todo.route("/tasks/<uuid:task_id>")
class ASpecificTodoTask(MethodView):

    @todo.response(status_code=200, schema=Task)
    def get(self, task_id):
        for task in tasks:
            if task["id"] == task_id:
                return task
        abort(404, f"Task with ID {task_id} not found.")

    
    @todo.arguments(UpdateTask)
    @todo.response(status_code=200, schema=Task)
    def put(self, payload, task_id):
        for task in tasks:
            if task["id"] == task_id:
                task["completed"] = payload["completed"]
                task["task"] = payload["task"]
                return task
        abort(404, f"Task with ID {task_id} not found.")

    #status code 204 denotes an empty response when an item is deleted because there is nothing to be returned
    @todo.response(status_code=204)
    def delete(self, task_id):
        for taskIdx, task in enumerate(tasks):
            if task["id"] == task_id:
                tasks.pop(taskIdx)
                #since it is delete, we return nothing
                return
        abort(404, f"Task with ID {task_id} not found.")



#Register Blueprint with the application object(server)
api.register_blueprint(todo)

