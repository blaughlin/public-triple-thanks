This is an online gratitude journal network application. It uses Django for the backend and HTML, JavaScript, and bootstrap for the front end.  Users can post daily private and public entries with the goal of posting three gratitude entries per day. This is a spin-off of the network project, with more features such as the ability to upload your own profile pic or avatar, GIS JavaScript map of user locations, private and public posts, ability to edit profile page, individual posts are grouped by the day they were created and displayed as a single post per day, the ability to reset passwords by emailing the user, and a responsive page design were the menu is adjusted depending on screen size. The content is displayed adequately whether on an iPhone or desktop screen. I was able to get this site to go live on google app engine at triplethanks.com but I might move to another provider due to the cost. 

Below is a description of each file in their corresponding folders.

								Main Directory
requirements.txt
Contains required packages needed to deploy this website. 

README.md
 Description of this network application and list of files created or modified for the application

manage.py
Django’s command-line utility for administrative tasks.

								Thanks Folder
thanks/settings.py
 Setting file for the application. Post app and localflavor was added to the installed apps. Post is the model app and localflavor manages US states in a dropdown menu. The static and media directories are also declared in here. Time zone was changed to Alaskan.

thanks/urls.py
URL Configuration file that links routes to URL views. Added posts and admin urls as well as setting up where static and media files should be places. 

								Static Folder
static/default.jpg
Contain the default profile picture for users who do not want to upload their own.

								Posts Folder:
posts/admin.py
 Registers User, Post, Like, and Social models so that they can be modified and managed with the default Django admin view. 

posts/apps.py
Declares post application configuration.

posts/forms.py
Declares PostForm which is part of the Post model, with the following fields: post and private.  CSS attributes on how to display the form are added here too. Declares the ProfileForm with is part of the User model with the following fields: first_name, last_name, city, state, zip_code, about, profile_pic, latitude, and longitude. CSS attributes on how to display the form are added here too.

posts/models.py
Defines the SQL models: User, Social, Post, and Like. There is also a dictionary of US state names with their abbreviation. This is needed to obtain correct longitude and latitude from geopy.geocoder. The User model contains the following fields: city, state, zip_code, profile_pic, first_name, last_name, about, latitude, and longitude. I have overwritten the save method to calculate the latitude and longitude of the user with each save call based on the user’s city, state abbreviation, and zip code. It is necessary to have all three to demarcate the correct location. The Social model tracks user followers and has the following fields: user and follower. The Post model takes care of user gratitude posts and contains the following fields: post, user, timestamp, liked, date, and private. There is serialize method to convert to JSON data and total likes method to calculate total likes of post. The last model is the Like model which keeps track of how many likes a post has per user. 

posts/views.py 
Contains callable views functions. Index function return index.html main page, which is the first page people see when they log into the site. The login_view returns the login page where people enter their username and password, which is authenticated via Django backend. The logout_view redirects the users to the index page. The register function redirects user to register.html page where they can create a username, password, and enter their email. It is authenticated via Django backend. The allPosts function redirects user to the allPosts page which displays all public posts made by every user consolidated by date and use. I t displays 20 posts per page. The addTanks function redirects to the addThanks page were users can enter their gratitude, there is an option to post privately or publicly. It keeps track of the date the last post and tracks and displays how many posts the user has made in one day. The editProfile function redirects user to the editProfile page where they can edit information about themselves including: first_name, last_name, city, state, zip_code, about, and profile_pic. It saves any changes made. The profile function redirects the user to the profile page which displays the information entered on the edit_profile page. It also displays the number of followers, people following the user, and number of posts the user has made. The journal function redirects to the journal page which shows the private and public posts made by the user that is logged in. Its dispays 10 posts per page. The posts are consolidated by day and ordered from newest to oldest. The editView function is called when the user wants to edit their post, it takes JASON data and saves the edited post called in posts.js. When the update follow function is called it adds the user clicked on the logged in users following list or removes from following list if the user is already following. The following function redirects to the following page which displays the posts created by the people the logged in user is following. The posts are consolidated by day and user and are shown from newest to oldest. Only 10 posts are displayed per page. When the like_post function is called it updates the like count on the post the logged in user clicked. If the logged in user has already liked the post it then removes the like. The maps function redirects the user to the maps page where the geolocator key is provided as well as all the user information in the user model. 

posts/templates/post/addThanks.html
HTML file that creates a user input form for their gratitude posts. It creates a button to submit the post and a bootstrap badge to display the number of posts made that day. The top of the page displays the last date the user entered a post and has the prompt, “Today I’m thankful for ..”

posts/templates/post/allPosts.html
HTML file that displays the displays all users’ public posts by day in a bootstrap card body. Each post contains a like button and badge that displays the total likes of the post. The top of each post contains the user name which is a link to their profile page, to the left of the user name is their profile picture, below the user name is the date they created their post. The end of the file contain code to handle and display pagination. 

posts/templates/post/editProfile.html
HTML file that displays forms for first_name, last_name, city, state, zip_code, about, and profile pic. It also creates a submit button.

posts/templates/post/following.html
HTML file that displays the displays the people the user is following public posts by day in a bootstrap card body. Each post contains a like button and badge that displays the total likes of the post. The top of each post contains the user name which is a link to their profile page, to the left of the user name is their profile picture, below the user name is the date they created their post. The end of the file contain code to handle and display pagination. 

posts/templates/post/index.html
HTML file that creates a navbar with the following links if the user is logged in: Thanks, Add Thanks, Journal, All Posts, Following, Profile, User Map, and Log Out. If the user is not logged in the following links will be displayed: Thanks, All Posts, Register Log in. If the user is logged text in the middle of the page will display a welcome message with a login and register button and a contact email. If the user is logged in the same welcome message and email will appear, but now there will be an Add Thanks button instead of login and register.

posts/templates/post/journal.html
HTML file that displays the displays the user’s public and private posts by day in a bootstrap card body. Each post contains a like button and badge that displays the total likes of the post. The top of each post contains the user name which is a link to their profile page, to the left of the user name is their profile picture, below the user name is the date they created their post. The end of the file contain code to handle and display pagination. Each post is highlighted gray when the user’s mouse scrolls over it, if the user clicks their post an a from will show up with the post’s text prefilled in. If the user changes their post text and pressed the edit button, the edited version of the post will then show up. 

posts/templates/post/layout.html
HTML file that all html file inherits from except index. It creates a fluid container with a navbar with the following links if the user is logged in: Thanks, Add Thanks, Journal, All Posts, Following, Profile, User Map, and Log Out. If the user is not logged in the following links will be displayed: Thanks, All Posts, Register Log in. It directs to the CSS file style.css. The end of the files loads bootstrap, jquery, and directs to the JavaScript file posts.js.

posts/templates/post/login.html
HTML file that displays username login form and password form. There is a submit button and a link to reset password.

posts/templates/post/maps.html
HTML file that contains script to load mapbox javascript data and a link for mapbox css. There is another javaScript script that creates a map of the world with a zoom of 1 and centered at (-770.3, 38.91). It then creates a marker for every user based on their calculated longitude and latitude. It also creates a popup of the user’s name, city and state if the marker is clicked. 

posts/templates/post/profile.html
HTML file that displays the user’s profile data and profile picture. Profile pic, user name, first name, last name, about section, number of followers, number of people following, post count, and an edit profile button are placed in a bootstrap card format. 

posts/templates/post/register.html
HTML file that allows users to create an account for the site. There is a username, email, password, and confirm password form along with a submit button. There is also a link to log in if the user is already registered. 

posts/templates/registration/password_reset_complete.html
HTML file that is displayed after submitting a password reset request that displays the message to check your email for instructions for setting your new password. 

posts/templates/registration/password_reset_confirm.html
HTML file that contains a form to enter a new password along with a submit button. If the link is not valid it displays a message that the link was invalid, possibly because it has already been used.

posts/templates/registration/reset_password.html
HTML file that displays instructions om how to reset your password. There is a form to enter an email to send the password reset link along with a submit button. There is a link to return to the home page which is index.html.

							Posts/Static Folder
posts/static/posts/posts.js
JavaScript file that contains the following functions: like, unlike, editPost, resetCounter, checkCounter, getCookie, and submitPost. Once DOM content is loaded the resetCounter function is called to check if it has been longer than a day since the user’s last post if it has it returns true. If resetCounter is true then the post count is reset to zero, else the post count is obtained from local storage. An event listener is added to the submit thanks button to call the function checkCounter when clicked. The checkCounter function obtains the current post count and increments it by 1 and updates the counterBadge HTML to reflect new value. The like function gets the current like count for the post and increments it by one. It then obtains a csrftoken from the getCookie function and posts the updated like count as JSON data to the like Django function. Similarly, the unlike function decreased the like count and send the JSON data to the Django like function in views.py. The editPost function is called when the user clicks a post on the journal.html page they want to edit. It stores the value of the edited post. The submit post value is called when the edit button is pressed on the journal.html page. It obtains a csrftoken and posts the new value of the post to the editView function in views.py. The getCookie function creates a csrftoken. 

posts/static/post/styles.css
Empty file for css styling 

								Media Folder
Folder that will contain uploaded user profile pictures. 
