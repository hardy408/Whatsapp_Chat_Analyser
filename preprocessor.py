import re
import pandas as pd

def preprocess(data: object) -> object:
    pattern = '\d{1,2}/\d{1,2}/\d{2}, \d{1,2}:\d{2}\s*[AP]M\s*-\s*'

    messages = re.split(pattern, data)[1:]

    dates = re.findall(pattern, data)

    df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    df['message_date'] = pd.to_datetime(df['message_date'], format='%m/%d/%y, %I:%M %p - ')
    df.rename(columns={'message_date': 'date'}, inplace=True)

    # saperate users and messages
    users = []
    messages2 = []
    for messages in df['user_message']:
        entry = re.split('([\w\W]+?):\s', messages)
        if entry[1:]:  # user name
            users.append(entry[1])
            messages2.append(entry[2])
        else:
            users.append('group_notification')
            messages2.append(entry[0])

    df['user'] = users
    df['message'] = messages2
    df.drop(columns=['user_message'], inplace=True)

    df['year'] = df['date'].dt.year
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    return df