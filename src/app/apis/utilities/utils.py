from flask_restx import Model


def fill_with_default_values(payload: dict, model: Model):
	"""
	Fill payload with default values from the model
	:param dict payload: payload to fill with default values
	:param flask_restx.Model model: model with default values
	"""

	included_keys = payload.keys()
	not_included_items = {k: v.default for k, v in model.items() if k not in included_keys}
	payload.update(not_included_items)
