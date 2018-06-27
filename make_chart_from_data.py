import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.patches as patches
import matplotlib.cbook as cbook
from matplotlib import gridspec
from matplotlib import rc
from matplotlib import lines
from matplotlib import font_manager as fm, rcParams
import os

def make_infographic(df, ward, alderman):
    matplotlib.rcParams['pdf.fonttype']= 42
    matplotlib.rcParams['ps.fonttype']=42
    plt.rc('text', usetex=True)

    font = {'weight' : 'normal',
            'size'   : 10}

    matplotlib.rc('font', **font)

    fpath = "Raleway-Regular.ttf"
    prop = fm.FontProperties(fname = fpath, weight='regular')
    fpath = "Raleway-Black.ttf"
    prop = fm.FontProperties(fname = fpath, weight='bold')

    """
    #Code to put everything on one chart
    fig = plt.figure(figsize=(10.0, 5.625))
    gs = gridspec.GridSpec(45,80)
    pie_chart = fig.add_subplot(gs[9:39,1:38])
    """

    fig1, pie_chart = plt.subplots()


    ### start pie chart ###

    #dict for how to aggregate data, grouping with a count, aggregating
    pie_df = df
    pie_df["donor_type_size"] = pie_df["donor_type"] + " " + pie_df["donation_size"]
    pie_df = pie_df.groupby(["donor_type_size"])
    pie_agg = {'amount':['sum'], 'donor_type_size':['count','max']}
    pie_df = pie_df.agg(pie_agg)

    #adding a range index
    pie_df.index = pd.RangeIndex(len(pie_df.index))

    #Totals for center of chart
    total_amount = df['amount'].sum()
    total_donors = df['amount'].count()

    # The slices will be ordered and plotted counter-clockwise.
    labels = ["\\bf \Large \sffamily \${:,d}\n{} Donors".format(list(pie_df['amount']['sum'])[x],list(pie_df['donor_type_size']['count'])[x]) for x in range(len(pie_df.index))]
    sizes = list(pie_df['amount']['sum'])
    colors = ['#122547','#0190EF','#6C0A0C','#D62259','#00865B','#00D9B8']

    pie_chart.pie(sizes, labels=labels, colors=colors)

    #draw a circle at the center of pie to make it look like a donut
    centre_circle = plt.Circle((0,0),0.50,color='white', fc='white',linewidth=1.25)
    pie_chart.add_artist(centre_circle)


    # Set aspect ratio to be equal so that pie is drawn as a circle.
    plt.axis('equal')

    pie_chart.text(0, 0,'Total\n\\bf \Huge \sffamily \${:,d}\n{} Donors'.format(total_amount, total_donors),
         horizontalalignment='center',
         verticalalignment='center')

    plt.tight_layout()
    plt.savefig(os.path.join('infographics', '{} - {} pie chart.png'.format(ward, alderman)), dpi=1000)
    plt.close()


    ### start bar graph ###

    """
    #Code to put everything on one chart
    bar_graph = fig.add_subplot(gs[10:38,41:78])
    """
    fig1, bar_graph = plt.subplots()

    bar_df = df

    bar_df['amount'].replace('',0)
    #initialize arrays, order is within_ward, in_Chicago_outside_ward, in_IL_outside_Chicago, outside_IL
    small_ind_amt = [0, 0, 0, 0]
    large_ind_amt = [0, 0, 0, 0]
    small_bus_amt = [0, 0, 0, 0]
    large_bus_amt = [0, 0, 0, 0]
    small_org_amt = [0, 0, 0, 0]
    large_org_amt = [0, 0, 0, 0]
    small_ind_cnt = [0, 0, 0, 0]
    large_ind_cnt = [0, 0, 0, 0]
    small_bus_cnt = [0, 0, 0, 0]
    large_bus_cnt = [0, 0, 0, 0]
    small_org_cnt = [0, 0, 0, 0]
    large_org_cnt = [0, 0, 0, 0]

    #loop to populate arrays
    for index, row in bar_df.iterrows():
    	if row[13] == "within_ward":
    		if row[11] == 'Individual':
    			if row[12] == 'under 500':
    				small_ind_cnt[0] += 1
    				small_ind_amt[0] += row[3]
    			elif row[12] == 'over 500':
    				large_ind_cnt[0] += 1
    				large_ind_amt[0] += row[3]
    		elif row[11] == 'Business':
    			if row[12] == 'under 500':
    				small_bus_cnt[0] += 1
    				small_bus_amt[0] += row[3]
    			elif row[12] == 'over 500':
    				large_bus_cnt[0] += 1
    				large_bus_amt[0] += row[3]
    		elif row[11] == 'Political Group':
    			if row[12] == 'under 500':
    				small_org_cnt[0] += 1
    				small_org_amt[0] += row[3]
    			elif row[12] == 'over 500':
    				large_org_cnt[0] += 1
    				large_org_amt[0] += row[3]
    	elif row[13] == 'in_Chicago_outside_ward':
    		if row[11] == 'Individual':
    			if row[12] == 'under 500':
    				small_ind_cnt[1] += 1
    				small_ind_amt[1] += row[3]
    			elif row[12] == 'over 500':
    				large_ind_cnt[1] += 1
    				large_ind_amt[1] += row[3]
    		elif row[11] == 'Business':
    			if row[12] == 'under 500':
    				small_bus_cnt[1] += 1
    				small_bus_amt[1] += row[3]
    			elif row[12] == 'over 500':
    				large_bus_cnt[1] += 1
    				large_bus_amt[1] += row[3]
    		elif row[11] == 'Political Group':
    			if row[12] == 'under 500':
    				small_org_cnt[1] += 1
    				small_org_amt[1] += row[3]
    			elif row[12] == 'over 500':
    				large_org_cnt[1] += 1
    				large_org_amt[1] += row[3]
    	elif row[13] == 'in_IL_outside_Chicago':
    		if row[11] == 'Individual':
    			if row[12] == 'under 500':
    				small_ind_cnt[2] += 1
    				small_ind_amt[2] += row[3]
    			elif row[12] == 'over 500':
    				large_ind_cnt[2] += 1
    				large_ind_amt[2] += row[3]
    		elif row[11] == 'Business':
    			if row[12] == 'under 500':
    				small_bus_cnt[2] += 1
    				small_bus_amt[2] += row[3]
    			elif row[12] == 'over 500':
    				large_bus_cnt[2] += 1
    				large_bus_amt[2] += row[3]
    		elif row[11] == 'Political Group':
    			if row[12] == 'under 500':
    				small_org_cnt[2] += 1
    				small_org_amt[2] += row[3]
    			elif row[12] == 'over 500':
    				large_org_cnt[2] += 1
    				large_org_amt[2] += row[3]
    	elif row[13] == 'outside_IL':
    		if row[11] == 'Individual':
    			if row[12] == 'under 500':
    				small_ind_cnt[3] += 1
    				small_ind_amt[3] += row[3]
    			elif row[12] == 'over 500':
    				large_ind_cnt[3] += 1
    				large_ind_amt[3] += row[3]
    		elif row[11] == 'Business':
    			if row[12] == 'under 500':
    				small_bus_cnt[3] += 1
    				small_bus_amt[3] += row[3]
    			elif row[12] == 'over 500':
    				large_bus_cnt[3] += 1
    				large_bus_amt[3] += row[3]
    		elif row[11] == 'Political Group':
    			if row[12] == 'under 500':
    				small_org_cnt[3] += 1
    				small_org_amt[3] += row[3]
    			elif row[12] == 'over 500':
    				large_org_cnt[3] += 1
    				large_org_amt[3] += row[3]


    # The position of the bars on the x-axis
    r = [0,1,2,3]

    # Names of group and bar width
    names = ['Ward','Chicago','Illinois','United States']
    barWidth = .6

    # Create small_ind_amt bars
    bar_graph.bar(r, small_ind_amt, color='#D62259', width=barWidth)
    # Create large_ind_amt
    bar_graph.bar(r, large_ind_amt, bottom=small_ind_amt, color='#6C0A0C', width=barWidth)
    # Create small_bus_amt
    bar_graph.bar(r, small_bus_amt, bottom=np.add(small_ind_amt, large_ind_amt), color='#0190EF', width=barWidth)
    # Create large_bus_amt
    bar_graph.bar(r, large_bus_amt, bottom=np.array([small_bus_amt, small_ind_amt, large_ind_amt]).sum(axis=0), color='#122547', width=barWidth)
    # Create small_org_amt
    bar_graph.bar(r, small_org_amt, bottom=np.array([large_bus_amt, small_bus_amt, small_ind_amt, large_ind_amt]).sum(axis=0), color='#00D9B8', width=barWidth)
    # Create large_org_amt
    bar_graph.bar(r, large_org_amt, bottom=np.array([small_org_amt, large_bus_amt, small_bus_amt, small_ind_amt, large_ind_amt]).sum(axis=0), color='#00865B', width=barWidth)

    # Y axis
    ax = plt.gca()
    fmt = '\${x:,.0f}'
    tick = ticker.StrMethodFormatter(fmt)
    ax.yaxis.set_major_formatter(tick)

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

    #put labels on top of bars
    heights = np.array([large_org_amt, small_org_amt, large_bus_amt, small_bus_amt, small_ind_amt, large_ind_amt]).sum(axis=0)
    donor_numbers = np.array([small_ind_cnt, large_ind_cnt,small_bus_cnt,large_bus_cnt,small_org_cnt, large_org_cnt]).sum(axis=0)
    labels = ["\\bf \Large \sffamily \${:,.0f}\n{} Donors".format(heights[i],donor_numbers[i]) for i in range(len(heights))]
    xs = [0,1,2,3]
    for height, label, x in zip(heights, labels, xs):
        ax.text(x, height+10, label, ha='center', va='bottom')

    #title
    #plt.title("Donations By Location", y=1.01)



    # Show graphic
    plt.tight_layout()
    plt.savefig(os.path.join('infographics', '{} - {} bar graph.png'.format(ward, alderman)), dpi=1000)
    plt.close()

    """
    #Code to put everything on one chart
    plt.savefig('{} - {}.pdf'.format(ward, alderman), dpi=1000, orientation='landscape', papertype='b0')
    """
