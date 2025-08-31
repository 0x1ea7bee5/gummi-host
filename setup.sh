#!/bin/bash


if [ -d "venv" ]; then
	echo "Virtual Environment found, not installin nuffin"
else
	echo -e "No Virtual Environment found, installing now"
	python -m venv venv
	source venv/bin/active
	pip install -r requirements.txt
	echo -e "Setup is done"
fi
