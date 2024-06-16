import setuptools

PACKAGE_NAME = "user-local"
package_dir = PACKAGE_NAME.replace("-", "_")

# used by python -m build
# python -m build needs pyproject.toml or setup.py
setuptools.setup(
    name=PACKAGE_NAME,
    version='0.0.19',  # https://pypi.org/project/user-local/
    author="Circles",
    author_email="info@circlez.ai",
    description="PyPI Package for Circles Python user Local Python",
    long_description="This is a package for user local python",
    long_description_content_type="text/markdown",
    url=f"https://github.com/circles-zone/{PACKAGE_NAME}-python-package",
    packages=[package_dir],
    package_dir={package_dir: f'{package_dir}/src'},
    package_data={package_dir: ['*.py']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "database-mysql-local>=0.0.113",
        "logger-local>=0.0.46",
        "database-infrastructure-local>=0.0.9",
        "email-address-local",
        "location-local",
    ]
)
