## Setup instructions

### Files required

- playyn.zip

### Software required

- Python Version `3.6.12`
- MySQL
- MySQL Workbench

### Libraries required

- PyMySQL
- Flask
- Flask-Cors
- Jinja2

### Installation directory

No specific requirements

### Specifications

The following are expected to be working in order:
1. Install `Python3.6.12`, `MySQL` and `MySQL Workbench`
2. Clone the project **OR** download and extract the provided `playyn.zip`
3. Navigate to the project folder
4. Open a command prompt
	a. Now run the following commands:
	```
	pip install pymysql flaskpip flask_cors jinja2
	```
	b. If no errors are shown, proceed to next step
5. Open MySQL Workbench
6. Create new MySQL Connection if no exists
7. Here we have two options:
	a. Import dump file `playyn_dump.sql`
	b. If by any chance that does not work, we can open all .sql files in `/sql` folder and run in the following order:
		i. projectchakrabortyd.create_table.sql
		ii. projectchakrabortyd.procedure.sql
		iii. projectchakrabortyd.function.sql
		iv. projectchakrabortyd.populate_table.sql
8. Open the `.config` file in project folder
9. Enter the necessary database credentials (database: `playyn`)
10. Open the command prompt again in the base project folder that contains the file `app.py`
	a. Now run the following command:
	```
	flask run
	```
	b. Copy the URL showing after ‘Running on’
11. Open a browser (Preferably Chrome)
	a. Paste the URL in the address bar
12. The setup should be complete at this point.

## Technical Specifications

Host language: Python
MySQL connector: PyMySQL
Backend Framework: Flask
Other front-end technologies used: HTML, CSS, JavaScript, JQuery

## UPDATE: UML Diagram

![UML](/img/uml.png?raw=true)

## Logical Design

![Logical Design](/img/logical-design.png?raw=true)

## Final User Flow

### Create new artist

![Create new artist](/img/create-new-artist.png?raw=true)

### Create new customer

![Create new customer](/img/create-new-customer.png?raw=true)

### Login as artist

![Login as artist](/img/login-as-artist.png?raw=true)

### Login as customer

![Login as customer](/img/login-as-customer.png?raw=true)

### Edit artist

![Edit artist](/img/edit-artist.png?raw=true)

### Edit customer

![Edit customer](/img/edit-customer.png?raw=true)

### Delete artist profile

![Delete artist profile](/img/delete-artist.png?raw=true)

### Delete customer profile

![Delete customer profile](/img/delete-customer.png?raw=true)

### Create band

![Create band](/img/create-band.png?raw=true)

## Future Work

This section is a compilation of the future work planned for this project:

### Planned use of database

This database can be used as an extensive resource for storing various artist information, their associated album and track information along with track metadata such as its upload date, duration, acousticness, danceability, energy, instrumentalness, keynotes, liveness, loudness, scales, speechiness, tempo and valence. These can help analyze individual tracks and in the future assist customers in making a informed choice from their recommended play lists.

### Potential areas for added functionality

The potential areas for added functionality can be identified as:
- Including session-based time-limited logins
- Preserving passwords in a secured hashed manner
- Better way to transform data in front-end
- UI improvements