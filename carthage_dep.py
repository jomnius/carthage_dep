#!/usr/bin/python

import os
import sys

clean_names = {
    "adjust/ios_sdk": "Adjust",
    "accengage-ios-sdk-releases": "Accengage",
    "accengage-ios-extension-sdk-releases": "Accengage\nextension",
    "usabilla-u4a-ios-swift-sdk": "Usabilla",
    "test-cloud-xcuitest-extensions": "Xamarin\nXCUITest\nextensions",
    "SwinjectStoryboard": "Swinject\nStoryboard",
    "ios-snapshot-test-case": "iOSSnapshot\nTestCase"
}

def find_files(path, filenames):
    found = []
    exclude_ios = ["Carthage", ".git", "Index", "Build", "Pods"]
    exclude_android = ["bundle"]
    exclude_dirs = exclude_ios + exclude_android

    for filename in filenames:
        filename = filename.lower()
        for root, dirs, files in os.walk(path):
            dirs[:] = [x for x in dirs if x not in exclude_dirs]
            for file in files:
                if filename == file.lower():
                    found.append(os.path.join(root, file))
    return found

def parse_cartfile(filename, show_version):
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
        # Dependency (full) name
        dependency = parse_dependency_name(items[1])
        result.append(dependency)
        # Dependency (short) name with version
        if show_version:
            if len(items) > 3 and not items[3].startswith("#"):
                items[2] = "%s %s" % (items[2], items[3])
            result.append(items[2].strip('\"'))
        found.append(result)
    file.close()
    return found

def parse_dependency_name(items):
    dependency_fullname = items.strip('\"')
    dependency_fullname = clean_dependency_name(dependency_fullname, clean_names)
    dependency = filter(None, dependency_fullname.strip().split("/"))[-1]
    dependency = clean_dependency_name(dependency, clean_names)
    if dependency.endswith((".git", ".json", ".swift")):
        dependency = dependency[:dependency.rfind(".")]
    return dependency

def clean_dependency_name(name, dictionary):
    return dictionary[name] if name in dictionary.keys() else name

def generate_dot_graph(files, data, show_title):
    lines = []
    for module in data:
        for item in module:
            if len(item) == 2:
                (framework, dependency) = item
                lines.append([framework, dependency])
            elif len(item) == 3:
                (framework, dependency, version) = item
                lines.append([framework, dependency, "%s\\n%s" % (dependency.split("/")[-1], version)])
    # lines.sort(key = lambda x:x[1])

    # Dot header
    graph_data = "digraph G {\nconcentrate = true\n"
    if show_title:
        graph_data += "labelloc = t\nlabel = \"" + ",\n".join(files) + "\"\n"
    graph_data += "\n"
    # Dot graph
    for line in lines:
        if len(line) == 2:
            graph_data += "\"%s\" -> \"%s\"\n" % (line[0], line[1])
        elif len(line) == 3:
            graph_data += "\"%s\" -> \"%s\" -> \"%s\"\n" % (line[0], line[1], line[2])
    # Dot footer
    graph_data += "}\n"
    return graph_data

#####

path = os.getcwd()

# Poor man's command line parameters
# carthage_dep.py --use-resolved --ignore_version
use_resolved = False
show_version = False
show_title = False
if len(sys.argv) > 1:
    for arg in sys.argv:
        if arg.endswith("resolved"):
            use_resolved = True
        elif arg.endswith("version"):
            show_version = True
        elif arg.endswith("files"): # --list-files
            show_title = True

files = []
if use_resolved:
    files = find_files(path, ["Cartfile.resolved"])
else:
   files = find_files(path, ["Cartfile", "Cartfile.private"])

found = []
for filename in files:
    found.append(parse_cartfile(filename, show_version))
dot_graph = generate_dot_graph(files, found, show_title)
print(dot_graph)
