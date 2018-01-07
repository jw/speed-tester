import os
from setuptools import setup

from pipenv.project import Project
from pipenv.utils import convert_deps_to_pip

here = os.path.abspath(os.path.dirname(__file__))

project = Project(chdir=False).parsed_pipfile
requirements = convert_deps_to_pip(project['packages'], r=False)
test_requirements = convert_deps_to_pip(project['dev-packages'], r=False)

setup(
    name="speed-tester",
    version="0.1.13",
    description="Test the speed of your network connection and "
                "send the result to a monitor.",
    url="https://github.com/jw/speed-tester",
    author='Jan Willems',
    author_email="jw@elevenbits.com",
    license="MIT",
    py_modules=['speedtester', 'speedscheduler'],
    install_requires=requirements,
    python_requires='~=3.6',
    entry_points={
        'console_scripts': [
            'speedtester=speedtester:main',
            'speedscheduler=speedscheduler:main',
        ]
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'Natural Language :: Dutch',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: System :: Networking',
    ],
)
