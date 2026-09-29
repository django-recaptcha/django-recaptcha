# Django Recaptcha: Enterprise

This submodule lets you protect a form using [reCAPTCHA Enterprise](https://docs.cloud.google.com/recaptcha/docs):

- implements a field and several widgets for different use cases
- supports all [essential tier](https://docs.cloud.google.com/recaptcha/docs/compare-tiers) features
- uses a custom client that supports proxies\*

This is still a work in progress; it does not support the following (yet):

- annotating assessments
- authentication methods besides access tokens
- providing various forms of additional information
- (other stuff that I'm probably forgetting)

_\*: The official [google-cloud-recaptcha-enterprise](https://pypi.org/project/google-cloud-recaptcha-enterprise/) package does not support proxies._

## Comparison with Classic reCAPTCHA

Many aspects of Enterprise reCAPTCHA are still the same as Classic reCAPTCHA.
However, there are several noteworthy differences:

- the secret key has been replaced with alternative authentication methods
- an assessment always includes a risk score ranging from 0.0 to 1.0, even for binary situations such as checkbox widgets
- risk scores are limited to specific values:
  - free tiers: `0.1`, `0.3`, `0.7`, `0.9`
  - paid tiers: `0.0`, `0.1`, ..., `0.9`, `1.0`
- paid tiers include many more options to provide additional information
- assessments can be annotated afterwards for more accurate results


## Fields and Widgets

This module includes only one field class: `ReCAPTCHAEnterpriseV1`.
It supports several widgets for different use cases:

- `ReCAPTCHAEnterpriseV1CheckboxWidget` (default)
  - used with a checkbox key
  - widget is a [checkbox widget](https://docs.cloud.google.com/recaptcha/docs/instrument-web-pages-with-checkbox#render_widget)
  - requires no further customization
- `ReCAPTCHAEnterpriseV1HiddenWidget`
  - used with score-based (and policy-based?) keys
  - widget is invisible to user
  - requires [client-side integration](https://docs.cloud.google.com/recaptcha/docs/instrument-web-pages)
- `ReCAPTCHAEnterpriseNoHTMLWidget`
  - can be used with any key
  - recommended for highly customized client-side integrations
  - only handles the server-side processing of reCAPTCHA tokens

## Settings

You can configure your setup in several ways (in order of priority):

1. a value passed along as an argument to the field instance
2. a value set as a global django settings
3. default value (see `conf.py`)

See `conf.py` for a list of available settings.


## Minimal Example: Enterprise V1 Checkbox widget

Providing values for the following settings is required.
A typical project will set these globally in the Django settings file:

```python3
# settings.py
RECAPTCHA_ENTERPRISE_PROJECT_ID=...
RECAPTCHA_ENTERPRISE_SITEKEY=...
RECAPTCHA_ENTERPRISE_ACCESS_TOKEN=...
```

To protect an existing form, add a `ReCAPTCHAFieldV1` field to the form:

```python3
from django.forms import Form
from django_recaptcha.enterprise.fields import ReCAPTCHAFieldV1
from django_recaptcha.enterprise.widgets  import ReCAPTCHAEnterpriseV1CheckboxWidget

class MyForm(Form):
    ...
    recaptcha = ReCAPTCHAFieldV1()

```

This should work out of the box; no additional client-side scripting is needed.


## Providing Additional Information

reCAPTCHA Enterprise lets you provide additional information that can be used to help Google identify bad actors.
You should provide this additional information before validating the form's data.

```python3
from forms import MyForm

def my_view(request):
    if request.method == "POST":
        form = MyForm(request.POST)
        form.recaptcha.add_additional_information(request)
        if form.is_valid():
            ... # success!  
        else:
            ... # failure!
    else:
        ... # not a POST request 
    ...
```
