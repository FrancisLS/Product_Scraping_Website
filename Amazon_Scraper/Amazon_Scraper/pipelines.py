# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import math

class AmazonScraperPipeline:
    def process_item(self, item, spider):
        for k, v in item.items():
            if not v:
                item[k] = ''  # replace empty list or None with empty string
                continue
            if k == 'Title':
                item[k] = v.strip()
            elif k == 'Rating':
                item[k] = v.replace(' out of 5 stars', '')
            elif k == 'NumberOfReviews':
                item[k] = v.split()[0]
                item[k] = item[k].replace(",", "")
            elif k == 'Price':
                v = v.replace("$", "")    # have to remove because of Bootstrap Table reorder feature
                item[k] = str(math.ceil(float(v)))  # round up price to remove decimals for BST reorder feature
            elif k == 'AvailableSizes' or k == 'AvailableColors':
                item[k] = ", ".join(v)
            elif k == 'BulletPoints':
                item[k] = ", ".join([i.strip() for i in v if i.strip()])
        return item
