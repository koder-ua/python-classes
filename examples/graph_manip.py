#!/usr/bin/env python

import os
import sys
import glob
import os.path
from xml.etree.ElementTree import fromstring, tostring

def process(fc):
	root = fromstring(fc)
	ns = "{http://www.yworks.com/xml/graphml}"

	new_node_code = \
	"""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
	<graphml xmlns="http://graphml.graphdrawing.org/xmlns" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:y="http://www.yworks.com/xml/graphml" xmlns:yed="http://www.yworks.com/xml/yed/3" xsi:schemaLocation="http://graphml.graphdrawing.org/xmlns http://www.yworks.com/xml/schema/graphml/1.1/ygraphml.xsd">
		<y:StyleProperties>
		    <y:Property class="com.yworks.yfiles.bpmn.view.TaskTypeEnum" name="com.yworks.bpmn.taskType" value="TASK_TYPE_ABSTRACT"/>
		    <y:Property class="com.yworks.yfiles.bpmn.view.ActivityTypeEnum" name="com.yworks.bpmn.activityType" value="ACTIVITY_TYPE_TASK"/>
		    <y:Property class="java.awt.Color" name="com.yworks.bpmn.icon.fill2" value="#d4d4d4"/>
		    <y:Property class="java.awt.Color" name="com.yworks.bpmn.icon.fill" value="#ffffff"/>
		    <y:Property class="com.yworks.yfiles.bpmn.view.BPMNTypeEnum" name="com.yworks.bpmn.type" value="ACTIVITY_TYPE"/>
		    <y:Property class="java.awt.Color" name="com.yworks.bpmn.icon.line.color" value="#000000"/>
		</y:StyleProperties>
	</graphml>
	"""
	new_node = fromstring(new_node_code).find("{}StyleProperties".format(ns))

	for node in root.findall('.//{}ShapeNode'.format(ns)):
		node.tag = "{}GenericNode".format(ns)
		node.attrib['configuration'] = "com.yworks.bpmn.Activity.withShadow"

		color = node.find("{}Fill".format(ns))
		del color.attrib['color']
		color.attrib['color1'] = "#FFFFFFE6"
		color.attrib['color2'] = "#D4D4D4CC"
		del color

		node.find("{}BorderStyle".format(ns)).attrib['color'] = '#123EA2'
		node.remove(node.find("{}Shape".format(ns)))

		node.append(new_node)

	return tostring(root, "UTF-8")

for fname in glob.glob("/home/koder/Dropbox/python-classes/slides/images/*.graphml"):
	fc = open(fname).read()
	res = process(fc)
	open(os.path.join('/home/koder/Dropbox/python-classes/slides/images/new', os.path.basename(fname)), "w").write(res)







