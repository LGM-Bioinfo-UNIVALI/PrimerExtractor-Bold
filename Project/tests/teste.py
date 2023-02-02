# import pandas as pd 

# df = pd.DataFrame(columns=["id", "code", "name", "nuc", "notes", "cocktail", "marker", "direction"])

# primer_info = {'id': '334', 'code': '1709Fg', 'name': 'COI forward', 'nuc': 'TAATTGGAGGATTTGGWAAYTG', 'notes': 'Trichoptera (degenerate)', 'cocktail': 'f', 'public': 't', 'submitter': 'Xin Zhou', 'marker': 'COI-5P', 'alias': None, 'updated': None, 'posreference': None, 'direction': 'F', 'reference': 'Zhou, X., K. M. Kjer, and J. C. Morse. 2007. Associating larvae and adults of Chinese Hydropsychidae (Insecta: Hydropsychidae) using DNA sequences. Journal of the North American Benthological Society 26(4): 718-741.'}
# primer_info = pd.DataFrame(primer_info, index=[0])

# df = pd.concat([df, primer_info], join='inner').reset_index(drop=True)

# print(df)

# =================================================================================

# import pandas as pd

# df1 = pd.DataFrame({'A':[1, 2, 3], 'B': [1, 2, 3]})

# df2 = pd.DataFrame({'A':[4, 5, 6], 'B': [4, 5, 6], 'C': [1, 2, 3], 'D': [1, 2, 3]})


# df1 = pd.concat([df1, df2[list(df1.columns) + ['C']]], join='outer', ignore_index=True)
# # df1.merge(df2[]])
# print(df1)
# =================================================================================

# import pandas as pd


# original = ['A', 'B']
# df1 = pd.DataFrame({'A':[1, 2, 3], 'B': [1, 2, 3]})
# df2 = pd.DataFrame({'A':[4, 5, 6], 'B': [4, 5, 6], 'C': [1, 2, 3], 'D': [1, 2, 3]})
# df3 = pd.DataFrame({'A':[7, 8, 9], 'B': [7, 8, 9], 'C': [4, 5, 6], 'E': [1, 3, 3]})
# df1 = pd.concat([df1, df2[original + ['C', 'D']]], join='outer', ignore_index=True)
# df1 = pd.concat([df1, df3[original + ['C', 'E']]], join='outer', ignore_index=True)

# print(df1)



# =================================================================================

import pandas as pd

primer1 = {"publicfield":"t","primer":{"id":"333","code":"1709Fs","name":"COI forward","nuc":"TAATTGGAGGATTTGGAAATTG","notes":"Trichoptera","cocktail":"f","public":"t","submitter":"Xin Zhou","marker":"COI-5P","alias":None,"updated":None,"posreference":None,"direction":"F","reference":"Zhou, X., K. M. Kjer, and J. C. Morse. 2007. Associating larvae and adults of Chinese Hydropsychidae (Insecta: Hydropsychidae) using DNA sequences. Journal of the North American Benthological Society 26(4): 718-741."},"primerstats":{"High":0,"Medium":0,"Low\\/Fail":0},"pairedstats":{"high":[],"medium":[],"low":[]},"isAllowEdit":False}
primer3 = {"publicfield":"t","primer":{"id":"20","code":"FishF2","name":None,"nuc":"TCGACTAATCATAAAGATATCGGCAC","notes":None,"cocktail":"f","public":"t","submitter":"Brianne St. Jacques","marker":"COI-5P","alias":None,"updated":None,"posreference":None,"direction":"F","reference":None},"primerstats":{"High":"1473","Medium":"501","Low\\/Fail":400},"pairedstats":{"high":{"FishR2":1456,"VR1":38,"VR2":31,"FR1d_t1":1,"MFR3":1,"VF2":1},"medium":{"FishR2":422,"VR2":72,"VR1":6,"MFR3":1,"VF2":1,"FR1d_t1":0},"low":{"FishR2":296,"VR2":101,"VR1":4,"MFR3":2,"VF2":0,"FR1d_t1":0}},"isAllowEdit":False}
primer2 = {"publicfield":"t","primer":{"id":"73","code":"Fish-BCH","name":None,"nuc":"ACTTCYGGGTGRCCRAARAATCA","notes":"targeted for all bony fish, but works for cartilaginous too; can be tailed with sequencing primers also.","cocktail":"f","public":"t","submitter":"Megan A. Milton","marker":"COI-5P","alias":"COIfishR1","updated":"2005-11-30 00:50:29.911299","posreference":None,"direction":"R","reference":"Baldwin, CC, JH Mounts, DG Smith, LA Weigt. 2009. Genetic Identification and color descriptions of early life-history stages of Belizean Phaeoptyx and Astrapogon (Teleostei: Apogonidae) with comments on identification of adult Phaeoptyx. Zootaxa 2008:1-22."},"primerstats":{"High":"3046","Medium":"322","Low\\/Fail":552},"pairedstats":{"high":{"Fish-BCL":4841},"medium":{"Fish-BCL":500},"low":{"Fish-BCL":617}},"isAllowEdit":False}
primer4 = {"publicfield":"t","primer":{"id":"333","code":"1709Fs","name":"COI forward","nuc":"TAATTGGAGGATTTGGAAATTG","notes":"Trichoptera","cocktail":"f","public":"t","submitter":"Xin Zhou","marker":"COI-5P","alias":None,"updated":None,"posreference":None,"direction":"F","reference":"Zhou, X., K. M. Kjer, and J. C. Morse. 2007. Associating larvae and adults of Chinese Hydropsychidae (Insecta: Hydropsychidae) using DNA sequences. Journal of the North American Benthological Society 26(4): 718-741."},"primerstats":{"High":0,"Medium":0,"Low\\/Fail":0},"pairedstats":{"high":[],"medium":[],"low":[]},"isAllowEdit":False}
primers = [primer1, primer2, primer3, primer4]



df_original_columns = ["id", "code", "name", "nuc", "notes", "cocktail", "marker", "direction", "reference", 'High', 'Medium', 'Low\\/Fail']
df = pd.DataFrame(columns=df_original_columns)
for primer_request in primers:
	primer_info = {**primer_request['primer'], **primer_request['primerstats']}
	primer_paired = primer_request['pairedstats']

	primer_info_df = pd.DataFrame(primer_info, index=[0])

	if ":" not in str(primer_info['nuc']):
		if primer_info['High'] != 0 or primer_info['Medium'] != 0 or primer_info['Low\\/Fail'] != 0:
			print('aqui1')
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

df.to_csv('teste.csv', sep=';', index=False)

writer = pd.ExcelWriter('teste.xlsx', engine='xlsxwriter')
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
	elif col in ['nuc', 'notes', 'reference']:
		worksheet.set_column(pos, pos, 24)
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