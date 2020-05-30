# Sample Web discussion forum built in Django - CRUD (Create Read Update Delete) database operations


I created this while learning Django from this tutorial : [SimpleIsBetterThanComplex](https://simpleisbetterthancomplex.com/series/beginners-guide/1.11/)


*I was a total beginner in Django while developing this project, however I learnt a lot during the development.
This sample application contains limited features and therefore can be updated to include new ones.*


## Brief description of project:

- Only admin users can create new Boards.
- Users can ask queries by starting topics under existing boards.
- Users can also post replies to existing topics.

(You can consider Python as a Board and all queries regarding Python can be asked by starting topics)


## Functionalities included in project:

- User signup
- User login
- Password reset - in case user forgets password
- Change password
- Topic creation
- Posting replies to topic
- Markdown editor for post message

## Tools and technologies :

- Django - Python framework for web application
- HTML - for creating django webpage templates
- W3.CSS - CSS framework which is similar to Bootstrap
- markdown - Python library for markdown
- django-mdeditor - Python library for markdown editor
- python-decouple - Python library for separating secret setting parameters of project from source code
- dj_database_url - Python library to simplify database connection values
- sendgrid - Python library for free email service using Sendgrid API
- PythonAnywhere - for deployment of django application, serving static & media files
- Sublime Text Editor - for writing code
- Git - for version control

## How to run this project :

0. Make sure you have Python 3, Git and virtualenv library installed
1. Create a directory - `forum_folder`
2. Inside `forum_folder`, create virtual environment using `virtualenv menv`
3. Activate virtualenv by going in `menv`>`Scripts`> run `activate`. `menv` is now activated in shell or cmd prompt.
4. Inside `forum_folder`, run `git clone https://github.com/mir1198yusuf/discussion_forum`
5. Navigate to newly created folder `discussion_forum`, run `pip install -r requirements.txt`
6. Generate Django secret key for project. Run `python generate_secret_key.py` and copy the output string
7. Paste it in `.env` file at `YOUR_SECRET_KEY`
8. Run `python manage.py migrate` to apply database migrations.
9. Create a user `python manage.py createsuperuser`
10. Finally start the project - `python manage.py runserver`
11. Go to the link displayed in shell/cmd prompt to view site. 

## Live demo site

The project is live at [site](bit.ly/forum_live)


