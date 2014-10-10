#!/usr/bin/python

## README
#
# Script for making automated readme files
#

import codecs
import sys
import os
import re
import getopt
import html

class Template:
	def __init__ ( self ):
		pass
	def sectionTemplate ( self ):
		pass
	def sectionsTemplate ( self ):
		pass
	def annotationsTemplate ( self ):
		pass
	def annotationLineTemplate ( self ):
		pass
	def textTemplate ( self ):
		pass
	def lineTemplate ( self ):
		pass
	def contentTemplate ( self ):
		pass
	def contentPartTemplate ( self ):
		pass
	def tocTemplate ( self ):
		pass
	def tocSectionTemplate ( self ):
		pass
	def tocSubsectionTemplate ( self ):
		pass
	def pageTemplate ( self ):
		pass


class TXTTemplate ( Template ):
	def __init__ ( self ):
		Template . __init__ ( self )
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
	def render ( self, filename, readmes ):
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

		with codecs . open ( filename, "w", encoding = "utf-8" ) as outputFile:
			
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
	def __init__ ( self ):
		Template . __init__ ( self )

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

	def render ( self, filename, readmes ):

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

		with codecs . open ( filename, "w", encoding = "utf-8" ) as outputFile:
			
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
					<span class="lead">
						%(header)s
					</span>
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
		self . _section = options [ "section" ] if "section" in options . keys () else "[A-Z0-9]+:"

	def begin ( self ):
		return self . _readme_comment_begin
	def end ( self ):
		return self . _readme_comment_end
	def comment ( self ):
		return self . _comment
	def blankLine ( self ):
		return self . _separate_lines
	def blank ( self ):
		return " \t"
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

		self . subsections ( string )
		self . text ( string )
		self . annotations ( string )

	def name ( self ):
		return self . _name

	def subsections ( self, string = None ):
		if not string:
			return self . _sections
		pattern = "(?m)^[" + self . _comment . blank () + "]{" + repr ( self . _depth * 4 ) + "}" + self . _comment . section () + "[" + self . _comment . blank () + "]*[\n](^[" + self . _comment . blank () + "]{" + repr ( self . _depth * 4 + 1 ) + ",}.*[\n])*"
		sections = re . finditer ( pattern, string )
		for section in sections:
			section = section . group ()
			self . _sections . append ( Section ( section, self . _depth + 1, self . _comment ) )
		return self . _sections
	def text ( self, string = None ):
		if not string:
			return self . _lines
		pattern = "(?m)^[" + self . _comment . blank () + "]{" + repr ( self . _depth * 4 ) + "}[^" + self . _comment . blank () +"@][^A-Z].*"
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
		ann = re . finditer ( "(?m)^[" + self . _comment . blank () + "]{" + repr ( self . _depth * 4 ) + "}@[a-zA-Z0-9]+[" + self . _comment . blank () + "].*", string )

		for annotation in ann:
			#print ( "..." )
			#print ( annotation . group () )
			if re . match ( "(?m)^[" + self . _comment . blank () + "]{" + repr ( self . _depth * 4 ) + "}@[a-zA-Z0-9]+[" + self . _comment . blank () + "]+.*?", annotation . group () ):
				key = re . sub ( "(?m)^[" + self . _comment . blank () + "]{" + repr ( self . _depth * 4 ) + "}@(?P<key>[a-zA-Z0-9]+).*", lambda m: m . group ("key"), annotation.group() )
				val = re . sub ( "(?m)^[" + self . _comment . blank () + "]{" + repr ( self . _depth * 4 ) + "}@[a-zA-Z0-9]+[" + self . _comment . blank () + "]+(?P<val>.*?)", lambda m: m . group ("val"), annotation.group() )
				self . _annotations . append ( { key: val } )
		return self . _annotations


	def id ( self, index = [], separator = "-" ):
		return separator . join ( str (val) for val in index )


class Readme:
	def __init__ ( self, name, string, comment ):

		self . _comment = comment
		self . _name = name

		self . _lines = []
		self . _section = []
		self . _annotations = []

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
		string = re . sub ( "^[ ][@][^A-Z0-9].*", "", string )
		pattern = "(?m)^[ ][A-Z0-9]+:([\n]|.)*?(?=^[ ][A-Z0-9]+:|\Z)"
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
		ann = re . finditer ( "(?m)^[ ]{1}@[a-zA-Z0-9]+[" + self . _comment . blank () + "].*", string )
		for annotation in ann:
			if re . match ( "(?m)^[ ]{1}@[a-zA-Z0-9]+[" + self . _comment . blank () + "]+.*?", annotation . group () ):
				key = re . sub ( "(?m)^[ ]{1}@(?P<key>[a-zA-Z0-9]+).*", lambda m: m . group ("key"), annotation.group() )
				val = re . sub ( "(?m)^[ ]{1}@[a-zA-Z0-9]+[" + self . _comment . blank () + "]+(?P<val>.*?)", lambda m: m . group ("val"), annotation.group() )
				annotations . append ( { key: val } )
		self . _annotations = annotations
		return annotations

	def text ( self, string = None ):
		if not string:
			return self . _lines
		pattern = "(?m)^[ ][^" + self . _comment . blank () + "@][^A-Z].*"
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

		self . _output_file = options [ "output_file" ] if "output_file" in options . keys () else "README.txt"
		self . _comment = options [ "comment" ] if "comment" in options . keys () else Comment ()
		self . _options = options

		self . _readmes = []

		self . _template = HTMLTemplate ()




	def readme ( self, filename ):
		sections_template = self . _template . sectionsTemplate ()
		annotations_template = self . _template . annotationsTemplate ()
		annotation_line = self . _template . annotationLineTemplate ()
		table_of_contents_template = self . _template . tocTemplate ()
		text_template = self . _template . textTemplate ()
		line_template = self . _template . lineTemplate ()
		html = self . _template . pageTemplate ()

		header = ""
		table_of_contents = ""
		view = ""
		annotations = ""
		annotation_lines = ""


		with codecs . open ( filename, "r", encoding = "utf-8" ) as inputFile:
			content = inputFile . read ()
			content = re . sub ( "\r", "\n", content )
			content = re . sub ( "\n\n", "\n", content )
			content = re . sub ( "\t", "    ", content )
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
				
				readme = re . sub ( "(?m)" + self . _comment . comment (), "", readme )


				self . _readmes . append ( Readme ( filename, readme, self . _comment ) )


		self . _template . render ( "README.html", self . _readmes )




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

	def usage ():
		print ( "Usage: " + sys.argv[0] + " [options]" )
		print ( "" )
		print ( "Options:" )
		print ( "	--help|-h			show this help message and exit" )
		print ( "	--input|-i <dir>		set the input file/directory" )
		print ( "	--output|-o <dir|file>		set the output directory, default is the same as input" )
		print ( "	--language|-l <lang>		set the language" )
		print ( "	--merge|-m			set if the thread files should be merged after complete run" )
		print ( "	--delete-after-merge		set if thread files should be deleted after complete run" )
		print ( "	--name|-n <name>		set the subdirectory of output directory where the results will be stored; %(lang)s can be used" )
		print ( "	--threads|-t <number>		number of threads" )
		print ( "	--number-of-links <number>	number of links processed by thread in a loop" )
		print ( "" )
		print ( "Examples:" )
		print ( "	script.py --input ..\\languages\\nowiki\\ -t 8 --merge -c 500 -l nn" )
		print ( "	script.py --input ..\\languages\\nowiki\\nn.links.txt.00000000.txt -t 8 --merge --delete-after-merge -c 20 -l nn" )


	if not argv:
		argv = sys . argv

	options = {}
	threads = 5
	input = []
	lang = None

	if argv is None:
		argv = sys.argv
	try:
		opts, args = getopt.getopt(
			argv[1:], "hvl:o:i:mdn:t:c:", [
				"help", "language=", "input=", "output=",
				"merge", "delete-after-merge", "name=", "threads=" "number-of-links=" ])
	except getopt.GetoptError:
		usage ()
		return 0
	for opt, arg in opts:
		if opt in ('-h', '--help'):
			usage ()
			return 0
		elif opt in ("--language", "-l"):
			lang = str ( arg )
		elif opt in ("--input", "-i"):
			input = arg
		elif opt in ("--output", "-o"):
			options [ "output_path_directory" ] = arg
		elif opt in ("--name", "-n"):
			options [ "output_path" ] = arg
		elif opt in ("--merge", "-m"):
			options [ "merge" ] = True
		elif opt in ("--delete-after-merge", "-d"):
			options [ "delete_after_merge" ] = True
		elif opt in ("--number-of-links", "-c"):
			options [ "number_of_links" ] = int ( arg )
		elif opt in ("--threads", "-t"):
			threads = int ( arg )
		elif opt == "-v":
			options [ "verbose" ] = True
		else:
			assert False, "Fatal error. Bad option."



	return 0

if __name__ == "__main__":
	
	#options = { "readme_comment_begin": "/\*\* README",
	#			"readme_comment_end": "\*/",
	#			"comment": "(^[ \t]*\*)" }
	#c = Comment ( options )			
	#d = Readme1 ( { "comment": c } )
	d = Readme1 ()
	#d . readme ( "download.py" )
	d . readme ( "CArray.h" )

	sys.exit(main())