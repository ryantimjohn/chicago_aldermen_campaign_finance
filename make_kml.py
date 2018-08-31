from bs4 import BeautifulSoup
import os

def make_kml():
    kml = ""
    with open(os.path.join('kml', 'Boundaries - Wards (2015-).kml')) as f:
        kml = f.read()
    soup = BeautifulSoup(kml, "lxml")
    placemarks = soup.findAll('placemark')

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

    for ward, placemark in enumerate(placemarks, 1):
        name = "<name>Ward {}</name>".format(ward)
        name = BeautifulSoup(name, 'xml')
        placemark.find('extendeddata').replaceWith(name.find('name'))
        placemark = str(placemark)
        with open(os.path.join('kml', '{}.kml'.format(ward)), 'w') as f:
            f.write(start_template + placemark + end_template)
