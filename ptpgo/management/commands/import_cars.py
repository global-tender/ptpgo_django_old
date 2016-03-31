from django.core.management.base import BaseCommand, CommandError
import pymysql.cursors

from ptpgo.models import CarType, CarMark, CarModel, CarGeneration, CarSerie, CarModification, CarCharacteristic, CarCharacteristicValue


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.import_cars()

    def connection(self):
        # change connection details
        conn = pymysql.connect(
            host='localhost',
            user='import_cars',
            password='import_cars',
            db='import_cars',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor)
        return conn

    def import_cars(self):

        # self.import_characteristic()
        # self.import_mark()
        # self.import_model()
        # self.import_generation()
        # self.import_serie()
        # self.import_modification()
        # self.import_characteristic_value()

    def import_characteristic(self):

        CarCharacteristic.objects.all().delete()

        connection = self.connection()
        try:
            with connection.cursor() as cursor:
                sql = """SELECT * FROM car_characteristic"""
                cursor.execute(sql)
                result = cursor.fetchall()

                for res in result:
                    print(res)
                    transac = CarCharacteristic(
                        id_car_characteristic = res['id_car_characteristic'],
                        name = res['name'],
                        parent = res['id_parent'],
                    )
                    transac.save()

        finally:
            connection.close()

        return True


    def import_mark(self):

        CarMark.objects.all().delete()

        car_type = CarType.objects.filter(id=1).first()

        connection = self.connection()
        try:
            with connection.cursor() as cursor:
                sql = """SELECT * FROM car_mark"""
                cursor.execute(sql)
                result = cursor.fetchall()

                for res in result:
                    print(res)
                    transac = CarMark(
                        id_car_mark = res['id_car_mark'],
                        name = res['name'],
                        name_rus = res['name_rus'],
                        id_car_type = car_type,
                    )
                    transac.save()

        finally:
            connection.close()

        return True

    def import_model(self):

        CarModel.objects.all().delete()

        connection = self.connection()
        try:
            with connection.cursor() as cursor:
                sql = """SELECT * FROM car_model"""
                cursor.execute(sql)
                result = cursor.fetchall()

                for res in result:
                    print(res)
                    transac = CarModel(
                        id_car_model = res['id_car_model'],
                        name = res['name'],
                        name_rus = res['name_rus'],
                        id_car_mark = res['id_car_mark'],
                    )
                    transac.save()

        finally:
            connection.close()

        return True


    def import_generation(self):

        CarGeneration.objects.all().delete()

        connection = self.connection()
        try:
            with connection.cursor() as cursor:
                sql = """SELECT * FROM car_generation"""
                cursor.execute(sql)
                result = cursor.fetchall()

                for res in result:
                    print(res)
                    transac = CarGeneration(
                        id_car_generation = res['id_car_generation'],
                        name = res['name'],
                        year_begin = res['year_begin'],
                        year_end = res['year_end'],
                        id_car_model = res['id_car_model'],
                    )
                    transac.save()

        finally:
            connection.close()

        return True

    def import_serie(self):

        CarSerie.objects.all().delete()

        connection = self.connection()
        try:
            with connection.cursor() as cursor:
                sql = """SELECT * FROM car_serie"""
                cursor.execute(sql)
                result = cursor.fetchall()

                for res in result:
                    print(res)
                    transac = CarSerie(
                        id_car_serie = res['id_car_serie'],
                        name = res['name'],
                        id_car_model = res['id_car_model'],
                        id_car_generation = res['id_car_generation'],
                    )
                    transac.save()

        finally:
            connection.close()

        return True

    def import_modification(self):

        CarModification.objects.all().delete()

        connection = self.connection()
        try:
            with connection.cursor() as cursor:
                sql = """SELECT * FROM car_modification"""
                cursor.execute(sql)
                result = cursor.fetchall()

                for res in result:
                    print(res)
                    transac = CarModification(
                        id_car_modification = res['id_car_modification'],
                        name = res['name'],
                        start_production_year = res['start_production_year'],
                        end_production_year = res['end_production_year'],
                        price_min = res['price_min'],
                        price_max = res['price_max'],
                        id_car_model = res['id_car_model'],
                        id_car_serie = res['id_car_serie'],
                    )
                    transac.save()

        finally:
            connection.close()

        return True

    def import_characteristic_value(self):

        CarCharacteristicValue.objects.all().delete()

        connection = self.connection()
        try:
            with connection.cursor() as cursor:
                sql = """SELECT * FROM car_characteristic_value"""
                cursor.execute(sql)
                result = cursor.fetchall()

                for res in result:
                    print(res)
                    transac = CarCharacteristicValue(
                        id_car_characteristic_value = res['id_car_characteristic_value'],
                        value = res['value'],
                        unit = res['unit'],
                        id_car_characteristic = res['id_car_characteristic'],
                        id_car_modification = res['id_car_modification'],
                    )
                    transac.save()

        finally:
            connection.close()

        return True
