# coding: utf8
""" 
@software: PyCharm
@author: Lionel Johnson
@contact: https://fairy.host
@organization: https://github.com/FairylandFuture
@since: 2024-05-09 16:38:27 UTC+8
"""

import os.path
import setuptools
import sys
import requests

from typing import Literal
import subprocess
from datetime import datetime

_MARK_TYPE = Literal["release", "test", "alpha", "beta"]

_ROOT_PATH = os.path.abspath(os.path.dirname(__file__))
_MAJOR = 1
_SUB = 0
_STAGE = 0
_MARK: _MARK_TYPE = "release"

if sys.version_info < (3, 8):
    sys.exit("Python 3.8 or higher is required.")


class InstallDependenciesCommand(setuptools.Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        command = "python -m pip install --force git+https://github.com/imba-tjd/pip-autoremove@ups"
        subprocess.call(command, shell=True)


class PackageInfo(object):
    """
    Public package

    :param major: major num
    :type major: int
    :param sub: sub num
    :type sub: int
    :param stage: stage num
    :type stage: int
    :param revise: revise num
    :type revise: int
    :param mark: version mark
    :type mark: str
    """

    def __init__(self, major: int, sub: int, stage: int, mark: _MARK_TYPE):
        self.__major = self.__paramscheck(major, int)
        self.__sub = self.__paramscheck(sub, int)
        self.__stage = self.__paramscheck(stage, int)
        self.__revise = self.__get_github_commit_count()

        if not mark.lower() in _MARK_TYPE.__args__:
            raise TypeError(f"Param: mark type error, mark must in {_MARK_TYPE.__args__}.")

        self.__mark = mark

    @property
    def name(self):
        return "PyFairylandFuture"

    @property
    def author(self):
        return "Lionel Johnson"

    @property
    def email(self):
        return "fairylandfuture@outlook.com"

    @property
    def url(self):
        return "https://github.com/PrettiestFairy/pypi-fairylandfuture"

    @property
    def version(self):
        # if len(self.__revise.__str__()) < 5:
        #     nbit = 5 - len(self.__revise.__str__())
        #     self.__revise = "".join((("0" * nbit), self.__revise.__str__()))
        # else:
        #     self.__revise = self.__revise.__str__()
        self.__revise = self.__revise.__str__()

        date_str = datetime.now().date().__str__().replace("-", "")
        revise_after = "-".join((self.__revise.__str__(), date_str))
        release_version = ".".join((self.__major.__str__(), self.__sub.__str__(), self.__stage.__str__()))

        if self.__mark == "release":
            version = release_version
        elif self.__mark == "test":
            version = ".".join((release_version, "".join(("rc.", revise_after))))
        elif self.__mark == "alpha":
            version = ".".join((release_version, "".join(("alpha.", revise_after))))
        elif self.__mark == "beta":
            version = ".".join((release_version, "".join(("beta.", revise_after))))
        else:
            version = ".".join((release_version, "".join(("rc.", revise_after))))

        return version

    @property
    def description(self):
        return "personally developed Python library."

    @property
    def long_description(self):
        with open(os.path.join(_ROOT_PATH, "README.md"), "r", encoding="UTF-8") as FileIO:
            long_description = FileIO.read()

        return long_description

    @property
    def long_description_content_type(self):
        return "text/markdown"

    @property
    def packages_include(self):
        include = ("fairylandfuture", "fairylandfuture.*")

        return include

    @property
    def packages_exclude(self):
        exclude = (
            "bin",
            "conf",
            "deploy",
            "docs",
            "scripts",
            "temp",
            "test",
            # "fairylandfuture/test",
        )

        return exclude

    @property
    def packages_data(self):
        data = {"": ["*.txt", "*.rst", "*.md"], "fairylandfuture": ["conf/*"]}

        return data

    @property
    def fullname(self):
        return self.name + self.version

    @property
    def python_requires(self):
        return ">=3.8"

    @property
    def keywords(self):
        return [
            "fairyland",
            "Fairyland",
            "pyfairyland",
            "PyFairyland",
            "fairy",
            "Fairy",
            "fairylandfuture",
            "PyFairylandFuture",
            "FairylandFuture",
        ]

    @property
    def include_package_data(self):
        return True

    @property
    def classifiers(self):
        results = [
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.11",
            "Programming Language :: Python :: 3.12",
            "Programming Language :: Python :: Implementation :: CPython",
            "Programming Language :: Python :: Implementation :: PyPy",
            "Programming Language :: SQL",
            "Framework :: Django :: 2",
            "Framework :: Django :: 3",
            "Framework :: Django :: 4",
            "Framework :: Flask",
            "Framework :: FastAPI",
            "Framework :: Flake8",
            "Framework :: IPython",
            "Framework :: Jupyter",
            "Framework :: Scrapy",
            "Natural Language :: English",
            "Natural Language :: Chinese (Simplified)",
            "Operating System :: Microsoft :: Windows :: Windows 11",
            "Operating System :: POSIX :: Linux",
            "Operating System :: POSIX :: Linux",
            "Topic :: Software Development :: Libraries :: Python Modules",
            "Topic :: Software Development :: Libraries :: Application Frameworks",
            "Topic :: Software Development :: Version Control :: Git",
            "Topic :: System :: Operating System Kernels :: Linux",
            "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        ]

        return results

    @property
    def install_requires(self):
        results = [
            "setuptools",
            "loguru",
            "python-dateutil",
            "requests",
            "pymysql",
            "pyyaml",
            "netifaces",
            "cryptography",
            # "pip-review",
            # "pip-autoremove",
            # "python-dotenv",
            # "psycopg2-binary",
            # "fake-useragent",
            # "tornado",
            # "pandas",
            # "django",
            # "django-stubs",
            # "djangorestframework",
            # "django-cors-headers",
        ]
        return results

    @property
    def cmdclass(self):
        results = {
            "install_dependencies": InstallDependenciesCommand,
        }
        return results

    @staticmethod
    def __paramscheck(param, _type):
        if not isinstance(param, _type):
            raise TypeError(f"{param} type error.")

        return param

    @staticmethod
    def __get_local_gitcommitcr():
        try:
            with open(os.path.join(_ROOT_PATH, "conf", "publish", "gitcommitrc"), "r", encoding="UTF-8") as FileIO:
                commit_count = FileIO.read()
            return int(commit_count)
        except Exception as err:
            print(f"Error: {err}")
            return 0

    @classmethod
    def __get_github_commit_count(cls):
        try:
            url = "https://raw.githubusercontent.com/PrettiestFairy/pypi-fairylandfuture/Pre-release/conf/publish/gitcommitrc"
            response = requests.get(url)
            if response.status_code == 200:
                commit_count = int(response.text)
                return commit_count
            else:
                return cls.__get_local_gitcommitcr()
        except Exception as err:
            print(err)
            return cls.__get_local_gitcommitcr()


package = PackageInfo(_MAJOR, _SUB, _STAGE, _MARK)

setuptools.setup(
    name=package.name,
    fullname=package.fullname,
    keywords=package.keywords,
    version=package.version,
    author=package.author,
    author_email=package.email,
    description=package.description,
    long_description=package.long_description,
    long_description_content_type=package.long_description_content_type,
    url=package.url,
    # license="AGPLv3+",
    # packages=setuptools.find_packages(include=package.packages_include, exclude=package.packages_exclude),
    packages=setuptools.find_packages(exclude=package.packages_exclude),
    package_data=package.packages_data,
    include_package_data=package.include_package_data,
    classifiers=package.classifiers,
    python_requires=package.python_requires,
    install_requires=package.install_requires,
    cmdclass=package.cmdclass,
)
