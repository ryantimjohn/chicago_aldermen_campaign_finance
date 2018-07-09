import matplotlib
import process_il_sunshine as pis
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.patches as patches
import matplotlib.cbook as cbook
from matplotlib import gridspec
from matplotlib import rc
from matplotlib import lines
from matplotlib import font_manager as fm, rcParams
import os

all_aldermen='''Joe Moreno
Brian Hopkins
Pat Dowell
Sophia King
Leslie Hairston
Roderick Sawyer
Gregory Mitchell
Michelle Harris
Anthony Beale
Susan Sadlowski Garza
Patrick Thompson
George Cardenas
Marty Quinn
Ed Burke
Raymond Lopez
Toni Faulkes
David Moore
Derrick Curtis
Matthew O'Shea
Willie Cochran
Howard Brookins
Ricardo Munoz
Michael Zalewski
Michael Scott
Daniel Solis
Roberto Maldonado
Walter Burnett
Jason Ervin
Chris Taliaferro
Ariel Reboyas
Milly Santiago
Scott Waguespack
Deborah Mell
Carrie Austin
Carlos Ramirez-Rosa
Gilbert Villegas
Emma Mitts
Nicholas Sposato
Margaret Laurino
Patrick O'Connor
Anthony Napolitano
Brendan Reilly
Michelle Smith
Thomas Tunney
John Arena
James Cappleman
Ameya Pawar
Harry Osterman
Joseph Moore
Debra Silverstein'''.split("\n")

def get_donation_data(alder_data): #parse the report file to get small donaitons, donations from inside ward, and total
    feo_itemized=float(alder_data[alder_data.find("FEO ITEMIZED:")+13:].split("\n")[0].replace("$","")) #parse out the total for itemized contributions that would still be under the FEO limit. Small donaitons=non itemized contributions + itemized contributions less than 175
    #non_itemized=float(alder_data[alder_data.find("SECTOR small donors:")+19:].split("\n")[0].replace("$",""))
    sectors={}
    for item in alder_data.split("\n"):
        if "SECTOR" in item and "SECTORS" not in item:
            amount=float(item.split(":")[1].split(",")[0].replace("$",""))
            sectors[item.split(":")[0]]=amount
    nonitemized=sectors['SECTOR small donors'] #this is always uatomtically inserted, we dpon't need to worry about whether it's there
    try:
        individual_in_ward=sectors['SECTOR local individual ']
    except KeyError: #no donations from this sector
        individual_in_ward=0
    total=0
    for item in sectors:
        total=total+sectors[item]
    return [total, nonitemized+feo_itemized, individual_in_ward]



for alderman in all_aldermen:
    print(alderman)
    try:
        alder_file=open(os.path.join("data","reports",alderman.replace(" ","_")+" report.txt"),'r')
        alder_file_lines=alder_file.read()
        alder_file.close()
        print(str(get_donation_data(alder_file_lines)))
    except FileNotFoundError:
        print("Couldn't load file")
        
    
