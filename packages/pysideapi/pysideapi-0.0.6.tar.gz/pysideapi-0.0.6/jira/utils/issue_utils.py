# Timezone Peru
import datetime
from datetime import datetime

import pytz

tz = pytz.timezone('America/Lima')


def get_dates(changelog, status):
    date1 = date_to_status(status, changelog.get('histories'))
    finish = ""
    if date1 != "":
        finish = datetime.strptime(date1, '%Y-%m-%dT%H:%M:%S.%f%z')
        finish = finish.astimezone(tz)
        finish = finish.strftime("%Y-%m-%d %H:%M:%S")
    return finish


def get_dates_key(Arr, criteria_col, criteria, lastdate=''):
    date1 = []
    for element in Arr:
        if criteria in element[criteria_col]:
            finish = datetime.strptime(element.get('created'), '%Y-%m-%dT%H:%M:%S.%f%z')
            finish = finish.astimezone(tz)
            finish = finish.strftime("%Y-%m-%d %H:%M:%S")
            if lastdate != '':
                if finish > lastdate:
                    date1.append(finish)
            else:
                date1.append(finish)

    return date1.pop(0)


def convert_date_local(strdate, input_format='%Y-%m-%dT%H:%M:%S.%f%z', out_format="%Y-%m-%d %H:%M:%S"):
    finish = ""
    if strdate != "":
        finish = datetime.strptime(strdate, input_format)
        finish = finish.astimezone(tz)
        finish = finish.strftime(out_format)
    return finish


def get_date_servicedesk_by_key(arr, criteria, lastdate=''):
    date1 = []
    for element in arr:
        subject_change = element.get("items")[0].get("toString")
        if subject_change is None:
            # print("ingreso nontype")
            subject_change = ''
        if criteria in subject_change:
            finish = datetime.strptime(element.get('created'), '%Y-%m-%dT%H:%M:%S.%f%z')
            finish = finish.astimezone(tz)
            finish = finish.strftime("%Y-%m-%d %H:%M:%S")
            if lastdate != '':
                if finish > lastdate:
                    date1.append(finish)
            else:
                date1.append(finish)
    nuevoDate = ""
    if date1 == []:
        nuevoDate = ""
    else:
        nuevoDate = date1.pop(0)
    return nuevoDate


def get_last_dates_key(Arr, criteria_col, criteria, lastdate):
    comment = [element for element in Arr if criteria in element[criteria_col]]
    date1 = comment[0]['created'] if comment else ''
    finish = ""
    if (date1 != ""):
        finish = datetime.strptime(date1, '%Y-%m-%dT%H:%M:%S.%f%z')
        finish = finish.astimezone(tz)
        finish = finish.strftime("%Y-%m-%d %H:%M:%S")
    return finish


def date_to_status(status, stories):
    date1 = []
    for story in stories:
        items = story.get('items')
        for item in items:
            if item.get('field') == 'status' and item.get('toString') == status:
                date1.append(story.get('created'))

    nuevoDate = ""
    if (date1 == []):
        nuevoDate = ""
    else:
        # if (status == "In Progress"):
        nuevoDate = date1.pop(0)  # [1,2,3,4,5] - POP -> 5 | SHIFT -> 1 | POP(0) -> 1
        # else: nuevoDate = date1.pop();
    return nuevoDate;


def find_etiquetas(changelog, etiqueta):
    valor = string_to_etiqueta(changelog.get('histories'), etiqueta);
    valor2 = ""
    if (valor):
        valor2 = valor.get('toString')

    if etiqueta == "status" and valor2 == "":
        valor2 = "New"

    return valor2


def string_to_etiqueta(stories, eti):
    etiqueta = ""
    for story in stories:
        items = story.get('items')
        for item in items:
            if item.get('field') == eti:
                etiqueta = item

    return etiqueta


def diff_dates_in_milliseconds(date1, date2):
    milliseconds1 = (date1.timestamp() * 1000) + (date1.microsecond / 1000)
    milliseconds2 = (date2.timestamp() * 1000) + (date2.microsecond / 1000)
    diff = (milliseconds1 - milliseconds2) / ((24 * 3600 * 1000))
    return diff


def format_number_to_string(number, decimals):
    number = round(number, decimals)
    return str(number).replace('.', ',')


def get_number_days_for_status(currentStatus, date1, date2, status):
    totalDays = 0
    if currentStatus == status:
        totalDays = diff_dates_in_milliseconds(date1, date2)
    return totalDays
