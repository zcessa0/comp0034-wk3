# Creating REST API routes

COMP0034 2023-24 Week 3 coding activities.

## 1. Preparation

This assumes you have already forked the coursework repository and cloned the resulting repository to your IDE.

1. Create and activate a virtual environment
2. Install the requirements `pip install -r requirements.txt`
3. Run the app `flask --app paralympics run --debug`
4. Open a browser and go to http://127.0.0.1:5000
5. Check that you have an instance folder containing `paralympics.sqlite`
6. Stop the app using `CTRL+C`

## 2. Introduction

Assume that the following routes were designed for the API.

| HTTP method | URL                | Body                                                       | Response                                                      | 
|:------------|:-------------------|:-----------------------------------------------------------|:--------------------------------------------------------------|
| GET         | region             | None                                                       | Returns a list of NOC region codes with region name and notes | 
| GET         | region/\<code\>    | None                                                       | Returns the region name and notes for a given code            | 
| PATCH       | region/\<code\>    | Changed fields for the NOC record                          | Return all the details of the updated NOC record              | 
| POST        | region             | Region code, region name and (optional) notes              | Status code 201 if new NOC code was saved.                    | 
| DELETE      | region/\<code\>    | None                                                       | Removes an NOC code and if successful returns  202 (Accepted) | 
| GET         | event              | None                                                       | Returns a list of events with all details                     | 
| GET         | event/\<event_id\> | None                                                       | Returns all the details for a given event                     | 
| POST        | event              | Event details                                              | Status code 201 if new event was saved.                       | 
| PATCH       | event/\<event_id\> | Event details to be updated (specific fields to be passed) | Return all the details of the updated event                   | 
| DELETE      | event/\<event_id\> | None                                                       | Removes an event and if successful returns  202 (Accepted)    | 

You will need to refer to the Flask documentation:

- [routing](https://flask.palletsprojects.com/en/2.3.x/quickstart/#routing)
- [HTTP methods](https://flask.palletsprojects.com/en/2.3.x/quickstart/#http-methods)

## 2. Serialize and deserialize the data

Serialization refers to the process of converting a Python object into a format that can be used to store or transmit
the
data and then recreate the object when needed using the reverse process of deserialization.

There are different formats for the serialization of data, such as JSON, XML, and Python's pickle. JSON returns a
human-readable string form, while Python’s pickle library can return a byte array.

In the COMP0034 teaching materials pickle is used for serializing and deserializing machine learning models, and JSON
for the REST API.

You could serialize your own classes, for example by adding a `to_json` method to a class, or by creating an instance of the class and `dump`ing. The limitation of this is it cannot
be handle relationships between classes:

```python
import json
from sqlalchemy.orm import Mapped, mapped_column
from paralympics import db


class User(db.Model):
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    email: Mapped[str] = mapped_column(db.String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(db.String, unique=True, nullable=False)

    def __init__(self, email: str, password_string: str):
        self.email = email
        self.password = self._hash_password(password_string)

    def to_json(self):
        return json.dumps(self.__dict__)

# Get a list of users then use the to_json method to convert to JSON
users = get_all_users()
return [user.to_json() for user in users]
```

This is a shortcut to passing the data to the jsonify() function, which will serialize any supported JSON data type.
That means that all the data in the dict or list must be JSON serializable.

For complex types such as database models, you can use a serialization library to convert the data to valid JSON types.
There are many serialization libraries, this activity uses:

- [Flask-Marshmallow](https://flask-marshmallow.readthedocs.io/en/latest/)
- [marshmallow-sqlalchemy](https://marshmallow-sqlalchemy.readthedocs.io/en/latest/)

These packages are included in this week's requirements.txt. If you did not install the requirements.txt
then `pip install flask-marshmallow marshmallow-sqlalchemy` will install them.

The steps for this part are:

- 2.1 Configure the app for Flask-Marshmallow
- 2.2 Create Marshmallow-SQLAlchemy schemas. The schema can then be used to dump and load ORM objects (i.e. objects from
  SQLAlchemy).

### 2.1 Configure the app for Flask-Marshmallow

Flask-Marshmallow will be used with Flask-SQLAlchemy.
The [documentation](https://flask-marshmallow.readthedocs.io/en/latest/#optional-flask-sqlalchemy-integration) states
that Flask-SQLAlchemy must be initialized before Flask-Marshmallow.

Other code from the `__init__.py` file is not shown here. Add the code to create and initialise Marshmallow to
the `__init__.py` file:

```python
from flask_marshmallow import Marshmallow

# Create a global SQLAlchemy object
db = SQLAlchemy()
# Create a global Flask-Marshmallow object
ma = Marshmallow()


def create_app():
    # Initialise Flask-SQLAlchemy
    db.init_app(app)
    # Initialise Flask-Marshmallow
    ma.init_app(app)
```

### 2.2 Create Marshmallow-SQLAlchemy schemas

You now need to
define [Marshmallow SQLAlchemy schemas as per their documentation](https://marshmallow-sqlalchemy.readthedocs.io/en/latest/#generate-marshmallow-schemas).
These allow Marshmallow to essentially 'translate' the fields for a SQLAlchemy object and provide methods that allow you
to convert the objects to JSON.

For this paralympics example the code is given for you below. There are two methods for creating schemas in this code.

The first example (for Region) you would use if you wish to only provide some, not all, the fields from a class in the
data. This inherits `ma.SQLAlchemySchema` and you then need to state the fields that you wish to be included in the
data.

The second example (for Event) provides all the fields. This inherits `ma.SQLAlchemyAutoSchema` and this automatically
includes all the fields from your models class, so you do not have to repeat them.

`model = Region` states the name of the model class. You need to include this.

`sqla_session = db.session` tells Marshmallow the session to use to work with the database. You need to include this.

`load_instance = True` is optional and will deserialize to model instances

`include_fk = True` is only needed if you want the foreign key field to be included in the data.

`include_relationships = True` is only needed if you have relationships between tables.

Create a file called `schemas.py`:

```python
from paralympics.models import Event, Region
from paralympics import db, ma


# -------------------------
# Flask-Marshmallow Schemas
# See https://marshmallow-sqlalchemy.readthedocs.io/en/latest/#generate-marshmallow-schemas
# -------------------------


class RegionSchema(ma.SQLAlchemyS
chema):
    """Marshmallow schema defining the attributes for creating a new region."""

    class Meta:
        model = Region
        load_instance = True
        sqla_session = db.session
        include_relationships = True

    NOC = ma.auto_field()
    region = ma.auto_field()
    notes = ma.auto_field()


class EventSchema(ma.SQLAlchemyAutoSchema):
    """Marshmallow schema for the attributes of an event class. Inherits all the attributes from the Event class."""

    class Meta:
        model = Event
        include_fk = True
        load_instance = True
        sqla_session = db.session
        include_relationships = True

```

## 3. Create instances of the schemas

First you need to import the Marshmallow SQLAlchemy schemas and create instances of them. This is the 'Schemas' section
in the code below.

There are two variants of each schema shown, one provides a single result (e.g. one event), the other provides for
multiple results (e.g. all events).

Add the following code to the file where the routes are defined i.e. in `paralympics.py`:

```python
from paralympics.schemas import RegionSchema, EventSchema

# Flask-Marshmallow Schemas
regions_schema = RegionSchema(many=True)
region_schema = RegionSchema()
events_schema = EventSchema(many=True)
event_schema = EventSchema()
```

## 3. Route that returns all regions

The first route is `/region` which gets a list of all the region codes and returns these in an HTTP response in JSON
format.

To define a route with an HTTP method in Flask:

```python
# Use route and specify the HTTP method(s). If you do not specify the methods then it will default to GET.
@app.route('/something', methods=['GET', 'POST'])
def something():


# Use Flask shortcut methods for each HTTP method `.get`, `.post`, `.delete`, `.patch`, `.put`
@app.get('/something')
def something():
```

The Flask-SQLAlchemy query syntax for a 'SELECT' query is explained in
the [Flask-SQLAlchemy 3.1 documentation](https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/queries/#select)

You query the database to get the results, then use the schemas to convert the SQLAlchemy result objects to a JSON
syntax.

```python
@app.get("/region")
def get_regions():
    """Returns a list of NOC region codes and their details in JSON."""
    # Select all the regions using Flask-SQLAlchemy
    all_regions = db.session.execute(db.select(Region)).scalars()
    # Get the data using Marshmallow schema (returns JSON)
    result = regions_schema.dump(all_regions)
    # Return the data
    return result

```

The code above will return the JSON data that is the result of the `schema.dump()`. You could also use
the [`flask.make_response()` function](https://flask.palletsprojects.com/en/2.2.x/api/#flask.Flask.make_response) to
control what is returned.

Run the app and check that the route returns JSON.

- Run the app `flask --app paralympics run --debug`
- Go to <http://127.0.0.1:5000/noc>
- Stop the app using `CTRL+C`

Now try and implement the `@app.get('/event')` route yourself.

## 4. Return one region/event

To return a single event you need to specify the event id in the URL. This is done using a variable in the URL.

Variable routes in Flask can be defined as follows:

```python
@app.get("/noc/<int:event_id>")
def event_id(event_id):
    """Returns the details for a specified event id"""
    event = db.session.execute(
        db.select(Event).filter_by(event_id=event_id)
    ).scalar_one_or_none()
    return events_schema.dump(event)

```

Run the app and check that the route returns JSON for just one region.

- Run the app `flask --app paralympics run --debug`
- Go to <http://127.0.0.1:5000/noc/2>

Now try and implement the `@app.get('/event/<event-id>')` route yourself.

## 5. Return 1 region

## 6. Add new event

## 7. Add new region

## 9. Update event

PATCH AND PUT - EXPLAIN the difference

Patch - partial update, so can just provide some of the fields.

Put - all fields, so all fields must be provided.

## 10. Update region

Delete event

Delete region
