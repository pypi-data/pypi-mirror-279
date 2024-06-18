# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json
from datetime import datetime
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

        float_keys = ['latitude','longitude']
        
        area_keys = ['property_living_area_sqm']

        date_keys = ['timeline_advertisement_creation']

        int_keys = ['property_construction_year','property_rooms_amount','property_floor_number',]

        special_str_keys = ['property_housing_type','address_full','source','address_postal_code',
                            'property_listing_type','address_country','property_sauna','property_heating',
                            'property_energy_label',
                            'property_additonal_terms','property_renovation_info','property_bathroom_features',
                            'property_kitchen_features','property_condition','property_configuration','property_description',
                            'property_rent_price_currency','property_sale_price_currency']

        if isinstance(value, int) or isinstance(value, float):

            if key in int_keys:

                try:

                    numeric_value = int(value)
                    
                    return numeric_value
                
                except:

                    return 0

            if key in area_keys:

                try:

                    cleaned_value = float(value)

                    return cleaned_value
                
                except:

                    pass
            else:
                return value

        if isinstance(value,str):

            if key in float_keys:

                try:

                    numeric_value = float(value)

                    return numeric_value
                
                except:

                    pass
        
            if key in int_keys:

                try:

                    numeric_value = int(value)

                    return numeric_value
                
                except:

                    pass
            
            elif key in date_keys:

                return self.convert_to_timestamp(value)
            
            elif key in special_str_keys:

                return value
            
        else:
            return value 
            
    def convert_to_timestamp(self,date_string):
        # Define the format of your date string
        date_format = '%Y-%m-%d %H:%M:%S'

        # Convert the date string to a datetime object
        date_object = datetime.strptime(date_string, date_format)

        # Convert the datetime object to a Unix timestamp
        timestamp = date_object.timestamp()

        return int(timestamp)
    
# class RawDataPipeline:

#     def __init__(self):
#         self.raw_data = []

#     def process_item(self, item, spider):
#         # Basic data validation: Check if the scraped item is not empty
#         adapter = ItemAdapter(item)
#         if adapter.get('source'):
#             self.raw_data.append(adapter.asdict())
#         return item

#     def close_spider(self, spider):
#         with open('asunnot_raw_data.json', 'w',encoding='utf-8') as file:
#             json.dump(self.raw_data, file, indent=2, ensure_ascii=False)

# class CleanedDataPipeline:

#     def __init__(self):

#         self.cleaned_data = []

#     def process_item(self, item, spider):

#         cleaned_item = self.clean_item(item)
#         self.cleaned_data.append(cleaned_item)
#         return item
    
#     def close_spider(self, spider):

#         with open('asunnot_cleaned_data.json', 'w' , encoding = 'utf-8') as file:
#             json.dump(self.cleaned_data, file, indent=2, ensure_ascii=False)
    
#     def clean_item (self,item):

#         if isinstance(item, dict):
#             cleaned_item = {}
#             for key, value in item.items():
#                 cleaned_value = self.clean_value(key, value)
#                 if cleaned_value is not None:
#                     cleaned_item[key] = cleaned_value
#             return cleaned_item
#         elif isinstance(item,list):
#             cleaned_list = []
#             for element in item:
#                 cleaned_element = self.clean_item(element)
#                 if cleaned_element:
#                     cleaned_list.append(cleaned_element)
#             return cleaned_list
#         else:
#             return item
    
#     def clean_value(self, key, value):

#         price_keys = ['price']

#         float_keys = ['latitude','longitude']
        
#         area_keys = ['size']

#         date_keys = ['creation_date']

#         int_keys = ['cardid','construction_hear','number_of_rooms']

#         special_str_keys = ['property_type','address','location_path','source','zipcode','or_rent','type_of_construction','address_country']

#         if isinstance(value, int) or isinstance(value, float):

#             if key in price_keys:
                
#                 try:

#                     numeric_value = float(value)

#                     cleaned_value ={
#                         f"{key}_value": numeric_value,
#                         f"{key}_currency": 'EUR',
#                     }

#                     return cleaned_value
                
#                 except:

#                     pass

#             if key in int_keys:

#                 try:

#                     numeric_value = int(value)
                    
#                     return numeric_value
                
#                 except:

#                     return 0

#             if key in area_keys:

#                 try:

#                     numeric_value = float(value)

#                     cleaned_value = {
#                         f"{key}_value": numeric_value,
#                         f"{key}_unit": 'square meter',
#                     }

#                     return cleaned_value
                
#                 except:

#                     pass

#         if isinstance(value,str):

#             if key in float_keys:

#                 try:

#                     numeric_value = float(value)

#                     return numeric_value
                
#                 except:

#                     pass
        
            
#             elif key in date_keys:

#                 return self.convert_to_timestamp(value)
            
#             elif key in special_str_keys:

#                 return value
            
#         else:
#             return value 
            
#     def convert_to_timestamp(self,date_string):
#         # Define the format of your date string
#         date_format = '%Y-%m-%d %H:%M:%S'

#         # Convert the date string to a datetime object
#         date_object = datetime.strptime(date_string, date_format)

#         # Convert the datetime object to a Unix timestamp
#         timestamp = date_object.timestamp()

#         return int(timestamp)