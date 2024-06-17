import psycopg2
from custom_development_standardisation.function_output import *
from psycopg2 import OperationalError,Error

class foundation():
    def __init__(self) -> None:
        self.cursor = None

    def initialise(self,database_name,user=None,host=None):
        try:
            if user == None and host == None:
                connection = psycopg2.connect(
                    database=database_name,
                    port=5433,
                )
                
                self.cursor = connection.cursor()
                return generate_outcome_message("success","Cursor object has been created...")
            else:
                connection = psycopg2.connect(
                    database=database_name,
                    user=user,
                    host=host,
                    port=5433
                )
                self.cursor = connection.cursor()
                return generate_outcome_message("success","Cursor object has been created...")
            # Attempt to establish a connection
            
        
        except OperationalError as e:
            # Print the error message
            return generate_outcome_message("error",e,the_type="others")
            
    def execute(self,command):
        if self.cursor == None:
            return generate_outcome_message("error","cursor has not been initialised...Run initialise method...",the_type="custom")
        try:
            self.cursor.execute(command)
            outcome = self.cursor.fetchall()
            return generate_outcome_message("success",outcome)
        except Error as e:
            return generate_outcome_message("error",e.pgerror,the_type="others")
        

    
x = foundation()
print(x.initialise("logging_data",user="marcus",host="39.109.219.232"))
print(x.execute("select * from test"))
