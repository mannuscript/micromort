
from bs4 import BeautifulSoup
import re
import sys
sys.path.append("./utils/")
from logger import logger

# media support: channel news asia provides aggregated share/like over all social media channels
def get_shares_counts(url, html, media):
    soup = BeautifulSoup(html, 'lxml')
    try:
        p = soup.findAll('p', {'class' : ['sharing__text']})
        if len(p) && p[0].text:
            return p[0].text.strip().split(" ")[0]
        else:
            logger.error("Failed to load count for url: " + url)
            return 0
    except Exception as ex:
        logger.error("Failed to load count for url: " + url)
        import traceback
        traceback.print_exc()