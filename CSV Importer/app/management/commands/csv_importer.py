from typing import Any
from django.core.management.base import BaseCommand, CommandParser
from django.core.exceptions import ValidationError
import csv
import json
import logging
from typing import Union
from ...models import User
import re
from django.core.validators import validate_email

logging.basicConfig(
    level=logging.DEBUG, format=f"%(asctime)s - %(levelname)s - %(message)s"
)


class Command(BaseCommand):

    help = "Command for Importing CSV file into Database"

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str, help="Path of CSV file")

    def handle(self, *args, **kwargs):
        file_path = kwargs.get("file_path")

        validation_data = {"Success": 0, "Failed": 0, "Corrupted_data": []}

        try:
            with open(file_path, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Name, Age, Phone No"])
                writer.writerow(["Prakash", 20, "9981567130"])
                writer.writerow(["Nilesh", 19, "998157123"])
                writer.writerow(["Nayan", 21, "9981567i30"])
                writer.writerow(["Aakash 1", -1, "9981567130"])
                writer.writerow(["Vivek", 122, "9981567130"])

            with open(file_path, "r") as file:
                reader = csv.reader(file)

                i = 0
                for row in reader:
                    if i == 0:
                        i += 1
                        continue

                    is_valid_name = (
                        True
                        if len(re.findall("[0-9]", row[0])) == 0
                        and len(re.findall("/s", row[0])) == 0
                        else False
                    )

                    is_valid_age = (
                        True
                        if int(row[1]) > 0
                        and int(row[1]) <= 100
                        and len(re.findall("[a-zA-Z]", row[2])) == 0
                        and len(re.findall("/s", row[2])) == 0
                        else True
                    )

                    is_valid_phone_number = (
                        True
                        if len(re.findall("/s", row[2])) == 0
                        and len(re.findall("[a-zA-Z]", row[2])) == 0
                        else False
                    )

                    if (
                        not is_valid_name
                        or not is_valid_age
                        or not is_valid_phone_number
                    ):
                        validation_data["Corrupted_data"].append(row)
                        validation_data["Failed"] += 1
                        continue

                    validation_data["Success"] += 1
                    # product = User(name=row[0], age=row[1], phone_no=row[3])
                    user = User.objects.create(name=row[0], age=row[1], phone_no=row[2])
                    print(user)

                with open("validation_data.json", "a") as file:
                    json.dump(validation_data, file)

                logging.info("data importer successfully")

        except ValidationError as e:
            logging.error(f"{e}")
        except PermissionError as e:
            logging.error(f"{e}")
        except Exception as e:
            logging.error(f"{e}")
