# html-qa-thing

quick script hacked together for a specific purpose

* logs a table of HTML elements used, containing the tag name, id and class(es) for each, in two files
* logs the % difference in the amount of pixels between images of rendered HTML for both files (with chrome) (should be configured depending on your use-case) and generates diff.png in the current working directory

## usage

### htmlqa: (file1: dict, file2: dict, should_justify: bool, image_size: tuple = (1920, 1080)) -> None

```python
# converting it to work from the command line is trivial
# the htmlqa folder should be placed under the parent directory of the file you're calling htmlqa from 
from htmlqa import htmlqa
htmlqa.htmlqa({"path": r"path\to\file1.html"}, {
       "path": r"path\to\file2.html", "css_files": [r"path\to\a.css", r"path\to\b.css"]}, True)
       
# dict attributes 
# path: path to HTML file
# css_files: a list of multiple css files or a single css file used by an HTML file
# if you specify css files used in an HTML file make sure you're actually including them
# e.g with <link rel="stylesheet" type="text/css" href="./styles.css"  />
# it might work if you don't specify `css_files` too but it's not guaranteed

```
## requirements
Python 3.x
dependencies can be installed by navigating to this directory and running `pip -r requirements.txt`



depends on lxml, PIL, pixelmatch, bs4, html2image
