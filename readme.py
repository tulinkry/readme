#!/usr/bin/python

## README
#
# Script for making automated readme files
# With as less as possible effort you can create a readme file
# of your source code
#
#	USAGE:
#		Script reads input given in <n> files and creates a readme files for them
#		[[c]]Usage: ./readme.py [options] <file1> [file2, file3, ...][[/c]]
#		ARGUMENTS:
#			without [[c]]-d[[/c]] and with more than one files given
#			will every file overwrite the previous readme
#			so the result will be only readme file of the last one
#		OPTIONS:
#			[[c]]-d[[/c]]
#			running with -d on script named "script.sh" will produce
#			a new directory "script" and place a readme file there
#			also a copy of a script will be present in that directory
#			[[c]]--cpp|--bash|--windows|--assembler[[/c]]
#			is for selecting a comment style used in your source code
#			if none of those is given, script will try to guess the comment
#			style himself
#			[[c]]--html|--txt[[/c]]
#			output formats, the produced file will be named as
#			[[c]]README.<format>[[/c]]
#			EXAMPLES:
#				[[c]]./readme.py -d script.py[[/c]]
#				[[c]]./readme.py --txt --cpp CArray.cpp[[/c]]
#
#	README FORMAT:
#		Writing a readme in your scripts is quite easy
#		BASIC:
#			For correct work of readme parser you need to do following:
#			- readme comment needs to be in format specific for 
#			programming language and after the first comment there has to 
#			be a "README" word.
#			[[c]]/** README[[/c]] or [[c]]## README[[/c]] or
#			[[c]];; README[[/c]] or [[c]]:: README[[/c]]
#			no rules aplies for the end comment
#		SECTIONS:
#			For using sections it is neccessary to keep a right indentation level of sections
#			Traditional format for section name is [[c]][a-zA-Z0-9]+:[[/c]]
#			EXAMPLE:
#				|[[c]]USAGE:[[/c]]
#				|	|[[c]]This text will be visible in section usage[[/c]]
#				|	|[[c]]EXAMPLES:[[/c]]
#				|	|	|[[c]]This text will be visible in section examples[[/c]]
#				|	|[[c]]ANOTHER:[[/c]]
#				|	|	|[[c]]Another text in other section[[/c]]
#		ANNOTATIONS:
#			For using annotations are defined some rules:
#			- keep the indentations right
#			- every annotation starts with @
#			- annotations can be also attached to sections, just keep the indentation
#			EXAMPLE:
#				This will be visible in annotations
#				[[c]]@author Jan novák[[/c]]
#				[[c]]@year 2014[[/c]]
#
# @author Kryštof Tulinger
# @year 2014
# @place Norway

import codecs
import sys
import os
import re
import getopt
import html

class Template:
	def __init__ ( self, options = {} ):
		self . _output = options [ "output" ] if "output" in options . keys () else None
		self . _filename = options [ "filename" ] if "filename" in options . keys () else "README.txt"
	def open ( self, f ):
		self . __del__ ()
		if f == None:
			self . solveCollisions ( self . _filename )
			self . _output = codecs . open ( self . _filename, "w", encoding = "utf-8" )
		elif isinstance ( f, type( str () ) ):
			self . solveCollisions ( f )
			self . _output = codecs . open ( f, "w", encoding = "utf-8" )
		return self . _output
	def __del__ ( self ):
		if self . _output:
			if hasattr ( self . _output, "closed" ) and not self . _output . closed:
				self . _output . close ()

	def solveCollisions ( self, filename ):
		if os . path . isfile ( filename ):
			try:
				os . remove ( filename + "~" )
			except:
				pass
			finally:
				os . rename ( filename, filename + "~" )		

	def render ( self, readmes, filename = None ):
		pass


class TXTTemplate ( Template ):
	def __init__ ( self, options = {} ):
		Template . __init__ ( self, options )
	def tocSection ( self, section, index = [ 1 ] ):
		section_template = self . tocSectionTemplate ()
		subsections_template = self . tocSubsectionTemplate ()
		subsections = ""
		if section . subsections ():
			for i, s in enumerate ( section . subsections () ):
				subsections = subsections + subsections_template % { "section": self . tocSection ( s, list ( index + [ i + 1 ] ) ) }
			
		return section_template % { "name": section . name (), 
						   			"number": section . id ( index, "." ), 
						   			"subsections": subsections }	

	def renderSection ( self, section, index = [ 1 ] ):
		section_template = self . sectionTemplate ()
		annotations_template = self . annotationsTemplate ()
		annotation_line = self . annotationLineTemplate ()
		text_template = self . textTemplate ()
		line_template = self . lineTemplate ()
		content_template = self . contentTemplate ()
		content_part_template = self . contentPartTemplate ()

		text = ""
		for line in section . text ():
			text = text + line_template % { "line": line }

		text = text_template % { "text": text } if text else ""

		content = ""
		for i, s in enumerate ( section . subsections () ):
			content = content + content_part_template % { "content_part": self . renderSection ( s, list ( index + [ i + 1 ] ) ) } #list ( index + [ i + 1 ] ) )
		content = content_template % { "content": content } if content else ""

		annotation_lines = ""
		for all in section . annotations ():
			for key in all . keys ():
				annotation_lines = annotation_lines + annotation_line % { "key" : key [0] . upper () + key [ 1:],
																		  "value" : all [ key ] }
		annotations = annotations_template % { "heading": "",
											   "annotations": annotation_lines } if annotation_lines else ""


		return section_template % { "number" : section . id ( index, "." ),  
 								    "name" : str ( section . name () ), 
 								    "text": text,
 								    "content": content,
 								    "annotations": annotations }
	def render ( self, readmes, filename = None ):
		sections_template = self . sectionsTemplate ()
		annotations_template = self . annotationsTemplate ()
		annotation_line = self . annotationLineTemplate ()
		table_of_contents_template = self . tocTemplate ()
		text_template = self . textTemplate ()
		line_template = self . lineTemplate ()
		html = self . pageTemplate ()

		header = ""
		table_of_contents = ""
		view = ""
		annotations = ""
		annotation_lines = ""
		name = ""

		for readme in readmes:
			for i, section in enumerate ( readme . sections () ):
				table_of_contents = table_of_contents + self . tocSection ( section, [ i + 1 ] )
				view = view + self . renderSection ( section, [ i + 1 ] )

			t = ""
			for line in readme . text ():
				t = t + line_template % { "line": line }
			header = header + text_template % { "text": t }

			a = ""
			for ann in readme . annotations ():
				for key in ann . keys ():
					a = a + annotation_line % { "key": key [ 0 ] . upper () + key [ 1: ],
												"value": ann [ key ] }

			annotations = annotations + annotations_template % { "id": "annotations",
																 "heading": "Annotations",
																 "annotations": a }
			name = readme . name ()

		table_of_contents = table_of_contents_template % { "table_of_content": table_of_contents }
		view = sections_template % { "sections" : view } if view else ""

		view = re . sub ( "\[\[(c|code)\]\]", "", view )
		view = re . sub ( "\[\[/(c|code)\]\]", "", view )
	
		with self . open ( filename ) as outputFile:
			
			substitute = html % { "name": name,
								  "table_of_contents" : table_of_contents,
								  "header" : header, 
								  "content": view, 
								  "annotations" : annotations }
			outputFile . write ( substitute )

	def sectionsTemplate ( self ):
		sections_template = """%(sections)s"""
		return sections_template
	def sectionTemplate ( self ):
		section_template = """%(number)s %(name)s\n%(annotations)s\n%(text)s\n%(content)s"""
		return section_template
	def annotationsTemplate ( self ):
		annotations_template = """%(heading)s\n%(annotations)s"""		
		return annotations_template
	def annotationLineTemplate ( self ):
		annotation_line = """%(key)s: %(value)s\n"""
		return annotation_line
	def textTemplate ( self ):
		text_template = """%(text)s"""
		return text_template
	def lineTemplate ( self ):
		line_template = """%(line)s\n"""
		return line_template
	def contentTemplate ( self ):
		content_template = """%(content)s"""	
		return content_template
	def contentPartTemplate ( self ):
		content_part_template = """%(content_part)s\n"""	
		return content_part_template
	def tocTemplate ( self ):
		return """%(table_of_content)s"""
	def tocSectionTemplate ( self ):
		section = """%(number)s %(name)s\n%(subsections)s"""
		return section
	def tocSubsectionTemplate ( self ):
		subsections_template = """%(section)s"""
		return subsections_template
	def pageTemplate ( self ):
		page_template = """README %(name)s\n\n%(header)s\n\n%(table_of_contents)s\n\n%(content)s\n%(annotations)s\n\nThis readme file was automaticaly generated by \"readme.py\" script from the original file."""
		return page_template

class HTMLTemplate ( Template ):
	def __init__ ( self, options = {} ):
		Template . __init__ ( self, options )
		self . _filename = "README.html"
	def tocSection ( self, section, index = [ 1 ] ):
		section_template = self . tocSectionTemplate ()
		subsections_template = self . tocSubsectionTemplate ()
		subsections = ""
		if section . subsections ():
			for i, s in enumerate ( section . subsections () ):
				subsections = subsections + subsections_template % { "section": self . tocSection ( s, list ( index + [ i + 1 ] ) ) }
			
		return section_template % { "id": section . id ( index ), 
							   		"name": section . name (), 
						   			"number": section . id ( index, ". " ), 
						   			"subsections": subsections }	

	def renderSection ( self, section, index = [ 1 ] ):
		section_template = self . sectionTemplate ()
		annotations_template = self . annotationsTemplate ()
		annotation_line = self . annotationLineTemplate ()
		text_template = self . textTemplate ()
		line_template = self . lineTemplate ()
		content_template = self . contentTemplate ()
		content_part_template = self . contentPartTemplate ()

		text = ""
		for line in section . text ():
			text = text + line_template % { "line": html.escape ( line ) }

		text = text_template % { "text": text } if text else ""

		content = ""
		for i, s in enumerate ( section . subsections () ):
			content = content + content_part_template % { "content_part": self . renderSection ( s, list ( index + [ i + 1 ] ) ) } #list ( index + [ i + 1 ] ) )
		content = content_template % { "content": content } if content else ""

		annotation_lines = ""
		for all in section . annotations ():
			for key in all . keys ():
				annotation_lines = annotation_lines + annotation_line % { "key" : key [0] . upper () + key [ 1:],
																		  "value" : all [ key ] }
		annotations = annotations_template % { "heading": "Annotations",
											   "id": None,
											   "annotations": annotation_lines } if annotation_lines else ""


		return section_template % { "id" : section . id ( index ), 
 								    "number" : section . id ( index, ". " ),  
 								    "name" : str ( section . name () ), 
 								    "text": text,
 								    "content": content,
 								    "annotations": annotations }

	def render ( self, readmes, filename = None ):

		sections_template = self . sectionsTemplate ()
		annotations_template = self . annotationsTemplate ()
		annotation_line = self . annotationLineTemplate ()
		table_of_contents_template = self . tocTemplate ()
		text_template = self . textTemplate ()
		line_template = self . lineTemplate ()
		html = self . pageTemplate ()

		header = ""
		table_of_contents = ""
		view = ""
		annotations = ""
		annotation_lines = ""
		name = ""

		for readme in readmes:
			for i, section in enumerate ( readme . sections () ):
				table_of_contents = table_of_contents + self . tocSection ( section, [ i + 1 ] )
				view = view + self . renderSection ( section, [ i + 1 ] )

			t = ""
			for line in readme . text ():
				t = t + line_template % { "line": line }
			header = header + text_template % { "text": t }

			a = ""
			for ann in readme . annotations ():
				for key in ann . keys ():
					a = a + annotation_line % { "key": key [ 0 ] . upper () + key [ 1: ],
												"value": ann [ key ] }

			annotations = annotations + annotations_template % { "id": "annotations",
																 "heading": "<h3>Annotations</h3>",
																 "annotations": a }
			name = readme . name ()

		table_of_contents = table_of_contents_template % { "table_of_content": table_of_contents }
		view = sections_template % { "sections" : view } if view else ""

		view = re . sub ( "(?P<begin>\[\[(c|code)\]\])(?P<content>.*?)(?P<end>\[\[/(c|code)\]\])", lambda x: "<code>" + x . group ( "content" ) + "</code>", view )

		with self . open ( filename ) as outputFile:
			
			substitute = html % { "name": name,
								  "table_of_contents" : table_of_contents,
								  "header" : header, 
								  "content": view, 
								  "annotations" : annotations }

			outputFile . write ( substitute )


	def sectionTemplate ( self ):
		section_template = """
			<div class=\"panel panel-default\" id=\"%(id)s\">
				<div class="panel-heading">
					<h4>%(number)s %(name)s</h4>
				</div>
				<div class="panel-body">
					%(text)s
					%(content)s
					%(annotations)s
				</div>
			</div>
		"""
		return section_template
	def sectionsTemplate ( self ):
		sections_template = """%(sections)s
		"""
		return sections_template
	def annotationsTemplate ( self ):
		annotations_template = """
			<div class=\"panel panel-default\" id="%(id)s">
				<div class="panel-heading">
					%(heading)s
				</div>
				<div class="panel-body">
					<dl class="dl-horizontal">%(annotations)s</dl>
				</div>
			</div>
		"""		
		return annotations_template
	def annotationLineTemplate ( self ):
		annotation_line = """
			<dt>%(key)s</dt>
			<dd>%(value)s</dt>
		"""
		return annotation_line
	def textTemplate ( self ):
		text_template = """
		<p>%(text)s</p>
		"""
		return text_template
	def lineTemplate ( self ):
		line_template = """
		%(line)s<br />
		"""
		return line_template
	def contentTemplate ( self ):
		content_template = """
		%(content)s
		"""	
		return content_template
	def contentPartTemplate ( self ):
		content_part_template = """
		%(content_part)s
		"""	
		return content_part_template
	def tocTemplate ( self ):
		return """<ol class=\"nav list-group\">%(table_of_content)s</ol>"""

	def tocSectionTemplate ( self ):
		section = """<li class=\"nav list-group-item\"><a href="#%(id)s" title="Section %(number)s">%(number)s %(name)s</a>%(subsections)s</li>\n"""
		return section

	def tocSubsectionTemplate ( self ):
		subsections_template = """<ol class=\"nav\">%(section)s</ol>"""
		return subsections_template

	def pageTemplate ( self ):

		page_template = """
		<!DOCTYPE html>
		<html>
		<head>
			<meta charset="utf-8">
			<title>%(name)s</title>
			<style>
				body {
				  padding-top: 50px;
				}
				.starter-template {
				  padding: 40px 15px;
				  text-align: left;
				}

			</style>
			<link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css" rel="stylesheet">
			<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/js/bootstrap.min.js"></script>
		</head>
		<body>
    <div class="navbar navbar-inverse navbar-fixed-top" role="navigation">
      <div class="container">
        <div class="navbar-header">
          <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target=".navbar-collapse">
            <span class="sr-only">Toggle navigation</span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <a class="navbar-brand" href="#">%(name)s</a>
        </div>
        <div class="collapse navbar-collapse">
          <ul class="nav navbar-nav">
            <li><a href="#description">Description</a></li>
            <li><a href="#toc">Table of content</a></li>
            <li><a href="#content">Content</a></li>
            <li><a href="#annotations">Annotations</a></li>
          </ul>
        </div><!--/.nav-collapse -->
      </div>
    </div>

    <div class="container">

      <div class="starter-template">
		<h1>README %(name)s</h1>
			<div class="page">
				<div class="content">
					<div class="panel panel-default" id="description">
						<div class="panel-heading">
							<h3>Description</h3>
						</div>
						<div class="panel-body">
							<span class="lead">
								%(header)s
							</span>
						</div>
					</div>				

					<hr />
					<div class="panel panel-default" id="toc">
						<div class="panel-heading">
							<h3>Table of content</h3>
						</div>
						<div class="panel-body">
						%(table_of_contents)s
						</div>
					</div>
					<hr />
					<div class="panel panel-default" id="content">
						<div class="panel-heading">
							<h3>Content</h3>
						</div>
						<div class="panel-body">
						%(content)s
						</div>
					</div>
					<hr />
					%(annotations)s
				</div>
				<div class="well">
					This readme file was automaticaly generated by \"readme.py\" script from the original file.
				</div>
			</div>        
      </div>

    </div><!-- /.container -->


    <!-- Bootstrap core JavaScript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
    <script src="../../dist/js/bootstrap.min.js"></script>
    <!-- IE10 viewport hack for Surface/desktop Windows 8 bug -->
    <script src="../../assets/js/ie10-viewport-bug-workaround.js"></script>		
		</body>
		</html>
		"""

		return page_template




class Comment:
	def __init__ ( self, options = {} ):
		self . _readme_comment_begin = options [ "readme_comment_begin" ] if "readme_comment_begin" in options . keys () else "## [rR][eE][aA][dD][mM][eE]"
		self . _readme_comment_end = options [ "readme_comment_end" ] if "readme_comment_end" in options . keys () else ""
		self . _comment = options [ "comment" ] if "comment" in options . keys () else "(#|[" + self . blank () + "]*#)"
		self . _separate_lines = options [ "separate_lines" ] if "separate_lines" in options . keys () else "([" + self . blank () + "]*[-]+[" + self . blank () + "]*$|[" + self . blank () + "]*[#]+[" + self . blank () + "]*$|[" + self . blank () + "]*[*]+[" + self . blank () + "]*$|[" + self . blank () + "]*[_]+[" + self . blank () + "]*$|[" + self . blank () + "]*[+]+[" + self . blank () + "]*$)"
		self . _section = options [ "section" ] if "section" in options . keys () else "[a-zA-Z0-9]+:"

	def begin ( self ):
		return self . _readme_comment_begin
	def end ( self ):
		return self . _readme_comment_end
	def comment ( self ):
		return self . _comment
	def blankLine ( self ):
		return self . _separate_lines
	def blank ( self ):
		return " "
	def section ( self ):
		return self . _section

class Section:
	def __init__ ( self, string, depth, comment ):

		self . _depth = depth

		self . _lines = []
		self . _annotations = []
		self . _sections = []


		self . _comment = comment

		s = string . split ( "\n" )
		name = s [ 0 ] . strip ()
		if self . _comment . comment ():
			name = re . sub ( self . _comment . comment (), "", name ) . strip ()
			#name = name . split ( self . _comment . comment () ) [ 1 ]
		name = name [ :-1] if name [ -1 ] == ":" else name
		self . _name = name


		string = "\n".join ( s [ 1: ] )

		#print ( "----- section ------" )
		#print ( string )


		string = re . sub ( "(?m)^[ ]{0,4}", "", string )

		#print ( "----- section modified ------" )
		#print ( string )

		#print ( "----- section updated ------" )
		#print ( string )

		self . subsections ( string )
		self . text ( string )
		self . annotations ( string )

	def name ( self ):
		return self . _name

	def subsections ( self, string = None ):
		if not string:
			return self . _sections

		pattern = "(?m)^" + self . _comment . section () + "[" + self . _comment . blank () + "]*[\n](^[ ]{1,}.*[\n])*"
		sections = re . finditer ( pattern, string )
		for section in sections:
			section = section . group ()
			self . _sections . append ( Section ( section, self . _depth + 1, self . _comment ) )
		return self . _sections
	def text ( self, string = None ):
		if not string:
			return self . _lines
		pattern = "(?m)^(?!" + self . _comment . section () + ")[^@\s][^A-Z].*"
		text = re . finditer ( pattern, string )
		for t in text:
			t = t . group ()
			for line in t . split ( "\n" ):
				line = line . strip ()
				if not re . match ( self . _comment . blankLine (), line ):
					self . _lines . append ( line )
		return self . _lines

	def annotations ( self, string = None ):
		if not string:
			return self . _annotations
		
		ann = re . finditer ( "(?m)^@[a-zA-Z0-9]+[" + self . _comment . blank () + "].*", string )

		for annotation in ann:
			if re . match ( "(?m)^@[a-zA-Z0-9]+[" + self . _comment . blank () + "]+.*?", annotation . group () ):
				key = re . sub ( "(?m)^@(?P<key>[a-zA-Z0-9]+).*", lambda m: m . group ("key"), annotation.group() )
				val = re . sub ( "(?m)^@[a-zA-Z0-9]+[" + self . _comment . blank () + "]+(?P<val>.*?)", lambda m: m . group ("val"), annotation.group() )
				self . _annotations . append ( { key: val } )
		return self . _annotations


	def id ( self, index = [], separator = "-" ):
		return separator . join ( str (val) for val in index )


class Readme:
	def __init__ ( self, name, string, comment, delimiter = " " ):

		self . _comment = comment
		self . _name = name
		self . _delimiter = delimiter

		self . _lines = []
		self . _section = []
		self . _annotations = []

		#print ( "------------- readme -------------- " )
		#print ( string )

		string = re . sub ( "(?m)^" + re . escape ( delimiter ), "", string )

		#print ( "------------- readme modified -------------- " )
		#print ( string )


		self . text ( string )
		self . sections ( string )
		self . annotations ( string )

	def name ( self ):
		return self . _name

	def sections ( self, string = None ):
		if not string:
			return self . _section
		s = []
		# untext
		string = re . sub ( "(?m)^[@][^A-Z0-9].*", "", string )
		string = re . sub ( "(?m)^(?!" + self . _comment . section () + ")[^@\s][^A-Z].*", "", string )
		pattern = "(?m)^" + self . _comment . section () + "([\n]|.)*?(?=^" + self . _comment . section () + "|\Z)"
		#pattern = "[^\s]*.*\n(?:\s+.*\n*)*"
		sections = re . finditer ( pattern, string )
		for section in sections:
			section = section . group ()
			s . append ( Section ( section, 1, self . _comment ) )
		self . _section = list ( self . _section + s )
		return s

	def annotations ( self, string = None ):
		if not string:
			return self . _annotations
		annotations = []
		ann = re . finditer ( "(?m)^@[a-zA-Z0-9]+[" + self . _comment . blank () + "].*", string )
		for annotation in ann:
			if re . match ( "(?m)^@[a-zA-Z0-9]+[" + self . _comment . blank () + "]+.*?", annotation . group () ):
				key = re . sub ( "(?m)^@(?P<key>[a-zA-Z0-9]+).*", lambda m: m . group ("key"), annotation.group() )
				val = re . sub ( "(?m)^@[a-zA-Z0-9]+[" + self . _comment . blank () + "]+(?P<val>.*?)", lambda m: m . group ("val"), annotation.group() )
				annotations . append ( { key: val } )
		self . _annotations = annotations
		return annotations

	def text ( self, string = None ):
		if not string:
			return self . _lines
		pattern = "(?m)^(?!" + self . _comment . section () + ")[^@\s][^A-Z].*"
		text = re . finditer ( pattern, string )
		lines = []
		for t in text:
			t = t . group ()
			for line in t . split ( "\n" ):
				line = line . strip ()
				if not re . match ( self . _comment . blankLine (), line ):
					lines . append ( line )
		self . _lines = list ( self . _lines + lines )
		return lines

class Readme1:
	def __init__ ( self, options = {} ):

		self . _comment = options [ "comment" ] if "comment" in options . keys () else Comment ()
		self . _template = options [ "template" ] if "template" in options . keys () else HTMLTemplate ()
		self . _options = options

		self . _readmes = []



	def readme ( self, filename ):
		self . _readmes = []
		with codecs . open ( filename, "r", encoding = "utf-8" ) as inputFile:
			content = inputFile . read ()
			content = re . sub ( "\r", "\n", content )
			content = re . sub ( "\n\n", "\n", content )
			#content = re . sub ( "\t", "    ", content )
			#print ( re . sub ( "\t", "    ", content ) )
			
			if self . _comment . end ():
				#/\*\* README[\n](.*[\n])*[ \t]*\*/
				pattern = "" + self . _comment . begin () + "[\n](.*[\n])*" + self . _comment . blank () + "*" + self . _comment . end ()
			else:
				pattern = "" + self . _comment . begin () + "[\n](" + self . _comment . comment () + ".*|" + self . _comment . comment () + "*[\n])*"
			#print ( pattern )
			readmes = re . finditer ( pattern, content )
			readmes = list ( readmes )
			if len ( readmes ) <= 0:
				"""error"""
				readmes = self . suggest ( content )
				#print ( "No readme was found. Trying guess ..." )

			if len ( readmes ) <= 0:
				raise Exception ( "Fatal error. No readme found." )


			x = 0
			for readme in readmes:
				readme = readme . group ()
				readme = re . sub ( self . _comment . begin () + "\s", "", readme )
				if self . _comment . end ():
					readme = re . sub ( "\s" + self . _comment . end (), "", readme )

				
				readme = re . sub ( "(?m)^" + self . _comment . comment (), "", readme )
				#readme = re . sub ( "(?m)^\t", "\t\t", readme )
				c = self . _comment . comment ()
				readme = re . sub ( "(?m)^(?P<s>[ ]+)", lambda x: "\t" * ( int ( len ( x . group ( "s" ) ) / 4 ) + 1 ), readme )
				readme = readme . expandtabs (4)


				x = re . finditer ( "(?m)^([ ]+?)(?=[^ ])", readme )
				delimiter = list ( x )
				if len ( delimiter ) <= 0:
					delimiter = " "
				else:
					delimiter =  delimiter[ 0 ] . group ( 1 )



				self . _readmes . append ( Readme ( filename, readme, self . _comment, delimiter ) )

		self . _template . render ( self . _readmes )




	def suggest ( self, content ):
		comments = []
		options = { "readme_comment_begin": "/\*\* README",
					"readme_comment_end": "\*/",
					"comment": "(^[ \t]*\*)" }
		comments . append ( Comment ( options ) ) # cpp
		comments . append ( Comment () ) # bash
		options = { "readme_comment_begin": ";; README",
					"comment": "(;|[ \t]*;)" }
		comments . append ( Comment ( options ) ) # assember
		options = { "readme_comment_begin": ":: README",
					"comment": "(::|[ \t]*::)" }
		comments . append ( Comment ( options ) ) # windows

		for comment in comments:
			if comment . end ():
				#/\*\* README[\n](.*[\n])*[ \t]*\*/
				pattern = "" + comment . begin () + "[\n](.*[\n])*" + comment . blank () + "*" + comment . end ()
			else:
				pattern = "" + comment . begin () + "[\n](" + comment . comment () + ".*|" + comment . comment () + "*[\n])*"
			readmes = re . finditer ( pattern, content )
			readmes = list ( readmes )
			if len ( readmes ) > 0:
				self . _comment = comment
				return readmes
		return []



def main ( argv = None ):

	def cp(source, dest, buffer_size=1024*1024):
	    """
	    Copy a file from source to dest. source and dest
	    can either be strings or any object with a read or
	    write method, like StringIO for example.
	    """
	    if not hasattr(source, 'read'):
	        source = open(source, 'rb')
	    if not hasattr(dest, 'write'):
	        dest = open(dest, 'wb')

	    while 1:
	        copy_buffer = source.read(buffer_size)
	        if copy_buffer:
	            dest.write(copy_buffer)
	        else:
	            break

	    source.close()
	    dest.close()

	def usage ():
		print ( "Usage: " + sys.argv[0] + " [options]" )
		print ( "" )
		print ( "Options:" )
		print ( "	-h		show this help message and exit" )
		print ( "	-o <filename>	set the output file, \"-\" stands for stdout" )
		print ( "	-d		program will create a subdirectory and place readme and copy of the script there" )
		print ( "	--cpp		style of comments" )
		print ( "	--bash		style of comments" )
		print ( "	--assember	style of comments" )
		print ( "	--windows	style of comments" )
		print ( "	--html		output format" )
		print ( "	--txt		output format" )
		print ( "" )
		print ( "Examples:" )
		print ( "	script.py --input ..\\languages\\nowiki\\ -t 8 --merge -c 500 -l nn" )
		print ( "	script.py --input ..\\languages\\nowiki\\nn.links.txt.00000000.txt -t 8 --merge --delete-after-merge -c 20 -l nn" )


	if not argv:
		argv = sys . argv

	options = {}
	directories = False
	output_file = None

	comments = {}
	comments [ "cpp" ] = Comment ( { "readme_comment_begin": "/\*\* [rR][eE][aA][dD][mM][eE]",
							  "readme_comment_end": "\*/",
							  "comment": "(^[ \t]*\*)" } )
	comments [ "bash" ] = Comment ()
	comments [ "windows"] = Comment ( { "readme_comment_begin": ";; [rR][eE][aA][dD][mM][eE]",
								 "comment": "(;|[ \t]*;)" } )
	comments [ "assember" ] = Comment ( { "readme_comment_begin": ":: [rR][eE][aA][dD][mM][eE]",
								   "comment": "(::|[ \t]*::)" } )

	templates = {}
	templates [ "html" ] = HTMLTemplate ()
	templates [ "txt" ] = TXTTemplate ()

	if argv is None:
		argv = sys.argv
	try:
		opts, args = getopt.getopt(
			argv[1:], "ho:d", [
				"help", "cpp", "bash", "assembler", "windows", "html", "txt" ])
	except getopt.GetoptError:
		usage ()
		return 0
	for opt, arg in opts:
		if opt in ('-h', '--help'):
			usage ()
			return 0
		elif opt == "-o":
			output_file = arg
		elif opt == "--cpp":
			options [ "comment" ] = comments [ "cpp" ]
		elif opt == "--bash":
			options [ "comment" ] = comments [ "bash" ]
		elif opt == "--assembler":
			options [ "comment" ] = comments [ "assembler" ]
		elif opt == "--windows":
			options [ "comment" ] = comments [ "windows" ]
		elif opt == "--html":
			options [ "template" ] = templates [ "html" ]
		elif opt == "--txt":
			options [ "template" ] = templates [ "txt" ]
		elif opt == "-v":
			options [ "verbose" ] = True
		elif opt == "-d":
			directories = True
		else:
			assert False, "Fatal error. Bad option."

	r = Readme1 ( options )


	if len ( args ) <= 0:
		assert False, "Fatal error. No input given."

	for arg in args:
		if directories:
			delim = "\\"
			if sys . platform . startswith ( 'linux' ):
				delim= "/"
			if arg . rfind ( delim ) >= 0:
				f = arg [ arg . rfind ( delim ): ]
			else:
				f = arg
			d = arg [ :arg . rfind ( "." )]
			d = re . sub ( "(\.|[ ])", "_", d )
			try:
				os . makedirs ( d )
			except:
				#print ( "Fatal error. Not able to create directory " + repr ( d ) )
				pass

			cw = os . getcwd ()
			os . chdir ( d )
			r . readme ( cw + delim + f )
			os . chdir ( cw )
			
			cp ( f, d + delim + f )
		else:
			r . readme ( arg )





	return 0

if __name__ == "__main__":

	sys.exit(main())