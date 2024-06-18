# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'source/packages'}

packages = \
['mojo', 'mojo.waiting']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'mojo-waiting',
    'version': '1.3.4',
    'description': 'Automation Mojo Waiting Module',
    'long_description': '\n=============================================\nAutomation Mojo Waiting Module - mojo-waiting\n=============================================\n\nThis package provides support for enhanced context based waiting.  This module will greatly enhance the\ninformation presented when a wait timeout occurs.  Wait contexts are particularly useful for distributed\nautomation.  Distributed automation scenarios required lots of wait loops in order wait for the effects\nof an effect to distributed throughout the distributed system.\n\nThe waiting code patterns used are designed to present the best results in test stacktraces presented\nwhen a wait fails.  This makes the `mojo.waiting` module perfect for use with\ntest frameworks such as `pytest` and `testplus` that show code context in the error\nreport stack traces.\n\nAnother important aspect of the `mojo.waiting` module is that it uses `datetime`\ntimestamps and `timespan` for lengths of time so timeouts in error reporting are easier\nto interpret.\n\n.. code::\n\n    Traceback (most recent call last):\n    File "/home/myron/repos/mojo.waiting/source/tests/test_wait_for_it.py", line 97, in test_basic_wait_for_it_timeout\n        future.result()\n    File "/usr/lib/python3.10/concurrent/futures/_base.py", line 451, in result\n        return self.__get_result()\n    File "/usr/lib/python3.10/concurrent/futures/_base.py", line 403, in __get_result\n        raise self._exception\n    File "/usr/lib/python3.10/concurrent/futures/thread.py", line 58, in run\n        result = self.fn(*self.args, **self.kwargs)\n    File "/home/myron/repos/mojo.waiting/source/tests/test_wait_for_it.py", line 88, in wait_task\n        ctxwait.wait_for_it(wait_helper, interval=.5, timeout=2)\n    File "/home/myron/repos/mojo.waiting/source/packages/ctxwait/waiting.py", line 103, in wait_for_it\n        raise toerr\n    TimeoutError: Timeout waiting for \'wait_helper\':\n        timeout=2 start_time=2023-03-13 14:57:29.860302, end_time=2023-03-13 14:57:31.860302 now_time=2023-03-13 14:57:31.863681 time_diff=0:00:02.003379\n\n\nThe following is an example of how the `mojo.waiting` module is used.\n\n.. code:: python\n\n    from ctxwait import WaitContext, wait_for_it\n\n    def some_wait_helper(wctx: WaitContext):\n        finished = False\n\n        // TODO: Check if something is finished, the code and variables used\n        //       here will show up in any tracebacks from pytest or testplus\n        //       because the timeout is being raised in the appropriate scope.\n\n        if not finished and wctx.final_attempt:\n            whatfor = "Test timeout"\n            toerr = wctx.create_timeout(whatfor)\n            raise toerr\n\n        return finished\n\n    wait_for_it(some_wait_helper)\n\n\nThe `wait_for_it` method has many different parameters that can be used to override the\nbehavior of the wait loop.\n\n.. code:: python\n\n    def wait_for_it(looper: WaitCallback, *largs, what_for: Optional[str]=None, delay: float=DEFAULT_WAIT_DELAY,\n                interval: float=DEFAULT_WAIT_INTERVAL, timeout: float=DEFAULT_WAIT_TIMEOUT,\n                lkwargs: Dict[Any, Any]={}, wctx: Optional[WaitContext]=None):\n        """\n            Provides for convenient mechanism to wait for criteria to be met before proceeding.\n\n            :param looper: A callback method that is repeatedly called while it returns `False` up-to\n                        the end of a timeout period, and that will return `True` if a waited on\n                        condition is met prior to a timeout condition being met.\n            :param largs: Arguements to pass to the looper callback function.\n            :param what_for: A breif description of what is being waited for.\n            :param delay: An initial time delay to consume before beginning the waiting process.\n            :param interval: A period of time to delay between rechecks of the wait conditon\n            :param timeout: The maximum period of time in seconds that should be waited before timing out.\n            :param lkwargs: Additional keyword arguments to pass to the looper function\n\n            :raises TimeoutError: A timeout error with details around the wait condition.\n\n            ..note: The \'delay\', \'interval\' and \'timeout\' parameters will be ignored if the \'wctx\' parameter\n                    is passed as the wctx (WaitContext) parameter includes these values with it.\n        """\n        ...\n\nThe `wait_for_it` function must be passed a method that follows the `WaitCallback` protocol.  The function\ncan have variable arguments and keyword arguements but the first parameter to the `WaitCallback` method\nmust be a `WaitContext` object.\n\n==========\nReferences\n==========\n\n- `User Guide <userguide/userguide.rst>`_\n- `Coding Standards <userguide/10-00-coding-standards.rst>`_\n\n',
    'author': 'Myron Walker',
    'author_email': 'myron.walker@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'http://automationmojo.com',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
