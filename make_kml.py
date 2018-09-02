from bs4 import BeautifulSoup
import os

def make_kml():
    kml = ""
    with open(os.path.join('kml', 'Boundaries - Wards (2015-).kml'),
              encoding='utf8') as f:
        kml = f.read()
    soup = BeautifulSoup(kml, "lxml-xml")
    placemarks = soup.findAll('Placemark')

    start_template = '''<?xml version='1.0' encoding='UTF-8'?>
<kml xmlns:kml="http://earth.google.com/kml/2.2">
  <Document id="featureCollection">
<Style id="defaultStyle">
  <LineStyle>
    <width>1.5</width>
  </LineStyle>
  <PolyStyle>
    <color>7d8a30c4</color>
  </PolyStyle>
</Style>
  <Folder>'''

    end_template='''</Folder>  </Document>
    </kml>'''

    for placemark in placemarks:
        ward = placemark.select('ExtendedData Data value')[0].string
        name = "<name>Ward {}</name>".format(ward)
        name = BeautifulSoup(name, "lxml-xml")
        placemark.find('ExtendedData').replaceWith(name.find('name'))
        placemark = str(placemark)

        with open(os.path.join('kml', '{}.kml'.format(ward)), 'w',
                  encoding='utf8') as f:
            f.write(start_template + placemark + end_template)

make_kml()
