creative project
sneaker aggregator
framework: flask

rubric (5 points)
x rubric is turned in on time (5 points)

website functionality (23 points)
x users can sign in and log in to the website (3 points)
x users can sign up as standard users or admins (5 points)
x users cannot alter other's posts (5 points)
x Relational database is configured with correct data types and foreign keys (5 points)
x ONLY admins can upload picture, name and release date to the website (5 points)

reviews (10 points)
x users can post reviews (text) and scores (out of 100) of sneakers (5 points)
x all points are averaged and displayed on the sneaker display page (5 points)

usability (7 points)
x site in intuitive to use and navigate (5 points)
x site is visually appealing (2 points)

user home page (15 points)
x each user has a favorites page where their favorites are listed (10 points)
x users can send messages to others users, which are posted to that users' homepage (5 points)

best practices (20 points)
x code is well formated and easy to read, with proper commenting (2 points)
x requests that contain sensitive information or modify something ont he server are performed via POST not GET (3 points)
x Safe from XSS attacks (all content is escaped on output) (3 points)
x Safe from SQL injection attacks (2 points)
CSRF tokens passed when editing or deleting posts (3 points)
x Session cookie is HTTP-only (3 points)
x page passes the W3C validator (2 points)
x passwords are salted and encrypted (2 points)

creative portion (20 points)
x shoes can be associated with brands and then searched by brand (10 points)
x only admins may delete posts (5 points)

to do:
make sure user can only favorite a shoe once
