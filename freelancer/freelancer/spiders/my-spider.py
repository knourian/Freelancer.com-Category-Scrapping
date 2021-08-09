import scrapy
import json
import csv


class MySpider(scrapy.Spider):
    name = "freelancer_bot"
    base_url = "https://www.freelancer.com"

    def start_requests(self):
        url = "https://www.freelancer.com/job"
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        Categories = response.css(".PageJob-category")
        output = []
        for category in Categories:
            category_heading = category.css(".PageJob-category-title::text").get().strip()
            category_title = category_heading.split("(")[0]
            category_num = category_heading.split("(")[-1][:-1]
            sub_category = []
            sub_categories = category.css(".PageJob-category ul li")
            for sub in sub_categories:
                sub_category_heading = sub.css("a::text").get().strip().replace("\xa0", "")
                sub_category_title = sub_category_heading.split("(")[0]
                sub_category_num = sub_category_heading.split("(")[-1][:-1]
                sub_category_link = self.base_url + sub.css("a::attr(href)").get()
                sub_category.append(
                    {
                        "title": sub_category_title,
                        "number": sub_category_num,
                        "link": sub_category_link,
                        "category": category_title,
                    }
                )

            output.append(
                {
                    "title": category_title,
                    "number": category_num,
                    "categories": sub_category,
                }
            )
        filename = "freelancer categories {}"
        with open(filename.format(".json"), "w") as my_file:
            my_file.write(json.dumps(output, indent=4))

        headers = ["title", "number", "link", "category"]
        sub_categories_list = [s.values() for cateogry in output for s in cateogry["categories"]]
        with open(filename.format(".csv"), "w", newline="") as my_file:
            wr = csv.writer(my_file)
            wr.writerow(headers)
            for sub_category in sub_categories_list:
                wr.writerow(sub_category)

        self.log(f"Saved file {filename}")
