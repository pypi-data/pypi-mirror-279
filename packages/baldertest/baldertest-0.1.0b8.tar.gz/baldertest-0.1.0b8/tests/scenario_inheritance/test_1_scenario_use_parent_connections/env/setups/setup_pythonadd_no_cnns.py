import balder
from ..lib.connections import MySimplySharedMemoryConnection
from ..lib.utils import SharedObj
from .features_setup import PyAddCalculate, PyAddProvideANumber


class SetupPythonAddNoCnns(balder.Setup):

    class Calculator(balder.Device):
        calc = PyAddCalculate()

    class NumberProvider1(balder.Device):
        n = PyAddProvideANumber()

    class NumberProvider2(balder.Device):
        n = PyAddProvideANumber()

    @balder.fixture(level="testcase")
    def cleanup_memory(self):
        SharedObj.shared_mem_list = []
