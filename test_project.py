import unittest
from project import Plates, Dumbbell, Pin


class TestPlates(unittest.TestCase):
    def setUp(self):
        barbs = [
            {"w": "40", "u": "kg"},
            {"w": "25", "u": "kg"},
            {"w": "50", "u": "kg"},
            {"w": "100", "u": "kg"},
            {"w": "210", "u": "kg"},
            {"w": "60", "u": "kg"},
            {"w": "225", "u": "lb"},
            {"w": "135", "u": "lb"},
            {"w": "150.725", "u": "lb"},
        ]

        self.equips = []  # List to hold instances of Plates objects

        for weight_dict in barbs:
            equip = Plates(weight_dict["w"], weight_dict["u"], "barbell")
            self.equips.append(equip)
            # append to equips a Plates object that has "w" as weight and "u" as unit

        # plate-loaded machines
        self.machine1 = Plates("20", "kg")

        # weight too low -> sys.exit
        self.error1 = Plates("25", "kg", "barbell")
        self.error2 = Plates("35", "lb", "barbell")
        self.error3 = Plates("0", "lb", "barbell")
        self.error4 = Plates("20", "kg", "barbell")

    def test_table_test(self):
        # GPT
        test_cases = {
            (40, "kg"): [20, 30],
            (25, "kg"): [20],
            (50, "kg"): [25, 35, 40],
            (100, "kg"): [60, 75, 85],
            (210, "kg"): [60, 100, 140, 175],
            (60, "kg"): [30, 45, 50],
            (225, "lb"): [135, 165, 190],
            (135, "lb"): [70, 100, 110],
            (150.725, "lb"): [80, 110, 125],
        }

        for equip in self.equips:
            key = (equip.weight, equip.unit)
            self.assertEqual(
                equip.table_test(equip.to_warmups()), test_cases.get(key, [])
            )

        self.assertEqual(self.machine1.table_test(self.machine1.to_warmups()), [10, 15])

        with self.assertRaises(SystemExit):
            self.error1.table_test(self.error1.to_warmups())
            self.error2.table_test(self.error2.to_warmups())
            self.error3.table_test(self.error3.to_warmups())
            self.error4.table_test(self.error4.to_warmups())

    def test_plate_it(self):
        self.plate1 = Plates("35", "kg", "barbell")
        self.plate2 = Plates("290", "lb", "barbell")

        self.assertEqual(self.plate1.plate_it(self.plate1.weight), "5\n2.5")
        self.assertEqual(self.plate1.plate_it(155), "3 x 20\n5\n2.5")
        self.assertEqual(self.plate2.plate_it(290), "2 x 45\n25\n5\n2.5")
        self.assertEqual(self.plate2.plate_it(210), "45\n35\n2.5")
        self.assertEqual(self.plate2.plate_it(90), "2 x 10\n2.5")


class TestDumbbell(unittest.TestCase):
    def setUp(self):
        self.db1 = Dumbbell("25", "lb")
        self.db2 = Dumbbell("10", "lb")
        self.db3 = Dumbbell("100", "lb")

    def test_table_test(self):
        self.assertEqual(self.db1.table_test(self.db1.to_warmups()), [12, 17.5, 20])
        self.assertEqual(self.db2.table_test(self.db2.to_warmups()), [5, 8])
        self.assertEqual(self.db1.table_test(self.db3.to_warmups()), [55, 75, 85])


class TestPin(unittest.TestCase):
    def setUp(self):
        self.pin1 = Pin("12.5", "lb")
        self.pin2 = Pin("18", "lb")
        self.pin3 = Pin("30", "kg")

    def test_table_test(self):
        self.assertEqual(self.pin1.table_test(self.pin1.to_warmups()), [5, 7.5, 10])
        self.assertEqual(self.pin2.table_test(self.pin2.to_warmups()), [7.5, 12.5, 15])
        self.assertEqual(self.pin3.table_test(self.pin3.to_warmups()), [15, 20, 25])


if __name__ == "__main__":
    unittest.main()
