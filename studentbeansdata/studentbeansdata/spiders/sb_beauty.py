import json
import scrapy
from ..items import StudentbeansdataItem

items = StudentbeansdataItem()


class StudentBeans(scrapy.Spider):
    name = "beauty"
    base_urls = "https://582mp15edn-dsn.algolia.net/1/indexes/production_student_discounts_codes_last_week_dsc/query" \
                "?x-algolia-agent=Algolia%20for%20JavaScript%20(4.17.0)%3B%20Browser%20(" \
                "lite)&x-algolia-api-key=3421572be458e587667d4c5b590d89b9&x-algolia-application-id=582MP15EDN "

    data = {
        "query": "",
        "filters": "countryCode: uk AND     enabled: true AND     categoryData.slug: beauty AND          "
                   "contentType: native_student_discount OR contentType: competitor_student_discount AND          "
                   "startDate <= 1684517137 AND     endDate >= 1684517137 AND     consumerGroups: student AND NOT     "
                   "denyListedConsumerUids: e55920fd-5410-4534-b926-b1214c85f64a",
        "hitsPerPage": 10,
        "page": 0,
        "facets": [
            "brandName"
        ]
    }
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Origin': 'https://www.studentbeans.com',
        'Referer': 'https://www.studentbeans.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/113.0.0.0 Safari/537.36',
        'content-type': 'application/x-www-form-urlencoded',
        'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
    }

    def start_requests(self):
        yield scrapy.Request(url=self.base_urls,
                             method='POST',
                             headers=self.headers,
                             body=json.dumps(self.data),
                             callback=self.parse)

    def parse(self, response):
        json_data = json.loads(response.body)
        all_data = json_data.get('hits')
        for r in all_data:
            offer_name = r.get('title')
            brand = r.get('brandName')
            if brand != str(None):
                brand_name = "".join(brand.split(" "))
            # else:
            #     brand_name = ""
            redemption = r.get('redemptionClass')
            if redemption != str(None):
                redemption_type = redemption + " at " + brand_name
            # else:
            #     redemption_type = ""
            platform = "Student Beans"

            items['Offer_Detail'] = offer_name
            items['Brand_Partner'] = brand_name
            items['Redemption_Type'] = redemption_type
            items['Platform'] = platform

            yield items

        current_page = int(json_data.get('page'))
        total_page = int(json_data.get('nbPages'))
        if current_page < total_page:
            data = {
                "query": "",
                "filters": "countryCode: uk AND     enabled: true AND     categoryData.slug: beauty AND          "
                           "contentType: native_student_discount OR contentType: competitor_student_discount AND          "
                           "startDate <= 1684517137 AND     endDate >= 1684517137 AND     consumerGroups: student AND NOT     "
                           "denyListedConsumerUids: e55920fd-5410-4534-b926-b1214c85f64a",
                "hitsPerPage": 10,
                "page": str(current_page+1),
                "facets": [
                    "brandName"
                ]
            }
            yield scrapy.Request(url=self.base_urls,
                                 method='POST',
                                 headers=self.headers,
                                 body=json.dumps(data),
                                 callback=self.parse)


