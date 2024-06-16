import setuptools 

PACKAGE_NAME = 'profile-reddit-restapi-imp-local'
package_dir = PACKAGE_NAME.replace("-", "_")

setuptools.setup(
    name=PACKAGE_NAME,
    version='0.0.37',  # https://pypi.org/project/profile-reddit-restapi-imp-local/
    author="Circles",
    author_email="info@circlez.ai",
    url=f"https://github.com/circles-zone/{PACKAGE_NAME}-python-package",
    packages=[package_dir],
    package_dir={package_dir: f'{package_dir}/src'},
    package_data={package_dir: ['*.py']},
    long_description="Profile Reddit REST API Implementation Local Python Package",
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'praw>=7.4.0',
        'tqdm>=4.64.1',
        'requests',
        'data-source-local',
        'entity-type-local>=0.0.13',
        'importer-local>=0.0.43',
        'location-local',
        'logger-local>=0.0.93',
        'profile-local>=0.0.61',
        'group-remote>=0.0.105',
        'python-sdk-remote>=0.0.65',
        'user-context-remote>=0.0.54',
    ],
)
