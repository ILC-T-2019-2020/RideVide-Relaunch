import requests, datetime, time
from bs4 import BeautifulSoup

'''
    flight_number: string (UA660)
    date: datetime object
'''


def information(flight_number, date, from_chicago):
    '''
    Possible errors:
    FORMAT -- (Error code) error desc.
    O(-1) Check flight flies that day
    O(-2) Check departure and arrival location to have at least Chicago
    X Certain flights don't have time information (especially weirder locations like Guam)
    '''

    ''' Parse information for use '''
    airline = ''
    number = ''
    for c in flight_number:
        if c.isalpha():
            airline += c
        else:
            number += c

    if not number or not airline:
        return -1, None

    page = requests.get('https://www.flightstats.com/v2/flight-tracker/' \
                        + airline + '/' + number + '?year=' + str(date.year) + '&month=' + str(date.month) + \
                        '&date=' + str(date.day))

    soup = BeautifulSoup(page.content, 'html.parser')

    valid_check = soup.find_all(class_='layout-row__Title-s1uoco8s-4 bRoHMJ')
    if list(valid_check)[0].get_text() == 'Flight Status Not Available':
        print('This flight information is not available or invalid flight number')
        return -1, None

    ''' Checking all possible flights on given date for Chicago flights '''
    flight_info = soup.find(class_='tabs-content__Panel-rymvp0-5 eGqjWl')
    if not flight_info:
        return scrape(page, flight_number, date)
    locations = flight_info.find_all(class_='past-upcoming-flights__TextHelper-s1haoxfm-2 ieHvs')
    links = flight_info.find_all(class_='past-upcoming-flights__LinkTableRow-s1haoxfm-0 hiZfCr')

    chicago_index = -1
    for i, loc in enumerate(list(locations)):
        if loc.text == 'Chicago':
            if i % 2 == 0 and from_chicago:
                chicago_index = i
                break
            if i % 2 == 1 and not from_chicago:
                chicago_index = i
                break


    if chicago_index >= 0:
        link = list(links)[chicago_index // 2]['href']
        return scrape(requests.get('https://www.flightstats.com' + link), flight_number, date)

    return -2, None


def scrape(page, flight_number, date):
    ''' Check flight information is available '''
    soup = BeautifulSoup(page.content, 'html.parser')

    ''' Going to or from Chicago? '''
    loc_info = soup.find_all(class_="text-helper__TextHelper-s8bko4a-0 eFnGmW")
    from_chicago = "Chicago" == list(loc_info)[0].get_text()
    to_chicago = "Chicago" == list(loc_info)[1].get_text()

    if not from_chicago and not to_chicago:
        return -2, None

    ''' Which airport in Chicago? '''
    airport_info = soup.find_all(class_="route-with-plane__AirportLink-s154xj1h-3 dBXRil")
    if from_chicago:
        airport = list(airport_info)[0].get_text()
    else:
        airport = list(airport_info)[1].get_text()

    ''' Retrieve time information '''
    time_info = soup.find_all(class_='text-helper__TextHelper-s8bko4a-0 cCfBRT')
    sched_dpt = list(time_info)[0].get_text()
    expec_dpt = list(time_info)[1].get_text()
    sched_arr = list(time_info)[2].get_text()
    expec_arr = list(time_info)[3].get_text()

    to_return = {
        "flight_number": flight_number,
        "from_chicago": from_chicago,
        "airport": airport,
        "date": date,
        "time": (expec_dpt if len(expec_dpt) == 9 else sched_dpt) \
            if from_chicago else (expec_arr if len(expec_arr) == 9 else sched_arr)
    }
    return to_return
