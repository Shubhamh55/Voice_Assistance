from plyer import notification
import datetime
import mysql.connector

import time as t



while True:

    myDatabase = mysql.connector.connect(host="localhost", user="admin", password="Ssd@1551", database="voice_assistant")
    myCursor = myDatabase.cursor()


    now = datetime.datetime.now()

    # Get Day Name as Like 'Sunday'
    today = now.strftime("%A")
    # Get Current Time as Like '12:40'
    currentHour = now.strftime("%I")
    currentMinute = now.strftime("%M")
    currentAMPM = now.strftime("%p")
    currentAMPM = currentAMPM.lower()
    newAMPM = ''
    for i in currentAMPM:
        # print(i + '.', end='')
        newAMPM += i + '.'

    if currentHour[0] == '0':
        currentHour = currentHour[1:]

    currentTime = currentHour + ':' + currentMinute +' '+ newAMPM
    print(currentTime)
    # Get today's date & Month as Like '10 oct'
    dateMonth = now.strftime("%d %b")


    query = "select * from reminder"
    myCursor.execute(query)
    reminderTable = myCursor.fetchall()
    print(reminderTable)

    for getName, getDay, getTime, getState in reminderTable:
        # print(getState, '\t', getName, '\t', getDay, '\t', getTime)
        if getState == 'Active':
            if getDay == today:
                if getTime == currentTime:
                    print(getDate, ':', getName)

                    notification.notify(
                        title="Reminder",
                        message=getName,
                        timeout=10
                    )
                    stateQuery = f"Update reminder Set reminder_state= 'Complete' Where getTime='{currentTime}'"
                    myCursor.execute(stateQuery)
                    myDatabase.commit()
                else:
                    print(getDate, ':', "failed Day")

            elif getDay is None:
                if getTime == currentTime:
                    print(currentHour, getName)
                    notification.notify(
                        title="Reminder",
                        message=getName,
                        timeout=10
                    )

                    stateQuery = f"Update reminder Set reminder_state= 'Complete' Where reminder_time='{currentTime}'"
                    myCursor.execute(stateQuery)
                    myDatabase.commit()

                else:
                    print(currentTime, "Failed time")

    t.sleep(10)
