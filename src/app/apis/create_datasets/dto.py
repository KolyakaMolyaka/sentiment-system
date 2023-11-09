from flask_restx.reqparse import RequestParser

# sportmaster parser info request json parser
sportmaster_parser_info_reqparser = RequestParser(bundle_errors=True)
sportmaster_parser_info_reqparser.add_argument(
	name='catalog_url', type=str, location='json', required=True, nullable=False
)
sportmaster_parser_info_reqparser.add_argument(
	name='pages', type=int, location='json', required=True, nullable=False
)
