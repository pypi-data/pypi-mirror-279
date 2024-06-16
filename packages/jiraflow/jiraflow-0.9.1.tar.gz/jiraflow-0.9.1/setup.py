from setuptools import setup, find_packages

setup(
    name='jiraflow',
    version='0.9.1',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'jiraflow': ["ExampleConfig.json"],
    },
    install_requires=[
        "argparse", "flowmetricscsv", "montecarlocsv", "requests"
    ],
    entry_points={
        'console_scripts': [
            'jiraflow=jiraflow.main:main',
        ],
    },
    author='Benjamin Huser-Berta',
    author_email='benj.huser@gmail.com',
    description='A package to generate flow metrics charts and run Monte Carlo Simulation based Forecasts based on JQL queries against Jira.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://letpeople.work',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
