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

from .vectorize_text.dto import vectorization_sequence_model, tokenlist_model, embedding_vectorization_model
api.models[vectorization_sequence_model.name] = vectorization_sequence_model
api.models[tokenlist_model.name] = tokenlist_model
api.models[embedding_vectorization_model.name] = embedding_vectorization_model

from .analyse_text.dto import sentiment_model
api.models[sentiment_model.name] = sentiment_model

from .model_train.dto import train_model
api.models[train_model.name] = train_model

from .create_datasets.create_datasets_ns import ns as create_datasets_ns
api.add_namespace(create_datasets_ns)

from .get_datasets_results.get_datasets_results_ns import ns as get_datasets_results_ns
api.add_namespace(get_datasets_results_ns)

from .auth.auth_ns import ns as auth_ns
api.add_namespace(auth_ns)

from .tokenize_text.tokenize_text_ns import ns as tokenize_text_ns
api.add_namespace(tokenize_text_ns)

from .vectorize_text.vectorize_text_ns import ns as vectorize_text_ns
api.add_namespace(vectorize_text_ns)

from .analyse_text.analyse_text_ns import ns as analyse_text_ns
api.add_namespace(analyse_text_ns)

from .model_train.model_train_ns import ns as model_train_ns
api.add_namespace(model_train_ns)
