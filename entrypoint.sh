#!/bin/bash
flask --app src.app.run delete-previous-models
flask --app src.app.run download-nltk-data
flask --app src.app.run download-navec-data
flask --app src.app.run init-db
flask --app src.app.run fill-db
flask --app src.app.run run -h 0.0.0.0 -p 5000 --debug

