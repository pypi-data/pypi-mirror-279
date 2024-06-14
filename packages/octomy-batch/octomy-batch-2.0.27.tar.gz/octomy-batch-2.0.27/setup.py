#!/usr/bin/env python
from octomy.utils.setup import megasetup
import logging
import os
import pprint
from setuptools import setup

logger = logging.getLogger(__name__)



source_data = {
	  "base_name": "batch"
	, "group_base_name": "octomy"
	, "keywords": [ "python3", "batch", "processing", "async" ]
	, "cwd": os.path.dirname(os.path.abspath(__file__))
	, "executable_package": 'batch'
	, "executable_name": 'octomy-batch'
	, "debug": True
}

package = megasetup(source_data = source_data)

setup(**package)




'''
package = {
	  "name": package_name
	, "version": get_version_string()
	, "author": author_name
	, "author_email": author_email
	, "maintainer": author_name
	, "maintainer_email": author_email
	, "description": short_description
	, "license": get_license_name()
	, "platforms": ["Linux"]
	, "keywords": "software"
	, "url": f"https://gitlab.com/{group_base_name}/{base_name}"
	# We use namespace packages to allow multiple packages to use the octomy prefix
	# We omit __init__.py tio accomplish this
	# See https://packaging.python.org/en/latest/guides/packaging-namespace-packages/
	, "namespace_packages": modules
	, "packages": get_packages()
	, "package_dir": {'': package_dir}
	, "long_description": read_file(readme_file)
	, "long_description_content_type": "text/markdown"
	, "setup_requires": setup_requirements
	, "zip_safe": True
	# Allow flexible deps for install
	, "install_requires": read_requirements_file("requirements/requirements.in")
	# Use flexible deps for testing
	, "tests_require": read_requirements_file("requirements/test_requirements.in")
	, "test_suite": os.path.join(package_dir, "tests")
	, "python_requires": ">=" + python_version
	# NOTE: "data_files" is deprecated
	# NOTE: "package_data" need to reside inside a package, in other words a directory with __init__.py
	, "package_data": get_package_data()
	, "include_package_data": True
	, "classifiers": get_classifiers()
}
'''
