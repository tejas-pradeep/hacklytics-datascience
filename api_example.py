"""
Georgia Institute of Technology - CS1301
HW07 - APIs and JSON
"""
__author__ = """ Tejas Rajamadam Pradeep """
__collab__ = """ I worked on the project alone with help only from resources provided in the course """

import requests

"""
Function name: currencyConverter
Parameters: country (string), money (int or float), conversionFactor (int or
float)
Returns: string indicating either that the function errored or the monetary
conversion
Description: An important aspect of traveling is money! Write a function that
takes in the name of the country you’re traveling to, the amount of money to
convert, and the conversion factor, and return a string of the format
"In [country name], $[money] USD is worth [foreign currency symbol][money times
currency factor, rounded to 2 decimal places] [three-letter foreign currency
code]." Your code should be able to handle an invalid country name and instead
of erroring, should return "[country name] is not a valid country."
"""


def currencyConverter(con,money,conv):
    result=requests.get('https://restcountries.eu/rest/v2/all')
    data=result.json()
    count=0
    nl=[]
    ##pprint(data[0])
    for i in data:
        for j in i['altSpellings']:
            nl.append(j.lower())

        if i['name'].lower()==con.lower() or con.lower() in nl:
            return 'In {}, ${} USD is worth {}{} {}.'.format(con,money,i['currencies'][0]['symbol'],round(money*conv,2),i['currencies'][0]['code'])
        nl=[]
    return '{} is not a valid country.'.format(con)



"""
Function name: translator
Parameters: codeList (list of strings)
Returns: dictionary where key and value are both strings
Description: Travelling around the world involves learning new languages! Write
a function that takes in a list of 3-letter codes representing a country and
return a dictionary where the key is the name of the country and the value is
the name of the country in its own language. Note that this function must be
able to ignore three letter codes that do not correspond to a country without
erroring. You can assume that we will not test strings that contain numbers.
Hint: The API will output something different if the country code is not valid.
Try using pprint with a request that uses an incorrect three-letter code and see
swhat it outputs!

"""


def translator(codeList):
    result=requests.get('https://restcountries.eu/rest/v2/all')
    data=result.json()
    newdic={}
    for i in data:
        for j in codeList:
            if j.lower()==i['alpha3Code'].lower():
                newdic[i['name']]=i['nativeName']
    return newdic


"""
Function name: nearbyLocations
Parameters: codeList (list of strings)
Returns: a list of tuples, each tuple containing floats
Description: You’ve finally eliminated the list of countries you’d like to visit
down to a few finalists and think that you’d get the most out of your money if
you could go somewhere with many other nearby places to visit. Write a function
that takes in a list of 3-letter codes representing a country, finds which
country has the most bordering countries, and returns a list of tuples
containing the latitude and longitude of its bordering countries. If there are
multiple countries with the same number of borders, use the one whose name
occurs last in the alphabet. If none of the countries have bordering countries,
return an empty list. Assume that all the country codes passed in will be valid.

Hint: You may need to request data more than once.
"""


def nearbyLocations(codeList):
    result=requests.get('https://restcountries.eu/rest/v2/all')
    data=result.json()
    t=()
    temp=[]
    k=0
    large=0
    nl=[]
    for i in data:
        for j in codeList:
            if j.lower()==i['alpha3Code'].lower():
                temp.append(i)
    large=len(temp[0]['borders'])
    for m in range(1,len(temp)):
        if len(temp[m]['borders'])>large:
            large=len(temp[m]['borders'])
            k=m
        elif len(temp[m]['borders'])==large and (temp[m]['name']>temp[k]['name']):
            large=len(temp[m]['borders'])
            k=m
    for i in data:
        if i['alpha3Code']in temp[k]['borders']:
            t=(i['latlng'][0],i['latlng'][1])
            nl.append(t)
    return nl



"""
Function name: humidityCheck
Parameters: locationsList (list of ints), maxHumidity (int)
Returns: list of strings or an error message as a string if an error occurs
Description: You have some suggestions for places to visit on your much-needed
vacation, but you don’t want to go somewhere that has too much humidity. Create
a function that takes in a list of location IDs (ints) and a max humidity (int)
and returns a list of cities (strings) that have humidities less than the max
humidity. If any of the IDs are invalid, return "[Location ID] is not a valid
ID".

Hint: Use the "Current weather data" to answer this question ("weather"
endpoint) and search by IDs

"""


def humidityCheck(alist,maxh):
    newl=[]
    k=0
    try:
        for i in alist:
            k=i
            result=requests.get('https://api.openweathermap.org/data/2.5/weather?id={}&appid=2e9c8561c85c354d690013d412d96e5d'.format(i))
            data=result.json()
            if data['main']['humidity']<maxh:
                newl.append(data['name'])

        return newl
    except:
        return "{} is not a valid ID".format(k)


"""
Function name: locationTemps
Parameters: coordinatesList (list of tuples of floats)
Returns: list of tuples with the first item a string and the second item a float
Description: You are given some possible locations to visit, but you want to
know the temperatures of the locations so that you can plan accordingly. Create
a function that takes in a list of tuples that contain a latitude (float) and
longitude (float) and returns a list of tuples whose first item is the name of
the location (string) and the second item is the current temperature of that
location (float). The returned list should be sorted by temperatures from low to
high. Assume all coordinates are valid latitudes and longitudes.

Hint: Use the "Current weather data" to answer this question ("weather"
endpoint) and search by latitude and longitude. You can also use the
nearbyLocations() function to create your parameters to test!

"""


def locationTemps(colist):
    t=()
    newl=[]
    for i in colist:
        result=requests.get('https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid=2e9c8561c85c354d690013d412d96e5d'.format(i[0],i[1]))
        data=result.json()
        newl.append((data['name'],data['main']['temp']))
    newl.sort(key=lambda t:t[1])
    return newl


"""
Function name: typesOfWeather
Parameters: locationsList (list of ints)
Returns: dictionary with strings as keys and lists of strings as values or an
error message as a string if error occurs
Description: You want to know the types of weather of different locations so
that you can plan an amazing trip! Create a function that takes in a list of
location IDs (ints) and returns a dictionary that’s keys are types of weather
(string) and values are lists of the names of the locations (string) that have
that weather. If any of the IDs are invalid, return "[Location ID] is not a
valid ID".

Hint: Use the "Current weather data" to answer this question ("weather"
endpoint) and search by IDs

"""


def typesOfWeather(l):
    dicc={}
    k=0
    try:
        for i in l:
            result=requests.get('https://api.openweathermap.org/data/2.5/weather?id={}&appid=2e9c8561c85c354d690013d412d96e5d'.format(i))
            data=result.json()
            try:
                dicc[data['weather'][0]['main']]+=[data['name']]
            except:
                dicc[data['weather'][0]['main']]=[data['name']]
            k=i
        return dicc
    except:
        return '{} is not a valid ID'.format(i)
