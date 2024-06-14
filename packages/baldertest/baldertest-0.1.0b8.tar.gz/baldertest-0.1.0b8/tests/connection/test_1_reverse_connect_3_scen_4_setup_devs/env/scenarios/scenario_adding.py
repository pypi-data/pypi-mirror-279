import balder
from ..lib.features import AddCalculateFeature, ProvidesANumberFeature


class ScenarioAdding(balder.Scenario):

    @balder.connect("NumberOneDevice", over_connection=balder.Connection)
    @balder.connect("NumberTwoDevice", over_connection=balder.Connection)
    class Calculator(balder.Device):
        # we could add vDevices here later too -> f.e. `NumberOne="NumberOneDevice", NumberTwo="NumberTwoDevice"`
        adds = AddCalculateFeature()

    class NumberOneDevice(balder.Device):
        number = ProvidesANumberFeature()

    class NumberTwoDevice(balder.Device):
        number = ProvidesANumberFeature()

    def test_add_two_numbers(self):
        self.NumberOneDevice.number.set_number(3)
        self.NumberTwoDevice.number.set_number(4)

        self.NumberOneDevice.number.sends_the_number()
        self.NumberTwoDevice.number.sends_the_number()

        self.Calculator.adds.get_numbers()
        result = self.Calculator.adds.add_numbers()
        assert result == 7, "result is not as expected"
