import unittest


class AlwaysTeardownTestCase(unittest.TestCase):
    """
    SafeTestCase makes sure that tearDown / cleanup methods are always run when
    They should be.
    """

    def run(self, result=None):
        test_method = getattr(self, self._testMethodName)
        wrapped_test = self._cleanup_wrapper(test_method, KeyboardInterrupt)
        setattr(self, self._testMethodName, wrapped_test)

        self.setUp = self._cleanup_wrapper(self.setUp, BaseException)

        return super().run(result)

    def _cleanup_wrapper(self, method, exception):
        def wrapped(*args, **kwargs):
            try:
                return method(*args, **kwargs)
            except exception:
                self.tearDown()
                self.doCleanups()
                raise

        return wrapped

__all__=[

]