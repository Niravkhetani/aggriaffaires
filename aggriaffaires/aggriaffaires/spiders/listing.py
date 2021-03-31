import scrapy
import re
from fake_headers import Headers
from aggriaffaires.items import AggriaffairesListing



class ListingSpider(scrapy.Spider):
    name = 'listing'

    allowed_domains = ['agriaffaires.us']
    url = 'https://www.agriaffaires.us/'

    header = Headers(
        browser="chrome",  # Generate only Chrome UA
        os="win",  # Generate ony Windows platform
        headers=True  # generate misc headers
    )

    def start_requests(self):
        header1 = self.header.generate()
        yield scrapy.Request(self.url,self.parse,headers=header1)

    def parse(self,response):
        data3 = response.xpath("//ul[@class='unstyled sub--list-1col']/li/a/span/text()").getall()
        category3 = []
        for i in data3:
            category3.append(i.strip())
        cat_name3 = ''
        category3 = [name for name in category3 if name.strip("")]
        for i in category3:
            if i == "Farm Tractor":
                header1 = self.header.generate()
                cat_name3 = i
                data = response.xpath("//ul[@aria-labelledby='menu_1_1']")
                list_cat = data.xpath("li/a/@href").getall()
                for i,j in zip(list_cat,category3):
                    if j == "Farm Tractor":
                        category_temp = {
                        'cat_name': j,
                        }
                        url1 = "https://www.agriaffaires.us" + i
                        yield scrapy.Request(url1, self.CrawlerReuest, headers=header1,meta={'cat':category_temp})


    def CrawlerReuest(self,response):
        header1 = self.header.generate()
        item = AggriaffairesListing()
        text = response.xpath("//div[@class='listing--element  js-classified']")
        cat = response.meta.get('cat')
        for i in text:
            item['title']  = i.xpath("a[@class='link']/div/text()").get('')
            item['category'] = {
                'cat1_name':'Farming',
                'cat1_id': 'Farming',
                'cat2_name':'Tractor',
                'cat2_id':'Tractor',
                'cat_name':cat['cat_name'],
                'cat3_id':cat['cat_name']
            }
            item['item_custom_info'] = {
                "desc":''
            }
            item['thumbnail_url'] = i.xpath("div[@class='listing--element--txt']/div[@class='img']/div/img/@data-src").get('')
            item['item_url'] = "https://www.agriaffaires.us"+i.xpath("a[@class='link']/@href").get('')
            buying_format = i.xpath(".//*[@class='maicons maicons-auction']").get('')
            if buying_format == "":
                item['buying_format'] = "sale"
            else:
                item['buying_format'] = "auction"
            yield item
        category_temp = {
            'cat_name': cat['cat_name']
        }
        next = response.xpath("//li[@class='pagination--nav nav-right']/a/@href").get()
        if next is not None:
            next1 = response.urljoin(next)
            yield scrapy.Request(next1,self.CrawlerReuest,headers=header1,meta={'cat':category_temp})



