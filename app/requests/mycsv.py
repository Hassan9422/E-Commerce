import csv

with open("C:/Users/Hassa/PycharmProjects/E-Commerce/app/requests/token.csv", "w", newline='') as file:
    writer = csv.DictWriter(file, fieldnames=['time', 'token'])
    writer.writeheader()
    writer.writerow({'time': int('0'), 'token': ''})

import os
print(os.getcwd())