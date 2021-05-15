# who-may-twit-this

This is a Flask web application that will guess who might twit the text (user input).






To create all table, in flask shell:
~~~
from app.models import DB
DB.create_all()
~~~

To add users to table
~~~
flask shell
from app.twitter import add_or_update_user
add_or_update_user('nasa')
~~~