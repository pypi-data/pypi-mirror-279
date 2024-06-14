import balder
from ..balderglob import RuntimeObserver


class FeatureI(balder.Feature):

    def do_something(self):
        RuntimeObserver.add_entry(
            __file__, FeatureI, FeatureI.do_something, "enter `FeatureI.do_something`", category="feature")


class FeatureIChild(FeatureI):

    def do_something(self):
        RuntimeObserver.add_entry(
            __file__, FeatureIChild, FeatureIChild.do_something,
            "enter `FeatureIChild.do_something`", category="feature")


class FeatureII(balder.Feature):

    def do_something(self):
        RuntimeObserver.add_entry(
            __file__, FeatureII, FeatureII.do_something, "enter `FeatureII.do_something`", category="feature")


class FeatureNewI(balder.Feature):

    def do_something(self):
        RuntimeObserver.add_entry(
            __file__, FeatureNewI, FeatureNewI.do_something,
            "enter `FeatureNewI.do_something`", category="feature")


class FeatureOfRelevanceLvl1(balder.Feature):
    """this feature will be used in scenario"""

    class VDeviceWithI(balder.VDevice):
        i = FeatureI()

    class VDeviceWithII(balder.VDevice):
        i = FeatureII()

    def do_something(self):
        RuntimeObserver.add_entry(
            __file__, FeatureOfRelevanceLvl1, FeatureOfRelevanceLvl1.do_something,
            "enter `FeatureOfRelevanceLvl1.do_something`", category="feature")

