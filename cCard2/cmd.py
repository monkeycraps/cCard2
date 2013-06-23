#!/usr/bin/env python
#-*- coding: UTF-8 -*-
import sys 
import settings 
from django.core.management import setup_environ 
sys.path.append(settings.PROJECT_PATH) 
setup_environ(settings) 

import logging
logger = logging.getLogger( 'card' );
from app.models import SphinxFilter

r = SphinxFilter.search.query("中医")
print r._sphinx