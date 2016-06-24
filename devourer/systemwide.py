# -*- coding: utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from hitsl_utils.cas import CasExtension

app = Flask(__name__)

db = SQLAlchemy()

cas = CasExtension()
