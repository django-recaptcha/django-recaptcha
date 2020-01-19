from setuptools import setup, find_packages


long_desc = open('README.rst', 'rb').read().decode('utf-8') + '\n\n' + \
            open('AUTHORS.rst', 'rb').read().decode('utf-8') + '\n\n' + \
            open('CHANGELOG.rst', 'rb').read().decode('utf-8')

setup(
    name='django-recaptcha',
    version='2.0.6',
    description='Django recaptcha form field/widget app.',
    long_description=long_desc,
    author='Praekelt Consulting',
    author_email='dev@praekelt.com',
    license='BSD',
    url='http://github.com/praekelt/django-recaptcha',
    packages=find_packages(),
    install_requires=[
        'django>1.11,<4.0',
    ],
    tests_require=[
        'tox',
    ],
    keywords=['django', 'reCAPTCHA', 'reCAPTCHA v2', 'reCAPTCHA v3'],
    include_package_data=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Django :: 3.0',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 2.1',
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 1.11',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    zip_safe=False,
)
