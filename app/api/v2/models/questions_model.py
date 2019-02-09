from datetime import datetime
from flask import Flask, json, jsonify
from .base_model import BaseModel

class Question(BaseModel):
    """ questions class """
    def __init__(self):
        """initialize and define objects """
        super().__init__()
      
    def create_question(self,**kwargs):
        """" defines the logic for adding a question """

        self.title= kwargs['title']
        self.body= kwargs['body']
        self.meetup_id= kwargs['meetup_id']
        self.votes =int(x=0)
        self.username=kwargs['username']

        user = self.get_by_key("users","username",self.username)
        check_meetup = self.check_if_exists("meetups","id",self.meetup_id)

        if not check_meetup:
            return jsonify({
                "status": 404,
                "error": "{} not found".format("meetup record")
            }), 404
        else:
            question = self.check_if_question_exists("questions",**kwargs)
            if question:  
                return jsonify({
                    "status": 401,
                    "error": "question already exists"
                }), 401
            else:
                self.user_id = user[0]["id"]
                sql = """ INSERT INTO questions (meetup_id,created_by,title,body,votes)
                    VALUES({},{},'{}','{}','{}') RETURNING questions.id;""".format(self.meetup_id,self.user_id,
                        self.title,self.body,self.votes)
                save_question=self.save_data(sql)
                question =self.get_by_key("questions","id",save_question["id"])
                return jsonify({"status": 201,
                        "question":question,
                        "message":"question posted successfully",
                }), 201

    def get_question(self,id):
        ''' get question by key id '''
        pass

    def upvote_question(self,user,question_id):

        self.username=user
        self.question_id=question_id
        self.vote_count =1

        user = self.get_by_key("users","username",self.username)
        check_question = self.check_if_exists("questions","id",self.question_id)
        question =self.get_by_key("questions","id",self.question_id)
      

        if not check_question:
            return jsonify({
                "status": 404,
                "error": "{} not found".format("Question")
            }), 404
        else:
            self.user_id = user[0]["id"]
            self.current_upvotes = question[0]["upvotes"]
            vote = self.check_if_vote_exists(self.user_id,self.question_id,status="upvote")

            # check if upvote exists
            downvote = self.check_if_vote_exists(self.user_id,self.question_id,status="downvote")

            if vote:
                return jsonify({
                    "status": 401,
                    "error": "user already upvoted the question"
                }), 401
            else:
               
                if downvote:
                    value=question[0]["downvotes"]-1
                    # delete downvote record and update questions table
                    vote_sql = """DELETE FROM votes WHERE user_id ='{}' AND question_id='{}' AND downvotes=1;""".format(self.user_id,self.question_id)
                    self.delete_data(vote_sql)
                    update_sql= """UPDATE questions SET downvotes='{}'  WHERE id='{}' RETURNING questions.id;""".format(value,self.question_id)
                    self.save_data(update_sql)

                # add  upvote
                vote_sql = """ INSERT INTO votes (user_id,question_id,upvotes)
                    VALUES('{}','{}','{}') RETURNING votes.id;""".format(self.user_id,self.question_id,self.vote_count)
                self.save_data(vote_sql)
                new_votes = self.current_upvotes +1
                
                # update question vote
                update_sql= """UPDATE questions SET upvotes='{}'  WHERE id='{}' RETURNING questions.id;""".format(new_votes,self.question_id)
                self.save_data(update_sql)

                # get question
                question =self.get_by_key("questions","id",self.question_id)
                return jsonify({"status": 201,
                        "data":question,
                        "message":"sucessfully upvoted question",
                }), 201

    def downvote_question(self,user,question_id):

        self.username=user
        self.question_id=question_id
        self.vote =1

        user = self.get_by_key("users","username",self.username)
        check_question = self.check_if_exists("questions","id",self.question_id)
        question =self.get_by_key("questions","id",self.question_id)

        if not check_question:
            return jsonify({
                "status": 404,
                "error": "{} not found".format("Question")
            }), 404
        else:
            self.user_id = user[0]["id"]
            self.current_vote = question[0]["downvotes"]
            vote = self.check_if_vote_exists(self.user_id,self.question_id,status="downvote")
            # check if upvote exists
            upvote = self.check_if_vote_exists(self.user_id,self.question_id,status="upvote")
            if vote:
                return jsonify({
                    "status": 401,
                    "error": "user already downvoted the question"
                }), 401
            else:
                
                if upvote:
                    value=question[0]["upvotes"]-1
                    # delete upvote record and update questions table
                    vote_sql = """DELETE FROM votes WHERE user_id ='{}' AND question_id='{}' AND upvotes=1;""".format(self.user_id,self.question_id)
                    self.delete_data(vote_sql)
                    update_sql= """UPDATE questions SET upvotes='{}'  WHERE id='{}' RETURNING questions.id;""".format(value,self.question_id)
                    self.save_data(update_sql)

                # add downvote record
                vote_sql = """ INSERT INTO votes (user_id,question_id,downvotes)
                    VALUES('{}','{}','{}') RETURNING votes.id;""".format(self.user_id,self.question_id,self.vote)
                self.save_data(vote_sql)
                vote = self.current_vote+1

                # update question votes
                update_sql= """UPDATE questions SET downvotes='{}'  WHERE id='{}' RETURNING questions.id;""".format(vote,self.question_id)
                self.save_data(update_sql)

                # update question
                question =self.get_by_key("questions","id",self.question_id)
                return jsonify({"status": 201,
                        "data":question,
                        "message":"sucessfully downvoted question",
                }), 201

