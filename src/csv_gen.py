"""
- Generate a random file name
    - File name should use datetime
    - Have param for specific name
- open file of that name
- Create random number of rows
- Function will have certain datatypes it can do
    - Name
    - Age
    - Education type
    - random floats
    - random ints
- each row should have a pid
"""

import time
import datetime
import random
import re

NAMES = [
    "Gladys Conway",
    "Kristen Sanford",
    "Leyton Lutz",
    "Ehsan Schmitt",
    "Kacy Clarkson",
    "Carmen Kemp",
    "Bill Garza",
    "Dougie Singh",
    "Eiliyah Phelps",
    "Zofia Compton"
]

def create_file(name=None):
    """
    Function that will create a CSV file
    with either a user defined name or a
    random name generated by the function.
    """
    if not name:
        filename = str(int(time.time()))
    else:
        filename = name
    filename+=".csv"
    f = open(filename, "w")
    return f, filename

def gen_rand_number(dt):
    """
    Function which will generate a random
    number based on the datatypes defined in
    the generation functions.
    """
    if re.search("(int)([0-9]*)",dt):
        return random.randrange(int(dt.split("int")[1]))
    elif re.search("(float)([0-9]*)",dt):
        return random.uniform(0,int(dt.split("float")[1]))
    else:
        return "0"


def generate(name=None,
            rows=50,
            headers=["Name","Age", "Education", "GPA"],
            datatypes=["name", "int100", "edu", "float5"],
            categorical={"edu":["PhD", "Masters", "Bachelors", "Secondary", "Primary"]}):
    """
    Function which is used to create random CSV to be used for testing of
    data analysis functionality. The headers for the CSV are defined in
    by the inputs, as are the datatypes, the name of the file to be
    created and the amount of data to be generated. It will then go
    through the datatypes and headers and build each row, before writing
    it to the created CSV file.
    """
    if len(headers) != len(datatypes):
        print("Need a datatype for each header")
        return
    f, filename = create_file(name)
    headers.insert(0,"pid")
    f.write(','.join(headers)+"\n")

    for pid in range(0, rows):
        row = [str(pid)]
        for i in range(0, len(datatypes)):
            if datatypes[i] == "name":
                row.append(random.choice(NAMES))
            elif re.search("(int|float)", datatypes[i]):
                row.append(str(gen_rand_number(datatypes[i])))
            else:
                try:
                    category = categorical[datatypes[i]]
                    row.append(category[(random.randrange(100)%(len(category)+1))-1])
                except:
                    print("No Defined Category")

        f.write(','. join(row)+"\n")
    return filename

def generate_output_data(name=None,
                        rows=50,
                        headers=["Name", "Age", "Education", "GPA"],
                        datatypes=["name", "int100", "edu", "float5"],
                        generalise=["Age", "GPA"],
                        categorical={"edu":["PhD", "Masters", "Bachelors", "Secondary", "Primary"]}):
    """
    Function which is used to create random CSV to be used for testing of
    data analysis functionality. The headers for the CSV are defined in
    by the inputs, as are the datatypes, the name of the file to be
    created and the amount of data to be generated. It will then go
    through the datatypes and headers and build each row, before writing
    it to the created CSV file. This function also allows a user to define
    which headers to generalise, in order to simulate some of the functionality
    of the CASTLE algorithm.
    """
    if len(headers) != len(datatypes):
        print("Need a datatype for each header")
        return
    f, filename = create_file(name)
    temp = []
    temp.append("pid")
    for i in range(0, len(headers)):
        # In this loop, each header should be check if its in generalise
        # If it is, create a min and a max
        if headers[i] in generalise:
            temp.append("min"+headers[i])
            temp.append("spc"+headers[i])
            temp.append("max"+headers[i])
        else:
            temp.append(headers[i])
    f.write(','.join(temp)+"\n")

    for pid in range(0, rows):
        row = [str(pid)]
        for i in range(0, len(headers)):
            if datatypes[i] == "name":
                row.append(random.choice(NAMES))
            elif re.search("(int|float)", datatypes[i]):
                max = gen_rand_number(datatypes[i])
                if headers[i] in generalise:
                    min = random.uniform(0, max)
                    med = random.uniform(min, max)
                    if type(max) is int:
                        min = int(min)
                        med = int(med)
                        while min == max:
                            if max == 0:
                                max = 1
                            min = int(random.uniform(0, max))
                            med = int(random.uniform(med, max))

                    else:
                        while min == max:
                            min = random.uniform(0, max)
                            med = random.uniform(min, max)
                    row.append(str(min))
                    row.append(str(med))
                row.append(str(max))
            else:
                try:
                    category = categorical[datatypes[i]]
                    row.append(category[(random.randrange(100)%(len(category)+1))-1])
                except:
                    print("No Defined Category")
        f.write(','. join(row)+"\n")
    return filename
