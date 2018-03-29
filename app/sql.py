from app import app
#sql config
def init_sql():
	app.config['MYSQL_HOST'] = 'localhost'
	app.config['MYSQL_USER'] = 'root'
	app.config['MYSQL_PASSWORD'] = 'Galako99!!'
	app.config['MYSQL_DB'] = 'Epytodo'
	app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

#sql init
