from setuptools import find_packages, setup  # type: ignore

setup(
    name='pixiv-tag-analyzer',
    version='0.3',
    description="Collects information on any pixiv user's posts and bookmarks, and explores the user's sexuality from the tags.",
    description_content_type='',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/eggplants/pixiv-tag-analyzer',
    author='eggplants',
    packages=find_packages(),
    python_requires='>=3.8',
    include_package_data=True,
    license='MIT',
    install_requires=open('requirements.txt').read().rstrip().split('\n'),
    entry_points={
        'console_scripts': [
            'pta=pta.main:main'
        ]
    }
)
