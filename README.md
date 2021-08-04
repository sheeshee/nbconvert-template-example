# nbconvert Example Template
An example nbconvert template distributable through PyPi.

## Installation instructions
This nbconvert template can be installed with pip:
```
pip install nbconvert_template_example
```
This will make the template "avocadify" available in the python environment.


## Usage
Once installed, convert Jupyter notebooks into templated slides by running:

```
jupyter nbconvert --to avocadify notebook.ipynb
```
_Install for development:_
* clone this repo,
* create a fresh environment and install the packages in `requirements.txt`,
* test the code by running `tox`.

# Project Purpose

This is a simple yet complete package that demonstrates how to organize an
nbconvert template in a way that makes it distributable through the Python
Package Index (PyPi).

The key components of this project are
* a minimal nbconvert  exporter and template (which turns a notebook into a
  stylized Reval.js document),
* the various files needed to distribute a package through PyPi, and
* tests to check that the package functions as expected and is distributable.

The following summarizes the project directory structure at a glance and briefly
explains for what each file is useful. It is possible to create
an even more minimal template package (by omitting testing, for example)
but this will seriously impact the quality and ease-of-development of the
code.
```
nbconvert-template-example/ (root project dir)
|─fruit_styles/             (package dir)
|  |─ __init__.py           (Python code defining our custom template exporter)
|  └─ avocado/              (dir giving the template)
|     |─ conf.json          (configuration parameters for the template)
|     |─ index.html.j2      (the Jinja template and entry point for nbconvert)
|     └─ etc...             (various media/resource files used in template)
|─ tests/                   (test dir)
|  |─ test_export.py        (tests to check produced html is correct)
|  └─ etc...                (various test resource files)
|─ pytest.ini               (pytest config - ignores deprecation warnings)
|— tox.ini                  (sets up testing the packaged template)
|— requirements.txt         (additional python libraries needed for development)
|─ pyproject.toml           (sets up the packaging tools)
|— setup.cfg                (defines metadata for the package)
|─ MANIFEST.in              (adds additional data files to packaging)
|— LICENSE                  (defines who can use the template and how)
|— README.md                (this file)
|— etc...                   (various other files useful for git or documentation)
```

The rest of this document explains the key components of the project in more
detail and then summarizes the commands/workflow for publishing the package
online.

## Key Package Elements
### The Template

See [here](https://nbconvert.readthedocs.io/en/latest/customizing.html) for nbconvert's documentation on creating custom templates.

The actual template is called `avocado` and it exists in the package
`fruit_styles`. That said, the entry point (defined in `setup.cfg`) is aliased
as `avocadify` and it is this term which users would use when calling the
template from the nbconvert CLI.

I purposefully used different names here between the package, template and entry
point to allow readers to distinguish better how different elements throughout
the project relate to one another.

#### The Jinja template: `index.html.j2`

This template makes two changes to the default Reveal.js template provided by
nbconvert: it places a title slide at the beginning of the presentation with a
background image (photo by [Dirk Ribbler on Unsplash](https://unsplash.com/photos/xEFoRSMT-x4)) and it changes the colour of the headings to green.

It adds the title slide by extending the original Reveal.js jinja template file
and adding an additional `section` just after the `body_header` block. This
inserts the title slide just before the content of the presentation.

The template defines its own header colours by including an additional CSS file
in which it defines the style of the `h1` elements in the html file.

#### The configuration file: `conf.json`

nbconvert expects to find the configuration file inside the template directory.
This file defines
* the base from which which the template will inherit,
* the compatible output formats (mimetypes), and
* what pre-processors to apply to the notebook (in this case, it removes certain
  cells according to their metadata tags).

#### The Custom Exporter: `__init__.py:AvocadoExporter`

The `__init__.py` file in the package directory defines a custom exporter which
inherits from the `SlidesExporter` from the nbconvert project.

This custom exporter
* tells nbconvert where to find our custom template, and
* provides additional media resource to the template (in this case an image
  that will be included directly in the HTML file as an encoded media.)

### Packaging the Template

See [here](ging.python.org/tutorials/packaging-projects/) for PyPi's packaging tutorial.

The template exists inside a normal if somewhat minimal python package. As such,
it uses the typical packaging files:
* `pyproject.toml` defines the build environment.
* `setup.cfg` defines the metadata for the package.
* `MANIFEST.in` specifies which data files to include in the distribution.
* `LICENSE` tells users how they are allowed to use this code.

The `setup.cfg` file has a few key details which are worth mentioning:
1. Note the setting `include_package_data = True`; this tells setuptools to look
   at the `MANIFEST.in` file which then tells it to include all the files inside
   the package.
2. This file specifies the entry point for nbconvert towards the end of the
   file. This defines how users refer to the template when using the nbconvert
   CLI:
   ```
   [options.entry_points]
   nbconvert.exporters =
       avocadify = fruit_styles:AvocadoExporter
   ```

### Testing

It is important to test your template creation before publishing it so users
have a smooth experience. Pytest and Tox can greatly facilitate the testing
cycle.

**Pytest** defines unit tests which particular aspects of the python code. In this
example project, there is only one test. This test uses the custom exporter to
generate the HTML file as a string and then passes this string to an HTML
library that validates its syntax. This can help catch errors in the template such as a hanging tag.

**Tox** is a powerful tool which handles a few things:
* It creates an isolated environment, packages the project and then runs
the tests inside this environment. This makes sure that all the additional
files are included properly.
* Tox also checks that the nbconvert CLI completes successfully.
* It repeats these tests for each Python environment specified, providing
  assurance the produced package is compatible with different Python versions.


# How to Publish the Package

This will be the general process for deploying the template online:

1. Run tests with `tox` to check everything is working as expected
2. Build the package with `python -m build`
3. Upload to PyPi with `python -m twine upload dist/*`
