"""
module containing all unittest classes for the Seller application
"""
import unittest as ut

from src import seller as driver


class TestSeller(ut.TestCase):
    """
    class containing the unittest methods for the Seller app
    """

    def test_appExists(self):
        app = driver.Seller()
        print(app)
        self.assertIsNotNone(app)

    def test_guiExists(self):
        app = driver.Seller()
        gui = app.build()
        print(gui)
        self.assertIsNotNone(gui)

    def test_widgetsExists(self):
        """
        test that all the gui form has all it's elements
        :return:
        """
        app = driver.Seller()
        gui = app.build()
        widgets = gui.root.winfo_children()
        print(widgets)
        self.assertIsNotNone(widgets)

        self.assertEqual(len(widgets),7)

        for i in widgets:
            self.assertIsNotNone(i)


if __name__ == '__main__':
    ut.main()