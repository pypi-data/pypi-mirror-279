import scrapy
import re
import xml.etree.ElementTree as ET
import json
from scrapy.selector import Selector

class AsunnotsellspiderSpider(scrapy.Spider):
    name = "asunnotsellspider"
    start_urls = ["https://asunnot.oikotie.fi/sitemaps/index.xml"]

    def parse(self, response):

        # Preprocess the XML content to remove incorrect URLs
        xml_content = response.body.decode('utf-8')
        xml_content_cleaned = re.sub(r'<loc>https://asunnot.oikotie.fi/sitemapssunnot.oikotie.fi/', '<loc>https://asunnot.oikotie.fi/', xml_content)

        # Parse the cleaned XML content
        root = ET.fromstring(xml_content_cleaned)

        # Extract URLs from the cleaned XML
        sitemap_urls = [elem.text for elem in root.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc")]

        # Filter URLs that start with 'https://asunnot.oikotie.fi/sitemaps/sm_ad'
        filtered_urls = [url for url in sitemap_urls if url.startswith('https://asunnot.oikotie.fi/sitemaps/sm_ad')]

        # Extract the content between <loc> tags
        for sitemap_url in filtered_urls:

            link = sitemap_url.strip()  # Remove any leading or trailing whitespace

            yield scrapy.Request(url = link, callback = self.get_urls)
    
    def get_urls(self,response):

        # Decode the response body and create a new Selector
        body = response.body.decode('utf-8')
        selector = Selector(text=body)
        
        # Extract URLs between <loc> tags that contain "myytavat-asunnot"
        urls = selector.xpath('//url/loc[contains(text(), "myytavat-asunnot")]/text()').getall()
        
        # Process each URL as needed
        for link in urls:
            yield scrapy.Request(url=link, callback=self.parse_property)
    
    def parse_property(self,response):

        property_info = {}
        
        property_info['source'] = response.url

        if 'vuokra' in property_info['source']:

            property_info['property_listing_type'] = 'rent'

        else:

            property_info['property_listing_type'] = 'sale'
        try:

            property_info['property_description'] = " ".join(response.css('div.listing-overview p::text').getall())
        except:

            pass
        
        try:
            property_info['property_floor_number'] = re.search(r'\d+', response.xpath('//dt[text()="Kerros"]/following-sibling::dd/text()').get()).group() if response.xpath('//dt[text()="Kerros"]/following-sibling::dd/text()').get() else None
        
        except:
            pass

        try:
            property_info['property_layout'] = response.css('dt:contains("Huoneiston kokoonpano") + dd::text').get()

        except:
            pass

        try:
            property_info['property_condition'] = response.css('dt:contains("Kunto") + dd::text').get()

        except:
            pass

        try:
            property_info['property_kitchen_features'] = response.css('dt:contains("Keittiön varusteet") + dd::text').get()
        
        except:
            pass

        try:
            property_info['property_bathroom_features'] = response.css('dt:contains("Kylpyhuoneen varusteet") + dd::text').get()

        except:
            pass

        try:
            property_info['property_renovation_info'] = response.css('dt:contains("Tehdyt remontit") + dd::text').get()

        except:
            pass

        try:
            property_info['property_additional_terms'] = response.css('dt:contains("Muut ehdot") + dd::text').get()
        except:
            pass

        try:
            property_info['property_sauna'] = response.css('dt:contains("Taloyhtiössä on sauna") + dd::text').get()

        except:
            pass

        try:
            property_info['property_heating'] = response.css('dt:contains("Lisätietoja lämmityksestä") + dd::text').get()

        except:
            pass

        try:
            property_info['property_energy_label'] = response.css('dt:contains("Energialuokka") + dd::text').get()

        except:
            pass

        try:
            image_urls = response.css('div.tabs-content a::attr(href)').getall()
            filtered_image_urls = [url for url in image_urls if url.startswith('https://cdn.asunnot.oikotie.fi/')]

            property_info['media_set'] = filtered_image_urls

        except:
            pass
        
        # Iterate through each script tag
        for script_text in response.css("script::text").getall():
            # Check if the script text contains 'analytics'
            if 'analytics' in script_text:
                # Extract JSON data from the script
                json_data = script_text.split("window.page=")[0].strip().rstrip(';')[script_text.split("window.page=")[0].strip().rstrip(';').find('{'):]
                json_data = json.loads(json_data)
                
                # Populate property_info dictionary with extracted data
                property_info['property_housing_type'] = json_data['analytics']['apartmentType']
                property_info['address_full'] = json_data['address']
                property_info['property_living_area_sqm'] = json_data['analytics']['size']
                property_info['property_sale_price'] = json_data['analytics']['price']
                property_info['property_sale_price_currency'] = 'EUR'
                property_info['timeline_advertisement_creation'] = json_data['analytics']['published']
                try:

                    property_info['address_postal_code'] = json_data['analytics']['zipCode']

                except KeyError:

                    property_info['address_postal_code'] = None

                    
                property_info['property_construction_year'] = json_data['analytics']['apartmentBuildYear']
                
                # Break the loop after finding the relevant script
                break

        match = re.match(r'^(.*?)(\d+)(.*)\,', property_info['address_full'])
        if match:
            property_info['address_street'] = match.group(1).strip()
            property_info['address_house_number'] = match.group(2).strip()
            property_info['address_addition'] = match.group(3).strip()
        else:
            property_info['address_street'] = re.match(r'^([^,]*)', property_info['address_full'])[0].strip()

        # Iterate through each script tag again to find additional data
        for script_text in response.css("script::text").getall():
            # Check if the script text contains additional data (assuming it has 'numberOfRooms' and 'geo' keys)
            if 'numberOfRooms' in script_text and 'geo' in script_text:
                # Extract JSON data from the script
                json_data_1 = json.loads(script_text)
                
                # Populate property_info dictionary with additional data
                property_info['property_rooms_amount'] = json_data_1['numberOfRooms']
                property_info['latitude'] = json_data_1['geo']['latitude']
                property_info['longitude'] = json_data_1['geo']['longitude']
                property_info['address_country'] = json_data_1['address']['addressCountry']
                # Break the loop after finding the relevant script
                break

        yield property_info