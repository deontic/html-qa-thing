import uuid
from lxml import etree
from io import StringIO
from bs4 import BeautifulSoup
from html2image import Html2Image
from PIL import Image
from pixelmatch.contrib.PIL import pixelmatch


def htmlqa(file1, file2, should_justify, image_size=(1920, 1080)):
    filepaths = [file1['path'], file2['path']]
    for file in filepaths:
        with open(file, 'r', encoding="utf-8") as f:
            html = f.read()
            print(f"\nFile: {file}\n")

            etree.parse(StringIO(html), etree.HTMLParser(recover=False))
            soup = BeautifulSoup(html, features="lxml")
            tags = soup.find_all(name=True)
            padding = {}
            if should_justify:
                padding = {"name": 7, "id": 2}
                for tag in tags:
                    name_l, id_l = len(tag.name or ""), len(
                        tag.get('id') or "")

                    if name_l > padding['name']:
                        padding['name'] = name_l
                    if id_l > padding['id']:
                        padding['id'] = id_l

                def getPadding(key, value): return padding.get(
                    key) - len(value or '')

                separatorPos1 = padding['name']
                separatorPos2 = padding['id']

                # account for "id: " before ids and "name: " before names
                print(
                    f"Tag Name{(separatorPos1) * ' '} Id{(5+separatorPos2) * ' '}Class\n")

                for tag in tags:
                    class_list = tag.get('class') and '.' + \
                        (' .'.join(tag.get('class'))) or '-'
                    print(
                        f"name: {tag.name}{getPadding('name', tag.name) * ' '} | id: {tag.get('id') or '-'}{getPadding('id', tag.get('id') or '-') * ' '} | class: {class_list}")
            else:

                for tag in tags:
                    class_list = 'class' in tag and tag['class'] or '-'
                    print(
                        f"name: {tag.name}, id: {tag.get('id') or '-'}, class: {class_list}")

    print('\ncalculating difference between rendered HTML files...')
    hti = Html2Image()

    images = []

    for file in [file1, file2]:
        img_path = str(uuid.uuid4())+'.jpg'
        images.append(img_path)
        css_files = file.get('css_files')
        if css_files:
            hti.screenshot(
                html_file=file['path'], css_file=css_files, save_as=img_path, size=image_size
            )
        else:
            hti.screenshot(
                html_file=file['path'], save_as=img_path, size=image_size
            )

    img_a = Image.open(images[0])
    img_b = Image.open(images[1])

    w1, h1 = img_a.size

    img_diff = Image.new("RGBA", img_a.size)

    # specify more options if you want https://pypi.org/project/pixelmatch/
    mismatch = pixelmatch(img_a, img_b, img_diff,
                          includeAA=True, threshold=0.08)
    print(f'difference in number of pixels: {mismatch/w1*h1*0.01}%')
    img_diff.save("diff.png")
