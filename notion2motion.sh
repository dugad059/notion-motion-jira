#!/bin/bash

#TURN JSON TO CSV
cd /Users/david.dugas/Documents/repos/tools/david/notion-motion-jira
source .venv/bin/activate
python3 notion2motion.py
deactivate