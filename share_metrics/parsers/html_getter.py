'''
    selenium sucks while running on command line :(,
    Use this file to get the source to feed it beautiful soup and experiment 
    with dom (to get the likes for instance)
    Steps:
    from html_getter import main
    html = main(url)
    ctrl + c   //This is crucial step, haven't check why but after webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true'])  call command line starts misbehaving until we do ctrl+c
    
'''

from selenium import webdriver
from selenium.common.exceptions import TimeoutException

def main(article_url):
    driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true'])
    driver.set_page_load_timeout(45)
    driver.get(article_url)
    return driver.page_source