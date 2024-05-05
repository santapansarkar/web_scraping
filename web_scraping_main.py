import requests
from bs4 import BeautifulSoup
import pandas as pd


def grab_url(url):
    url_data = requests.get(url)
    if url_data.status_code == 200:
        return url_data
def parse_url_data(url_data):
    soup = BeautifulSoup(url_data.text, 'html.parser')
    return soup    

def parse_bestseller_topic_tags(**kwargs_parse_tags):
    h2_tag = kwargs_parse_tags['soup'].find_all('h2', class_=kwargs_parse_tags['selection_class'])
    bestseller_topic = []
    for tags in h2_tag:
        bestseller_topic.append(tags.text)
    return bestseller_topic    

def parse_bestseller_item_tags(**kwargs_parse_tags):
    h2_tag = kwargs_parse_tags['soup'].find_all('div', class_=kwargs_parse_tags['selection_class'])
    bestseller_item = []
    for tags in h2_tag:
        bestseller_item.append(tags.text)
    return bestseller_item   

def output_tab(**kwargs_output_tab):
    top_item_dict = {
        'topic_name' : kwargs_output_tab['topic_name'],
        'item_name' : kwargs_output_tab['item_name']
    }
    print(top_item_dict)
    try:
        df = pd.DataFrame(top_item_dict)
    except:
        print(f'Error in creating dataframe...trying alternate method')
        df = pd.DataFrame.from_dict(top_item_dict, orient='index')
        df = df.transpose()      
    df.to_csv('amazon_bestsellers.csv', index=False)    


if __name__ == '__main__':
    url = 'https://www.amazon.in/gp/bestsellers/?ref_=nav_cs_bestsellers'
    url_data = grab_url(url)
    print(len(url_data.text))
    with open('amazon_bestsellers.html', 'w') as f:
        f.write(url_data.text)
    soup = parse_url_data(url_data)
    selection_class = 'a-carousel-heading a-inline-block'
    kwargs_parse_tags = {
        'soup' : soup,
        'selection_class' : selection_class
    }
    bestseller_topic = parse_bestseller_topic_tags(**kwargs_parse_tags)    
    selection_class = 'p13n-sc-truncate p13n-sc-truncate-desktop-type2 p13n-sc-line-clamp-5'
    kwargs_parse_tags = {
        'soup' : soup,
        'selection_class' : selection_class
    }
    bestseller_item = parse_bestseller_item_tags(**kwargs_parse_tags)
    kwargs_output_tab = {
        'topic_name' : bestseller_topic,
        'item_name' : bestseller_item
    }    
    output_tab(**kwargs_output_tab)