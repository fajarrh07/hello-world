import pymysql
def lihat_profil():
	# Open database connection
	db = pymysql.connect("localhost","testuser","test123","testdb" )

	# prepare a cursor object using cursor() method
	cursor = db.cursor()

	sql = "SELECT * FROM employee"

#	try:
		# Execute the SQL command
	cursor.execute(sql)
		# Fetch all the rows in a list of lists.
	results = cursor.fetchall()
	for row in results:
		fname = row[0]
		lname = row[1]
		age = row[2]
		sex = row[3]
		income = row[4]
			# Now print fetched result
		print ("nama depan = %s \nlname = %s \nage = %s \nsex = %s \nincome = %s\n\n" % (fname, lname, age, sex, income ))
#	except:
#		print ("--Error: unable to fetch data--")


	# disconnect from server
	db.close()