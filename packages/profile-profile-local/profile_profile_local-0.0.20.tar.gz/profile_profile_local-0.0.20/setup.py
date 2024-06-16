import setuptools

PACKAGE_NAME = "profile-profile-local"
package_dir = PACKAGE_NAME.replace("-", "_")

setuptools.setup(
    name=PACKAGE_NAME,
    version='0.0.20',  # https://pypi.org/project/profile-profile-local/
    author="Circles",
    author_email="info@circlez.ai",
    description="PyPI Package for Circles profile-profile-local Python",
    long_description="This is a package for sharing common profile-profile-local function used in different repositories",
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
    install_requires=["logger-local>=0.0.71",
                      "database-mysql-local>=0.0.120"
                      ]

)
