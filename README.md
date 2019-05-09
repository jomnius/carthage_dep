# carthage_dep

![carthage_dep sample](carthage_dep.png)

## Use Case

You are developing an iOS application, which uses several frameworks. Both application and frameworks handle their dependencies using [Carthage](https://github.com/Carthage/Carthage).

When one framework is developed stand-alone, it uses its own dependencies. When framework is embedded into application, application should link all framework dependencies.

## Problem

There is a possibility that application uses same dependencies, even without frameworks. There is a possibility that application uses different version than needed by framework. There is a possibility that application embeds several frameworks, which depends on several dependencies, which depend on several dependencies.

## Not a Solution

To make this potential dependency spiderweb more visual, I wrote a python script to find and parse either `Cartfile` and `Cartfile.private` or `Cartfile.resolved` contents from a folder and its subfolders and generate a [GraphViz](https://graphviz.gitlab.io/download/) compatible DOT graph file.

This doesn't help much, but at least should make it easier to discover multiple different version number references to the same dependency.

## How to use

```
project/
├── application/
├── framework_a/
└── framework_b/
```

Run `carthage_dep.py` at project root folder to scan all project related folders at the same time. It will print `GraphViz` compatible text to output, which you can direct to a text file (and edit afterwards, if needed).

> carthage_dep.py --resolved > graph.dot
> open graph.dot -a graphviz

## What's Next

That's about it. This will help me now to visually check dependency graph and verify that there are no major issues.

This could assist in discovering all the modules depending on some framework(s) that I need to develop locally and verify that I did change all references from network http://github.com to local file:///folder temporarily.
