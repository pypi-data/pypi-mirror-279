import setuptools

PACKAGE_NAME = "profile-metrics-local"
package_dir = PACKAGE_NAME.replace("-", "_")

setuptools.setup(
    name=PACKAGE_NAME,
    version='0.0.14',  # https://pypi.org/project/profile-metrics-local/
    author="Circles",
    author_email="info@circlez.ai",
    description="PyPI Package for Circles profile-metrics-local Python",
    long_description="This Package implements CRUD operation of profile-metrics",
    long_description_content_type='text/markdown',
    url=f"https://github.com/circles-zone/{PACKAGE_NAME}-python-package",
    # packages=setuptools.find_packages(),
    packages=[package_dir],
    package_dir={package_dir: f'{package_dir}/src'},
    package_data={package_dir: ['*.py']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'database-mysql-local>=0.0.300',
        'logger-local>=0.0.135',
    ],
)
