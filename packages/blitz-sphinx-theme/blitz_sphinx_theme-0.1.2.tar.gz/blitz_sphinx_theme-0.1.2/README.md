# Blitz Sphinx Theme

Sphinx theme for [Blitz Docs](https://etched-ai.github.io/blitz/intro.html) forked from [Pytorch Sphinx Theme](https://github.com/pytorch/pytorch_sphinx_theme/tree/master).

## Local Development

Run python setup:

```
git clone https://github.com/etched-ai/blitz_sphinx_theme
pip install -e blitz_sphinx_theme
```

and install the dependencies using `pip install -r docs/requirements.txt`

In the root directory install the `package.json`:

If you have `npm` installed then run:

```
npm install
```

- If you want to see generated documentation for `docs/demo` then create
`.env.json` file and make it empty json file. Means `.env.json file` will
contain

```
{}
```

Run grunt to build the html site and enable live reloading of the demo app at `localhost:1919`:

```
npx grunt
```

Run grunt to build the html site for docs:

```
npx grunt --project=docs
```

The resulting site is a demo.

## Testing your changes and submitting a PR

When you are ready to submit a PR with your changes you can first test that your changes have been applied correctly against either the PyTorch Docs or Tutorials repo:

1. Run the `grunt build` task on your branch and commit the build to Github.
2. In your local docs or tutorials repo, remove any existing `blitz_sphinx_theme` packages in the `src` folder (there should be a `pip-delete-this-directory.txt` file there)
3. Clone the repo locally `git clone https://github.com/etched-ai/blitz_sphinx_theme`
4. Install `blitz_sphinx_theme` by running `pip install -e blitz_sphinx_theme`
5. Install the requirements `pip install -r requirements.txt`
6. Remove the current build. In the docs this is `make clean`, tutorials is `make clean-cache`
7. Build the static site. In the docs this is `make html`
8. Open the site and look around. In the docs open `docs/build/html/index.html`

If your changes have been applied successfully, remove the build commit from your branch and submit your PR.

## Publishing the theme

Before the new changes are visible in the theme the maintainer will need to run the build process:

```
grunt build
```

Once that is successful commit the change to Github.

### Developing locally against Blitz Docs

To be able to modify and preview the theme locally against the Blitz Docs first clone the repositories:

- [Blitz](https://github.com/etched-ai/blitz)

Then follow the instructions in each repository to make the docs.

Once the docs have been successfully generated you should be able to run the following to create an html build.

#### Docs

```
# in ./docs
make html
```

#### Tutorials

```
# root directory
make html
```

Once these are successful, navigate to the `conf.py` file in each project. In the Docs these are at `./docs/source`. The Tutorials one can be found in the root directory.

In `conf.py` change the html theme to `pytorch_sphinx_theme` and point the html theme path to this repo's local folder, which will end up looking something like:

```
html_theme = 'blitz_sphinx_theme'
html_theme_path = ["../../../blitz_sphinx_theme"]
```

Next create a file `.env.json` in the root of this repo with some keys/values referencing the local folders of the Docs and Tutorials repos:

```
{
  "DOCS_DIR": "../blitz/docs/blitz-notebook-docs"
}

```

You can then build the Docs or Tutorials by running

```
grunt --project=docs
```

These will generate a live-reloaded local build for the respective projects available at `localhost:1919`.

Note that while live reloading works these two projects are hefty and will take a few seconds to build and reload, especially the Docs.

### Built-in Stylesheets and Fonts

There are a couple of stylesheets and fonts inside the Docs repo itself meant to override the existing theme. To ensure the most accurate styles we should comment out those files until the maintainers of those repos remove them:

#### Docs

```
# ./docs/source/conf.py

html_context = {
    # 'css_files': [
    #     'https://fonts.googleapis.com/css?family=Lato',
    #     '_static/css/pytorch_theme.css'
    # ],
}
```

### Top/Mobile Navigation

The top navigation and mobile menu expect an "active" state for one of the menu items. To ensure that either "Docs" is marked as active, set the following config value in the respective `conf.py`, where `{project}` is `"docs"`.

```
html_theme_options = {
  ...
  'pytorch_project': {project}
  ...
}
```
