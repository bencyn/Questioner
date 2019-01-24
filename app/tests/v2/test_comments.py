import json ,unittest,instance,datetime
from .base_tests import BaseTest
from app import create_app

class CommentTest(BaseTest):

    def setUp(self):
        """define test user variables"""
        BaseTest.setUp(self)
    
    def test_user_can_post_comment(self):
        """ test if user can post a comment"""
        response = self._post_comment()
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(result['status'], 201)
        self.assertEqual(result['message'],"comment posted successfully")

    def test_user_cannot_post_empty_comment(self):
        """ test if user can post an empty comment"""
        response = self._post_comment(self.empty_comment)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(result['status'], 400)
        self.assertEqual(result['error'],"comment cannot be empty")

    def test_user_cannot_post_nonexistent_comment(self):
        """ test if user can post a non existent comment """
   
        question_result = json.loads(self._post_question().data.decode('utf-8'))
        question_id = question_result["question"][0]["id"]
        self.post_comment_url = 'api/v2/questions/{}/comments'.format(question_id)

        response = self.client.post(self.post_comment_url, data = json.dumps(self.comment_none), 
                                                                        content_type="application/json",headers=self._get_header())
        result = json.loads(response.data.decode('utf-8'))
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(result['status'], 400)
        self.assertEqual(result['error'],"comment field required")