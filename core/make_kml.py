import os
import io
import re

def make_kml():
    with io.open(os.path.join('kml', 'allwards.kml'), 'rb') as f:
        allwards = f.read()
    with io.open(os.path.join('kml', 'start.kml'), 'rb') as f:
        start = f.read()
    with io.open(os.path.join('kml', 'end.kml'), 'rb') as f:
        end = f.read()

    placemarkre = re.compile('\<Placemark\>[\S\s]*?\<\/Placemark\>'.encode(encoding='utf_8'))
    placemarks = re.findall(pattern=placemarkre, string=allwards)
    for placemark in placemarks:
        wardre = re.compile('\<value\>(.*?)\<\/value\>'.encode(encoding='utf_8'))
        ward = wardre.search(placemark).group(1)
        ward = int(str(ward, encoding='utf_8'))
        placemark = re.sub('\<ExtendedData\>[\S\s]*?\<\/ExtendedData\>'.encode(encoding='utf_8'),
                           '<name>Ward {}</name>'.format(ward).encode(encoding='utf_8'),
                           placemark)
        with io.open(os.path.join('kml', 'Ward{}.kml'.format(ward)), 'wb') as f:
            f.write(start + placemark + end)
    # soup = BeautifulSoup(kml, "lxml-xml")
    # placemarks = soup.findAll('Placemark')
    #
    # for placemark in placemarks:
    #     ward = placemark.select('ExtendedData Data value')[0].string
    #     name = "<name>Ward {}</name>".format(ward)
    #     name = BeautifulSoup(name, "lxml-xml")
    #     placemark.find('ExtendedData').replaceWith(name.find('name'))
    #     placemark = str(placemark).encode('utf-8')
    #
    #     with io.open(os.path.join('kml', '{}.kml'.format(ward)), 'wb') as f:
    #         f.write(start_template + placemark + end_template)

make_kml()
