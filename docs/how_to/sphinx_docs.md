# Setting up Sphinx

## Packages needed

To start, you'll need, at the very least, the `sphinx` package installed. We've
also installed `sphinx_rtd_theme` for basic theming of the published site,
`sphinxcontrib-napoleon` which lets us write Google-style docstrings in our
code, and `m2r2` for converting Markdown files into reStructuredText (into HTML).
Finally, `awscli` will be needed to publish to
[docs.rubikloudcorp.com](http://docs.rubikloudcorp.com).

We've specified these as extras in
[setup.py](https://github.com/rubikloud/pytemplate/blob/master/setup.py) since we'll be
using [nox](https://nox.thea.codes/en/stable/) to create a virtual environment to build
and publish our documentation. We'll also need the regular package dependencies
installed in order to use `sphinx-apidoc`.


```python
EXTRAS = {
    'test': [...],
    'linter': [...],
    'docs': [
        'sphinx',
        'sphinx_rtd_theme',
        'sphinxcontrib-napoleon',
        'm2r2',
        'awscli',
    ]
}
```

## Sphinx configuration

Running `sphinx-quickstart` will set up a source directory and create default
`index.rst` and `conf.py` files by asking you a few questions
(see [here](http://www.sphinx-doc.org/en/master/usage/quickstart.html)). We're using
`docs/` as the source directory with the following structure:

```
docs/
├── _static/
│   └── logo.svg
├── _templates/
│   └── layout.html
├── conf.py
└── index.rst
```

(The contents of the `_static` and `_templates` directories can be ignored for now.)

Copying the [conf.py](https://github.com/rubikloud/pytemplate/blob/master/docs/conf.py)
file from this repository and manually making any changes is probably the easiest way to
do it, though.

The most important modifications to the default configuration (`docs/conf.py`) are given
below:

### Project information

Specify the project name and release versions. These will be displayed in the sidebar.
The copyright shows up in the footer on every page.

```python
from pkg_resources import get_distribution

project = 'pytemplate'
copyright = '2021, Kinaxis'
author = 'Kinaxis'

release = get_distribution(project).version
version = '.'.join(release.split('.')[:2])
```

### Extensions

The extensions below are probably the most important for our purposes (i.e., autogenerating module docs, Google-style docstrings, and markdown files), but there may be others useful for other projects. Check out the [list of built-in extensions](http://www.sphinx-doc.org/en/master/usage/extensions/).

```python
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'm2r2',
]
```

### Source suffixes

If you want markdown files to also be converted to HTML pages, you'll need to specify
`.md` in `source_suffix` like so:

```python
source_suffix = ['.rst', '.md']
```

### HTML theme

We're using the basic layout of ReadTheDocs (with Rubikloud CSS on top):

```python
html_theme = 'sphinx_rtd_theme'

html_logo = 'logo.svg'
html_show_sphinx = False
html_show_sourcelink = True
```

### Syntax highlighting style

To better match the Rubikloud CSS theme, we're currently using the following syntax
highlighting style:

```python
pygments_style = 'friendly'
```

### Extension configuration

Finally, we can specify any configuration for the extensions we're using. In our case,
we want to use Google-style docstrings and to display docstrings for private methods.

```python
napoleon_google_docstring = True
napoleon_include_private_with_doc = True
napoleon_include_special_with_doc = True
```

## Static files

To show a logo in the sidebar, `html_logo` needs to be set in the `conf.py` file
[as specified above](#html-theme). We're using a Rubikloud logo, if you want to do the
same simply copy [logo.svg](https://github.com/rubikloud/pytemplate/blob/master/docs/_static/logo.svg)
into the `docs/_static/` directory.

In order to apply the Rubikloud CSS on top of the ReadTheDocs theme,
[layout.html](https://github.com/rubikloud/pytemplate/blob/master/docs/_templates/layout)
needs to be copied into the `docs/_templates/` directory.


```html
{% extends "!layout.html" %}
  {% block extrahead %} {{ super() }}
  <link rel="stylesheet" href="http://docs.rubikloudcorp.com/documentation-theme.css" type="text/css" />
{% endblock %}
```

## Index page

Time to create the most important part, the index page! This can be `index.rst` or
`index.md` if you're using the markdown extension. It's a bit easier to create a table
of contents using reStructuredText however.

We've used `.rst` for the index page, see below, and `.md` for most of our other docs.

Check out the [Sphinx reStructuredText Primer](http://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html)
for more information.


```
pytemplate
======================================

A bare-bones Python package that serves as a template for other Python packages.


.. toctree::
   :maxdepth: 2
   :caption: How To

   Create documentation with Sphinx <how_to/sphinx_docs>

API Reference
^^^^^^^^^^^^^^^^^

* :ref:`genindex`
* :doc:`pytemplate`
```

(Note: relative links in markdown files will have to be specified with the `.html`
extension so that the link won't be broken once published; in `.rst` files, the
extension doesn't need to be specified at all.)


## Nox

Here we add a function to the [noxfile.py](https://github.com/rubikloud/pytemplate/blob/master/noxfile.py)
file for building and publishing our documentation to the `docs.rubikloudcorp.com` S3
bucket. Then, `nox -s docs` will generate the API documentation, build the HTML, and
publish to S3.

Make sure to update the `package_name` and `s3_path` variables below:


```python
@nox.session(python='3.8', reuse_venv=True)
def docs(session):
    package_name = 'pytemplate'
    html_path = 'docs/_build/html'
    s3_path = 's3://docs.rubikloudcorp.com/pytemplate/'

    session.install('.[docs]')

    session.log('Generating documentation...')
    session.run('sphinx-apidoc', '-f', '-e', '-P', '-o', 'docs', f'{package_name}')
    session.run('sphinx-build', '-b', 'html', 'docs', f'{html_path}')

    if 'publish' in session.posargs:
        session.log('Publishing documentation...')
        session.run('aws', 's3', 'rm', '--recursive', f'{s3_path}')
        session.run('aws', 's3', 'cp', '--recursive', f'{html_path}', f'{s3_path}')
```

(For repositories that don't use `nox` just yet, MlaaS uses `invoke`
scripts to build documentation in docker. All of the instructions up to this point will
still apply, but the GHA stage will be a little different. See files
[1](https://github.com/rubikloud/mlaas/blob/master/.github/workflows/ci_cd.yml),
[2](https://github.com/rubikloud/mlaas/blob/4edd4f0112a399a46ad7e2adfad83e7173eab5e6/tasks.py#L11))

## Stage in Github Action

The final piece needed to automate the publishing of documentation to
[docs.rubikloudcorp.com](http://docs.rubikloudcorp.com) is adding a stage to the
GHA to trigger on commits to the `master` branch:


```
      - name: Build documentation
        run: |
          nox -s docs
      - name: Publish documentation
        if: github.ref == 'refs/heads/master'
        run: |
          nox -s docs --publish
```
