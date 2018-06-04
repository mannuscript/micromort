from pycorenlp import StanfordCoreNLP
import os
import subprocess

class StanfordDeeplymoving:
    def __init__(self, classPath = "./stanford-corenlp-full-2018-02-27/"):
        self.nlp = StanfordCoreNLP('http://gpu:9000')
        
    def get_sentiment_string(self, data):
        res = self.nlp.annotate(data,
                        properties={
                            'annotators': 'sentiment',
                            'outputFormat': 'json'
                        })
        try:
            
            return res["sentences"][0]["sentiment"]
        except Exception as e:
            print e
            return ""

if __name__ == "__main__":
    c = StanfordDeeplymoving("../../../stanford-corenlp-full-2018-02-27/")
    print c.get_sentiment_string("\n\nHow are various commodities doing? Which commodities are performing or trending better currently? How to invest in commodities using stocks or ETF funds?\n\n\n\nIt is now possible for stock market investors to participate in commodities markets (Energy, Materials - metals including gold & silver, Agricultural & Livestock).\n\n\n\nOne can implicitly participate by buying stocks of companies involved in commodity business. Or now, one can explicitly buy exchange traded funds (ETF) that track specific commodities like oil, gold and silver.\n\n\n\nNow, let us see how the major commodities are faring year to date. First, the commodity trackers - Oil [12%] Gasoline [7%] Heating Oil [7%] Agriculture [2%] Natural Gas [1%]\n\n\n\nNext, let us look at year to date performances of ETFs that holds stocks of companies in commodities business - Clean Energy [4%] Clean Energy [4%] Oil Services [3%] Energy [3%] Steel [3%] Solar Energy [2%] Nuclear Energy [2%] Ag-business [1%] Coal [1%] Materials [-3%] Gold Mining [-5%] Oil/Dry Bulk Tankers [-5%] .\n\n\n\nThere are also leveraged commodity ETFs that go up double or thrice the daily percent change in any commodity.\n\n\n\nAlso, inverse commodity ETFs that go up when the commodity that they are tracking goes down.\n\n"[:500])