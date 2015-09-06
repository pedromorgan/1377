# -*- coding: utf-8 -*-


import os
import yaml
import glob

from fabric.api import env, local, run, lcd, cd, sudo
import mistune
from bs4 import BeautifulSoup

ROOT_PATH = os.path.abspath( os.path.dirname(__file__) )

def _get_dirs():
	files = glob.glob( ROOT_PATH + '/[0-9]')
	#print files
	ret = []
	for f in files:
		ret.append( f.replace(".", "")[len(ROOT_PATH):] )
	return sorted(ret)		 

def _get_md_files(path):
	xpath = "%s%s" % (ROOT_PATH, path)
	files = glob.glob( "%s/*.md" % (xpath) )
	ret = []
	for f in files:
		if f.split("/")[-1] == "README.md":
			pass
		else:
			ret.append( f[len(ROOT_PATH):] )
	return sorted(ret)		 

def _read_file(fp):
	with open(fp, "r") as f:
		return f.read()

def _write_yaml(fp, dic):
	with open(fp, "w") as f:
		f.write( yaml.dump(dic) )
		f.close()

def index():
	
	
	dirs = _get_dirs()
	print dirs
	for d in dirs:
		files = _get_md_files(d)
		#print d, files
		print "==========", ROOT_PATH + d + "/README.md"
		txt =  _read_file(ROOT_PATH + d + "/README.md")
		html = mistune.markdown(txt)
		soup = BeautifulSoup(html)
		
		dic = {}
		dic['part_title'] = str(soup.find("h1").text).strip()
		dic['sections'] = []

		
		idx = []
		for f in files:
			print f
			txt =  _read_file(ROOT_PATH + f)
			html = mistune.markdown(txt)
			#print html
			soup = BeautifulSoup(html)
			print "------------------------------"
			title =  str(soup.find("h1").text).strip()
			toc = []
			for h2 in soup.findAll("h2"):
				toc.append( dict(title=str(h2.text).strip()) ) 
			print title, toc
			#'toc.append( dict(file=f, title=title, toc=toc) )
			fff =  f[len(ROOT_PATH):]
			idx.append( dict(title=title, clauses=toc, file=fff) )
		dic['sections'].append(idx)
		_write_yaml("%s/%s/index.yaml" % (ROOT_PATH, d), idx)
		print idx
		break
	
		