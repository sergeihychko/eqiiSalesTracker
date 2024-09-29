import unittest as ut

from src import guidriver as gui


class TestSeller(ut.TestCase):

    def test_appExists(self):
        app = gui.GUIDriver()
        print(app)
        self.assertIsNotNone(app)

if __name__ == '__main__':
    ut.main()