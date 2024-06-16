import setuptools

PACKAGE_NAME = "visibility-local"
package_dir = PACKAGE_NAME.replace("-", "_")

setuptools.setup(
    name=PACKAGE_NAME,
    version='0.0.4',  # https://pypi.org/project/visibility-local/
    author="Circles",
    author_email="info@circlez.ai",
    description="PyPI Package for Circles visibility-local Python",
    long_description="PyPI Package for Circles visibility-local Python",
    long_description_content_type='text/markdown',
    url=f"https://github.com/circles-zone/{PACKAGE_NAME}-python-package",  # https://pypi.org/project/<project-name>/
    # packages=setuptools.find_packages(),
    packages=[package_dir],
    package_dir={package_dir: f'{package_dir}/src'},
    package_data={package_dir: ['*.py']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    install_requires=[],
)
