README readme.py

Script for making automated readme files
With as less as possible effort you can create a readme file
of your source code


1 USAGE
1.1 ARGUMENTS
1.2 OPTIONS
1.2.1 EXAMPLES
1.3 BASIC
1.4 SECTIONS
1.4.1 EXAMPLE
1.5 ANNOTATIONS
1.5.1 EXAMPLE


1 USAGE

Script reads input given in <n> files and creates a readme files for them
Usage: ./readme.py [options] <file1> [file2, file3, ...]
Writing a readme in your scripts is quite easy

1.1 ARGUMENTS

without -d and with more than one files given
will every file overwrite the previous readme
so the result will be only readme file of the last one


1.2 OPTIONS

-d
running with -d on script named "script.sh" will produce
a new directory "script" and place a readme file there
also a copy of a script will be present in that directory
--cpp|--bash|--windows|--assembler
is for selecting a comment style used in your source code
if none of those is given, script will try to guess the comment
style himself
--html|--txt
output formats, the produced file will be named as
README.<format>

1.2.1 EXAMPLES

./readme.py -d script.py
./readme.py --txt --cpp CArray.cpp



1.3 BASIC

For correct work of readme parser you need to do following:
- readme comment needs to be in format specific for
programming language and after the first comment there has to
be a "README" word.
/** README or ## README or
;; README or :: README
no rules aplies for the end comment


1.4 SECTIONS

For using sections it is neccessary to keep a right indentation level of sections
Traditional format for section name is [a-zA-Z0-9]+:

1.4.1 EXAMPLE

|USAGE:
|   |This text will be visible in section usage
|   |EXAMPLES:
|   |   |This text will be visible in section examples
|   |ANOTHER:
|   |   |Another text in other section



1.5 ANNOTATIONS

For using annotations are defined some rules:
- keep the indentations right
- every annotation starts with @
- annotations can be also attached to sections, just keep the indentation

1.5.1 EXAMPLE

This will be visible in annotations
@author Jan novák
@year 2014




Annotations
Author: Kryštof Tulinger
Year: 2014
Place: Norway


This readme file was automaticaly generated by "readme.py" script from the original file.