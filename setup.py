#!/usr/bin/env python
# Copyright Jean-Michel Philippe (c) 2007
#   <http://philipjm.free.fr/blog/>
#
# This is open source software released under the GPL license.
# The full text of this license is found in the file 'LICENSE',
# included with this source code package.
###################

# importations
from distutils.core import setup
from distutils.command.install_data import install_data
import os

# sub-class install_data and tell it to use the install_lib directory as its root install directory
class smart_install_data(install_data):
	def run(self):
		#need to change self.install_dir to the library dir
		install_cmd = self.get_finalized_command('install')
		self.install_dir = getattr(install_cmd, 'install_lib')
		return install_data.run(self)

# data files




# build archives
setup(
	name='whois',
	version='0.2',
	packages = ['whois'],
	package_dir = {'whois': ''},
	data_files=[
	],
	cmdclass = {'install_data':smart_install_data},
	description='Whois requester',
	author='Sebdraven',
	platforms='any',
	author_email="sebdraven@gmail.com",
	url='',
	license='GNU GPL v2',
	long_description="""


* IP searched on an Internet whois service


Full Internet whois queries may also be accessed.
""",
)
