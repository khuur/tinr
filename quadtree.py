class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.r = 50

    def intersects(self, point):
        sum_r = (self.r + point.r) * (self.r + point.r)
        distance = (point.x - self.x) ** 2 + (point.y - self.y) ** 2

        if sum_r > distance:
            return True
        return False

class QuadTree:
    def __init__(self, point1, point2):
        self.x1 = point1.x
        self.y1 = point1.y

        self.x2 = point2.x
        self.y2 = point2.y

        self.point_x = -1
        self.point_y = -1

        self.top_left_tree = None
        self.top_right_tree = None
        self.bottom_left_tree = None
        self.bottom_right_tree = None


    def insert(self, point):

        if self.point_x == -1 and self.point_y == -1:
            # Če ni še nobenga pointa v tem quad treeju
            # naj rata to edini point, ki obstaja tuki notr
            self.point_x = point.x
            self.point_y = point.y
            return

        kam = ""
        # Torej je že bil en point pred tem notr
        # pogruntej a je v levi al v desni polovici
        if point.x > ((self.x1 + self.x2) // 2):
            kam += "desno"
        else:
            kam += "levo"

        # pogruntej a je gor al dol polovici
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
                self.point_x = -1
                self.point_y = -1
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
                self.point_x = -1
                self.point_y = -1
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
                self.point_x = -1
                self.point_y = -1
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
                self.point_x = -1
                self.point_y = -1

    def intersects(self, p1, p2):
        """
        Ta funkcija dobi kot parametr pravokotnik.
        Funkcija vrne ali se vstavljen pravokotnik in ta self.pravokotnik sekata
        :param p1: zgornja leva točka
        :param p2: spodnja desna točka
        :return: True, če se pravokotnika prekrivata
        """
        return not(
            p1.x > self.x2 or
            p2.x < self.x1 or
            p1.y > self.y2 or
            p2.y < self.y1
        )

    def contains(self, p1, p2):
        """
        Funkcija dobi pravokotnik in pove ali je ta pravokotnik znotraj self.pravokotnik
        :param p1: levi zgornji kot
        :param p2: desni spodnji kot
        :return: True, če je
        """
        return (
            p1.x > self.x1 and
            p2.x < self.x2 and
            p1.y > self.y1 and
            p2.y < self.y2
        )

    def query(self, p1, p2):
        found = []

        if not self.intersects(p1, p2):
            return found

        if







def bureeeeek():
    p1 = Point(0, 0)
    p2 = Point(1300, 800)
    qt = QuadTree(p1, p2)

    qt.insert(Point(1000, 50))
    qt.insert(Point(700, 300))


bureeeeek()
