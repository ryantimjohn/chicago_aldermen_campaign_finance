#from process_il_sunshine import alderman_list

#for alderman in alderman_list:
#	print("https://illinoissunshine.org/search/?term={}&table_name=committees&search_date__ge=&search_date__le=".format(alderman.replace(' ', '+')))
from collections import OrderedDict
from pprint import PrettyPrinter
pp = PrettyPrinter()

alder_committee = """Joe Moreno,20809
Brian Hopkins,25653
Pat Dowell, 16892
Sophia King, 32052
Leslie Hairston,14216
Roderick Sawyer, 22875
Gregory Mitchell,22816
Michelle Harris,20016
Anthony Beale,14556
Susan Sadlowski Garza, 26168
Patrick Thompson,26197
George Cardenas,17290
Marty Quinn,23282
Ed Burke,4410
Raymond Lopez, 23079
Toni Faulkes,20107
David Moore, 23127
Derrick Curtis, 26217
Matthew O'Shea,22919
Willie Cochran,19880
Howard Brookins,17003
Ricardo Munoz, 9487
Michael Zalewski,14156
Michael Scott,26204
Daniel Solis,12260
Roberto Maldonado,9533
Walter Burnett,10591
Jason Ervin,23112
Chris Taliaferro,25937
Ariel Reboyas,17163
Milly Santiago,26162
Scott Waguespack,19898
Deborah Mell,20627
Carrie Austin, 11884
Carlos Ramirez-Rosa,26021
Gilbert Villegas,26023
Emma Mitts,15622
Nicholas Sposato,19830
Margaret Laurino, 9808
Patrick O'Connor,4353
Anthony Napolitano, 26028
Brendan Reilly,19263
Michelle Smith,19682
Thomas Tunney,17150
John Arena,22749
James Cappleman,20952
Ameya Pawar,23607
Harry Osterman,22976
Joseph Moore,6380
Debra Silverstein, 22982"""

alder_committee = [a.split(',') for a in alder_committee.split('\n')]

alder_committee = [[e.strip() for e in a] for a in alder_committee]
alder_url_list = []
for counter, alder in enumerate(alder_committee, 1):
	alder_url_list.append([counter, alder[0], "https://illinoissunshine.org/api/receipts/?committee_id={}&datatype=csv&limit=100000".format(alder[1])])
pp.pprint(alder_url_list)
