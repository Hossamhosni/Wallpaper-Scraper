
from bs4 import BeautifulSoup
from PIL import Image
import requests
import argparse

def download_images(query, number):
    base_url = get_page_url(query)
    pages_urls = get_pages_url_based_on_number_of_images(base_url, number)
    get_images(pages_urls)

def get_page_url(query):
    url = 'https://wall.alphacoders.com/'
    if ' ' in query:
        queries = query.split(' ')
        if (query):
            url += 'search.php?search=' + '+'.join(queries)
    elif(query):
        url += 'search.php?search=' + query
    return url.strip()

def get_pages_url_based_on_number_of_images(url, number):
    urls = [url]
    pages = int(number / 60)
    for i in range(pages):
        urls.append(url+'&page=' + str(i+2))
    return urls

def get_containing_divs(soup):
    containers = soup.findAll("div", {"class": "thumb-container-big"})
    return containers

def get_img_urls_from_containers(containers):
    ids = [container['id'].split('_')[1] for container in containers]
    imgs = [container.find('img') for container in containers]
    base_urls = [img['data-src'].split('thumb')[0] for img in imgs]
    ext = [img['data-src'].split('.')[-1] for img in imgs]
    urls = [base_url + id + '.' + extension for base_url,
            id, extension in zip(base_urls, ids, ext)]
    return urls

def get_images(urls):
    print(urls)
    for url in urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        containers = get_containing_divs(soup)
        imgs_urls = get_img_urls_from_containers(containers)
        print(imgs_urls)
        for url in imgs_urls:
            print(url)
            img = Image.open(requests.get(url, stream=True).raw)
            img.save('E:\Programming\Projects\wallpaperscraper\downloads\\' +
                        str(url).split('/')[-1])
            print('saved')



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Search for wallpapers")
    parser.add_argument('--query')
    args = parser.parse_args()
    download_images({args.query}, 20)
