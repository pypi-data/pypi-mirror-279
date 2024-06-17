import scrapy
import re
import json

import scrapy.resolver

def normalize_key (text):

    if text is None:
        return ''
    
    if text is not None:
        
        normalized_key = text.replace('(p.m.)','').replace('(s)','').strip()

        # Replace spaces with underscores
        normalized_key = normalized_key.replace(' ', '_').replace('.','').replace('-','_').strip()
    
        # Remove special characters
        normalized_key = ''.join(char for char in normalized_key if char.isalnum() or char in ['_', '-'])

        normalized_key = normalized_key.replace('__',"_")

        # Decapitalize the key
        normalized_key = normalized_key.lower()

        return normalized_key

def clean_number(number):

    if number is None:
        return ""
    
    cleaned_number = number.replace("€","").replace(",","").replace('','').strip()

    return cleaned_number

def clean_text(text):

    if text is None:

        return '-'

    if text is not None:

        cleaned_value = re.sub(r'<(?!br\s?\/?)[^>]*>', '', text)
                
        # Remove leading and trailing whitespaces, including newline characters
        cleaned_value = cleaned_value.strip()

        # Replace consecutive newline characters with a single space
        cleaned_value = re.sub(r'\n+', ' ', cleaned_value)

        # Replace other unwanted characters
        cleaned_value = cleaned_value.replace("\xa0", "").replace("  ","").replace("m<sup>2</sup>","").replace("m<sup>3</sup>","").replace("\r","").replace("\t","").replace("<span>","").replace("</span>","").strip()

        # Use strip() to remove leading and trailing whitespace and newline characters
        return cleaned_value

class BoligsidensellingspiderSpider(scrapy.Spider):
    name = "boligsidensellingspider"
    start_urls = ["https://www.boligsiden.dk/landsdel"]

    def parse(self, response):
        
        regions = response.css('a.flex.flex-row.items-center::attr(href)').getall()

        for region in regions:

            yield response.follow(url = region, callback= self.get_sellings)
    
    def get_sellings(self, response):

        link = response.url + '/tilsalg/villa,ejerlejlighed,raekkehus,villalejlighed,andelsbolig,landejendom'

        yield scrapy.Request(url = link, callback = self.parse_properties )

    def parse_properties(self, response):

        properties = response.css('div.overflow-hidden a.text-center::attr(href)').getall()

        for property in properties:
            
            yield scrapy.Request(url = 'https://www.boligsiden.dk' + property, callback = self.parse_property)

        next_page_url = response.css('a[rel="next"][aria-disabled="false"]::attr(href)').get()

        yield scrapy.Request(url = 'https://www.boligsiden.dk' + next_page_url, callback = self.parse_properties)
    
    def parse_property(self, response) :

        for script_text in response.css("script::text").getall():

            if 'props' in script_text:
                
                property_info = {}
                
                property_data = "".join(script_text)

                property_data = json.loads(property_data)

                property_data = property_data['props']['pageProps']['address']['case']

                property_info['source'] = response.url
                
                try:
                    property_info['property_type'] = property_data['addressType']
                except:
                    pass
                
                try:
                    property_info['timeline_time_on_market'] = property_data['timeOnMarket']
                except:
                    pass

                try:
                    property_info['latitude'] = property_data['coordinates']['lat']
                    property_info['longitude'] = property_data['coordinates']['lon']
                except:
                    pass
                
                try:
                    property_info['property_description'] = property_data['descriptionBody']
                except:
                    pass

                try:
                    property_info['property_energy_label'] = property_data['energyLabel']
                except:
                    pass

                try:
                    property_info['property_living_area_sqm'] = property_data['housingArea']
                except:
                    pass

                try:
                    property_info['property_lot_area_sqm'] = property_data['lotArea']
                except:
                    pass

                try:
                    property_info['property_monthly_expense'] = property_data['monthlyExpense']
                except:
                    pass

                try:
                    property_info['property_floor_number'] = property_data['numberOfFloors']
                except:
                    pass

                try:
                    property_info['property_rooms_amount'] = property_data['numberOfRooms']
                except:
                    pass

                try:
                    property_info['property_toilets_amount'] = property_data['numberOfToilets']
                except:
                    pass

                try:
                    property_info['property_sale_price_per_sqm'] = property_data['perAreaPrice']
                except:
                    pass

                try:
                    property_info['property_sale_price'] = property_data['priceCash']
                except:
                    pass

                property_info['property_sale_price_currency'] = 'DKK'
                
                try:
                    property_info['property_price_change_percentage'] = property_data['priceChangePercentage']
                except:
                    pass

                try:
                    property_info['property_weighted_area_sqm'] = property_data['weightedArea']
                except:
                    pass

                try:
                    property_info['property_construction_year'] = property_data['yearBuilt']
                except:
                    pass

                try:
                    property_info['property_buildings'] = property_data['address']['buildings']
                except:
                    pass

                try:
                    property_info['address_city'] = property_data['address']['cityName']
                except:
                    pass

                try:
                    house_number = property_data['address']['houseNumber']

                    match = re.match(r'(\d+)(.*)', house_number)
                    
                    if match:
                        property_info['address_house_number'] = match.group(1)
                        property_info['address_addition'] = match.group(2).strip() or None
                    else:
                        property_info['address_house_number'] = house_number

                except:
                    pass

                try:
                    property_info['property_latest_valuation'] = property_data['address']['latestValuation']
                except:
                    pass

                try:
                    property_info['address_municipality_info'] = property_data['address']['municipality']
                except:
                    pass

                try:
                    property_info['address_municipality'] = property_data['address']['municipality']['name']

                except:
                    pass

                try:
                    property_info['address_mun_code'] = property_data['address']['municipality']['code']
                
                except:
                    pass

                try:
                    property_info['address_place'] = property_data['address']['placeName']
                except:
                    pass

                try:
                    property_info['address_street'] = property_data['address']['roadName'] 
                except:
                    pass

                try:
                    property_info['address_postal_code'] = str(property_data['address']['zipCode'])
                
                except:
                    pass

                try:
                    property_info['media_set'] = [source['url'] 
                                            for property_item in property_data['images'] 
                                            for source in property_item['imageSources'] 
                                            if source['size']['height'] == 600]

                except:
                    pass
                yield property_info

                break




