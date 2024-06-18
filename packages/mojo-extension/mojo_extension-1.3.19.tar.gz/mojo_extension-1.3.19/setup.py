# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'source/packages'}

packages = \
['mojo', 'mojo.extension']

package_data = \
{'': ['*']}

install_requires = \
['mojo-collections>=1.3.16,<1.4.0', 'mojo-startup>=1.3.11,<1.4.0']

setup_kwargs = {
    'name': 'mojo-extension',
    'version': '1.3.19',
    'description': 'Automation Mojo Extension Package',
    'long_description': '=================================\nAutomation Mojo Extension Package\n=================================\n\nThis is a python package that provides a mechanism for extending other python packages.  This\npackage is different from other python extension packages in that it uses the python Protocol\ntyping in order to query module hierarchies for extensions.\n\n\n===============================\nDeclaring an Extension Protocol\n===============================\n\nFor example, if we want to be able to create instance of object like these from a factory.\n\n.. code:: python\n\n    class Hey:\n        def __str__(self):\n            return "Hey"\n\n    class Ho:\n        def __str__(self):\n            return "Ho"\n\n    \n    # The following class defines a protocol that defines an extenstion type.\n    # Extensions \n\n    class MyExtTypeProtocol(ExtProtocol):\n\n        ext_protocol_name = "mojo-myextypeprotocol"\n\n        @classmethod\n        def give_me_a_hey(cls):\n            ...\n\n        @classmethod\n        def give_me_a_ho(cls):\n            ...\n\n==================================\nImplementing an Extension Protocol\n==================================\n\nThe code below is implementing the extension protocol defined above.  When a class\nimplements an extension protocol, it will inherit from the protocol it is implementing.\nBy inheriting from the protocol, it pulls in the `ext_protocol_name` variable which\nensures that the derived type is declared to implement a given protocol.\n\nAnother important thing to look at in the code below is the class variable `PRECEDENCE`.\nThe `PRECEDENCE` number indicates to the SuperFactory which extensions to return when\nan extension is queried based on precedence of overload and relevance.  The higher number\nprecedence is considered by the SuperFactory to have the most relevance.\n\n.. code:: python\n\n    class MyExtTypeFactory(ExtFactory, MyExtTypeProtocol):\n\n        PRECEDENCE = 10\n\n        @classmethod\n        def give_me_a_hey(cls):\n            return Hey\n        \n        @classmethod\n        def give_me_a_ho(cls):\n            return Ho\n\n\n===================================\nConfiguration for Custom Extensions\n===================================\n\nIn order to be able to extend packages, you must tell the `mojo-extension` code where\nthe root packages are that need to be searched for extension factories.  Then what we\ndo is we register the root modules under which the factory types will be found.\n\n---------------------------------------------------------------\nSetting the MJR_CONFIGURED_FACTORY_MODULES Variable from Python\n---------------------------------------------------------------\n\n.. code:: python\n\n    from mojo.extension.extensionconfiguration import ExtensionConfiguration\n    from mojo.extension.wellknown import ConfiguredSuperFactorySingleton\n\n    ExtensionConfiguration.MJR_CONFIGURED_FACTORY_MODULES = [\n            "mypkg.factories",\n        ]\n\n---------------------------------------------------------------\nSetting the MJR_CONFIGURED_FACTORY_MODULES Environment Variable\n---------------------------------------------------------------\n\n.. code::\n    \n    MJR_CONFIGURED_FACTORY_MODULES=mypkg.a.factories,mypkg.b.factories\n\n----------------------------------------------------------------\nSetting the MJR_CONFIGURED_FACTORY_MODULES in the Startup Config\n----------------------------------------------------------------\n\n.. code::\n    \n    [MOJO-EXTENSION]\n    MJR_CONFIGURED_FACTORY_MODULES=mypkg.a.factories,mypkg.b.factories\n\n========================\nLoading Custom Factories\n========================\n\nIn order to load extension factories, we utilize the `ConfiguredSuperFactorySingleton` singleton\nobject that is maintained by the `mojo-extension` package.  You can get a reference to the super\nfactory singleton by using code similar to the code below:\n\n.. code:: python\n\n    from mojo.extension.wellknown import ConfiguredSuperFactorySingleton\n\n    superfactory = ConfiguredSuperFactorySingleton()\n\n\nThen when we want to get the type from the extension, we utilize the protocol that\nwas declared and ask for the type using the function on the protocol that will return\nthe type.\n\n.. code:: python\n\n    hey_type = self._super_factory.get_override_types_by_order(MyExtTypeProtocol.give_me_a_hey)\n    ho_type = self._super_factory.get_override_types_by_order(MyExtTypeProtocol.give_me_a_ho)\n\n    hey = hey_type()\n    ho = ho_type()\n\n    print("")\n    print(f"{hey}... {ho}... {hey}... {ho}...")\n\n\n==========\nReferences\n==========\n\n- `User Guide <userguide/userguide.rst>`_\n- `Coding Standards <userguide/10-00-coding-standards.rst>`_\n',
    'author': 'Myron Walker',
    'author_email': 'myron.walker@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'http://automationmojo.com',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
