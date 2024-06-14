from setuptools import setup, find_packages

setup(
    name='gvita',
    version='0.5.0',
    description='Little game based on Game of Life from John Conway',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='me15degrees',
    author_email='me15degrees@gmail.com',
    url='https://github.com/me15degrees/game-of-life',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    entry_points={
        'console_scripts': [
            'gvita=gvita.main:main',
        ],
    },
)
