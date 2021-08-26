import scrapy
urls={
    "OLL":[
        "https://oll.libertyfund.org/title/trenchard-catos-letters-4-vols-in-2-lf-ed",
    ],
    
}
class oll_spider(scrapy.Spider):
    name="OLL"
    def start_requests(self):
        recs=urls.get("OLL",[])
        for rec in recs:
            yield scrapy.Request(rec,callback=self.parser,
                                 meta={})
    def parser(self):
        pass
