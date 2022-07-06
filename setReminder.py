import mysql.connector

myDatabase = mysql.connector.connect(host="localhost", user="admin", password="admin", database="voice_assistant")
myCursor = myDatabase.cursor()


def setReminderAt(set_title, set_time):
    try:
        query = f"Insert into reminder(reminder_name, reminder_time, reminder_state) values('{set_title}', '{set_time}', 'Active')"
        # query = f"Drop table reminder"
        myCursor.execute(query)
        myDatabase.commit()
        print("Reminder Set Successful")

    except Exception as e:
        print(e)


def setReminderOn(set_title, set_day, set_time):
    try:
        query = f"Insert into reminder(reminder_name, reminder_day, reminder_time, reminder_state) values('{set_title}', '{set_day}', '{set_time}', 'Active')"
        myCursor.execute(query)
        myDatabase.commit()
        print("Reminder Set Successful")

    except Exception as e:
        print(e)


# setReminderAt("This is First Function", "13:00", )
# setReminderOn("this use of function", "10 Oct", "12:55")


if __name__ == '__main__':
    # setReminderAt("Hello world", "12:44")
    setReminderOn("Hello world", 'Monday', "12:44")
    # getQuery = "set a reminder write application on Monday at 7:30"
    # getQuery = "Set reminder at 10:30"
    # getQuery = input(">>>")


    # start = getQuery.find(' on ')
    # end = getQuery.find(' at ')
    #
    #
    # getDay = getQuery[start+4:end]
    # getTime = getQuery[end+4:]
    #
    # print(getDay)
    # print(getTime)
    #
    #
    # if 'on' in getQuery and 'at' in getQuery:
    #     print("Set Reminder on Method Called")
    # else:
    #     print("Set Reminder at Method Called")
    #
    #     # print(word)
