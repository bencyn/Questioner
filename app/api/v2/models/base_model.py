from flask import Flask, json, jsonify
from app import conn
import datetime

class BaseModel:
    """ defines global functions for sub models """

    def __init__(self):
        """ initialize database """
        pass

    def save_data(self,sql):
        """defines global save function"""
        conn.cursor.execute(sql)

        result = conn.cursor.fetchone()
        conn.connection.commit()

        return result
    def delete_data(self,sql):
        """ defines global delet function"""
        
        conn.cursor.execute(sql)
        conn.connection.commit()

        return True

    def update_data(self,sql):
        """ define global update function """
        pass
  
    def check_if_exists(self, table, field, data):
        """ check if a record or records exist """
       
        query = "SELECT * FROM {} WHERE {}='{}'".format(table, field, data)
        conn.cursor.execute(query)
        if conn.cursor.fetchone():
            return True
        else:
            return False

    def check_if_vote_exists(self,data,data2,status):
        """ checks if a vote is present"""
        if status == "upvote":
            query = "SELECT * FROM votes WHERE user_id='{}' AND question_id='{}' AND number=1".format(data,data2)
        else:
            query = "SELECT * FROM votes WHERE user_id='{}' AND question_id='{}' AND number=-1".format(data,data2)
        conn.cursor.execute(query)
        if conn.cursor.fetchone():
            return True
        else:
            return False

    def check_if_question_exists(self,table,**kwargs):
        """ checks if record is present"""
        query = "SELECT * FROM {} WHERE title='{}' AND body='{}' AND meetup_id='{}'".format(table,kwargs['title'],
                                kwargs["body"],kwargs["meetup_id"])
        conn.cursor.execute(query)
        if conn.cursor.fetchone():
            return True
        else:
            return False

    def check_if_meetup_exists(self,table,**kwargs):
        """ checks if record is present"""
        query = "SELECT * FROM {} WHERE topic='{}' AND location='{}' AND happening_on='{}'".format(table,kwargs["topic"],
                                    kwargs["location"],kwargs["happening_on"])
        conn.cursor.execute(query)
        if conn.cursor.fetchone():
            return True
        else:
            return False


    def get_user_by_username(self,username):
        """ get user by username """
        
        query="""SELECT username, password FROM users WHERE username = '{}'""".format(username)
        conn.cursor.execute(query)
        data = conn.cursor.fetchone()
        # conn.cursor.close()

        return data

    def get_all(self,table,meetup=False):
        """ get all records"""
        now = datetime.datetime.now()
        current_date = now.strftime("%Y-%m-%d")
        if meetup:
            query="""SELECT * FROM {} WHERE happening_on > '{}' """.format(table,current_date)
        else:
            query="""SELECT * FROM {} """.format(table)
        conn.cursor.execute(query)
        data = conn.cursor.fetchall()
        result = []
        for row in data:
            result.append(dict(row))
        return result

    def get_by_key(self,table,field,value):
        """ get records  by id"""
        query = """SELECT * FROM %s WHERE %s='%s';"""%(table,field,value)
        try:
            conn.cursor.execute(query)
            data= conn.cursor.fetchall()  
            if not data:
                return False
            else:
                result = []
                for row in data:
                    result.append(dict(row))
                return result

        except ValueError as e:
            message = {'message': '{}'.format(e)}
            return jsonify({"status": 400,"error":message}), 400
    
    def delete_by_key(self,table,field,value):
        """ delete record by id"""
        query = "DELETE FROM {} WHERE {}={}".format(table,field,value)
        try:
            conn.cursor.execute(query)
            conn.connection.commit()
            return True
        except ValueError as e:
            message = {'message': '{}'.format(e)}
            return jsonify({"status": 400,"error":message}), 400
       

    def execute_query(self,query):
        conn.cursor.execute(query)
        conn.connection.commit()
    