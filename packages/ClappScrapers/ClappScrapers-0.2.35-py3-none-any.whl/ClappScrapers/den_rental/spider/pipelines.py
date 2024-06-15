# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from datetime import datetime
import time
import json
import re
from scrapy.signalmanager import dispatcher
from scrapy import signals

class MergedDataPipeline:
    def __init__(self):
        self.raw_data = []
        self.cleaned_data = []
    def process_item(self,item,spider):
        adapter = ItemAdapter(item)

        if adapter.get('source'):
            #Process raw data
            self.raw_data.append(adapter.asdict())

            #Process cleaned data
            cleaned_item = self.clean_item(item)
            self.cleaned_data.append(cleaned_item)
        return item
    def close_spider(self,spider):

        #Process data
        spider.log("pipeline Closing spider and sending custom_closed_signal...")
        dispatcher.send(signal=signals.spider_closed, 
                        sender=spider, 
                        cleaned_data = self.cleaned_data, 
                        raw_data = self.raw_data)
    def clean_item (self,item):

        if isinstance(item, dict):
            cleaned_item = {}
            for key, value in item.items():
                cleaned_value = self.clean_value(key, value)
                if cleaned_value is not None:
                    cleaned_item[key] = cleaned_value
            return cleaned_item
        elif isinstance(item,list):
            cleaned_list = []
            for element in item:
                cleaned_element = self.clean_item(element)
                if cleaned_element:
                    cleaned_list.append(cleaned_element)
            return cleaned_list
        else:
            return item
        
    def clean_value(self, key, value):
        
        date_keys = ['timeline_advertisement_creation']


        if isinstance(value,str):

            if key in date_keys:

                return self.convert_to_unix_timestamp(value)
            
            else :
                return value
                
        else:

            return value
    
    def convert_to_unix_timestamp(self,date_str):
        try:
            # Specify the format for "01 February 2024"
            date_formats = ["%d %B %Y", "%d %b %Y", "%d/%m/%Y","%Y-%m-%d"]  # You can add more formats as needed
            for date_format in date_formats:
                try:
                    date_object = datetime.strptime(date_str, date_format)
                    unix_timestamp = int(date_object.timestamp())
                    return unix_timestamp
                except ValueError:
                    pass

            # If the input is not in the specified date formats, try parsing it as datetime string
            dt_formats = ["%Y-%m-%dT%H:%M:%S.%f%z", "%Y-%m-%dT%H:%M:%S%z"]  # Add more formats as needed
            for dt_format in dt_formats:
                try:
                    dt_obj = datetime.strptime(date_str, dt_format)
                    timestamp = round(dt_obj.timestamp())
                    return timestamp
                except ValueError:
                    pass

            return None  # Return None if no valid format is found
        except Exception as e:
            return None

        
    def to_boolean(self, value):
        if value == "Yes":
            return True
        elif value == "No":
            return False
        else:
            return None

    def to_integer(self, value):
        try:
            return int(value.replace(',', '').replace('.', ''))
        except ValueError:
            return None
        
    def to_float(self, value):
        if value is None:
            return
        try:
            return float(value.replace('.','').replace(',','.').replace(' kr', '').replace(' m²', ''))
        except ValueError:
            return None

    def map_floor_to_integer(self, floor):
        floor = floor.strip().lower()
        if floor == "ground floor":
            return 0
        elif floor[:-2].isdigit():
            return int(floor[:-2])
        else:
            return None