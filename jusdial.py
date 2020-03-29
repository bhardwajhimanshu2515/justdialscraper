from bs4 import BeautifulSoup
import urllib
import requests
import urllib.request
import requests
import csv


def innerHTML(element):
    return element.decode_contents(formatter="html")


def get_name(body):
    return body.find('span', {'class': 'jcn'}).a.string


def which_digit(html):
    mappingDict = {'icon-ji': 9,
                   'icon-dc': '+',
                   'icon-fe': '(',
                   'icon-hg': ')',
                   'icon-ba': '-',
                   'icon-lk': 8,
                   'icon-nm': 7,
                   'icon-po': 6,
                   'icon-rq': 5,
                   'icon-ts': 4,
                   'icon-vu': 3,
                   'icon-wx': 2,
                   'icon-yz': 1,
                   'icon-acb': 0,
                   }
    return mappingDict.get(html, '')


def get_phone_number(body):
    i = 0
    phoneNo = "No Number!"
    try:

        for item in body.find('p', {'class': 'contact-info'}):
            i += 1
            if (i==2):
                phoneNo = ''
                try:
                    for element in item.find_all(class_=True):
                        classes = []
                        classes.extend(element["class"])
                        phoneNo += str((which_digit(classes[1])))
                except:
                    pass
    except:
        pass
    body = body['data-href']
    soup = BeautifulSoup(body, 'html.parser')
    for a in soup.find_all('a', {"id": "whatsapptriggeer"}):
        # print (a)
        phoneNo = str(a['href'][-10:])

    return phoneNo
page_number = 1
service_count = 1

fields = ['Name', 'Phone', ]
out_file = open('mobilenumbyhimanshu.csv', 'a')
csvwriter = csv.DictWriter(out_file, delimiter=',', fieldnames=fields)

# Write fields first
# csvwriter.writerow(dict((fn,fn) for fn in fields))
while True:
    # Check if reached end of result
    if page_number > 2:
        break

    url = "https://www.justdial.com/Jaipur/Electricians-in-Muhana-Road-Mansarovar/nct-10184166-%s" % (page_number)
    print(url)
    req = urllib.request.Request(url, headers={'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64)"})
    page = urllib.request.urlopen(req)
    # page=urllib2.urlopen(url)

    soup = BeautifulSoup(page.read(), "html.parser")
    services = soup.find_all('li',{'class':'cntanr'})
    
    # Iterate through the 10 results in the page
    for service_html in services:

        # Parse HTML to fetch data
        dict_service = {}
        name = get_name(service_html)
        print(name);
        phone = get_phone_number(service_html)
        if name != None:
            dict_service['Name'] = name
        if phone != None:
            print('getting phone number')
            dict_service['Phone'] = phone
        # Write row to CSV
        csvwriter.writerow(dict_service)

        print("#" + str(service_count) + " ", dict_service)
        service_count += 1

    page_number += 1

out_file.close()
