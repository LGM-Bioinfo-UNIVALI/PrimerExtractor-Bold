import requests
import time
import pandas as pd
from bs4 import BeautifulSoup


class PrimersExtractor():
	def __init__(self, number_of_pages, items_per_page):
		super(PrimersExtractor, self).__init__()
		self.list_url = 'https://www.boldsystems.org/index.php/Public_Primer_PrimerSearch/getSearchResultPage'
		self.primer_url = 'https://www.boldsystems.org/index.php/Public_Ajax_PrimerView'
		self.number_of_pages = number_of_pages
		self.items_per_page = items_per_page
		self.primers = []


	def extract_primers_list(self):  # Get html content of all primers
		request_params = {
			'offset': 0,
			'limit': self.items_per_page
		}

		for page in range(self.number_of_pages):
			primers_list = requests.get(self.list_url, params=request_params)
			soup = BeautifulSoup(primers_list.content, 'html.parser')
			self.primers.extend(soup.find_all("div", {"name": "code"}))
			request_params['offset'] += self.items_per_page

		return self.primers


	def get_primerstats(self, primer_request):
		if isinstance(primer_request['primerstats'], list):
			primer_request['primerstats'] = {'High': primer_request['primerstats'][0], 'Medium': primer_request['primerstats'][1], 'Low/Fail': primer_request['primerstats'][2]}
		else:
			for key in primer_request['primerstats'].keys():
				if primer_request['primerstats'][key] == [] or primer_request['primerstats'][key] is None:
					primer_request['primerstats'][key] = 0

		return primer_request


	def get_primer_pairedstats(self, primer_request, primer_info_df):
		primer_paired = primer_request['pairedstats']
		pair_columns = {}

		for key in primer_paired.keys():
			for pos, pair in enumerate(primer_paired[key]):
				pair_columns[f"{key.capitalize()} Pair {pos + 1}"] = pair
				pair_columns[f"{key.capitalize()} Pair {pos + 1} Qtd."] = primer_paired[key][pair]
		
		pair_df = pd.DataFrame(pair_columns, index=[0])
		primer_info_df = primer_info_df.reset_index(drop=True).merge(pair_df.reset_index(drop=True), left_index=True, right_index=True)

		return primer_info_df, pair_df


	def concat_pairedstats_to_df(self, primers_df, primers_df_columns, primer_info_df, pair_df):
		primers_df = pd.concat([primers_df, primer_info_df[primers_df_columns + list(pair_df.keys())]], join='outer', ignore_index=True)
		columns2reorder = [col for col in primers_df.columns if 'High Pair' in col]
		columns2reorder.extend([col for col in primers_df.columns if 'Medium Pair' in col])
		columns2reorder.extend([col for col in primers_df.columns if 'Low Pair' in col])

		primers_df = primers_df[[col for col in primers_df if col not in columns2reorder] + columns2reorder]

		return primers_df


	def extract_primer_data(self, primers):
		primers_df_columns = ["id", "code", "name", "nuc", "notes", "cocktail", "marker", "direction", "reference", 'High', 'Medium', 'Low/Fail']
		primers_df = pd.DataFrame(columns=primers_df_columns)

		for pos, primer in enumerate(primers):
			if pos > 1000 and pos <= 1500:
				if pos % 200 == 0:
					time.sleep(60)

				primer_id = primer['id']

				request_params = {
					'id': primer_id
				}
				try:
					primer_request = requests.get(self.primer_url, params=request_params).json()

					if ":" not in str(primer_request['primer']['nuc']):
						primer_request = self.get_primerstats(primer_request)

						primer_info = {**primer_request['primer'], **primer_request['primerstats']}
						primer_info_df = pd.DataFrame(primer_info, index=[0])

						if int(primer_info['High']) != 0 or int(primer_info['Medium']) != 0 or int(primer_info['Low/Fail']) != 0:
							primer_info_df, pair_df = self.get_primer_pairedstats(primer_request, primer_info_df)
							primers_df = self.concat_pairedstats_to_df(primers_df, primers_df_columns, primer_info_df, pair_df)

						else:
							primers_df = pd.concat([primers_df, primer_info_df[primers_df_columns]], join='outer', ignore_index=True)
				except Exception as e:
					print(e, 'Primer:', pos, primer, primer_id)

				print(pos)
				time.sleep(2)

		return primers_df

