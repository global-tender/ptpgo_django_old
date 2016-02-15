from django.core.management.base import BaseCommand, CommandError
import pymysql.cursors

import operator

class Command(BaseCommand):

	def handle(self, *args, **options):
		self.import_cars()

	def import_cars(self):
		# Connect to the database
		connection = pymysql.connect(host='localhost',
									 user='import_cars',
									 password='import_cars',
									 db='import_cars',
									 charset='utf8mb4',
									 cursorclass=pymysql.cursors.DictCursor)

		try:
			with connection.cursor() as cursor:
				# Read a single record
				sql = "SELECT * FROM car_characteristic"
				cursor.execute(sql)
				result = cursor.fetchall()

				for res in result:
					print('=====')
					for key, value in res.items():
						print (str(key) + ': ' + str(value))
		finally:
			connection.close()