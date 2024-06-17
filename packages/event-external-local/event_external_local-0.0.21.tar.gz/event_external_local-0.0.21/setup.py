import setuptools

PACKAGE_NAME = "event-external-local"
package_dir = PACKAGE_NAME.replace("-", "_")

setuptools.setup(
    name=PACKAGE_NAME,  # https://pypi.org/project/event-external-local/
    version='0.0.21',
    author="Circles",
    author_email="info@circlez.ai",
    description="PyPI Package for Circles event-external-local Python",
    long_description="PyPI Package for Circles event-external-local Python",
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
        'logger-local>=0.0.135',
        'database-mysql-local>=0.0.290',
        'python-sdk-remote>=0.0.93',
    ],
)
