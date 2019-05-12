#!/usr/bin/python

import os
import sys

def find_files(path, filenames):
    found = []
    for filename in filenames:
        filename = filename.lower()
        exclude_ios = ["Carthage", ".git", "Index", "Build", "Pods"]
        exclude_android = ["bundle"]
        exclude_dirs = exclude_ios + exclude_android

        for root, dirs, files in os.walk(path):
            dirs[:] = [x for x in dirs if x not in exclude_dirs]
            for file in files:
                if filename == file.lower():
                    found.append(os.path.join(root, file))
    return found

def parse_cartfile(filename):
    found = []
    module_name = filename.split("/")[-2]
    file = open(filename, "r")
    for line in file:
        result = []
        items = filter(None, line.strip().split(" "))
        if len(items) < 3 or (items[0].startswith("#")):
            continue
        # Module that has dependencies
        result.append(module_name)
        # Dependency full name
        result.append(items[1].strip('\"').replace(".git", ""))
        # Dependency short name with version
        if len(items) > 3 and not items[3].startswith("#"):
            items[2] = "%s %s" % (items[2], items[3])
        result.append(items[2].strip('\"'))
        found.append(result)
    file.close()
    return found

def generate_dot_graph(files, data):
    lines = []
    for module in data:
        for item in module:
            (framework, dependency, version) = item
            lines.append([framework, dependency, "%s\\n%s" % (dependency.split("/")[-1], version)])
    # lines.sort(key = lambda x:x[1])

    # Dot header
    graph_data = "digraph G {\nconcentrate = true\n"
    graph_data += "labelloc = t\nlabel = \"" + ",\n".join(files)
    graph_data += "\"\n\n"
    # Dot graph
    for line in lines:
        graph_data += "\"%s\" -> \"%s\" -> \"%s\"\n" % (line[0], line[1], line[2])
    # Dot footer
    graph_data += "}\n"
    return graph_data

#####

found = []
path = os.getcwd()

files = []
if len(sys.argv) > 1 and sys.argv[1].endswith("resolved"):
    files = find_files(path, ["Cartfile.resolved"])
else:
   files = find_files(path, ["Cartfile", "Cartfile.private"])

for filename in files:
    found.append(parse_cartfile(filename))
dot_graph = generate_dot_graph(files, found)
print(dot_graph)
