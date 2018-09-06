Utilities for downloading data from Illinois Sunshine and computing stats on it.

This is what we use to compare aldermen (i.e. who gets the most money from developers)
and compute statistics on them. The code is not extensively commented yet but we are working on it.

Files:

aldermen.csv--file mapping aldermen names to committee IDs
downloaddata.py--run this to download new data from IL sunshine. Also attempts to look up the ward for each donor address; this process takes a while.
analyze2.py--generate a report on each aldermen's donations. These are human readable but also contian the data for the pie charts
analyze3_makesimplereport.py--Creates an even more human readable report.
analyze2-feo.py.--Attempts to simulate what donations would look like to each person were the FEO passed. Use caution as these are rough estimates at best.
donorclass3.csv--training data for the Bayesian classifier that classifiers the sector (i.e. real estate, retail, etc) of donations.