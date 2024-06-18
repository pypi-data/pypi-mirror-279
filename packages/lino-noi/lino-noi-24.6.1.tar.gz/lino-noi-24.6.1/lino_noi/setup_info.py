# -*- coding: UTF-8 -*-
# Copyright 2014-2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
# python -m unittest tests.test_packages

ATELIER_INFO = dict(
    nickname="noi",
    verbose_name="Lino Noi",
    # srcref_url='https://gitlab.com/lino-framework/cosi/blob/master/%s',
    intersphinx_urls=dict(docs="https://noi.lino-framework.org"))

SETUP_INFO = dict(
    name='lino-noi',
    version='24.6.1',
    install_requires=['lino-xl'],
    # tests_require=['pytest', 'mock'],
    test_suite='tests',
    description=("Manage support tickets and working time."),
    long_description="""\

- End-user documentation: https://using.lino-framework.org/apps/noi
- Demo site: https://noi1r.lino-framework.org
- Developer documentation: https://dev.lino-framework.org/specs/noi
- Source code: https://gitlab.com/lino-framework/noi
- Changelog: https://dev.lino-framework.org/changes
- Author: https://www.synodalsoft.net

""",
    author='Rumma & Ko Ltd',
    author_email='info@lino-framework.org',
    url="https://gitlab.com/lino-framework/noi",
    license_files=['COPYING'],
    classifiers="""\
Programming Language :: Python
Programming Language :: Python :: 3
Development Status :: 5 - Production/Stable
Environment :: Web Environment
Framework :: Django
Intended Audience :: Developers
Intended Audience :: System Administrators
Intended Audience :: Information Technology
Intended Audience :: Customer Service
License :: OSI Approved :: GNU Affero General Public License v3
Operating System :: OS Independent
Topic :: Software Development :: Bug Tracking
""".splitlines())

SETUP_INFO.update(packages=[
    str(n) for n in """
lino_noi
lino_noi.lib
lino_noi.lib.noi
lino_noi.lib.noi.fixtures
lino_noi.lib.contacts
lino_noi.lib.contacts.fixtures
lino_noi.lib.public
lino_noi.lib.trading
lino_noi.lib.trading.fixtures
lino_noi.lib.users
lino_noi.lib.users.fixtures
lino_noi.lib.products
lino_noi.lib.subscriptions
lino_noi.lib.groups
lino_noi.lib.cal
lino_noi.lib.cal.fixtures
lino_noi.lib.courses
lino_noi.lib.tickets
""".splitlines() if n
])

SETUP_INFO.update(
    message_extractors={
        'lino_noi': [
            ('**/cache/**', 'ignore', None),
            ('**.py', 'python', None),
            ('**.js', 'javascript', None),
            ('**/config/**.html', 'jinja2', None),
        ],
    })

SETUP_INFO.update(include_package_data=True, zip_safe=False)
# SETUP_INFO.update(package_data=dict())

# def add_package_data(package, *patterns):
#     l = SETUP_INFO['package_data'].setdefault(package, [])
#     l.extend(patterns)
#     return l

# l = add_package_data('lino_noi.lib.noi')
# for lng in 'de fr'.split():
#     l.append('locale/%s/LC_MESSAGES/*.mo' % lng)
