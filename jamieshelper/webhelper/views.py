from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from BeautifulSoup import BeautifulSoup
import urllib2, urllib
import json
import xml.etree.ElementTree as ET
# Create your views here.

@csrf_exempt
def home(request):
    if request.method == "POST":
        city = request.POST['City']
        state = request.POST['State']
        address = request.POST['Street Address']
        zillowurl = getzillowid(address, city, state)
        trulia = gettrulia(address, city, state)
        realtor = getrealtor(address, city, state)
        holder = {'urls_list': [zillowurl, trulia, realtor]}
        return render(request, template_name='home.html', context=holder)

    else:
        return render(request=request, template_name='home.html')


def getzillowid(addres, city, state):

    url = "http://www.zillow.com/webservice/GetSearchResults.htm?zws-id="+settings.ZILLOWKEY+"&address="+addres+"&citystatezip="+city+"%2C"+state
    final = url.replace(" ", "%20")
    data = urllib2.urlopen(final)
    root = ET.fromstring(data.read())

    for zid in root.iter("zpid"):
        url2 = "http://www.zillow.com/webservice/GetUpdatedPropertyDetails.htm?zws-id="+settings.ZILLOWKEY+"&zpid="+zid.text
        data2 = urllib2.urlopen(url2)
        newroot = ET.fromstring(data2.read())
        for url in newroot.iter("homeDetails"):
            return url.text


def gettrulia(addres, city, state):
    url = "https://www.google.com/search?q=site%3Atrulia.com+"+addres+"+"+city+"+"+state
    final = url.replace(" ", "+")
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
    headers = {'User-Agent': user_agent}
    request = urllib2.Request(final, None, headers)
    response = urllib2.urlopen(request)
    data = response.read()
    soup = BeautifulSoup(data)

    for item in soup.findAll('h3', 'r'):
        return item.find('a').get('href')


def getrealtor(addres, city, state):
    url = "https://www.google.com/search?q=site%3Arealtor.com+"+addres+"+"+city+"+"+state
    final = url.replace(" ", "+")
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
    headers = {'User-Agent': user_agent}
    request = urllib2.Request(final, None, headers)
    response = urllib2.urlopen(request)
    data = response.read()
    soup = BeautifulSoup(data)

    for item in soup.findAll('h3', 'r'):
        return item.find('a').get('href')




