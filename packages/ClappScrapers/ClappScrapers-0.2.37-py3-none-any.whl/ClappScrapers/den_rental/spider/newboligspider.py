import scrapy
import json
from scrapy.exceptions import CloseSpider
import re
import time
from datetime import datetime, timedelta, timezone

def clean_text(text):

    if text is None:

        return '-'

    if text is not None:
                
        # Remove leading and trailing whitespaces, including newline characters
        cleaned_value = text.strip()

        # Replace consecutive newline characters with a single space
        cleaned_value = re.sub(r'\n+', ' ', cleaned_value)

        # Replace other unwanted characters
        cleaned_value = cleaned_value.replace("\u2022", "").replace("\u2013", "").replace("\u2028", "").replace("\u0000", "").replace("\u00A0", "").strip()

        # Use strip() to remove leading and trailing whitespace and newline characters
        return cleaned_value

def normalize_key (text):

    if text is None:
        return ''
    
    if text is not None:
        

        normalized_key = text.replace('(p.m.)','').replace('(s)','').replace('_m2','').strip()

        # Replace spaces with underscores
        normalized_key = normalized_key.replace(' ', '_').replace('.','').strip()
    
        # Remove special characters
        normalized_key = ''.join(char for char in normalized_key if char.isalnum() or char in ['_', '-'])

        # Decapitalize the key
        normalized_key = normalized_key.lower()

        return normalized_key
    
class NewboligspiderSpider(scrapy.Spider):

    name = "newboligspider"

    start_urls = ["https://www.boligportal.dk/en/rental-properties/?offset=0"]

    base_url = "https://www.boligportal.dk/en/rental-properties/?offset={}"

    # Define the date threshold (two days ago)
    date_threshold = datetime.now(tz=timezone.utc) - timedelta(days=1)

    def parse(self, response):

        # Extract the current page number from the URL
        current_page = int(response.url.split("offset=")[1])

        # Calculate the next page number with an increment of 18
        next_page_number = current_page + 18

        # Construct the next page URL
        next_page_url = self.base_url.format(next_page_number)
        
        properties_data = "".join(response.css("script::text")[-2].get())

        properties_data = json.loads(properties_data)

        properties = properties_data["props"]["page_props"]["results"]

        if not properties:

            return

        for property in properties:

            property_link = 'https://www.boligportal.dk' + property['url']

            yield scrapy.Request(url = property_link, callback = self.parse_property_page)

        yield scrapy.Request(next_page_url, callback=self.parse)
    
    def parse_property_page(self, response):

        property_info = {}

        property_data = "".join(response.css("script::text")[-2].get())

        property_data = json.loads(property_data)

        data = property_data['props']['page_props']['ad']

        property_info['source'] = response.url

        property_info['address_country'] = 'Denmark'

        property_info['property_listing_type'] = 'rent'

        try:
            property_info['timeline_advertisement_creation'] = data['advertised_date']
        except :
            property_info['timeline_advertisement_creation'] = None

        try:
            property_info['address_city'] = data['city']
        except :
            property_info['address_city'] = None

        try:
            property_info['address_city_area'] = data['city_area']
        except :
            property_info['address_city_area'] = None

        try:
            property_info['address_street'] = data['street_name']
        except :
            property_info['address_street'] = None

        try:
            property_info['address_postal_code'] = str(data['postal_code'])
        except :
            property_info['address_postal_code'] = None

        try:
            property_info['property_description'] = data['description']
        except :
            property_info['property_description'] = None

        try:
            property_info['property_type'] = data['category']
        except :
            property_info['property_type'] = None

        try:
            property_info['property_advertisement_title'] = data['title']
        except :
            property_info['property_advertisement_title'] = None

        try:
            property_info['property_rooms_amount'] = data['rooms']
        except :
            property_info['property_rooms_amount'] = None

        try:
            property_info['property_living_area_sqm'] = data['size_m2']
        except :
            property_info['property_living_area_sqm'] = None

        try:
            property_info['property_rent_price'] = data['monthly_rent']
        except :
            property_info['property_rent_price'] = None

        try:
            property_info['property_rent_price_currency'] = data['monthly_rent_currency']
        except :
            property_info['property_rent_price_currency'] = None

        try:
            property_info['property_rent_monthly_extra_cost'] = data['monthly_rent_extra_costs']
        except :
            property_info['property_rent_monthly_extra_cost'] = None

        try:
            property_info['property_prepaid_rent'] = data['prepaid_rent']
        except :
            property_info['property_prepaid_rent'] = None

        try:
            property_info['property_deposit'] = data['deposit']
        except :
            property_info['property_deposit'] = None

        try:
            property_info['latitude'] = data['location']['lat']
        except :
            property_info['latitude'] = None

        try:
            property_info['longitude'] = data['location']['lon']
        except :
            property_info['longitude'] = None

        try:
            property_info['media_set'] = [image['url'] for image in data['images'][:15]]
        except :
            property_info['media_set'] = []

        try:
            property_info['property_floor_number'] = data['floor']
        except :
            property_info['property_floor_number'] = None

        try:
            property_info['property_rental_period'] = data['rental_period']
        except :
            property_info['property_rental_period'] = None

        try:
            property_info['address_neighbourhood'] = data['city_level_3']
        except :
            property_info['address_neighbourhood'] = None

        try:
            match = re.match(r'([A-Z])(\d{4})?', data['energy_rating'])
            if match:
                property_info['property_energy_label'] = match.group(1)
                property_info['property_energy_label_year'] = int(match.group(2)) if match.group(2) else None

        except :
            property_info['property_energy_label'] = None


        try:
            property_info['property_is_social_housing'] = data['social_housing']
        except :
            property_info['property_is_social_housing'] = None

        try:
            property_info['property_features_dictionary'] = [{feature: value} for feature, value in data['features'].items() if value]
        except :
            property_info['property_features_dictionary'] = None


        # Parse the creation date of the property
        created_date_str = property_info.get('timeline_advertisement_creation')
        created_date = datetime.fromisoformat(created_date_str.replace('Z', '+00:00'))

        # Check if the created date is older than the threshold
        if created_date < self.date_threshold:
            self.logger.info("Stopping spider, found a property created more than 1 days ago.")
            raise CloseSpider(reason="Found property created more than 1 days ago")

        yield property_info