from flask_restx.reqparse import RequestParser

# auth from form parser
auth_from_form_reqparser = RequestParser(bundle_errors=True)
auth_from_form_reqparser.add_argument(
	name='username', type=str, location='form', required=True, nullable=False
)
auth_from_form_reqparser.add_argument(
	name='password', type=str, location='form', required=True, nullable=False
)
