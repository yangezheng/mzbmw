#!/usr/bin/env bash
pip install poetry
poetry config virtualenvs.create false
poetry install --no-root
