import setuptools

PACKAGE_NAME = "location-profile-local"
package_dir = PACKAGE_NAME.replace("-", "_")

setuptools.setup(
    name=PACKAGE_NAME,
    version='0.0.53',  # https://pypi.org/project/location-profile-local/
    author="Circles",
    author_email="info@circlez.ai",
    description="PyPI Package for Circles location-profile-local Local Python",
    long_description="This is a package for sharing common functions of operational hours CRUD to location_profile database used in different repositories",
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
        'database-mysql-local>=0.0.180',
        'language-remote',
        'logger-local>=0.0.71',
        'python-sdk-remote',
    ],
)
