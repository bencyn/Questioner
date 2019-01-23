# Questioner
  Questioner is a platform that allows users to crowdsource questions for a meetup.
  
Badges
------

[![Build Status](https://travis-ci.org/bencyn/Questioner.svg?branch=develop)](https://travis-ci.org/bencyn/Questioner)  [![Coverage Status](https://coveralls.io/repos/github/bencyn/Questioner/badge.svg?branch=develop)](https://coveralls.io/github/bencyn/Questioner?branch=develop) [![Maintainability](https://api.codeclimate.com/v1/badges/3ae0d2569165f3344e8e/maintainability)](https://codeclimate.com/github/bencyn/Questioner/maintainability)

Overview
--------
The platform helps meetup organizer priotize questions to be answered.Other users can vote on asked questions.

This project is managed using a pivotal tracker board. [View the board here](https://www.pivotaltracker.com/n/projects/2235259)

[Github Pages](https://bencyn.github.io/Questioner/UI/) 
[Documentation](https://documenter.getpostman.com/view/2456985/RznHHciU)
[Heroku Link](https://bencyn-questioner.herokuapp.com/api/v1)

[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://bencyn-questioner.herokuapp.com/api/v1/)


Features
-----------------------
1.users can get all meetups

2.users can get a specific meetups

3.users can post a question to a specific meetup

4.users can downvote a question

5.users can upvote a question

6.users can RSVP meetup


Pre-requisites
----------------------
1. Python3
2. Flask
3. Flask restplus
4. Postman

Getting started
--------------------
1. Clone this repository
```
    https://github.com/bencyn/Questioner.git
```

2. Navigate to the cloned repository
```
    cd Questioner
```

Installation
---------------------------------
1. Create a virtual environment
```
    virtualenv -p python3 venv
```

2. Activate the virtual environment
```
    source venv/bin/activate
```

3. Install git
```
    sudo apt-get install git-all
```

4. Switch to 'develop' branch
```
    git checkout develop
```

5. Install requirements
```
    pip install -r requirements.txt
```
Run the application
---------------------------------
```
    python3 run.py
```

When you run this application, you can test the following API endpoints using postman
-----------------------------------------------

| Endpoint | Functionality |
----------|---------------
POST/meetups | Create a meetup record
GET/meetups/<meetup-id> | Fetch a specific meetup record
GET /meetups/upcoming/ | Fetch all upcoming meetup records
POST /meetups/<meetup-id>/questions | Create a question for a specific meetup
PATCH /questions/<question-id>/upvote | Upvote (increase votes by 1) a specific question
PATCH /questions/<question-id>/downvote | Downvote (decrease votes by 1) a specific question
POST /meetups/<meetup-id>/rsvps | Respond to meetup RSVP
POST /users | Create a user account
GET  /users/all | Fetch users
GET  /users/<user-id> | Get a specific user account


Authors
-----------------------------
**Benson Njung'e** - _Initial work_-[becnyn](https://github.com/bencyn/Questioner)

Acknowledgements
-------------------------------
1. Andela Workshops
2. Team members



