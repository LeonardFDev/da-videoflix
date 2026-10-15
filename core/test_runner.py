from django.test.runner import DiscoverRunner

class ContentTestProtocolDeletedRunner(DiscoverRunner):
    """Before running a test, this is executed"""

    def setup_test_environment(self, **kwargs):
        """The content of test_protocol.log will be deleted"""
        open("test_protocol.log", "w").close()

        super().setup_test_environment(**kwargs)
