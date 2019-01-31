from django.urls import path
from django.contrib import admin
from django.views.generic.edit import FormView

from captcha.tests.forms import TestWizardRecaptchaForm

#django < 2
#urlpatterns = [
#    path("admin/", admin.site.urls),
#    path(r"^form/$",
#        FormView.as_view(
#            form_class=TestWizardRecaptchaForm,
#            template_name="test_form.html",
#            success_url="/admin"
#        ),
#        name="form"
#    )
#]
urlpatterns = [
    path("admin/", admin.site.urls),
    path(r"form/$",
        FormView.as_view(
            form_class=TestWizardRecaptchaForm,
            template_name="test_form.html",
            success_url="/admin"
        ),
        name="form"
    )
]
