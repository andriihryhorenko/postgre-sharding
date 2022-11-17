import psycopg2
import uuid
import random
import time
import sys



def str_time_prop(start, end, time_format, prop):
    stime = time.mktime(time.strptime(start, time_format))
    etime = time.mktime(time.strptime(end, time_format))

    ptime = stime + prop * (etime - stime)

    return time.strftime(time_format, time.localtime(ptime))


def random_date(start, end, prop):
    return str_time_prop(start, end, '%m/%d/%Y %I:%M %p', prop)


print ('Number of arguments:', len(sys.argv), 'arguments.')
print ('Argument List:', str(sys.argv))

if len(sys.argv)>1:
    rownum=int(sys.argv[1])
else:
    rownum=10

start_time = time.time()
#Establishing the connection
conn = psycopg2.connect(
   database="usersdb", user='postgres', password='postgres', host='127.0.0.1', port= '5432'
)
#Setting auto commit false
conn.autocommit = True

#Creating a cursor object using the cursor() method
cursor = conn.cursor()

for x in range(rownum):
    cursor.execute("SELECT Max(\"Id\") FROM public.Users")
    record = cursor.fetchall()
    max = int(int(record[0][0]))
    randomdate= random_date("1/1/1990 1:30 PM", "1/1/2022 4:50 AM", random.random())
    max += 1
    # Preparing SQL queries to INSERT a record into the database.
    cursor.execute(f"INSERT INTO public.\"Users\" (\"Id\", \"UserName\", \"BirthDate\", \"CreateTime\", \"UniqueName\")	VALUES ({max}, 'User-{max}', '{randomdate}', '1/1/2022 4:50 AM', '{str(uuid.uuid4())}')")


# Commit your changes in the database
conn.commit()


# Closing the connection
conn.close()
print("--- %s seconds ---" % (time.time() - start_time))