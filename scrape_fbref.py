import requests
from bs4 import BeautifulSoup, Comment
import pandas as pd

#Target URL
url = "https://fbref.com/en/comps/9/stats/Premier-League-Stats"

#Step 1: Download the page
res = requests.get(url)
soup = BeautifulSoup(res.text, 'lxml')

#Step 2: Extract HTML comments containing the tables
comments = soup.find_all(string=lambda text: isinstance(text, Comment))

#Step 3: Search for the correct table in the commented HTML
table = None #Define the variable before the loop

for comment in comments:
	comment_soup = BeautifulSoup(comment, 'lxml')
	tables = comment_soup.find_all('table', id='stats_standard')
	if tables:
		table = tables[0]
		break

#Step 4: Check if table was found
if table is None:
	print("Could not find the 'stats_standard' table inside comments.")
else:

	#Step 5: Convert the table into a DataFrame
	df = pd.read_html(str(table), header=0)[0] #multi-index header
	df.columns = ['_'.join(col).strip() if isinstance(col, tuple) else col for col in df.columns]
	#Step 6: Clean up repeated headers or rank column
	if 'Rk' in df.columns:
		df = df[df['Rk'] != 'Rk'] #Remove repeated header rows
		df.drop(columns=['Rk'], inplace=True)
		df.reset_index(drop=True, inplace=True)

	#Step 7: Save it as CSV
	df.to_csv("data/premier_league_standard_stats.csv", index=False)
	print("Scraped and saved: premier_league_standard_stats.csv")
