""" This is a pseudocode structure for a REST API that has a database of 'things'

This contains 'pseudocode' that is, it is not Python code and will not work, but rather has lines of text that state
the code logic

Every request accepts an HTTP request and returns and HTTP response

HTTP request
Any route has access to the HTTP request that was made to that route.
You can access the HTTP request that was made to this route using Flask request
The request has: url (which may have a variable component), header and body, the body can have JSON

HTTP response
If you return JSON data from the function then it will be handled by Flask as an HTTP response with JSON content
If you want to modify the response, you can create your own response using make_response(body, HTTP status code,
headers)
Make response takes a status code, body (containing JSON) and a header
HTTP response codes are pre-defined, e.g. 200 OK, 404 Not Found (use a reference to find out what they are)

Converting from JSON to SQLAlchemy objects (called serialising/de-serialising)
'dump' means to take one or more objects and convert to JSON
'load' means to use JSON to load the data for one or more objects
There are different approaches to this:

1. Python json library (part of Python base install, so you don't need to pip install it)
json.dumps() returns JSON
json.loads() de-serialise JSON

2. Flask jsonify e.g. from flask import jsonify
jsonify() is like dumps() See https://flask.palletsprojects.com/en/3.0.x/patterns/javascript/#return-json-from-views
This function allows you take json from the request to an object:
https://flask.palletsprojects.com/en/3.0.x/patterns/javascript/#receiving-json-in-views (NB I have not tried this but
assume it works!)

3. Create a Flask-Marshmallow schema, ThingSchema, that defines how to turn a SQLAlchemy object into JSON
and vice-versa.
Create two instances of the schema, one that handles a single result and one that handles multiple objects.
things_schema = ThingSchema(many=True)
thing_schema = ThingSchema()

Once you have created the schemas then you can call the load() and dump() methods on the created schemas.
thing_schema.load() - converts from JSON to a SQLAlchemy object
things_schema.load() - converts from JSON to multiple SQLAlchemy objects
thing_schema.dump() - converts one SQLAlchemy object to JSON
things_schema.dump() - converts multiple SQLAlchemy objects into JSON

To use Flask_Marshmallow you also need to:
1. Create a Flask-Marshmallow instance (object)
2. Initialise the instance for the Flask app
3. Define schemas that map the SQLAlchemy objects defining the attributes and other features such as weather to load
the relationships
"""
from flask import current_app as app


@app.get('/things')
def get_all_things():
    # You do not need to access anything from the request

    # all_thing_objects = Query the database using FlaskSQLAlchemy syntax ending in .scalars() to get all things

    # all_things_json = Use things_schema.dumps(all_things_objects) to convert the FlaskSQLAlchemy
    # query result objects into JSON

    # Return the JSON which will generate a Flask HTTP response
    # You can optionally specify headers, status code and body by using flask make_response
    # return all_things_json
    pass  # This line is just here to prevent linting warnings while there is no real code, you do not use this in the
    # actual route!!


@app.get('/things/<thing_id>')
def get_one_thing(thing_id):
    # You do not need to access anything from the request. The 'thing_id' is passed from the URL itself to the
    # function
    # e.g. someone might request http//mythingsapi.com/thing/1 to get the thing that has an id of 1.

    # one_thing_object = Query the database using FlaskSQLAlchemy .scalar_one_or_none() and use the parameter
    # for the Thing id with the value of thing_id from the URL to find that thing. Note: the following code does not
    # handle the error if no Thing with that id is found, this is covered in week 5.

    # one_thing_json = Use thing_schema.dumps(one_thing_object) to convert the FlaskSQLAlchemy
    # query result objects into JSON

    # return one_thing_json which returns the JSON, this generates a Flask HTTP response

    pass  # This line is just here to prevent linting warnings while there is no real code, you do not use this in the
    # actual route!!


@app.post('/things')
def post_new_thing():
    # Get the json from the request
    # new_thing_json = request.get_json()

    # Create a new Thing object by using the thing_schema.load()
    # thing = thing_schema.load(new_thing_json)

    # Add to the session and commit it, this saves it to the database
    # db.session.add(event)
    # db.session.commit()

    # Return JSON, for example you can make response or just return a message in JSON structure to add to the body of
    # the response
    # return {"message": f"Thing added with id= {thing.id}"}

    pass  # This line is just here to prevent linting warnings while there is no real code, you do not use this in the
    # actual route!!


@app.delete('/things/<thing_id>')
def delete_one_thing(thing_id):
    # You do not need to access anything from the request. The 'thing_id' is passed from the URL itself to the
    # function
    # e.g. someone might request http//mythingsapi.com/thing/1 to get the thing that has an id of 1.

    # one_thing_object = Query the database using FlaskSQLAlchemy .scalar_one_or_none() and use the parameter
    # for the Thing id with the value of thing_id from the URL to find that thing. Note: the following code does not
    # handle the error if no Thing with that id is found, this is covered in week 5.

    # delete the thing you just found using db.session.delete(one_thing_object)
    # db.session.commit() completes the deletion

    # return JSON e.g. a message to say it has been deleted
    # return {"message": f"Thing with id= {thing_id} has been deleted."}

    pass  # This line is just here to prevent linting warnings while there is no real code, you do not use this in the
    # actual route!!


@app.patch('/things/<thing_id>')
def update_one_thing(thing_id):
    # The 'thing_id' is passed from the URL to the function
    # Find the thing and its current values in the database using that thing_id
    # existing_thing = db.session.execute(db.select(Thing).filter_by(id=thing_id)).scalar_one_or_none()

    # Get the updated details from the json sent in the HTTP patch request
    # thing_json = request.get_json()

    # Use the schema to create a thing which merges the changes from the json with the existing_thing
    # changed_thing = thing_schema.load(thing_json, instance=existing_thing, partial=True)

    # Save the changed_thing to the database using add() and commit()
    # db.session.add(changed_thing)
    # db.session.commit()

    # Return json e.g. a message to say all the thing was updated
    # return {"message": f"Thing with id= {thing_id} has been updated."}

    pass  # This line is just here to prevent linting warnings while there is no real code, you do not use this in the
    # actual route!!
