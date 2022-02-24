import mysql.connector as mySQL
import configparser
import hashlib
import pandas as pd

# from ..utilities.generalUtils import GeneralUtils
from ..database.dbManager import DBManager

config = configparser.ConfigParser()
config.read('config.ini')


class AuthManager:

    def __init__(self):

        # self.general_utils = GeneralUtils()
        self.db_manager= DBManager()
    

    def store_user(self, data):
        try:
            mydb = self.db_manager.getDatabaseConnection()
            cursor = mydb.cursor(buffered=True)

            select_query = "SELECT email FROM users WHERE email = \'" + data["email"] + "'"
            cursor.execute(select_query)
            select_result=cursor.fetchone()
            if select_result == None:
                insert_query = "INSERT INTO users (email, password) VALUES(%s, %s)"
                hashed_pass = hashlib.sha256(data["password"].encode('utf-8')).hexdigest()
                insert_args = (data["email"], hashed_pass)
                cursor.execute(insert_query, insert_args)
                mydb.commit()
            user = {"email": data["email"], "role": ["user"]}
        except Exception as e:
            print("====================" + str(e) + "====================")
            user = {}
        finally:
            cursor.close()
            mydb.close()
            return user

    def retrieve_user(self, data):
        
        user = {}
        message = ""
        try:
            mydb = self.db_manager.getDatabaseConnection()
            cursor = mydb.cursor(buffered=True)

            select_query = "SELECT * FROM users WHERE email = \'" + data["email"] + "'"
            cursor.execute(select_query)
            select_result=cursor.fetchone()
            if select_result != None:
                if data["password"] == select_result[1]:
                    user = {"email": select_result[0]} 
        except Exception as e:
            print("====================" + str(e) + "====================")
        finally:
            cursor.close()
            mydb.close()
            return user
    
    def retrieve_user_by_email(self, email):
        '''
            func that returns user
            input: user email
        '''
        user = {}
        try:
            mydb = self.db_manager.getDatabaseConnection()
            cursor = mydb.cursor(buffered=True)
            select_query = "SELECT * FROM users WHERE email = \'" + email + "'"
            cursor.execute(select_query)
            select_result = cursor.fetchone()
            if select_result != None:                
                user = {"email": select_result[0]}
        except Exception as e:
            print("====================" + str(e) + "====================")
        finally:
            cursor.close()
            mydb.close()
            return user
    

