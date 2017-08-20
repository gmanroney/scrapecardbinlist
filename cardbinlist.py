#!/usr/bin/python
from bs4 import BeautifulSoup
from IPython.display import Image
import urllib
import csv
import os.path

def getCountryPageRows(ofile,country,page):

    # Create file for country and generate URL
    tableCount = 0 
    urlPage = page - 1
    writer = csv.writer(ofile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    if urlPage == 0:
	urlExt=country+".html"
    else:
	urlExt=country+".html?page="+str(urlPage)

    # Read page
    r = urllib.urlopen('https://www.cardbinlist.com/bin-list-'+urlExt).read()

    # Parse page using BeautifulSoup
    soup = BeautifulSoup(r,"html.parser")

    # Find tables in the page
    tables=soup.findAll("table",attrs={"class":"full-width text-xs-left mt-1" })

    # Loop through tables in the page
    for table in tables:

        headings = [th.get_text() for th in table.find("tr").find_all("th")]
        datasets = []

        for row in table.find_all("tr")[1:]:

            dataset = zip(headings, (td.get_text() for td in row.find_all("td")))
            datasets.append(dataset)

        # If records contain bin list information write to file
        for record in datasets:
            if (record[0])[0] == "Bank Issuer":
		IssuingBankNetwork=(record[1])[1]
		IssuingBankBIN=(record[2])[1]
	        IssuingBank=(record[0])[1]
		if len((record[0])[1]) == 0:
		    IssuingBank="Undefined"
	        row=IssuingBank,IssuingBankNetwork,IssuingBankBIN
		writer.writerow(row)
                tableCount = tableCount + 1

    # Return count of bin records found in the page to decide
    # if we have found all or not
    return tableCount 

def getCountry(country):  
    
    # Create file for country
    pageCount=0
    totalRecords=0
    ofile  = open('bin_'+country+'.csv', "wb")
    
    # Loop until no more bin records found
    keepGoing = True 
    while keepGoing:
        pageCount += 1

        # getCountryPageRows parses each page and gets records
        tableCountFound = getCountryPageRows(ofile,country,pageCount)
        totalRecords = totalRecords + tableCountFound
        if tableCountFound == 0:
	    keepGoing = False
	    print "For country "+country+ " records found = ",totalRecords
 
    # Close file when done
    ofile.close()

# Read list of countries from configuration file
countries = []
my_path = os.path.abspath(os.path.dirname(__file__))
path = os.path.join(my_path, "cardbinlist.cfg") 
with open(path) as file:
    for line in file: 
        line = line.strip() 
        countries.append(line) 

# Loop through list of countries and get bin list from cardbinlist.com site
for line in countries:
    line = line.lower()
    getCountry(line)

