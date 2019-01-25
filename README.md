# Questioner
  Questioner is a platform that allows users to crowdsource questions for a meetup.
  
Badges
------

[![Build Status](https://travis-ci.org/bencyn/Questioner.svg?branch=develop)](https://travis-ci.org/bencyn/Questioner) [Maintainability](https://api.codeclimate.com/v1/badges/3ae0d2569165f3344e8e/maintainability)](https://codeclimate.com/github/bencyn/Questioner/maintainability)


Overview
--------
The platform helps meetup organizer priotize questions to be answered.Other users can vote on asked questions.

This project is managed using a pivotal tracker board. [View the board here](https://www.pivotaltracker.com/n/projects/2235259)

### HEROKU LINK
[HEROKU API](https://bencyn-questioner.herokuapp.com/api/v1)

<!-- [Github Pages](https://bencyn.github.io/Questioner/UI/)  -->
[Documentation](https://documenter.getpostman.com/view/2456985/RzthRBe9)

Features
-----------------------
1.users can get all meetups

2.users can get a specific meetups

3.users can post a question to a specific meetup

4.users can downvote a question

5.users can upvote a question

6.admin user can post a meetup


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


# API Auth


|Endpoint                           |   Method   | description         |
|  ------------                     | ---------- |  -----------------  |
|/api/v2/auth/signup                |   POST     | add  a new user     |
|                                   |            |                     |
|/api/v2/auth/login                 |   POST     | User Login token    |
|                                   |            |                     |
|/api/v2/auth/all                   |   GET      | get alls users      |
|                                   |            |                     |
|/api/v2/auth/<id>                  |   GET      | get user by id      |

# API Endpoints

|   # Endpoint                              |  # Methods    | # Description           |Auth Required           |
|   -----------                             | ----------    | -----------------       | ------------           |
|/api/v2/auth/<user-id>/meetups             |   GET         |  post a meetup          | admin                  |
|                                           |               |                         |                        | 
|/api/v2/meetups/upcoming/                  |   GET         |  get upcoming meetups   | normal user            | 
|                                           |               |                         |                        | 
|/api/v2/meetups/<id>                       |   DELETE      |  delete meetup          | normal user            | 
|                                           |               |                         |                        | 
|/api/v2/meetups/<id>                       |    GET        |  get specific meetup    | normal user            | 
|                                           |               |                         |                        | 
|/api/v2/meetups/<meetup-id>/questions      |    POST       |  post meetup question   | logged in normal user  | 
|                                           |               |                         |                        | 
|/api/v2/questions/<quetion-id>/downvote    |   PATCH       |  downvote a question    | logged in normal user  | 
|                                           |               |                         |                        | 
|/api/v2/questions/<question-id>/upvote     |   PATCH       |  upvote a question      | logged in normal user  | 
|                                           |               |                         |                        | 
|/api/v2/questions/<question-id>/comments   |   POST        |  post a comment         | logged in normal user  |
|                                           |               |                         |                        | 
|/api/v2/questions/all                      |   GET         |  display all questions  |  norma user            | 

Authors
-----------------------------
**Benson Njung'e** - _Initial work_-[becnyn](https://github.com/bencyn/Questioner)

Acknowledgements
-------------------------------
1. Andela Workshops
2. Team members



