import mysql.connector

server = 'mshresearch.marshall.usc.edu'
server_ip = '10.103.7.66'
db = 'yelp_michael_2'
# user = 'username'
# password = 'password'

conn = mysql.connector.connect(user=user, password=password,
                               host=server_ip,
                               database=db)
cursor = conn.cursor()
cursor.execute('USE yelp_michael_2')
cursor.execute('''
    SELECT *
    FROM reviews 
        LEFT JOIN review_images
            ON reviews.review_id = review_images.review_id
    LIMIT 0, 25
''')

data = []

for row in cursor:
    print(row[-2])
