import requests
import urllib

def getFBData(url):
    #url = urllib.quote(url)
    r = requests.get(url)
    return r


counter = 0;
while(True):
    res = getFBData("https://www.linkedin.com/countserv/count/share?format=json&url=https://www.dynamicyield.com/mobile-web/")
    #"https://stackoverflow.com/questions/5607551/how-to-urlencode-a-querystring-in-python"
    print counter, "res: ", res.text
    if(200 != res.status_code):
        break
    counter = counter + 1;
print counter