# A User Tag Tracking System Developed using Python Flask
**Author: Hanze Hu**<br>
**Email: hanzehu1998@gmail.com**

## Functionality
A website to input your labels, in the home page you can add your label, rename your label and delete your label. The system has its own login section, where the session would remember the user and user’s labels. When user store their labels, the labels would update to the database, and when user come back to the website page, the updated added label would be showed on current user the page.

## Running the System
To Run the application, simply run the command `python app.py` in the command line with the required packages installed (outlined below), the flask application will be running on a local host server at [http://192.168.0.153:5000/] and all actions can be completed there.

## Design Decisions
A SQLite database was used to keep track of the user authentication database as well as the tags database due to its portability, since it does not need to be set up, and this makes it much easier to be deployed to other machines (this is ok since this is a very small application).<br>
The user authentication database does not store the password directly due to security purposes, only the SALT used to hash the password (a randomly generated ID) and the hashed password are kept on the database, this is also to increase security of the website.


## Testing
The User database is initialized to have the following users:
|  Username  |  Password  |
| ---------- |:----------:|
| Hanze Hu   |password1   |
| James      |password2   |
| Jayden     |password3   |
| Clara      |password4   |

The Tags database is initialized to have the following tags:
|  Username  |  Tags                               |
| ---------- |:-----------------------------------:|
| Hanze Hu   |music, soccer, cooking, travelling   |
| James      |games                                |
| Jayden     |NFTs                                 |

These data can be updated by going into `init_database.py`, updating the init_data values and then running `python init_database.py`, or by simply running the system.

## References
Previous Projects

## Required packages
- Python Flask
- SQLite 3
- uuid
- hashlib
- secrets
- string