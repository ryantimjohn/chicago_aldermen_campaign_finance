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
import numpy as np
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

def make_small_donor_chart(donation_data, alderman):
    #Define the font parameters
    matplotlib.rcParams['pdf.fonttype']= 42
    matplotlib.rcParams['ps.fonttype']=42
    plt.rc('text', usetex=True)
    font = {'weight' : 'normal',
            'size'   : 10}
    matplotlib.rc('font', **font)
    fpath = "Raleway-Black.ttf"
    prop = fm.FontProperties(fname = fpath, weight='bold')
    #set up the bar graph
    ax=plt.gca()
    bar_width = 1
    opacity = 1
    error_config = {'ecolor': '0.3'}
    index=[0,1,2] #this just defines where things appear on X axis; we're not doing anything fancy o it's just a straight sequence ....
    names=[' \\bf \Large \sffamily All funds','\\bf \Large \sffamily From small donors', '\\bf \Large \sffamily From people in their ward'] #X labels
    colors=['#b51b89','#271ab5','#ff7b00'] #colors for each bar
    r=index
    rects = ax.bar(index, donation_data, bar_width,alpha=opacity, color=colors,label='Donations',align='center')
    #display dollar amounts on top of bars
    fmt = '\${x:,.0f}'
    tick = ticker.StrMethodFormatter(fmt)
    ax.yaxis.set_major_formatter(tick)

    # X axis
    plt.xticks(r, names)
    
    # X axis
    plt.xticks(r, names)

    # ticks
    plt.tick_params(
        axis='both',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        bottom=False,      # ticks along the bottom edge are off
        top=False,	# ticks along the top edge are off
        left=False)

    #spines
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_color('#989898')

    #show the dollar totals on top of the bars
    heights = np.array(donation_data)
    labels=["\\bf \Large \sffamily \$ {:,.0f}".format(donation_data[0]),"\\bf \Large \sffamily \$ {:,.0f}".format(donation_data[1]),"\\bf \Large \sffamily \$ {:,.0f}".format(donation_data[2])] #format the total for each of the three bars
    xs = [0,1,2]
    for height, label, x in zip(heights, labels, xs):
        ax.text(x, height+10, label, ha='center', va='bottom')
    # Show graphic
    plt.tight_layout()
    plt.savefig(os.path.join('infographics', (alderman+' donation overview')), dpi=1000)
    plt.close()



def make_sector_chart(donation_data, alderman):
    #set plot parameters
    matplotlib.rcParams['pdf.fonttype']= 42
    matplotlib.rcParams['ps.fonttype']=42
    plt.rc('text', usetex=True)
    font = {'weight' : 'normal',
            'size'   : 10}
    matplotlib.rc('font', **font)
    fpath = "Raleway-Black.ttf"
    prop = fm.FontProperties(fname = fpath, weight='bold')

    pie_chart=plt.gca()

    label_list=[]
    #create the labels
    for item in list(donation_data.keys()):
        label_list.append("\\bf \Large \sffamily \${:,.0f}".format(donation_data[item])+"\n"+item)

    #dict for how to aggregate data, grouping with a count, aggregating
    
    pie_chart.pie(list(donation_data.values()), labels=label_list)

    #draw a circle at the center of pie to make it look like a donut
    centre_circle = plt.Circle((0,0),0.50,color='white', fc='white',linewidth=1.25)
    pie_chart.add_artist(centre_circle)


    # Set aspect ratio to be equal so that pie is drawn as a circle.
    plt.axis('equal')

    plt.tight_layout()
    plt.savefig(os.path.join('infographics', (alderman+' sector chart')), dpi=1000)
    plt.close()
    
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

def get_sector_data(alder_data): #parse the report file to get contributions from all sectors
    sector_chunk=alder_data.split("SECTORS")[1].split("INTERESTING DONATIONS")[0] #get the chunk of the file containing sectors
    sector_donations={}#list to hold the money donated by each sector
    for item in sector_chunk.split("\n"):
        if len(item) > 2: #make sure this is an actual line with text not just a blank
            donation_temp=item.split(":")[1]
            donation_temp=donation_temp[:donation_temp.find(",")]
            sector_donations[item.split(":")[0]]=float(donation_temp.replace("$",""))
    return sector_donations

for alderman in all_aldermen:
    print(alderman)
    try:
        alder_file=open(os.path.join("data","reports",alderman.replace(" ","_")+" report.txt"),'r')
        alder_file_lines=alder_file.read()
        alder_file.close()
        #make_small_donor_chart((get_donation_data(alder_file_lines)),alderman)
        #print(str(get_sector_data(alder_file_lines)))
        make_sector_chart((get_sector_data(alder_file_lines)),alderman)
    except FileNotFoundError:
        print("Couldn't load file")
        
    
