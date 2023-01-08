import argparse
from bs4 import BeautifulSoup
import requests
from threading import Thread
threads = []
parser = argparse.ArgumentParser(
                    prog = 'wallhaven',
                    description = 'Download wallpapers from https://wallhaven.cc',
                    epilog = 'author: github.com/slashformotion')
parser.add_argument("folder")
args =parser.parse_args()
folder= args.folder

def download(url):
    req = requests.get(url)
    if req.status_code != 200:
        print(f"got {req.status} on {url}")
        return
    soup = BeautifulSoup(req.text,'html.parser')
    img = soup.find(id='wallpaper')
    target = img.get("src")
    res = requests.get(target)
    filename = target.split("/")[len(target.split("/"))-1]
    with open(f"./{folder}/{filename}", 'wb') as out:
        out.write(res.content)

while True:
    url = input("please gimme url like \"https://wallhaven.cc/w/mdvoq1\" (type 'quit' to stop):")
    if url == "quit":
        print("stopping now")
        break
    print(f"starting job for {url}")
    t = Thread(target=download, args=[url])
    threads.append(t)
    t.start()

print("finishing the last jobs")

for t in threads:
    t.join()

print("finished")
