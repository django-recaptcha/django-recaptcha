from setuptools import find_packages, setup

long_desc = (
    open("README.rst", "rb").read().decode("utf-8")
    + "\n\n"
    + open("AUTHORS.rst", "rb").read().decode("utf-8")
    + "\n\n"
    + open("CHANGELOG.rst", "rb").read().decode("utf-8")
)

setup(
    name="django-recaptcha429",
    version="2.1.0",
    description="Django recaptcha form field/widget app.",
    long_description=long_desc,
    long_description_content_type="text/x-rst",
    author="Andrew Chen Wang",
    author_email="acwangpython@gmail.com",
    license="BSD",
    url="http://github.com/Andrew-Chen-Wang/django-recaptcha429",
    packages=find_packages(),
    install_requires=["django"],
    tests_require=["tox"],
    keywords=["django", "reCAPTCHA", "reCAPTCHA v2", "reCAPTCHA v3"],
    include_package_data=True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Framework :: Django",
        "Framework :: Django :: 2.2",
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4.0",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    zip_safe=False,
)
