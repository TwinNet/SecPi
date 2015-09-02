# web framework
import cherrypy

# templating engine
from mako.lookup import TemplateLookup
from collections import OrderedDict

from tools import utils

import urllib

class BaseWebPage(object):
	"""A baseclass for a CherryPy web page."""
	
	def __init__(self, baseclass):
		self.baseclass = baseclass
		self.lookup = TemplateLookup(directories=['templates'], strict_undefined=True)
		self.fields = OrderedDict()
	
	
	def objectToDict(self, obj):
		data = {}
		
		for k, v in self.fields.iteritems():
			cherrypy.log("k: %s, v: %s"%(k,v))
			data[k] = obj.__dict__[k]
			
		return data;
	
	def objectsToList(self, objs):
		data = []
		
		for o in objs:
			data.append(self.objectToDict(o))
			
		return data;
	
	@property
	def db(self):
		return cherrypy.request.db
	
	@cherrypy.expose
	@cherrypy.tools.json_out()
	@cherrypy.tools.json_in()
	def fieldList(self):
		if(hasattr(cherrypy.request, 'json')):
			filter = cherrypy.request.json['filter'];
		
			return {'status': 'success', 'data': utils.filter_fields(self.fields, filter)}
		
		return {'status': 'error', 'message': 'No filter set.'}
	
	@cherrypy.expose
	@cherrypy.tools.json_out()
	def list(self):
		objects = self.db.query(self.baseclass).all()
		
		return {'status': 'success', 'data': self.objectsToList(objects)}
	
	
	@cherrypy.expose
	@cherrypy.tools.json_out()
	@cherrypy.tools.json_in()
	def delete(self):
		if(hasattr(cherrypy.request, 'json')):
			id = cherrypy.request.json['id']
			if id:
				obj = self.db.query(self.baseclass).get(id)
				if(obj):
					self.db.delete(obj)
					self.db.commit()
					return {'status': 'success', 'message': 'Object deleted!'}
		
		return {'status': 'error', 'message': 'ID not found!'}
		
		
	@cherrypy.expose
	@cherrypy.tools.json_out()
	@cherrypy.tools.json_in()
	def add(self, **params):
		if(not params):
			data = cherrypy.request.json
		else:
			data = params
			
		if(data and len(data)>0):
			cherrypy.log("got something %s"%params)
			newObj = self.baseclass()
			
			for k, v in params.iteritems():
				if(v and not v == ""):
					setattr(newObj, k, utils.str_to_value(v))
			
			self.db.add(newObj)
			self.db.commit()
			return {'status': 'success','message':"Added new object with id %i"%newObj.id}	
		
		return {'status': 'error', 'message': 'No parameters recieved!'}
		
		
	@cherrypy.expose
	@cherrypy.tools.json_out()
	@cherrypy.tools.json_in()
	def update(self, id=0, **params):
		
		if(not params):
			data = cherrypy.request.json
		else:
			data = params
		
		if(not id or id == 0):
			id = cherrypy.request.json.id
		
		# check for valid id
		if(id and id > 0):
			
			if(data and len(data)>0):
				cherrypy.log("update something %s"%data)
				obj = self.db.query(self.baseclass).get(id)
				
				for k, v in data.iteritems():
					if(v and not v == ""):
						setattr(obj, k, utils.str_to_value(v))
				
				self.db.commit()
				
				return {'status': 'success', 'message': "Updated object with id %i"%obj.id}
			else:
				cherrypy.log("got id to update: %s"%id)
				obj = self.db.query(self.baseclass).get(id)
				cherrypy.log("got from db: %s"%obj)
				return {'status': 'success', 'data': obj}
		else:
			return {'status':'error', 'message': "Invalid ID!" }






