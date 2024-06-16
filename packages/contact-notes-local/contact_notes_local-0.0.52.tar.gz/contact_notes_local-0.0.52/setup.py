import setuptools

PACKAGE_NAME = "contact-notes-local"
package_dir = PACKAGE_NAME.replace("-", "_")

setuptools.setup(
    name=PACKAGE_NAME,
    version='0.0.52',  # https://pypi.org/project/contact-notes-local/
    author="Circles",
    author_email="info@circlez.ai",
    description="PyPI Package for Circles contact-notes-local Python",
    long_description="PyPI Package for Circles contact-notes-local Python",
    long_description_content_type='text/markdown',
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
        'database-infrastructure-local>=0.0.20',
        'text-block-local>=0.0.9',
        'contact-group-local>=0.0.7',
        'action-items-local>=0.0.1',
        'logger-local>=0.0.135',
        'user-context-remote>=0.0.75',
        'database-mysql-local>=0.0.290',
        'profile-local>=0.0.61',
        'language-remote>=0.0.20',
    ],
)
