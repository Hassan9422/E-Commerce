import time
import requests
import csv
import login_reqs
import os
import sys
from pathlib import Path

# By default, Python looks for files in the same directory (including subdirectories) as the current script file,
# as well as in other standard locations defined in sys.path. FYI: sys.path is a set of specific directories in your system.
# if the file we want to import is somewhere else entirely, we'll first have to tell Python where to look by adding
# search directories to sys.path. Note that the path appended to sys.path is an absolute path.
# in below, we have explained more on how we can add this absolute path to sys.path. we have to use a method
# called append like below:
# sys.path.append("the absolute path of the directory you wanna add to sys.pth")
# and to get the absolute path of a directory/file, you can use many ways. but here we're gonna explain two methods:

# 1) we can make use of os.path.abspath("filename or directory_name")
# this method gives you a string which is the absuloute path of your file or directory.
# remember if you weann grab the absoloute path of your current working file, you can simply say:
# os.path.abspath(__file__)
# __file__ means your current working file.

# 2) you can use Path().resolve() from pathlib library. this returns you a complete path object instead of just a string.
# we use as_posix method to convert this object to a string. another benefit of this method is that you can convert
# backslashes to forward slashes using resolve() method. for example:
# Path(__file__).resolve().as_posix()
# this is gonna give you the absolute path of your current file and it will also convert \ to / in your path.

# in this method if you wanna go up one level, you can use .. after file like example below:
# Path(f"{__file__}/../..").resolve().as_posix()
# don't forget to use .. twice, if you wanna go up one level. because if you do it once it's gonna give you the directory of current folder.
# lets say our current working file is called "z.txt" and the absolute path is like a/b/c/d/z.txt.  when you use .. once
# you path is gonna become like: a/b/c/d.
# it's going to only exit from the current file to your current directory, not upper directory.

# also remember that os.getcwd() is very different than os.path.abspath().os.getcwd() looks at your directory that you are in command line.
# it doesn't have to do with the directory that your python file is located in.
sys.path.append(Path(f"{__file__}/../..").resolve().as_posix())

from config import setting

# # The HTTP request returns a Response Object with all the response data (content, encoding, status, etc).
while True:
    try:
        # env = input("Please specify the environment you would like to use:(D: Development/ P: Production")
        env = 'd'  # line above is asking the type of environment. but we have set it to development temporarily.
        if env.lower() == 'd':
            hostname = 'http://127.0.0.1:8000/'  # your local system hostname.
            break
        elif env.lower() == 'p':
            hostname = 'http://127.0.0.1:8000/'  # this is temporary. you should enter the hostname of your production environment here.
            break
        else:
            raise ValueError
    except ValueError:
        print("Please enter 'D' for Development and 'P' for Production.")

try:

    # with open('token.csv') as file1:
    #     reader = csv.DictReader(file1)
    #     for row in reader:
    #         t1, jwt_token = row['time'], row['token']
    #
    # if t1 == 0:
    #     t1, jwt_token = time.time(), login_reqs.jwt_token
    #
    #     with open('token.csv', 'w') as file1:
    #         writer = csv.DictWriter(file1, fieldnames=['time', 'token'])
    #         writer.writeheader()
    #         writer.writerow({'time': t1, 'jwt_token': jwt_token})
    # else:
    #     if time.time() - t1 > setting.access_token_expire_minutes:
    #         t1, jwt_token = time.time(), login_reqs.jwt_token
    #
    #         with open('token.csv', 'w') as file1:
    #             writer = csv.DictWriter(file1, fieldnames=['time', 'token'])
    #             writer.writeheader()
    #             writer.writerow({'time': t1, 'jwt_token': jwt_token})

    access_token = login_reqs.jwt_token['token']

    # create_one_product
    # product = {'name': 'rice', 'category': 'food', 'original_price': '109', 'discount': '0.3'}
    # print(requests.post(f'{hostname}products', json=product,
    #                     headers={'Authorization': f"Bearer {access_token}"}).json())
    # print(requests.post(f'{hostname}products', json=product).json())

    # get_all_products
    # remember that query parameters come after ? mark in the URL like below. also we can use as many queriesas we want, we have to just put
    # "&" to separate them. also if we wanna type space, we have to type "%20" in the URL, like below:
    # for x in requests.get(f'{hostname}products?search=new%20title&limit=3&skip=0', headers={'Authorization': f"Bearer {access_token}"}).json():
    for x in requests.get(f'{hostname}products', headers={'Authorization': f"Bearer {access_token}"}).json():
        print(x)
    # for x in requests.get(f'{hostname}products').json():
    #     print(x)

    # get_one_product
    # print(requests.get(f'{hostname}products/2?search=new%20title&limit=5&skip=3', headers={'Authorization': f"Bearer {access_token}"}).json())
    # print(requests.get(f'{hostname}products/1').json())

    # update_one_product
    # product = {'name': 'cake', 'category': 'food', 'original_price': '1', 'discount': '0.3'}
    # print(requests.put(f'{hostname}products/14', json=product,
    #                    headers={'Authorization': f"Bearer {access_token}"}).json())

    # delete_one_product
    # print(requests.delete(f'{hostname}products/12', headers={'Authorization': f"Bearer {access_token}"}).status_code)

    # Voting on a product
    # vote = requests.post(f'{hostname}votes', json={'product_id': 13, 'dir': 1}, headers={'Authorization': f"Bearer {access_token}"})
    # print(vote.json())
    # print(f"status_code= {vote.status_code}")

except:
    print("Please Login First!")
