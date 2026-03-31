#Testing the 'todo/tasks' route with the GET method
def test_get_todos(client):
    response = client.get('/todo/tasks')
    assert response.status_code == 200

#Testing the '/todo/tasks' route with the POST method
def test_post_todos(client):
    new_task = {"task":"Next, start an IaC project using AWS CloudFormation!"}
    response = client.post('/todo/tasks', json=new_task)
    assert response.status_code == 201
    assert response.get_json()['task'] == "Next, start an IaC project using AWS CloudFormation!" 



