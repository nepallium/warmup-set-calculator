import re, math, sys
from bisect import bisect_left
from tabulate import tabulate


class Equipment:
    def __init__(self, weight, unit, type=None):
        # parent class for everything "self." setting and other recurring fcts
        self.unit = unit
        self.type = type

        self.weight = float(weight)
        self.units = float(weight)

        self.percentage = [0.55, 0.75, 0.85]
        self.wset = []

    def to_warmups(self):
        if self.units == None:
            sys.exit(
                "Do some stretching and go straight to working sets! No warm up sets needed."
            )
        if self.type == "barbell" or self.type == None:
            self.plates_warmups()
        else:
            self.raw_sets()
            self.check_last_sets()

        return self.wset

    def raw_sets(self):
        for i in range(len(self.percentage)):
            self.units = (self.percentage[i]) * self.weight
            # setter is called. Will return None if the set's weight < 20
            if self.units != None:
                (self.wset).append(self.units)

    def check_last_sets(self):
        if len(self.wset) > 2:
            if (self.wset[-2]) / self.weight > 0.775:
                self.units = self.weight * 0.75
                (self.wset)[-2] = self.units
            if (self.wset[-1]) / self.weight > 0.85:
                self.units = self.weight * 0.85
                (self.wset)[-1] = self.units

    def round_it(self, old_list):
        new_list = []
        for weight in range(len(old_list)):
            # since not all DB or CABLE weights are rounded to 5
            if (
                old_list[weight] <= 20
                and self.type == "db"
                or old_list[weight] <= 15
                and self.type == "pin"
            ):
                new_list.append(old_list[weight])

            else:
                self.units = 5 * math.floor((old_list[weight]) / 5)
                if self.units != None:
                    new_list.append(self.units)

        new_list = list(dict.fromkeys(new_list))

        return new_list

    # fct to make sure the final warm up sets' weights are correct so that in unittests I dont have to assertEqual a whole table
    def table_test(self, weights_list):
        final_list = self.round_it(weights_list)
        # if there are no warm up sets
        if len(final_list) == 0:
            sys.exit(
                "Do some stretching and go straight to working sets! No warm up sets needed."
            )
        else:
            self.wset = final_list
            return self.wset

    def table(self):
        # elongate list if more than 3 warm up sets
        reps = [5, 3, 2]
        if len(self.wset) > 3:
            for _ in range(len(self.wset) - 3):
                reps.append(1)

        sets = []
        for weight in range(len(self.wset)):
            perc = round((self.wset[weight] / self.weight) * 100)

            sets.append(
                {
                    "Set": weight + 1,
                    "%": perc,
                    f"Weight ({self.unit})": self.wset[weight],
                    "Reps": reps[weight],
                }
            )

            if len(self.wset) >= 3:
                pass
            else:
                if perc <= 75:
                    sets[weight]["Reps"] = 3
                else:
                    # its gotta be > 75
                    sets[weight]["Reps"] = 2

        if self.type == "barbell" or self.type == None:
            for set in sets:
                plates = self.plate_it(set[f"Weight ({self.unit})"])
                if len(plates) != 0:
                    set[f"Plates/side ({self.unit})"] = plates
                else:
                    set[f"Plates/side ({self.unit})"] = "Empty"
            # tabulate w/ plates header
        else:
            pass
            # tabulate with no plates header

        return tabulate(sets, headers="keys", tablefmt="grid", numalign="center")

    @classmethod
    def get_weight(cls):
        while True:
            print(
                "Input your working weight by following this format: x lb or y kg\nAdd decimals if necessary"
            )
            weight = input("").lower().strip()
            if matches := re.search(r"^([^0](?:\d+)?(?:\.\d+)?)\s(lb|kg)$", weight):
                # 50.25 kg matches ("50.25" and "kg")
                return matches.groups()
            else:
                print("Invalid weight!")
                continue

    @classmethod
    def get_equipm(cls, w):
        # get equipment type
        print(
            "Input number to choose equipment:\n1: Barbell\n2: Dumbbells\n3: Pin-loaded (cable, machine, etc.)\n4: Plate-loaded machine"
        )
        while True:
            try:
                equipm = int(input(""))
                if 0 < equipm < 5:
                    break
                else:
                    print("Invalid input!")
                    continue

            except ValueError:
                print("Invalid input!")

        if equipm == 1:
            return Plates(*w, "barbell")
        elif equipm == 4:
            return Plates(*w)
        elif equipm == 2:
            return Dumbbell(*w)
        else:
            return Pin(*w)


class Plates(Equipment):
    # Machines, Barbells
    def __init__(self, weight, unit, type=None):
        self.type = type
        super().__init__(weight, unit, type)
        if self.type == "barbell":
            # plate is also bar weight
            if unit == "kg":
                self.oneplate = 60
                self.plate = 20
            else:
                self.oneplate = 135
                self.plate = 45

        # if plate loaded machine
        else:
            self.oneplate = 40
            self.plate = 20

    def plates_warmups(self):
        if self.units == None:
            sys.exit(
                "Do some stretching and go straight to working sets! No warm up sets needed."
            )
        else:
            formula = (self.units - self.oneplate) / ((self.plate) * 2)
            if formula == 0 or int(self.units) <= (self.oneplate + (self.plate) * 2):
                super().raw_sets()

                # 1 case where weight is 100, make 1rst set 60kg for ease of use
                if self.weight == (self.oneplate + (self.plate) * 2):
                    self.wset[0] = self.oneplate

            # weight > 100kg
            else:
                for i in range(int(math.ceil(formula))):
                    self.units = self.oneplate + ((self.plate) * 2) * i
                    (self.wset).append(self.units)

                # once S1= 1 plate, S2= 2 plates
                if len(self.wset) < 3:
                    self.units = self.weight * 0.85
                    (self.wset).append(self.units)

            super().check_last_sets()

    def plate_it(self, weight):
        if self.type == "barbell":
            weight -= self.plate

        side = weight / 2
        plates = ""

        if side >= self.plate:
            n = math.floor(side / self.plate)
            if n == 1:
                plates += f"{self.plate}"
            else:
                plates += f"{n} x {self.plate}"
            side -= n * self.plate
            # perfect plates! cool!
            if side == 0:
                return plates

        if self.unit == "lb":
            increments = [2.5, 5, 10, 25, 35, 45]
            while True:
                pos = bisect_left(increments, side)
                incrmnt = str(increments[pos])
                if side == 0:
                    break
                elif pos == 0 or int(side) == increments[pos]:
                    plates += f"\n{incrmnt}"
                    break
                else:
                    before = increments[pos - 1]
                    plates += f"\n{str(before)}"
                    side -= before

            if plates.count(f"\n10") == 2:
                plates = plates.replace("\n10\n10", "\n2 x 10")

        else:
            # kgs
            while True:
                if side == 0:
                    break
                elif int(side) >= 5:
                    n = 5 * math.floor(side / 5)
                    plates += f"\n{str(n)}"
                    side -= n
                else:
                    plates += f"\n2.5"
                    break

        return plates.removeprefix("\n")

    @property
    def units(self):
        return self._units

    @units.setter
    def units(self, units):
        if self.type == "barbell":
            if self.unit == "kg" and int(units) < 20:
                self._units = None
            elif self.unit == "lb" and int(units) <= 45:
                self._units = None
            else:
                self._units = units

        else:
            self._units = units


class Dumbbell(Equipment):
    def __init__(self, weight, unit, type="db"):
        self.low_list = [3, 5, 8, 10, 12, 15, 17.5, 20]
        super().__init__(weight, unit, type)

    @property
    def units(self):
        return self._units

    @units.setter
    def units(self, units):
        if float(units) <= self.low_list[-1]:
            pos = bisect_left(self.low_list, units)

            if units < self.low_list[0]:
                self._units = None

            # internet copy pasta
            elif self.low_list[pos] == units:
                self._units = units
            else:
                if pos == 0:
                    self._units = self.low_list[0]
                elif pos == len(self.low_list):
                    self._units = self.low_list[-1]
                else:
                    before = self.low_list[pos - 1]
                    self._units = before
        else:
            self._units = units


class Pin(Equipment):
    def __init__(self, weight, unit, type="pin"):
        super().__init__(weight, unit, type)

    @property
    def units(self):
        return self._units

    @units.setter
    def units(self, units):
        if float(units) < 15:
            self._units = 2.5 * math.floor((units) / 2.5)

        else:
            self._units = units


def main():
    work_weight = get_weight()
    equipment = get_equipm(work_weight)  # equipment is an object (from which class? will be determined by the get class method)
    print(tabulate_it(equipment))


def get_weight():
    return Equipment.get_weight()


def get_equipm(w):
    return Equipment.get_equipm(w)


def tabulate_it(e):
    e.table_test(e.to_warmups())
    return(e.table())
    # passing in self (equipment) and the list (equipment.wset)


if __name__ == "__main__":
    main()
