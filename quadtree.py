class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.r = 50


class QuadTree:
    def __init__(self, point1, point2):
        self.x1 = point1.x
        self.y1 = point1.y

        self.x2 = point2.x
        self.y2 = point2.y

        self.top_left_tree = None
        self.top_right_tree = None
        self.bottom_left_tree = None
        self.bottom_right_tree = None

        self.points = []

    def insert(self, point):
        kam = ""
        # pogruntej a je v levi al v desni polovici
        if point.x > ((self.x1 + self.x2) // 2):
            kam += "desno"
        else:
            kam += "levo"

        # pogruntej a je v levi al v desni polovici
        if point.y > ((self.y1 + self.y2) // 2):
            kam += "dol"
        else:
            kam += "gor"

        # zdej vem v ker kvadrant morm to vpisat
        if kam == "levogor":
            if self.top_left_tree is None:
                # torej je ta tree prazen
                self.top_left_tree = point
            else:
                # tree ni prazn
                prejsna_tocka = self.top_left_tree
                levo_zgoraj_x = self.x1
                levo_zgoraj_y = self.y1

                desno_spodaj_x = (self.x1 + self.x2) // 2
                desno_spodaj_y = (self.y1 + self.y2) // 2

                t1 = Point(levo_zgoraj_x, levo_zgoraj_y)
                t2 = Point(desno_spodaj_x, desno_spodaj_y)

                self.top_left_tree = QuadTree(t1, t2)
                self.top_left_tree.insert(prejsna_tocka)
                self.top_left_tree.insert(point)
        elif kam == "desnogor":
            if self.top_right_tree is None:
                # torej je ta tree prazen
                self.top_right_tree = point
            else:
                # tree ni prazn
                prejsna_tocka = self.top_right_tree
                levo_zgoraj_x = (self.x1 + self.x2) // 2
                levo_zgoraj_y = self.y1

                desno_spodaj_x = self.x2
                desno_spodaj_y = (self.y1 + self.y2) // 2

                t1 = Point(levo_zgoraj_x, levo_zgoraj_y)
                t2 = Point(desno_spodaj_x, desno_spodaj_y)

                self.top_right_tree = QuadTree(t1, t2)
                self.top_right_tree.insert(prejsna_tocka)
                self.top_right_tree.insert(point)
        elif kam == "levodol":
            if self.bottom_left_tree is None:
                # torej je ta tree prazen
                self.bottom_left_tree = point
            else:
                # tree ni prazn
                prejsna_tocka = self.bottom_left_tree
                levo_zgoraj_x = self.x1
                levo_zgoraj_y = (self.y1 + self.y2) // 2

                desno_spodaj_x = (self.x1 + self.x2) // 2
                desno_spodaj_y = self.y2

                t1 = Point(levo_zgoraj_x, levo_zgoraj_y)
                t2 = Point(desno_spodaj_x, desno_spodaj_y)

                self.bottom_left_tree = QuadTree(t1, t2)
                self.bottom_left_tree.insert(prejsna_tocka)
                self.bottom_left_tree.insert(point)
        elif kam == "desnodol":
            if self.bottom_right_tree is None:
                # torej je ta tree prazen
                self.top_right_tree = point
            else:
                # tree ni prazn
                prejsna_tocka = self.bottom_right_tree
                levo_zgoraj_x = (self.x1 + self.x2) // 2
                levo_zgoraj_y = (self.y1 + self.y2) // 2

                desno_spodaj_x = self.x2
                desno_spodaj_y = self.y2

                t1 = Point(levo_zgoraj_x, levo_zgoraj_y)
                t2 = Point(desno_spodaj_x, desno_spodaj_y)

                self.bottom_right_tree = QuadTree(t1, t2)
                self.bottom_right_tree.insert(prejsna_tocka)
                self.bottom_right_tree.insert(point)

def bureeeeek():
    p1 = Point(0, 0)
    p2 = Point(1300, 800)
    qt = QuadTree(p1, p2)

    qt.insert(Point(1000, 50))
    qt.insert(Point(700, 300))


bureeeeek()
