import csv
from loguru import logger


def init_csv_logger():
    with open("logs.csv", "a+", newline="") as csvfile:
        fieldnames = ["Time", "Level", "Message"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
