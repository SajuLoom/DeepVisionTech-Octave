# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List, Union

from rasa_sdk import Action, Tracker
import rasa_sdk
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import FollowupAction, SlotSet
from rasa_sdk.forms import FormAction
from datetime import date, datetime
from bs4 import BeautifulSoup
import requests

#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

product_name = ''
items_list = []

filter_link = []
brands_link = []

def get_product(product_name):
    product_name = product_name.replace(" ","+")
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close"
    }
    url = f'https://www.amazon.in/s?k={product_name}&rh=p_72%3A1318476031&dc&qid=1633508050&rnid=1318475031&ref=sr_nr_p_72_1'
    page = requests.get(url,headers= headers)
    doc = BeautifulSoup(page.content,"html.parser")

    items =[]
    if len(doc.find_all(class_="sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 AdHolder sg-col s-widget-spacing-small sg-col-4-of-20")) != 0:
        items = doc.find_all(class_="sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 AdHolder sg-col s-widget-spacing-small sg-col-4-of-20")
    else:
        items = doc.find_all(class_="s-result-item s-asin sg-col-0-of-12 sg-col-16-of-20 AdHolder sg-col s-widget-spacing-small sg-col-12-of-16")

    items_list = []
    i = 3
    for item in items[:i]:
        if item.find(class_="a-offscreen") is None:
            i= i+1
            continue
        current_item = {}
        link = item.find(class_="a-link-normal s-no-outline")
        current_item['link'] = "https://www.amazon.in" +link['href']
        image = item.find(class_="s-image")
        current_item['image'] = image['src']
        if item.find(class_="a-size-base-plus a-color-base a-text-normal") is not None:
            name = item.find(class_="a-size-base-plus a-color-base a-text-normal")
        else:
            name = item.find(class_="a-size-medium a-color-base a-text-normal")
        current_item['Product name'] = name.string
        price = item.find(class_="a-offscreen")
        current_item['price'] = price.string
        rating = item.find(class_="a-icon-alt")
        current_item['rating'] = rating.string

        items_list.append(current_item)

    return items_list


def get_product_1(url):
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close"
    }
    page = requests.get(url,headers= headers)
    doc = BeautifulSoup(page.content,"html.parser")

    items =[]
    if len(doc.find_all(class_="sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 AdHolder sg-col s-widget-spacing-small sg-col-4-of-20")) != 0:
        items = doc.find_all(class_="sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 AdHolder sg-col s-widget-spacing-small sg-col-4-of-20")
    else:
        items = doc.find_all(class_="s-result-item s-asin sg-col-0-of-12 sg-col-16-of-20 AdHolder sg-col s-widget-spacing-small sg-col-12-of-16")

    items_list =[]
    i = 3
    for item in items[:i]:
        if item.find(class_="a-offscreen") is None:
            i= i+1
            continue
        current_item = {}
        link = item.find(class_="a-link-normal s-no-outline")
        current_item['link'] = "https://www.amazon.in" +link['href']
        image = item.find(class_="s-image")
        current_item['image'] = image['src']
        if item.find(class_="a-size-base-plus a-color-base a-text-normal") is not None:
            name = item.find(class_="a-size-base-plus a-color-base a-text-normal")
        else:
            name = item.find(class_="a-size-medium a-color-base a-text-normal")
        current_item['Product name'] = name.string
        price = item.find(class_="a-offscreen")
        current_item['price'] = price.string
        rating = item.find(class_="a-icon-alt")
        current_item['rating'] = rating.string

        items_list.append(current_item)

    return items_list


def get_details(url):
    
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close"
    }

    page = requests.get(url,headers=headers)
    doc = BeautifulSoup(page.text,"html.parser")

    details_tag = doc.find('div', id ="dp-container")

    details = {}


    details['Name'] = details_tag.find('span', id="productTitle").string.strip()
    details['Rating'] = details_tag.find('span', class_="a-icon-alt").string
    details['Price'] = details_tag.find('span', id ="priceblock_dealprice").string if details_tag.find('span', id ="priceblock_dealprice") is not None else details_tag.find('span', id ="priceblock_ourprice").string
    details['Delivery'] = details_tag.find('div', id="ddmDeliveryMessage").find('b').string.strip()
    details['Variants'] = details_tag.find('ul', class_="a-unordered-list a-nostyle a-button-list a-declarative a-button-toggle-group a-horizontal a-spacing-top-micro swatches swatchesSquare").find_all('p', class_="a-text-left a-size-base") if details_tag.find('ul', class_="a-unordered-list a-nostyle a-button-list a-declarative a-button-toggle-group a-horizontal a-spacing-top-micro swatches swatchesSquare") is not None else 'No Varients Available'
    details['Availability'] = details_tag.find('span', class_ ="a-size-medium a-color-success").string.strip() if details_tag.find('span', class_ ="a-size-medium a-color-success") is not None else "Out of Stock"
    features = details_tag.find('div', id ="productOverview_feature_div").find_all('tr',class_="a-spacing-small")
    fr={}
    for feature in features:
        f = feature.find('span',class_="a-size-base a-text-bold").string
        r = feature.find('td',class_="a-span9").find('span').string
        fr[f]=r
    details['Features'] = fr
    reviews= details_tag.find('div',class_="a-section a-spacing-large reviews-content filterable-reviews-content celwidget").find('div',class_="a-section review-views celwidget").find('div',class_="a-section review aok-relative") if details_tag.find('div',class_="a-section a-spacing-large reviews-content filterable-reviews-content celwidget").find('div',class_="a-section review-views celwidget").find('div',class_="a-section review aok-relative") is not None else "No reviews yet."
    reviews= details_tag.find('div',class_="a-section a-spacing-large reviews-content filterable-reviews-content celwidget").find('div',class_="a-section review-views celwidget").find_all('div',class_="a-section review aok-relative") if details_tag.find('div',class_="a-section a-spacing-large reviews-content filterable-reviews-content celwidget").find('div',class_="a-section review-views celwidget").find_all('div',class_="a-section review aok-relative") is not None else "No reviews yet."
    re={}
    ref={}
    for item in reviews:
        revperso= item.find('span',class_="a-profile-name").string.strip()
        ref=revperso

    j=len(ref)
    i=3
    if j<3:
        i=j


    for review in reviews[:i]:
        revperson=review.find('span',class_="a-profile-name").string.strip()
        rev=review.find('div',class_="a-expander-collapsed-height a-row a-expander-container a-expander-partial-collapse-container").find('span').text.strip()
        re[revperson]=rev

    details['Review']=re

    details['img'] = doc.find('div', id = "imgTagWrapperId").find('img')['src']

    
    return details


class ActionTime(Action):

    def name(self) -> Text:
        return "action_what_is_time"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        message = "The Time is "+ current_time

        dispatcher.utter_message(message)

        return []


class ActionDate(Action):

    def name(self) -> Text:
        return "action_what_is_date"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        toDate = date.today()
        _date = toDate.strftime("%B %d, %Y, %A")
        message = "It's "+ _date
        print(_date)

        dispatcher.utter_message(message)

        return []


class ActionDailyDeals(Action):

    def name(self) -> Text:
        return "action_todays_deal"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # tracker.get_slot('product_image')
        # tracker.get_slot('product_details')
        headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close"
        }
        url = 'https://www.amazon.in/gp/bestsellers/electronics'

        page = requests.get(url,headers=headers)
        doc = BeautifulSoup(page.text,"html.parser")

        items = doc.find_all('li', class_="zg-item-immersion")
        global items_list
        items_list = []
        best_seller = []
        i = 4
        for item in items[:i]:
            if item.find('span', class_="aok-inline-block zg-item").find('a',class_="a-link-normal a-text-normal") is None:
                i =i+1
                continue
            c =item.find('a',class_="a-link-normal")
            current_item ={}
            current_item['link'] = "https://www.amazon.in" + c['href'] 
            img = c.find('img')['src']
            current_item['Image'] = img
            current_item['Rating'] = item.find('div', class_="a-icon-row a-spacing-none").find('a',class_="a-link-normal")['title']
            current_item['Name'] = c.find('img')['alt']
            current_item['Price'] = item.find('span', class_="aok-inline-block zg-item").find('a',class_="a-link-normal a-text-normal").find('span',class_="p13n-sc-price").string
            items_list.append(current_item)
            best_seller.append(current_item)
        

        dispatcher.utter_message(text="Today's Daily Deal are here")

        for index, item in enumerate(best_seller[:3]):
            print(item['Image'])
            name = item['Name']
            rating = item['Rating']
            price = item['Price']
            details = f'Product {index+1}:-Product Name: {name}\n Rating: {rating}\n Price:{price}'
            dispatcher.utter_message(image=item['Image'])
            dispatcher.utter_message(text= details)

        return []



class ActionSerchProduct(Action):

    def name(self) -> Text:
        return "action_search_product"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        global product_name
        product_name = tracker.get_slot('product_name')
        global items_list
        items_list = get_product(product_name)
        dispatcher.utter_message(text="Here are some results for you..")

        for index,item in enumerate(items_list):
            name = item['Product name']
            rating = item['rating']
            price = item['price']
            details =f'Product {index+1}:    --->Product Name: {name}    --->Rating: {rating}   --->Price:{price}'
            dispatcher.utter_message(image=item['image'])
            dispatcher.utter_message(text=details)
        return [SlotSet("product_name",None)]

class ActionByFilter(Action):

    def name(self) -> Text:
        return "action_filter"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        global product_name
        product = product_name
        product = product.replace(" ","+")

        headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close"
        }
        url = f'https://www.amazon.in/s?k={product}&rh=p_72%3A1318476031&dc&qid=1633508050&rnid=1318475031&ref=sr_nr_p_72_1'
        page = requests.get(url,headers= headers)
        doc = BeautifulSoup(page.content,"html.parser")

        fils =doc.find(id="priceRefinements").find_all(class_="a-link-normal s-navigation-item")

        fil_list = []
        global filter_link
        filter_link = []
        for fil in fils[:5]:
            current_item = {}
            current_item['link'] ="https://www.amazon.in" + fil['href']
            name = fil.find(class_="a-size-base a-color-base").string
            current_item['name'] = name
            filter_link.append(current_item["link"])
            fil_list.append(current_item)
        
        filters = 'Filters Available:- \n'
        for index, fil in enumerate(fil_list):
            filters += f'''
            \n\t{index+1}.{fil["name"]} 
            '''
        dispatcher.utter_message(text=filters)

        return []


class ActionByBrands(Action):

    def name(self) -> Text:
        return "action_brands"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        global product_name
        product = product_name
        product = product.replace(" ","+")

        headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close"
        }
        url = f'https://www.amazon.in/s?k={product}&rh=p_72%3A1318476031&dc&qid=1633508050&rnid=1318475031&ref=sr_nr_p_72_1'
        page = requests.get(url,headers= headers)
        doc = BeautifulSoup(page.content,"html.parser")

        print(doc)
        brands =doc.find(id="brandsRefinements").find_all('a',class_="a-link-normal s-navigation-item")

        brands_list = []
        global brands_link
        brands_link = []
        for brand in brands[:5]:
            current_item = {}
            current_item['link'] ="https://www.amazon.in" + brand['href']
            name = brand.find(class_="a-size-base a-color-base").string
            current_item['name'] = name
            brands_link.append(current_item["link"])
            brands_list.append(current_item)

        if len(items_list) == 0:
            dispatcher.utter_message(text="Nothing to show")
        filters = 'Brands Available:- \n'
        for index, fil in enumerate(brands_list):
            filters += f'''
            \n\t{index+1}.{fil["name"]} 
            '''
        dispatcher.utter_message(text=filters)

        return []


class ActionSearchProductFilter(Action):

    def name(self) -> Text:
        return "action_filterd"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        global filter_link
        url = ''
        option = tracker.get_slot('selected_option')
        if len(filter_link) == 0:
            dispatcher.utter_message(text="No products Searched for listing")
            return [SlotSet('selected_option',None)]
        if '1' in option:
            url = filter_link[0]
        elif '2' in option:
            url = filter_link[1]
        elif '3' in option:
            url = filter_link[2]
        elif '4' in option:
            url = filter_link[3]
        elif '5' in option:
            url = filter_link[4]
        else:
            dispatcher.utter_message(text="Sorry! I can't understand what you trying to say.")
            return [SlotSet('selected_option',None)]

        global items_list
        items_list = get_product_1(url)
        if len(items_list) == 0:
            dispatcher.utter_message(text="Nothing to show")
            return [SlotSet('selected_option',None)]
        for index,item in enumerate(items_list):
            name = item['Product name']
            rating = item['rating']
            price = item['price']

            details = f'Product {index+1}:- \nProduct Name: {name}\n Rating: {rating}\n Price:{price}'
            dispatcher.utter_message(image=item['image'])
            dispatcher.utter_message(text=details)

        return [SlotSet('selected_option',None)]


class ActionSearchProductBrand(Action):

    def name(self) -> Text:
        return "action_branded"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        global brands_link
        url = ''
        if len(brands_link) == 0:
            dispatcher.utter_message(text="No products Searched for listing")
            return [SlotSet('selected_option',None)]
        option = tracker.get_slot('selected_option')
        if '1' in option:
            url = brands_link[0]
        elif '2' in option:
            url = brands_link[1]
        elif '3' in option:
            url = brands_link[2]
        elif '4' in option:
            url = brands_link[3]
        elif '5' in option:
            url = brands_link[4]
        else:
            dispatcher.utter_message(text="Sorry! I can't understand what you trying to say.")
            return [SlotSet('selected_option',None)]

        global items_list
        items_list = get_product_1(url)

        if len(items_list) == 0:
            dispatcher.utter_message(text="Nothing to show")
            return [SlotSet('selected_option',None)]

        for index,item in enumerate(items_list):
            name = item['Product name']
            rating = item['rating']
            price = item['price']

            details = f'Product {index+1}:- \n\nProduct Name: {name}\n\nRating: {rating}\n\nPrice:{price}'
            dispatcher.utter_message(image=item['image'])
            dispatcher.utter_message(text=details)

        return [SlotSet('selected_option',None)]            

class ActionProductDetail(Action):

    def name(self) -> Text:
        return "action_product_details"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print()
        
        global items_list
        print(items_list)
        value =tracker.get_slot("selected_product")
        url =''
        if '1' in value:
            url = items_list[0]['link']
        elif '2' in value:
            url = items_list[1]['link']
        elif '3' in value:
            url = items_list[2]['link']
        else:
            dispatcher.utter_message(text="Sorry!I cant find what you are looking for. please give valid product id (ex: product 1, product 2)")
            return[]
        
        details = get_details(url)

        dispatcher.utter_message(image=details['img'])

        message = ''
        message += 'Product Name: ' + details['Name'] +'\n\n'
        message += 'Rating: ' + details['Rating'] + '\n\n'
        message += 'Price: ' + details['Price'] + '\n\n'
        message += 'Delivery Available at ' + details['Delivery'] + '\n\n'
        message += 'Availability: ' + details['Availability'] + '\n\n'
        message += 'Features:-\n'
        for i in details['Features']:
            message += i + ': ' + details['Features'][i] +'\n'
        
        message += '\nReviews:- \n'
        for i in details['Review']:
            message += i + ': ' + details['Review'][i]+'\n'
        message += '\nLink: ' + url
        dispatcher.utter_message(text=message)

        return []
