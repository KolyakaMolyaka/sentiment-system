from flask_restx import Api

authorizations = {
	'basicAuth': {
		'type': 'basic',
		'in': 'header',
		'name': 'Authorization'
	}
}

api = Api(
	prefix='/api/',
	title='Приложение для анализа тональности текста',
	description= \
		'Описание...',
	version='1.0',
	authorizations=authorizations
)

from .tokenize_text.dto import tokenization_model
api.models[tokenization_model.name] = tokenization_model

from .create_datasets.create_datasets_ns import ns as create_datasets_ns
api.add_namespace(create_datasets_ns)

from .get_datasets_results.get_datasets_results_ns import ns as get_datasets_results_ns
api.add_namespace(get_datasets_results_ns)

from .auth.auth_ns import ns as auth_ns
api.add_namespace(auth_ns)

from .tokenize_text.tokenize_text_ns import ns as tokenize_text_ns
api.add_namespace(tokenize_text_ns)
