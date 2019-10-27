from parseFile import *
from generateIndex import *
from os.path import *
from generateDirectoryPage import *
from os import listdir, mkdir
import sys

# inputs: path to directory and files it contains
# output: returns only directories or swift files
def preprocessFilenames(path, files):
	result = list()
	for file in files:
		name = path + "/" + file
		if isfile(name) and name.endswith(".swift"):
			result.append(file)
		elif isdir(name):
			result.append(file)
	return result

# inputs: path to directory and files it contains
# output: content of md file
def parseMD(path, files):
	for file in files:
		fullname = (path + "/" + file)
		if isfile(fullname) and (fullname).endswith(".md"):
			readme = open(fullname, mode="r")
			text = readme.read()
			readme.close()
			return text
	return "No catalog description"

# inputs: path to project (prefix + path), workingDirectory is a directory where we'll store documentation
# outputs: classes references across all project
# this function create all html files for each swift file in input project
def parseDirectory(prefix, path, workingDirectory):
	references = dict()
	allPath = prefix + path
	md = ""
	if isfile(allPath) and allPath.endswith(".swift"):
		references.update(parseFile(prefix, dirname(path) + "/", workingDirectory, basename(path)[:-6]))
	elif isdir(allPath):
		if not exists(workingDirectory + "/" + path):
			mkdir(workingDirectory + "/" + path)
		files = listdir(allPath + "/")
		file = open(workingDirectory + "/" + path + ".html", mode="w")
		md = parseMD(allPath, files)
		file.write(generatePage(basename(path), preprocessFilenames(allPath, files), md))
		file.close()
		for file in files:
			references.update(parseDirectory(prefix, path + "/" + file, workingDirectory))
	return references


if len(sys.argv) != 2:
	sys.exit()

projectPath = sys.argv[1]
rootProject = basename(projectPath)
if not exists("testOutput"):
	mkdir("testOutput")

references = parseDirectory(dirname(projectPath) + "/", rootProject, "testOutput")
sorted_references = sorted(references.items(), key=lambda kv: kv[0])

index = generateIndex("Yaza", "testOutput/" + rootProject + ".html", sorted_references)
page = open("index.html", mode='w')
page.write(index)
page.close()