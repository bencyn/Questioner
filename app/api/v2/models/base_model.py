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
        print(query)
        conn.connection.commit()
        if conn.cursor.fetchone():
            return True
        else:
            return False

    def check_if_vote_exists(self,user,question,status):
        """ checks if a vote is present"""
        if status == "upvote":
            query = "SELECT * FROM votes WHERE user_id='{}' AND question_id='{}' AND upvotes=1".format(user,question)
        else:
            query = "SELECT * FROM votes WHERE user_id='{}' AND question_id='{}' AND downvotes=1".format(user,question)
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
    
    def check_if_rsvp_exists(self,table,**kwargs):
        """ checks if record is present"""
        query = "SELECT * FROM {} WHERE meetup_id='{}' AND user_id='{}'".format(table,kwargs["meetup_id"],
                                    kwargs["user_id"])
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
        print(query)
        conn.cursor.execute(query)
        data = conn.cursor.fetchall()
        conn.connection.commit()
        result = []
        for row in data:
            result.append(dict(row))
        return result

    def get_by_query(self,status):
        """fetch data by query passed"""
        if(status=="posted"):
            query=''
        if(status =="feeds"):
            query=''
        if(status=="commented"):
            query=''
            
        try:
            conn.cursor.execute(query)
            data= conn.cursor.fetchall()  
            conn.connection.commit()
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

    def get_by_key(self,table,field,value):
        """ get records  by id"""
        query = """SELECT * FROM %s WHERE %s='%s' ORDER BY id DESC;"""%(table,field,value)
        
        try:
            conn.cursor.execute(query)
            data= conn.cursor.fetchall()  
            conn.connection.commit()
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
    def get_with_user(self,table,cast,field,value):
        """ get records  by id"""
        query = """SELECT *,{x}.id as {x}_id FROM %s RIGHT JOIN users ON users.id = CAST (%s AS INTEGER) WHERE %s='%s' ORDER BY {x}.id DESC;""".format(x=table)%(table,cast,field,value)
        
        try:
            conn.cursor.execute(query)
            data= conn.cursor.fetchall() 
            print(query) 
            conn.connection.commit()
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

    def user_profile(self,user_id,status):
        """ get user profile statistics """
        if (status =="feeds"):
            # query = """SELECT *,{x}.id as {x}_id FROM %s RIGHT JOIN users ON users.id = CAST (%s AS INTEGER) WHERE %s='%s' ORDER BY {x}.id DESC;""".format(x=table)%(table,cast,field,value)
            query=""" SELECT *,questions.body as questions_body,questions.id as questions_id FROM questions FULL OUTER JOIN users ON users.id = CAST (questions.created_by AS INTEGER) FULL OUTER JOIN meetups ON meetups.id=CAST (questions.meetup_id AS INTEGER)
                    FULL OUTER JOIN rsvps ON  CAST (rsvps.meetup_id AS INTEGER)=meetups.id 
                    WHERE rsvps.user_id='{}' ORDER BY questions.upvotes DESC LIMIT 5;""".format(user_id)
        if(status=="posted"):
            query="""SELECT COUNT(questions.id) FROM questions WHERE created_by='{}'""".format(user_id)
        if(status=="commented"):
            query="""SELECT COUNT(questions.id) FROM questions INNER JOIN comments ON CAST (comments.question_id AS INTEGER)=questions.id  WHERE comments.user_id='{}'""".format(user_id)

        return self.execute_get_query(query)

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
   
    def execute_get_query(self,query):
        try:
            conn.cursor.execute(query)
            data= conn.cursor.fetchall() 
            print(query) 
            conn.connection.commit()
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

    def execute_query(self,query):
        conn.cursor.execute(query)
        conn.connection.commit()
    
