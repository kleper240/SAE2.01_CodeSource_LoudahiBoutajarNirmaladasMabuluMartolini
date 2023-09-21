class Station:
    def __init__(self, id: int, lignes: int, terminus: int, nom):
        self.Iid = id
        self.Llignes = lignes
        self.Tterminus = terminus
        self.Nnom = nom

    def get_id(self):
        return self.Iid

    def get_lignes(self):
        return self.Llignes

    def get_terminus(self):
        return self.Tterminus

    def get_nom(self):
        return self.Nnom

    def est_terminus(self):
        if self.Tterminus == 1:
            return True
        else:
            return False