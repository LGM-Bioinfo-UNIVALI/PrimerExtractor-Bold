import requests
import pandas as pd 
import re
import time
from bs4 import BeautifulSoup


number_of_pages = 6
items_per_page = 500

primers = []

pages_params = {
	'offset': 0,
	'limit': items_per_page
}
for i in range(number_of_pages):
	primers_list = requests.get('https://www.boldsystems.org/index.php/Public_Primer_PrimerSearch/getSearchResultPage', params=pages_params)
	soup = BeautifulSoup(primers_list.content, 'html.parser')
	primers.extend(soup.find_all("div", {"name":"code"}))
	pages_params['offset'] += items_per_page


# with open('primers.html', 'r') as f:
#     contents = f.read()
#     soup = BeautifulSoup(contents, 'lxml')

# primers = soup.find_all("div", {"name":"code"})


df = pd.DataFrame(columns=["id", "code", "name", "nuc", "notes", "cocktail", "marker", "direction", "reference"])

df_original_columns = ["id", "code", "name", "nuc", "notes", "cocktail", "marker", "direction", "reference", 'High', 'Medium', 'Low/Fail']
df = pd.DataFrame(columns=df_original_columns)

for primer in primers:
	primer_id = primer['id']

	request_params = {
		'id': primer_id
	}
	time.sleep(2)
	primer_request = requests.get('https://www.boldsystems.org/index.php/Public_Ajax_PrimerView', params=request_params).json()
	print(primer_request)
	if ":" not in str(primer_request['primer']['nuc']):
		if type(primer_request['primerstats']) == list:
			primer_request['primerstats'] = {'High': primer_request['primerstats'][0], 'Medium': primer_request['primerstats'][1], 'Low/Fail': primer_request['primerstats'][2]}
		else:
			for key in primer_request['primerstats'].keys():
				if primer_request['primerstats'][key] == [] or primer_request['primerstats'][key] == None:
					primer_request['primerstats'][key] = 0
		primer_info = {**primer_request['primer'], **primer_request['primerstats']}
		primer_paired = primer_request['pairedstats']

		primer_info_df = pd.DataFrame(primer_info, index=[0])

		if ":" not in str(primer_info['nuc']):
			try:
				if int(primer_info['High']) != 0 or int(primer_info['Medium']) != 0 or int(primer_info['Low/Fail']) != 0:
					pair_columns = {}

					for key in primer_paired.keys():
						for pos, pair in enumerate(primer_paired[key]):
							pair_columns[f"{key.capitalize()} Pair {pos + 1}"] = pair
							pair_columns[f"{key.capitalize()} Pair {pos + 1} Qtd."] = primer_paired[key][pair]
					
					pair_df = pd.DataFrame(pair_columns, index=[0])
					primer_info_df = primer_info_df.reset_index(drop=True).merge(pair_df.reset_index(drop=True), left_index=True, right_index=True)

					df = pd.concat([df, primer_info_df[df_original_columns+ list(pair_df.keys())]], join='outer', ignore_index=True)
					columns2reorder = [col for col in df.columns if 'High Pair' in col]
					columns2reorder.extend([col for col in df.columns if 'Medium Pair' in col])
					columns2reorder.extend([col for col in df.columns if 'Low Pair' in col])

					df = df[[col for col in df if col not in columns2reorder] + columns2reorder]
				else:
					df = pd.concat([df, primer_info_df[df_original_columns]], join='outer', ignore_index=True)
			except Exception as e:
				print(e)

df.replace('\\n|\\r|\\t\\v', '', regex=True)
writer = pd.ExcelWriter('primers.xlsx', engine='xlsxwriter')
df.to_excel(writer, sheet_name='Sheet1', startrow=1, header=False, index=False)
workbook = writer.book
worksheet = writer.sheets['Sheet1']
(max_row, max_col) = df.shape
column_settings = [{'header': column} for column in df.columns]
worksheet.add_table(0, 0, max_row, max_col - 1, {'columns': column_settings, 'style': 'Table Style Medium 9'})

centered_cell = workbook.add_format({'align': 'center'})
for pos, col in enumerate(df.columns):
	if col == 'id':
		worksheet.set_column(pos, pos, 8, centered_cell)
	elif col in ['cocktail', 'direction', 'High']:
		worksheet.set_column(pos, pos, 10, centered_cell)
	elif col in ['notes', 'reference']:
		worksheet.set_column(pos, pos, 24)
	elif col == 'nuc':
		worksheet.set_column(pos, pos, 35)
	elif col in ['code', 'name', 'marker']:
		worksheet.set_column(pos, pos, 12, centered_cell)
	elif 'High' in col and 'Qtd.' in col or 'Low' in col and 'Qtd.' in col:
		worksheet.set_column(pos, pos, 17, centered_cell)
	elif 'Medium' in col and 'Qtd.' in col:
		worksheet.set_column(pos, pos, 21, centered_cell)
	elif 'High Pair' in col:
		worksheet.set_column(pos, pos, 14, centered_cell)
	elif 'Medium Pair' in col:
		worksheet.set_column(pos, pos, 16, centered_cell)
	else:
		worksheet.set_column(pos, pos, 12, centered_cell)

writer.save()
		# primer_info_df = pd.DataFrame(primer_info, index=[0])
		# df = pd.concat([df, primer_info_df], join='inner').reset_index(drop=True)


# df.replace('\\n|\\r|\\t\\v', '', regex=True)
# df.to_csv('output.csv', sep=';', index=False)
