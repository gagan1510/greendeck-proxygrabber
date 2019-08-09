import json

def update_proxies():
    # THIS FUNCTION UPDATES THE DEAD PROXIES WITH THE NEW ONE
    pass

def change_proxies(proxy_list, country_code):
    # THIS FUNCTION WILL BE CALLED TO CHANGE THE PROXY LIST
    # WITH A NEW ONE AFTER EVERY SPECIFIED SECONDS
    proxy_dict = {
        country_code: proxy_list
    }
    
    with open('proxy_{}.json'.format(country_code), 'r') as f: 
        f.write(json.dumps(proxy_dict))
    
    print('DUMPED!')
    