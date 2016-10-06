from setuptools import setup, find_packages


long_desc = open('README.rst', 'rb').read().decode('utf-8') + \
            open('AUTHORS.rst', 'rb').read().decode('utf-8') + \
            open('CHANGELOG.rst', 'rb').read().decode('utf-8')
setup(
    name='django-recaptcha',
    version='1.0.5',
    description='Django recaptcha form field/widget app.',
    long_description=long_desc,
    author='Praekelt Foundation',
    author_email='dev@praekelt.com',
    license='BSD',
    url='http://github.com/praekelt/django-recaptcha',
    packages=find_packages(),
    install_requires=[
        'django',
    ],
    tests_require=[
        'django-setuptest>=0.2.1',
    ],
    test_suite="setuptest.setuptest.SetupTestSuite",
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python",
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        "License :: OSI Approved :: BSD License",
        "Development Status :: 5 - Production/Stable",
        "Operating System :: OS Independent",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    zip_safe=False,
)
