import json ,unittest,instance,datetime
from .base_tests import BaseTest
from app import create_app

app = create_app("testing")

class TestMeetup(BaseTest):
    def setUp(self):
        """define test meetup variables"""
        BaseTest.setUp(self)
        self.get_meetups_url='api/v2/meetups/upcoming/'
        self.get_meetup_url = 'api/v2/meetups/1'
        self.delete_meetup_url = 'api/v2/meetups/1'

    def test_user_can_create_meeetup_record(self):
            ''' test user can create a meetup record'''
            url = self._meetup_post_url()
            response= self.client.post(url,data = json.dumps(self.meetups[0]), 
                                                    content_type="application/json",headers=self._get_header())

            result = json.loads(response.data.decode('UTF-8'))
            print(result)
            self.assertEqual(response.status_code, 201)
   
    def test_user_can_get_meetup_records(self):
        ''' test user can get all meetup records '''
        url = self._meetup_post_url()

        self.client.post(url,data = json.dumps(self.meetups[0]),content_type="application/json",headers=self._get_header())
        self.client.post(url,data = json.dumps(self.meetups[1]),content_type="application/json",headers=self._get_header())

        response = self.client.get(self.get_meetups_url,content_type = "application/json")
        self.assertEqual(response.status_code, 200)

    def test_user_can_get_specific_meetup_record(self):
        ''' test whether user can get a specific record using it's meetup id '''

        url = self._meetup_post_url()
        self.client.post(url,data = json.dumps(self.meetups[0]),content_type="application/json",headers=self._get_header())
        self.client.post(url,data = json.dumps(self.meetups[1]),content_type="application/json",headers=self._get_header())

        response = self.client.get(self.get_meetup_url, content_type="application/json")
        result = json.loads(response.data.decode('UTF-8'))
        print(result)
        self.assertEqual(response.status_code,200)
        self.assertEqual(result["meetup"][0]["topic"],"Hackathon For The Brave")

    def test_if_user_can_delete_specific_meetup_record(self):
        """tests whether user can delete a specific meetup record"""
        
        url = self._meetup_post_url()
        self.client.post(url,data = json.dumps(self.meetups[0]),content_type="application/json",headers=self._get_header())
        self.client.post(url,data = json.dumps(self.meetups[1]),content_type="application/json",headers=self._get_header())

        response = self.client.delete(self.delete_meetup_url, content_type="application/json",headers=self._get_header())

        self.assertEqual(response.status_code,200)