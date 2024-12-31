import datetime
import param

def dataStringList(string):
    time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    messages_texts = string.splitlines()
    datas = dict()
    if len(messages_texts) == 2:
        # type, values
        datas = {
            'date': time_now[0:10],
            'type': messages_texts[0],
            'values': messages_texts[1],
            'description': " "
        }
    elif len(messages_texts) == 3:
        if len(messages_texts[0]) == 8 and messages_texts[0].isdigit():
            # dates, type, values
            date_date = messages_texts[0][0:4] + "-" +\
                        messages_texts[0][4:6] + "-" +\
                        messages_texts[0][6:8]
            datas = {
                'date': date_date,
                'type': messages_texts[1],
                'values': messages_texts[2],
                'description': " "
            }
        else:
            # type, values, description
            datas = {
                'date': time_now[0:10],
                'type': messages_texts[0],
                'values': messages_texts[1],
                'description': messages_texts[2]
            }
    elif len(messages_texts) == 4:
        # dates, type, values, description
        date_date = messages_texts[0][0:4] + "-" +\
                    messages_texts[0][4:6] + "-" +\
                    messages_texts[0][6:8]
        datas = {
            'date': date_date,
            'type': messages_texts[1],
            'values': messages_texts[2],
            'description': messages_texts[3]
        }
    datas['time'] = time_now
    if param.EXPENDITURE_INCOME == 0:
        datas['action'] = 'expenditure'
    else:
        datas['action'] = 'income'
    return datas
