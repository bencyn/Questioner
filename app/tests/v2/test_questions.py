import json ,unittest,instance,datetime
from .base_tests import BaseTest
from app.api.v2.views import questions_view
from app import create_app

app = create_app("testing")


class QuestionTest(BaseTest):

    def setUp(self):
        """define test user variables"""
        BaseTest.setUp(self)
    
    def test_user_can_post_question(self):
        """ test if user can post a question"""
        response = self._post_question()
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(result['status'], 201)
        self.assertEqual(result['question'][0]["body"],self.question["body"])

    def test_user_upvote_question(self):
        """ test if user can upvote a question"""

        upvote_url = self._get_vote_url("upvote")
        print(upvote_url)
        response = self.client.patch(upvote_url, content_type="application/json",headers=self._get_header())
        result = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 201)
        self.assertEqual(result['data'][0]["body"],self.upvote_response["body"] )
        self.assertEqual(result['data'][0]["title"],self.upvote_response["title"] )

    def test_question_upvote_if_question_not_found(self):
        """ tests if user can upvote a non existent question """

        upvote_url = self._get_vote_url("upvote",id=30)
        response = self.client.patch(upvote_url, content_type="application/json",headers=self._get_header())
        result =json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(result["error"],"Question not found")

    def test_if_user_can_downvote_question(self):
        """ defines tests for downvoting a question """
    
        url = self._question_get_url()
        self.client.patch(url+'upvote', content_type="application/json",headers=self._get_header())
        response = self.client.patch(url+'downvote', content_type="application/json",headers=self._get_header())
        result = json.loads(response.data.decode('utf-8'))
        print(result)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(result['data'][0]["body"],self.downvote_response["body"])

    def test_question_downvote_if_question_not_found(self):
        """ test if user can downvote a non existent question """

        upvote_url = self._get_vote_url("upvote",id=30)
        response = self.client.patch(upvote_url, content_type="application/json",headers=self._get_header())
        result =json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(result["error"],"Question not found")

 
    def test_if_post_question_element_is_missing(self):
        """ test missing input elements"""

        response = self._post_question(self.question_er2)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(result['status'], 400)
        self.assertEqual(result['error'],"body field required")

    def test_if_post_question_input_is_empty(self):
        """ test empty input data"""

        response = self._post_question(self.question_er)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(result['status'], 400)
        self.assertEqual(result['error'],"title cannot be empty")
