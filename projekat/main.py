from flask import Flask, render_template, request, json
import os
import codecs
from owlready2 import *
import types
from rdflib import *

app = Flask(__name__)

network_forensics_onto = get_ontology("https://raw.githubusercontent.com/micamat/network-forensics-ontology/main/network_forensics.owl").load(reload = True)
forensics_onto = network_forensics_onto.imported_ontologies[0].load(reload = True)
network_onto = network_forensics_onto.imported_ontologies[1].load(reload = True)
network_forensics_instance_onto = network_forensics_onto.imported_ontologies[2].load(reload = True)

graph = default_world.as_rdflib_graph()

@app.route("/")
def home():
	return render_template("proba.html")

@app.route("/getForensicsAndNetworkRootClasses")
def getForensicsAndNetworkRootClasses():
	root_class_comments = dict()
	for c in network_onto.classes():
		if c.is_a[0] == owl.Thing:
			root_class_comments[c.name] = c.comment
	for c in forensics_onto.classes():
		if c.is_a[0] == owl.Thing:
			root_class_comments[c.name] = c.comment
	return json.dumps(root_class_comments)

@app.route("/getSubclasses", methods=['POST'])
def getSubclasses():
	data = request.get_json()
	print(data, file=sys.stdout)
	subclasses = dict()
	if network_onto[data['key']] != None:
		for c in network_onto[data['key']].subclasses():
			subclasses[c.name] = c.comment
	elif forensics_onto[data['key']] != None:
		for c in forensics_onto[data['key']].subclasses():
			subclasses[c.name] = c.comment
	elif network_forensics_onto[data['key']] != None:
		for c in network_forensics_onto[data['key']].subclasses():
			subclasses[c.name] = c.comment
	elif network_forensics_instance_onto[data['key']] != None:
		for c in network_forensics_instance_onto[data['key']].subclasses():
			subclasses[c.name] = c.comment
	return json.dumps(subclasses);

@app.route("/getSuperclass", methods=['POST'])
def getSuperclass():
	data = request.get_json()
	superclasses = dict()
	if network_onto[data['key']] != None:		
		for c in network_onto[data['key']].is_a[0].is_a[0].subclasses():
			superclasses[c.name] = c.comment
	elif forensics_onto[data['key']] != None:
		for c in forensics_onto[data['key']].is_a[0].is_a[0].subclasses():
			superclasses[c.name] = c.comment
	elif network_forensics_onto[data['key']] != None:
		for c in network_forensics_onto[data['key']].is_a[0].is_a[0].subclasses():
			superclasses[c.name] = c.comment
	elif network_forensics_instance_onto[data['key']] != None:
		for c in network_forensics_instance_onto[data['key']].is_a[0].is_a[0].subclasses():
			superclasses[c.name] = c.comment
	return json.dumps(superclasses);

@app.route("/getInstances", methods=['POST'])
def getInstances():
	data = request.get_json()
	instances = dict()
	if network_onto[data['key']] != None:		
		for c in network_onto[data['key']].instances():
			if c.is_a[0] == network_onto[data['key']]:
				instances[c.name] = c.comment
	elif forensics_onto[data['key']] != None:
		for c in forensics_onto[data['key']].instances():
			if c.is_a[0] == forensics_onto[data['key']]:
				instances[c.name] = c.comment
	elif network_forensics_onto[data['key']] != None:
		for c in network_forensics_onto[data['key']].instances():
			if c.is_a[0] == network_forensics_onto[data['key']]:
				instances[c.name] = c.comment
	elif network_forensics_instance_onto[data['key']] != None:
		for c in network_forensics_instance_onto[data['key']].instances():
			if c.is_a[0] == network_forensics_instance_onto[data['key']]:
				instances[c.name] = c.comment
	return json.dumps(instances);

@app.route("/addSubclass", methods=['POST'])
def addSubclass():
	data = request.get_json()
	if network_onto[data['key']] != None:
		with network_forensics_onto:
			NewClass = types.new_class(data['name'], (network_onto[data['key']],))
			NewClass.comment = data['comment']
	if forensics_onto[data['key']] != None:
		with network_forensics_onto:
			NewClass = types.new_class(data['name'], (forensics_onto[data['key']],))
			NewClass.comment = data['comment']
	if network_forensics_onto[data['key']] != None:
		with network_forensics_onto:
			NewClass = types.new_class(data['name'], (network_forensics_onto[data['key']],))
			NewClass.comment = data['comment']
	if network_forensics_instance_onto[data['key']] != None:
		with network_forensics_onto:
			NewClass = types.new_class(data['name'], (network_forensics_instance_onto[data['key']],))
			NewClass.comment = data['comment']
	network_forensics_onto.save("network-forensics-ontology/network_forensics.owl")
	subclasses = dict()
	if network_onto[data['key']] != None:
		for c in network_onto[data['key']].subclasses():
			subclasses[c.name] = c.comment
	elif forensics_onto[data['key']] != None:
		for c in forensics_onto[data['key']].subclasses():
			subclasses[c.name] = c.comment
	elif network_forensics_onto[data['key']] != None:
		for c in network_forensics_onto[data['key']].subclasses():
			subclasses[c.name] = c.comment
	elif network_forensics_instance_onto[data['key']] != None:
		for c in network_forensics_instance_onto[data['key']].subclasses():
			subclasses[c.name] = c.comment
	return json.dumps(subclasses);

@app.route("/deleteClass", methods=['POST'])
def deleteClass():
	data = request.get_json()
	if network_onto[data['key']] != None:
		superclass = network_onto[data['key']].is_a[0]
		destroy_entity(network_onto[data['key']])
	if forensics_onto[data['key']] != None:
		superclass = forensics_onto[data['key']].is_a[0]
		destroy_entity(forensics_onto[data['key']])
	if network_forensics_onto[data['key']] != None:
		superclass = network_forensics_onto[data['key']].is_a[0]
		destroy_entity(network_forensics_onto[data['key']])
	if network_forensics_instance_onto[data['key']] != None:
		superclass = network_forensics_instance_onto[data['key']].is_a[0]
		destroy_entity(network_forensics_instance_onto[data['key']])
	network_forensics_onto.save("network-forensics-ontology/network_forensics.owl")
	subclasses = dict()
	for c in superclass.subclasses():
		subclasses[c.name] = c.comment
	return json.dumps(subclasses);

@app.route("/getClass/<key>")
def getClass(key):
	retClass = dict()
	if network_onto[key] != None:
		retClass[network_onto[key].name] = network_onto[key].comment
	if forensics_onto[key] != None:
		retClass[forensics_onto[key].name] = forensics_onto[key].comment
	if network_forensics_onto[key] != None:
		retClass[network_forensics_onto[key].name] = network_forensics_onto[key].comment
	if network_forensics_instance_onto[key] != None:
		retClass[network_forensics_instance_onto[key].name] = network_forensics_instance_onto[key].comment
	return json.dumps(retClass);

@app.route("/modifyClass", methods=['POST'])
def modifyClass():
	data = request.get_json()
	if network_onto[data['key']] != None:
		network_onto[data['key']].comment = data['comment']
	if forensics_onto[data['key']] != None:
		forensics_onto[data['key']].comment = data['comment']
	if network_forensics_onto[data['key']] != None:
		network_forensics_onto[data['key']].comment = data['comment']
	if network_forensics_instance_onto[data['key']] != None:
		network_forensics_instance_onto[data['key']].comment = data['comment']
	network_forensics_onto.save("network-forensics-ontology/network_forensics.owl")
	subclasses = dict()
	if network_onto[data['key']] != None:
		for c in network_onto[data['key']].subclasses():
			subclasses[c.name] = c.comment
	elif forensics_onto[data['key']] != None:
		for c in forensics_onto[data['key']].subclasses():
			subclasses[c.name] = c.comment
	elif network_forensics_onto[data['key']] != None:
		for c in network_forensics_onto[data['key']].subclasses():
			subclasses[c.name] = c.comment
	elif network_forensics_instance_onto[data['key']] != None:
		for c in network_forensics_instance_onto[data['key']].subclasses():
			subclasses[c.name] = c.comment
	return json.dumps(subclasses);

@app.route("/addInstance", methods=['POST'])
def addInstance():
	data = request.get_json()
	if network_onto[data['key']] != None:
		with network_forensics_onto:
			NewInstance = network_onto[data['key']](data['name'])
			NewInstance.comment = data['comment']
	if forensics_onto[data['key']] != None:
		with network_forensics_onto:
			NewInstance = forensics_onto[data['key']](data['name'])
			NewInstance.comment = data['comment']
			print(NewInstance, file=sys.stdout)
	if network_forensics_onto[data['key']] != None:
		with network_forensics_onto:
			NewInstance = network_forensics_onto[data['key']](data['name'])
			NewInstance.comment = data['comment']
	if network_forensics_instance_onto[data['key']] != None:
		with network_forensics_onto:
			NewInstance = network_forensics_instance_onto[data['key']](data['name'])
			NewInstance.comment = data['comment']
	network_forensics_onto.save("network-forensics-ontology/network_forensics.owl")
	instances = dict()
	if network_onto[data['key']] != None:		
		for c in network_onto[data['key']].instances():
			if c.is_a[0] == network_onto[data['key']]:
				instances[c.name] = c.comment
	elif forensics_onto[data['key']] != None:
		for c in forensics_onto[data['key']].instances():
			if c.is_a[0] == forensics_onto[data['key']]:
				instances[c.name] = c.comment
	elif network_forensics_onto[data['key']] != None:
		for c in network_forensics_onto[data['key']].instances():
			if c.is_a[0] == network_forensics_onto[data['key']]:
				instances[c.name] = c.comment
	elif network_forensics_instance_onto[data['key']] != None:
		for c in network_forensics_instance_onto[data['key']].instances():
			if c.is_a[0] == network_forensics_instance_onto[data['key']]:
				instances[c.name] = c.comment
	return json.dumps(instances);

@app.route("/getRelations", methods=['POST'])
def gerRelations():
	query = """""";
	data = request.get_json()
	relations = dict()

	temp = {}
	if network_onto[data['key']] != None:
		temp = network_onto[data['key']]
	elif forensics_onto[data['key']] != None:
		temp = forensics_onto[data['key']]
	elif network_forensics_onto[data['key']] != None:
		temp = network_forensics_onto[data['key']]
	elif network_forensics_instance_onto[data['key']] != None:
		temp = network_forensics_instance_onto[data['key']]

	while temp.is_a[0] != owl.Thing:
		temp = temp.is_a[0]

	if network_onto[temp.name] != None:
		query = """PREFIX network: <https://raw.githubusercontent.com/micamat/network-forensics-ontology/main/network.owl#>
				SELECT ?relation ?range
				{ ?relation rdfs:domain network:""" + temp.name + """.
				?relation rdfs:range ?range}"""		
	elif forensics_onto[temp.name] != None:
		query = """PREFIX forensics: <https://raw.githubusercontent.com/micamat/network-forensics-ontology/main/forensics.owl#>
				SELECT ?relation ?range
				{ ?relation rdfs:domain forensics:""" + temp.name + """.
				?relation rdfs:range ?range}"""
	elif network_forensics_onto[temp.name] != None:
		query = """PREFIX network_forensics: <https://raw.githubusercontent.com/micamat/network-forensics-ontology/main/network-forensics.owl#>
				SELECT ?relation ?range
				{ ?relation rdfs:domain network_forensics:""" + temp.name + """.
				?relation rdfs:range ?range}"""
	elif network_forensics_instance_onto[temp.name] != None:
		query = """PREFIX network_forensics_instance: <https://raw.githubusercontent.com/micamat/network-forensics-ontology/main/network-forensics-instance.owl#>
				SELECT ?relation ?range
				{ ?relation rdfs:domain network_forensics_instance:""" + temp.name + """.
				?relation rdfs:range ?range}"""
	for i in list(graph.query_owlready(query)):
		relations[i[1].name] = i[1].comment
	return json.dumps(relations)

@app.route("/addDefinition", methods=['POST'])
def addDefinition():
	data = request.get_json()
	currentClass = data["currentClass"]
	definitionClass = data["definitionClass"]
	root_currentClass = {}
	root_definitionClass = {}
	prefix_currentClass = ""
	prefix_definitionClass = ""
	currentClassOwl = {}
	definitionClassOwl = {}

	if network_onto[currentClass] != None:
		root_currentClass = network_onto[currentClass]
		currentClassOwl = network_onto[currentClass]
	elif forensics_onto[currentClass] != None:
		root_currentClass = forensics_onto[currentClass]
		currentClassOwl = forensics_onto[currentClass]
	elif network_forensics_onto[currentClass] != None:
		root_currentClass = network_forensics_onto[currentClass]
		currentClassOwl = network_forensics_onto[currentClass]
	elif network_forensics_instance_onto[currentClass] != None:
		root_currentClass = network_forensics_instance_onto[currentClass]
		currentClassOwl = network_forensics_instance_onto[currentClass]

	while root_currentClass.is_a[0] != owl.Thing:
		root_currentClass = root_currentClass.is_a[0]

	if network_onto[definitionClass] != None:
		root_definitionClass = network_onto[definitionClass]
		definitionClassOwl = network_onto[definitionClass]
	elif forensics_onto[definitionClass] != None:
		root_definitionClass = forensics_onto[definitionClass]
		definitionClassOwl = forensics_onto[definitionClass]
	elif network_forensics_onto[definitionClass] != None:
		root_definitionClass = network_forensics_onto[definitionClass]
		definitionClassOwl = network_forensics_onto[definitionClass]
	elif network_forensics_instance_onto[definitionClass] != None:
		root_definitionClass = network_forensics_instance_onto[definitionClass]
		definitionClassOwl = network_forensics_instance_onto[definitionClass]

	while root_definitionClass.is_a[0] != owl.Thing:
		root_definitionClass = root_definitionClass.is_a[0]

	if network_onto[root_currentClass.name] != None:
		prefix_currentClass = "<https://raw.githubusercontent.com/micamat/network-forensics-ontology/main/network.owl#>"
	elif forensics_onto[root_currentClass.name] != None:
		prefix_currentClass = "<https://raw.githubusercontent.com/micamat/network-forensics-ontology/main/forensics.owl#>"
	elif network_forensics_onto[root_currentClass.name] != None:
		prefix_currentClass = "<https://raw.githubusercontent.com/micamat/network-forensics-ontology/main/network-forensics.owl#>"
	elif network_forensics_instance_onto[root_currentClass.name] != None:
		prefix_currentClass = "<https://raw.githubusercontent.com/micamat/network-forensics-ontology/main/network-forensics-instance.owl#>"

	if network_onto[root_definitionClass.name] != None:
		prefix_definitionClass = "<https://raw.githubusercontent.com/micamat/network-forensics-ontology/main/network.owl#>"
	elif forensics_onto[root_definitionClass.name] != None:
		prefix_definitionClass = "<https://raw.githubusercontent.com/micamat/network-forensics-ontology/main/forensics.owl#>"
	elif network_forensics_onto[root_definitionClass.name] != None:
		prefix_definitionClass = "<https://raw.githubusercontent.com/micamat/network-forensics-ontology/main/network-forensics.owl#>"
	elif network_forensics_instance_onto[root_definitionClass.name] != None:
		prefix_definitionClass = "<https://raw.githubusercontent.com/micamat/network-forensics-ontology/main/network-forensics-instance.owl#>"

	query = """PREFIX current:""" + prefix_currentClass + """PREFIX definition:""" + prefix_definitionClass + """SELECT ?property
			{?property rdfs:domain current:""" + root_currentClass.name + """.
			 ?property rdfs:range definition:""" + root_definitionClass.name + """}"""
	relation = list(graph.query_owlready(query))[0][0]

	currentClassOwl.equivalent_to.append(relation.some(definitionClassOwl))
	network_forensics_onto.save("network-forensics-ontology/network_forensics.owl")
	network_onto.save("network-forensics-ontology/network.owl")
	forensics_onto.save("network-forensics-ontology/forensics.owl")

	print(currentClassOwl.equivalent_to, file=sys.stdout)
	return ""

@app.route("/getLayerInstances")
def getLayerInstances():
	instances = []
	for i in onto.search(subclass_of = nsn.ComputerNetworkModel):
		if(len(onto.search(type = i)) > 0):
			for j in onto.search(type = i):
				instances.append(j.name)
	return json.dumps(list(dict.fromkeys(instances)))
	
@app.route("/getToolInstances")
def getToolInstances():
	instances = []
	for i in onto.search(subclass_of = nsf.Tool):
		if(len(onto.search(type = i)) > 0):
			for j in onto.search(type = i):
				instances.append(j.name)
	return json.dumps(list(dict.fromkeys(instances)))
	
@app.route("/postToolAndLayer", methods=['POST'])
def postToolAndLayer():
	data = request.get_json()
	instance1 = nsf.InvestigationMethod("instance1")
	nsf.instance1.appliesTo.append(nsi[data[0]])
	nsf.instance1.performedBy.append(nsi[data[1]])
	sync_reasoner()
	instance2 = nsf.EvidenceAdmissibility("instance2")
	nsf.instance2.reduces.append(nsf.instance1)
	nsf.instance2.guides.append(nsi[data[1]])
	sync_reasoner()
	steps = [i.name for i in onto.search(type = nsf.instance2.is_a) if i.name != nsf.instance2.name]
	return json.dumps(steps)
	

if __name__=="__main__":
	app.run()
