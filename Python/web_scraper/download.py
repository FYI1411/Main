import bs4 as bs
import requests
import os
import shutil
img_load, script_load, href_load = True, True, True
website = input("website? ")
source = requests.get(website).text
soup = bs.BeautifulSoup(source, 'lxml')
images = soup.findAll('img')
scripts = soup.findAll('script')
hrefs = soup.findAll('link')
download = True


if img_load:
    print(images)
    if 'img' in os.listdir():
        i = input("Delete old img dir?(y/n)\n>")
        shutil.rmtree('img/') if i.lower() == 'y' else print('pass')
    img_link = []
    for image in images:
        if image['src'][0] == '/':
            img = website + image['src']
        else:
            img = image['src']
        if img not in img_link:
            img_link.append(img)
            with open("img_links.txt", "a+", encoding="utf-8") as f:
                f.write(img+'\n')
    with open("img_links.txt", "a+", encoding="utf-8") as f:
        f.write(f"{website}\n=> {len(img_link)} img" + '\n')
    if download:
        index = 1
        for img_file in img_link:
            error = False
            try:
                r = requests.get(img_file)
                file = img_file.split("/")[-1]
                if file.lower().endswith(('.jpeg', '.jpg', '.png')):
                    pass
                else:
                    file = f"img{index}.png"
                try:
                    with open(f'img/{file}', 'wb') as f:
                        f.write(r.content)
                except FileNotFoundError:
                    os.mkdir('img')
                    with open(f'img/{file}', 'wb') as f:
                        f.write(r.content)
            except requests.exceptions.MissingSchema as e:
                print(e)
                error = True
            print(f'downloaded img_file{index}: {img_file}')
            if not error and index != len(img_link):
                index += 1
        print(f"downloaded {index} file(s)")

if script_load:
    print(scripts)
    if 'script' in os.listdir():
        i = input("Delete old script dir?(y/n)\n>")
        shutil.rmtree('script/') if i.lower() == 'y' else print('pass')
    script_link = []
    for link in scripts:
        if 'src' in link.attrs:
            if link['src'][0] == '/':
                scr = website + link['src']
            else:
                scr = link['src']
            script_link.append(scr)
            with open("script_links.txt", "a+", encoding="utf-8") as f:
                f.write(scr+'\n')
    with open("script_links.txt", "a+", encoding="utf-8") as f:
        f.write(f"{website}\n=> {len(script_link)} script" + '\n')
    if download:
        index2 = 1
        for script_file in script_link:
            error = False
            try:
                sr = requests.get(script_file)
                file = script_file.split("/")[-1]
                if file.lower().endswith('.js'):
                    pass
                else:
                    file = f"script{index2}.js"
                try:
                    with open(f'script/{file}', 'wb') as f:
                        f.write(sr.content)
                except FileNotFoundError:
                    os.mkdir('script')
                    with open(f'script/{file}', 'wb') as f:
                        f.write(sr.content)
            except requests.exceptions.MissingSchema as e:
                print(e)
                error = True
            print(f'downloaded script_file{index2}: {script_file}')
            if not error and index2 != len(script_link):
                index2 += 1
        print(f"downloaded {index2} file(s)")

if href_load:
    print(hrefs)
    href_link = [link["href"] for link in soup.findAll("link") if "stylesheet" in link.get("rel", [])]
    for href in href_link:
        with open("href_links.txt", "a+", encoding="utf-8") as f:
            f.write(href+'\n')
    with open("href_links.txt", "a+", encoding="utf-8") as f:
        f.write(f"{website}\n=> {len(href_link)} css files" + '\n')

i = input(">")  # cmd stop
