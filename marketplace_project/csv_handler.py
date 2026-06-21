import csv

def baca_csv(nama_file):
    with open(nama_file, mode="r", newline="") as file:
        return list(csv.DictReader(file))

def tulis_csv(nama_file, fieldnames, data):
    with open(nama_file, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()

        for row in data:
            writer.writerow(row)