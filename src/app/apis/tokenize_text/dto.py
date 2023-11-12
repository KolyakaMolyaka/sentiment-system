from flask_restx.reqparse import RequestParser

# tokenization info request json parser
tokenization_info_reqparser = RequestParser(bundle_errors=True)
tokenization_info_reqparser.add_argument(
	name='text', type=str, location='json', required=True, nullable=False
)
# tokenization_info_reqparser.add_argument(
# 	name='tokenizationType', type=int, location='json', required=True, nullable=False
# )