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
	title='API для анализа тональности текста',
	description= \
		'Главная цель API для анализа тональности текста заключается в определении оценки или '
		'эмоциональной окраски текста. Система может определить, является ли текст позитивным, '
		'негативным или нейтральным на основе предобученных моделей. Также пользователям системы будет '
		'предоставляться функционал по созданию (настройке) собственных систем анализа тональности текста с требуемыми параметрами. ',
	version='1.0',
	authorizations=authorizations
)

from .tokenize_text.dto import tokenization_model
api.models[tokenization_model.name] = tokenization_model

from .vectorize_text.dto import vectorization_sequence_model, tokenlist_model, embedding_vectorization_model
api.models[vectorization_sequence_model.name] = vectorization_sequence_model
api.models[tokenlist_model.name] = tokenlist_model
api.models[embedding_vectorization_model.name] = embedding_vectorization_model

from .tokenize_text.dto import tokenizer_info_model
api.models[tokenizer_info_model.name] = tokenizer_info_model

from .vectorize_text.dto import vectorization_info_model
api.models[vectorization_info_model.name] = vectorization_info_model

from .models_actions.dto import user_ml_model, user_prediction_model, user_prediction_model_v2
api.models[user_ml_model.name] = user_ml_model
api.models[user_prediction_model.name] = user_prediction_model
api.models[user_prediction_model_v2.name] = user_prediction_model_v2



from .analyse_text.dto import sentiment_model
api.models[sentiment_model.name] = sentiment_model

from .model_train.dto import train_model, train_model_v2
api.models[train_model.name] = train_model
api.models[train_model_v2.name] = train_model_v2

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
api.add_namespace(model_train_ns) # <---------------

# метрики модели
from .metrics.model_metrics_ns import input_to_output_model, ml_model_metrics
api.models[input_to_output_model.name] = input_to_output_model
api.models[ml_model_metrics.name] = ml_model_metrics


from .metrics.model_metrics_ns import model_metrics_ns
api.add_namespace(model_metrics_ns)

# models actions
from .models_actions.models_actions_ns import ns as models_actions_ns
api.add_namespace(models_actions_ns)

