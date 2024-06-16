import setuptools

PACKAGE_NAME = "storage-local"
PACKAGE_NAME_UNDERSCORE = PACKAGE_NAME.replace("-", "_")
package_dirs = ["aws_s3_storage_local"]

setuptools.setup(
    name=PACKAGE_NAME,
    version='0.1.43',  # https://pypi.org/project/storage-local/
    author="Circles",
    author_email="info@circlez.ai",
    description="PyPI Package for Circles Storage functions",
    long_description="This is a package for sharing common S3 functions used in different repositories",
    long_description_content_type="text/markdown",
    url=f"https://github.com/circles-zone/{PACKAGE_NAME}-python-package",
    packages=[f"{PACKAGE_NAME_UNDERSCORE}/{package_dir}" for package_dir in package_dirs],
    package_dir={f"{PACKAGE_NAME_UNDERSCORE}/{package_dir}": f'{package_dir}/src' for package_dir in package_dirs},
    package_data={f"{PACKAGE_NAME_UNDERSCORE}/{package_dir}": ['*.py'] for package_dir in package_dirs},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    install_requires=["requests",
                      "boto3>=1.28.44",
                      "database-mysql-local>=0.0.107",
                      "logger-local>=0.0.135",
                      "user-context-remote>=0.0.75",
                      "python-sdk-remote>=0.0.93"]
)
