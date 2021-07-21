
### Prerequisites
	Ubuntu 18.04
	Python3
	pip3




Steps :
	Install Postgresql & Create database user and the database
	Create Python virtual environment
	Install Flask and other required modules
	Create codebase
	Run database migration
	Run the Flask application


Install Postgresql & Create Database
	Run following command in terminal to install postgresql
	sudo apt-get install postgresql postgresql-contrib
	To verify installation, run the command:
	sudo -u postgres psql -c "SELECT version();"
	Create User and DB
	sudo su - postgres -c "createuser postgres"
	sudo su - postgres -c "createdb task"
	Grant privileges
	sudo -u postgres psql
	grant all privileges on database task to postgres;
	alter user postgres with password 'iotmax';
	run following to exit from psql
	\q
	Enable remote access to postgresql, edit
	sudo vi /etc/postgresql/10/main/postgresql.conf
	Change the line "listen_addresses = 'localhost'" to "listen_addresses = '*'"
	Save and exit the file
	Restart postgresql
	sudo /etc/init.d/postgresql restart
	

Make sure the virtual env is activated.

Install above dependencies using following command
	python -m pip install -r requirements.txt
	pip3 install -r requirement.txt



commands will create the schema in database
	pip3 install flask_sqlchemy
	python3 manage.py db init
	python3 manage.py db migrate
	python3 manage.py db upgrade
	
	
Running the App
	Run the following command from the root of project directory
	python3 manage.py runserver 
	Now Open the browser and hit the url - localhost:5000
	Access http://localhost:5000/add/form in browser to see the form to save data
	Access http://localhost:5000/getall to see all the data