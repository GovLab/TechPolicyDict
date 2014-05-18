#!/usr/bin/env python
# -*- coding: utf8 -*- 
import os, sys
from mongoengine import *
from datetime import datetime





class User(Document):
	ts = ComplexDateTimeField(default=datetime.now())
	email = StringField()
	name = StringField()
	password = StringField()

class Definition(EmbeddedDocument):
	definition = StringField()
	category = StringField()
	tags = ListField(StringField())
	voteUp = IntField()
	voteDown = IntField()

class Word(Document):
	ts = ComplexDateTimeField(default=datetime.now())
	word = StringField()
	defs = ListField(EmbeddedDocumentField(Definition))

