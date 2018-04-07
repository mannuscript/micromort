from micromort.pipeline import Pipeline
from micromort.utils.logger import logger
from micromort.share_metrics.shares_getter import SharesGetter

if __name__ == "__main__":
    logger.info("------------- Get number of shares/likes -----------")
    ob = Pipeline()
    day = 10
    share_getter = SharesGetter()
    while(True):
        try:
            for i in range(1, day+1):
                share_getter.main(ob.getUrlsToCrawl(i))
        except Exception as ex:
            logger.error(ex)
            continue