'''
https://gist.github.com/mw3i/b879895272a28d1c789f23ee91555620
Proof of Concept: 

Django devs built an ORM that seems way more straightforward than many existing tools. This class lets you leverage the django-orm without any project settings or other aspects of a django setup.

There are probably weak points and functionality missing, but it seems like a relatively intuitive proof of concept
'''
import os
import django
from django.conf import settings
from django.db import models, connections

class Database:
    def __init__(self, engine='django.db.backends.sqlite3', name=None, user=None, password=None, host=None, port=None):
        self.Model = None

        # Define the DATABASES dictionary
        databases = {
            'default': {
                'ENGINE': engine,
                'NAME': name,
                'USER': user,
                'PASSWORD': password,
                'HOST': host,
                'PORT': port,
                'APP_LABEL': 'isolated',
            }
        }

        # Update the settings with the custom DATABASES dictionary
        settings.configure(DATABASES=databases)

        # Initialize Django
        django.setup()

        # Create the custom base model
        class CustomBaseModel(models.Model):
            class Meta:
                app_label = 'isolated'
                abstract = True

        self.Model = CustomBaseModel

    # Create a table if it doesnt exist
    def create_table(self, model):
        with connections['default'].schema_editor() as schema_editor:
            if model._meta.db_table not in connections['default'].introspection.table_names():
                schema_editor.create_model(model)

    # Update table if you added fields (doesn't drop fields as far as i know, which i was too afraid to implement)
    def update_table(self, model):
        with connections['default'].schema_editor() as schema_editor:
            # Check if the table exists
            if model._meta.db_table in connections['default'].introspection.table_names():
                # Get the current columns in the table
                current_columns = [field.column for field in model._meta.fields]

                # Get the database columns
                database_columns = connections['default'].introspection.get_table_description(connections['default'].cursor(), model._meta.db_table)
                database_column_names = [column.name for column in database_columns]

                # Check if each field in the model exists in the database table
                for field in model._meta.fields:
                    if field.column not in database_column_names:
                        # Add the new column to the table
                        schema_editor.add_field(model, field)


# Example Usage (pretty easy right?)
if __name__ == '__main__':
    db = Database(engine='django.db.backends.sqlite3', name='mydatabase')

    # This is required
    class Test(db.Model):
        name = models.CharField(max_length = 200, null = True)
        email = models.CharField(max_length = 200, null = True)
    Test._meta.db_table = 'test' # <-- this is also required; otherwise, django assumes the table is named `{appname}_{tablename}`, which in this case would be 'isolated_test'

    db.create_table(Test) # <-- this is required if the table doesnt already exist; could probably even make this happen automatically when initializing the table

    # Add row to table
    test = Test(name = 'hey', email = 'test@test.com')
    test.save()

    test = Test(name = 'hi')
    test.save()

'''
This feels like it covers 95% of use cases for most lightweight projects involving relational databases, but I could be wrong
''' 