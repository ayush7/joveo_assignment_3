"""
Utils for working with links like filtering them, removing duplicate links etc. 

"""
import json 


def correct_name(name:str):
    """Corrects some pagetitle descripencies for easier readability for LLMs"""
    name = name.replace('\n','')
    name = name.replace('  ','')
    return name 



def categorize_links(links_dictionary):
    return



def prase_links(crawled_links_file):
    """
    Parses the links given by crawler in a much more 'sane' format. Also removes duplicate links
    Returns:
        list_of_links -> List
        link_pagetitle -> List (corresponds to previous)
        unique_items_dictionary -> Just the above two in dictionary format for ease
    """
    with open(crawled_links_file, 'r') as ff:
        links_data = json.load(ff)
    
    list_of_links = []
    link_titles = []
    unique_links = {} 
    for item in links_data:
 # Dictionary to track unique links
        
        # single_link_item = {}
        if item["pagetitle"] == None:
            item["pagetitle"] = item["sitemap"]
        link_titles.append(correct_name(item['pagetitle']))
        list_of_links.append(item['sitemap'])
        
        
        
        unique_links[f"{item['sitemap']}"] = correct_name(item['pagetitle'])
        
        sublinks = item['links']
        for key, value in sublinks.items():
            if value != None or value !='':
                
                list_of_links.append(value) 
                link_titles.append(correct_name(str(key)))
                unique_links[value] = correct_name(str(key))  # Store unique link and title

            

        # Reconstruct lists from unique_links dictionary
    list_of_links = list(unique_links.keys())
    link_titles = list(unique_links.values())
        
        
    # print(unique_links)
    # print(list_of_links)        
    return list_of_links, link_titles , unique_links


