from setuptools import find_packages, setup

long_desc = open("README.md").read() + "\n\n" + open("AUTHORS.md").read()

setup(
    name="django-recaptcha",
    version="4.0.0",
    description="Django recaptcha form field/widget app.",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    author="Torchbox and individual contributors",
    author_email="hello@torchbox.com",
    license="BSD",
    url="https://github.com/torchbox/django-recaptcha",
    project_urls={
        "Changelog": "https://github.com/torchbox/django-recaptcha/blob/main/CHANGELOG.md",
        "Issue Tracker": "https://github.com/torchbox/django-recaptcha/issues",
        "Discussions": "https://github.com/torchbox/django-recaptcha/discussions",
    },
    packages=find_packages(),
    install_requires=["django"],
    keywords=["django", "reCAPTCHA", "reCAPTCHA v2", "reCAPTCHA v3"],
    include_package_data=True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Framework :: Django",
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4.1",
        "Framework :: Django :: 4.2",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    zip_safe=False,
)
