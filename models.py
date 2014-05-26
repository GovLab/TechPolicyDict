#!/usr/bin/env python
# -*- coding: utf8 -*- 
import os, sys
from mongoengine import *
from datetime import datetime





class Users(Document):
	ts = ComplexDateTimeField(default=datetime.now())
	email = StringField()
	name = StringField()
	password = StringField()

class Definitions(EmbeddedDocument):
	ts = ComplexDateTimeField(default=datetime.now())
	d = StringField()
	category = StringField()
	voteUp = IntField()
	voteDown = IntField()
	sub = ReferenceField(Users)

class Words(Document):
	ts = ComplexDateTimeField(default=datetime.now())
	w = StringField()
	tags = ListField(StringField())
	defs = ListField(EmbeddedDocumentField(Definitions))
	sub = ReferenceField(Users)

