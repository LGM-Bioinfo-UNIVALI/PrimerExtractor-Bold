from utils import read_config_file
from PrimersExtractor import PrimersExtractor
from ExcelBuilder import ExcelBuilder


if __name__ == '__main__':
	config = read_config_file('config.yaml')

	primers_extractor = PrimersExtractor(config['SCRAPING']['PAGES'], config['SCRAPING']['PAGE_ITEMS'])

	primers = primers_extractor.extract_primers_list()
	primers_df = primers_extractor.extract_primer_data(primers)
	primers_df = primers_df.replace('\\n|\\r|\\t\\v', '', regex=True)
	primers_df.to_csv(config['OUTPUT']['FLAT_FILE_NAME'], sep='\t', index=False)

	excel_builder = ExcelBuilder(primers_df, config['OUTPUT']['EXCEL_FILE_NAME'], config['OUTPUT']['SHEET_NAME'])

	excel_builder.build_excel_file()
