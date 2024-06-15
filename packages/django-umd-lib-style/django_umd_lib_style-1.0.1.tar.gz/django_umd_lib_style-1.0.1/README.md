# django-umd-lib-style

Django app that provides theming for UMD Libraries applications.

## Installation

```zsh
pip install django-umd-lib-style
```

## Setup

Add `umd_lib_style` to the `INSTALLED_APPS` list in your Django
project's `settings.py` file:

```python
INSTALLED_APPS = [
    ...,
    'umd_lib_style',
    ...,
]
```

To get some useful values (application name and version, navigation links)
in the context for every request, add this context processor to your
project's `settings.py`:

```python
TEMPLATES = [
    {
        'OPTIONS': {
            'context_processors': [
                ...,
                'umd_lib_style.context_processors.app_info',
            ],
        },
    },
]
```

## Templates

This app comes with a base template that provides the basic layout for the
page (header with environment banner, logo, application name, navigation
links, and a footer with the application name and version, and the UMD web
accessibility link).

The easiest way to get the default page layout on your app's pages is to
create a `base.html` template for your views that extends the
`umd_lib_style/base.html` template:

```html
{% extends 'umd_lib_style/base.html' %}
{% block head %}
... any HTML that should go into every page's &lt;head&gt; element ...
{% endblock %}
{% block main %}
... any HTML that should precede a specific page's content ...
{% block content %}{% endblock %}
... any HTML that should follow a specific page's content ...
{% endblock %}
```

Then, your individual page templates would extend this template, and
supply their content in the `content` block:

```html
{% extends 'my_app/base.html` %}
{% block content %}
<p>Hello, world!</p>
{% endblock %}
```

The umd-lib-style base template includes an `h1` element whose content is
taken from the value of the `title` context variable. It will also render
any messages in the context. Both of these are rendered before the `main`
block.

### Context Values

If you have enabled the `umd_lib_style.context_processors.app_info`
context processor, then you will have access to the following variables in
all of your templates:

* `application_name` (str)
* `application_version` (str)
* `navigation_links` (dict)

Many of these are controlled by settings from your `settings.py` file.

## Settings

There are some additional values you should set in your `settings.py`:

### `PROJECT_PACKAGE_NAME`

Default value: `None`

The application version is taken from this package's version using
`importlib.metadata.version(PROJECT_PACKAGE_NAME)`. That version is
available in templates as `application_version`.

### `APPLICATION_NAME`

Default value: `"App"`

Application name to be displayed in the header and footer. Available in
templates as `application_name`.

### `NAVIGATION_LINKS`

Default value: `{}`

Dictionary mapping view names to labels. It is used to generate the
navigation links in the header. Available in templates as `navigation_links`.

### `FOOTER_LINKS`

Default value: `{}`

Dictionary mapping view names to labels. It is used to generate the
navigation links in the footer. Available in templates as `footer_links`.

### `ENVIRONMENT`

Default value: `"development"`

Used to trigger the display of the standard environment banner at the top
of every page. Should be one of `"development"`, `"test"`, or `"qa"`. Any
other value will suppress the display of the environment banner.

## CSS

### Custom Properties (a.k.a."Variables")

The included stylesheet defines a number of values using CSS custom
properties. Many of these are color values, but a few deal with fonts and
layout. They are all applied using the `:root` pseudo-element. See
[umd_lib_style.css](src/umd_lib_style/static/umd_lib_style/umd_lib_style.css)
for the full list.

### Semantic Classes

In addition to providing basic thematic and layout styling in accordance
with UMD's brand guidelines and the design of the UMD Libraries' other web
UIs, the included CSS also provides some semantic classes for styling
individual `button` elements.

| Class name | Use for buttons that ...                                    |
|------------|-------------------------------------------------------------|
| `create`   | ... immediately create or add a resource.                   |
| `edit`     | ... display a form or other method of modifying a resource. |
| `update`   | ... immediately save an already existing resource.          |
| `delete`   | ... immediately remove a resource.                          |

## License

See the [LICENSE](LICENSE.md) file for license rights and limitations
(Apache 2.0).
