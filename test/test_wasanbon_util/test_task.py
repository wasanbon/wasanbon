# test for wasanbon/utils/task.py

import unittest
from unittest import mock
from unittest.mock import Mock

from threading import Event

from wasanbon.util import task


class TestPlugin(unittest.TestCase):

    def test_TimeoutTask__init__(self):
        """test for TimeoutTask.__init__"""
        # mock settings
        func_mock = Mock()
        test_var = 'var'
        # test
        inst = task.TimeoutTask(func_mock, test_var)
        self.assertEqual(inst._var, test_var)
        self.assertEqual(inst._func, func_mock)
        self.assertIsInstance(inst._stop_event, Event)

    def test_TimeoutTask_run(self):
        """test for TimeoutTask.run"""
        # mock settings
        func_mock = Mock()
        test_var = 'var'
        inst = task.TimeoutTask(func_mock, test_var)
        # test
        inst.run()
        func_mock.assert_called_once_with(test_var)

    @mock.patch('threading.Event.set')
    def test_TimeoutTask_quit(self, event_set_mock):
        """test for TimeoutTask.quit"""
        # mock settings
        func_mock = Mock()
        test_var = 'var'
        inst = task.TimeoutTask(func_mock, test_var)
        # test
        inst.quit()
        event_set_mock.assert_called_once()

    def test_task_with_wdt(self):
        """test for task_with_wdt"""
        # mock settings
        func_mock = Mock()
        # test
        test_var = 'var'
        test_interval = 1
        task.task_with_wdt(func_mock, test_var, test_interval)
        func_mock.assert_called_once_with(test_var)


if __name__ == '__main__':
    unittest.main()
