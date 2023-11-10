#!/bin/bash
flask --app src.app.run init-db
flask --app src.app.run run -h 0.0.0.0
