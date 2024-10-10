import requests
import sys
import os
import concurrent.futures
import logging
from tqdm import tqdm

# Set up logging
logging.basicConfig(filename="dirbuster_errors.log", level=logging.ERROR)

# Custom headers
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; DirBuster/1.0)"}

def make_request(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=5)
        return (url, response.status_code)
    except requests.exceptions.Timeout:
        return (url, "Timeout")
    except requests.exceptions.RequestException as e:
        logging.error(f"Error for {url}: {e}")
        return (url, f"Error: {e}")

def main():
    if len(sys.argv) < 3:
        print("Usage: python dirbuster.py <wordlist> <base_url>")
        sys.exit(1)
    
    wordlist_path = sys.argv[1]
    base_url = sys.argv[2]

    if not os.path.isfile(wordlist_path):
        print(f"Error: File '{wordlist_path}' not found.")
        sys.exit(1)
    
    try:
        with open(wordlist_path, "r") as file:
            lines = [line.strip() for line in file if line.strip()]
        
        # Progress bar setup
        with tqdm(total=len(lines), desc="Scanning URLs") as pbar:
            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                futures = {executor.submit(make_request, base_url + line): line for line in lines}
                
                for future in concurrent.futures.as_completed(futures):
                    url, status_code = future.result()
                    if status_code == 200:
                        tqdm.write(f"{url} -> {status_code}")
                    pbar.update(1)

    except Exception as e:
        print(f"Error: An error occurred while processing the file: {e}")
        logging.error(f"File processing error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
