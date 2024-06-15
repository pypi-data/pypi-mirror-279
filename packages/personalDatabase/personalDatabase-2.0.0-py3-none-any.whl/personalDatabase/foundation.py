import psycopg2
from custom_development_standardisation.function_output import *
from psycopg2 import OperationalError,Error

class foundation():
    def __init__(self) -> None:
        self.cursor = None

    def initialise(self,database_name,port=5432):
        try:
            # Attempt to establish a connection
            connection = psycopg2.connect(
                database=database_name,
            )
            self.cursor = connection.cursor()
            return generate_outcome_message("success","Cursor object has been created...")
        
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
        

    

# outcome.execute("select * from companies")
# print(outcome.fetchall())