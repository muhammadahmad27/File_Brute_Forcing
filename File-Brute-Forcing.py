import requests
import os
from urllib.parse import urlparse

def print_heading():
    print(f"{'Path':<40} {'Status Code':<25} {'Content Length':<20} {'Word Count':<15} {'Character Count':<20} {'Message':<15}")
    print("="*150)

def validate_url(target_url):
    parsed_url = urlparse(target_url)
    if not parsed_url.scheme:
        target_url = "https://" + target_url
        parsed_url = urlparse(target_url)
    if not parsed_url.netloc:
        return None, False
    try:
        response = requests.get(target_url)
        if response.status_code == 200:
            return target_url, True
        else:
            return target_url, False
    except requests.RequestException:
        return target_url, False

def validate_wordlist(wordlist):
    return os.path.isfile(wordlist)

def save_url(status_code, url):
    if not os.path.exists('responses/files'):
        os.makedirs('responses')
        os.makedirs('responses/files')
    
    with open(f'responses/files/{status_code}.txt', 'a') as file:
        file.write(f"{url}\n")

def enumerate_files(target_url, wordlist):
    print_heading()
    with open(wordlist, 'r') as file:
        paths = file.readlines()
    
    for path in paths:
        path = path.strip()
        url = f"{target_url}/{path}"
        
        try:
            response = requests.get(url)
            content_length = len(response.content)
            word_count = len(response.text.split())
            character_count = len(response.text)
            
            if response.status_code == 200:
                print(f"{url:<40} {response.status_code:<25} {content_length:<20} {word_count:<15} {character_count:<20} - 200 OK")
            elif response.status_code == 302:
                print(f"{url:<40} {response.status_code:<25} {content_length:<20} {word_count:<15} {character_count:<20} - Redirect")
            elif response.status_code == 403:
                print(f"{url:<40} {response.status_code:<25} {content_length:<20} {word_count:<15} {character_count:<20} - Forbidden")
            elif response.status_code == 404:
                print(f"{url:<40} {response.status_code:<25} {content_length:<20} {word_count:<15} {character_count:<20} - Not Found")
            elif response.status_code == 500:
                print(f"{url:<40} {response.status_code:<25} {content_length:<20} {word_count:<15} {character_count:<20} - Server Error")
            else:
                print(f"{url:<40} {response.status_code:<25} {content_length:<20} {word_count:<15} {character_count:<20}")
            
            save_url(response.status_code, url)
        except requests.RequestException as e:
            print(f"Error accessing {url}: {e}")

if __name__ == "__main__":
    target_url = input("Enter the target URL or domain: ").strip()
    wordlist = input("Enter the path to the wordlist file: ").strip()
    
    valid_url, alive = validate_url(target_url)
    valid_wordlist = validate_wordlist(wordlist)
    
    if not valid_url:
        print("Invalid URL or domain entered. Usage: python3 file.py, hit enter, then enter a valid URL and a valid wordlist file.")
    elif not alive:
        print("The website is not alive or not responding.")
    elif not valid_wordlist:
        print("The path for the wordlist is not valid. Usage: python3 file.py, hit enter, then enter a valid URL and a valid wordlist file.")
    else:
        enumerate_files(valid_url, wordlist)
