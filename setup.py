from setuptools import setup, find_packages

setup(
    name='django-recaptcha',
    version='dev',
    description='Django recaptcha form field/widget app.',
    author='Praekelt Consulting',
    author_email='dev@praekelt.com',
    url='http://github.com/praekelt/django-recaptcha',
    packages = find_packages(),
    install_requires = [
        'recaptcha-client'
    ],
    include_package_data=True,
)
