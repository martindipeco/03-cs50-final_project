# N.G.O.´s Free Courses Web App
### Martin Di Peco
### Buenos Aires, Argentina

#### Video Demo: [NGO Free Courses Web App](https://youtu.be/VWNwXfzdy5k)

#### Description:

A web app to provide free educational services for N.G.O.s working with local communities.
In this first phase it only allows students to register to courses.
Its structure is based on [CS50´s Finance](https://finance.cs50.net/)
It runs under Flask, CS50´s served. Written in Python, using Jinja, CSS and HTML5. Database created with SQlite3
You can check the database structure [here](https://drawsql.app/martindipeco/diagrams/ngo)

##### What does it do?

- It registers students and allows use after logging in
- It shows available courses with their corresponding timetable
- It signs students in for any selected course
- It provides a contact page

##### What features does it have?

Registration: Inserts username and password hash into students table, checking that it is unique, that both username and password were submitted, that password was typed correctly, and then redirecting to log in

![Registration screenshot](/project/Screenshots/Screenshot-register.JPG)


Log in: Checks that username and password were submitted, that they are both correct and stores in `session["user_id"]` to remember which user has logged in

![Log in screenshot](/project/Screenshots/Screenshot-login.JPG)


Index: After logging in, shows list of enrolled courses, which will be empty at first

![Index a.k.a. My Courses after first sign in](/project/Screenshots/Screenshot-index-empty.JPG)


All Courses: Displays the content of the `courses_all` table, a complete list of courses with their timetable

![All courses screenshot](/project/Screenshots/Screenshot-allcourses.JPG)


Select & sign up: Displays menu to pick up a course to enroll

![Select and sign up screenshot](/project/Screenshots/Screenshot-select-signup.JPG)


Then you are redirected to index, where you will see your updated list

![My courses, after signing up](/project/Screenshots/Screenshot-index-math.JPG)


The `contact` page simply displays address, phone and email in case you would like to ask for more information, or eventually sign out of a course. There was a `sign out` button, but I thought it could encourage dropping out.


##### What does each file contain and do?

`application.py`: Controller file

`ngo.db`: Model, databese where info on students, courses and enrollments is organized

`static` and `templates` folders: View, where css and html files are


