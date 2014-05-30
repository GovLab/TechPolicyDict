#!/usr/bin/env python
# -*- coding: utf8 -*- 
import os, sys
from mongoengine import *
from datetime import datetime


class Vote(Document):
	user = ReferenceField('Users')
	definition = StringField()
	word = ReferenceField('Words')
	vote = StringField()

class Users(Document):
	ts = ComplexDateTimeField(default=datetime.now())
	email = StringField()
	name = StringField()
	password = StringField()
	votes = ListField(ReferenceField(Vote))

class Definitions(EmbeddedDocument):
	ts = ComplexDateTimeField(default=datetime.now())
	d = StringField()
	category = StringField()
	vote_tally = IntField()
	sub = ReferenceField(Users)

class Words(Document):
	ts = ComplexDateTimeField(default=datetime.now())
	name = StringField()
	prettyName = StringField()
	tags = ListField(StringField())
	defs = ListField(EmbeddedDocumentField(Definitions))
	status = StringField() #undefined or defined
	sub = ReferenceField(Users)

