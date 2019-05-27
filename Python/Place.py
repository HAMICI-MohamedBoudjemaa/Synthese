class Place:

    def __init__(self):
        self._name = None
        self._type = None
        self._ofCity = None
        self._ofCountry = None

    def __str__(self):
        result = '[' + 'name: ' + self.name + ' type: ' + self.type + ' country: ' + self.ofCountry + ']'
        return result

    @property
    def name(self):
        return self._name
    @property
    def type(self):
        return self._type
    @property
    def ofCity(self):
        return self._ofCity
    @property
    def ofCountry(self):
        return self._ofCountry

    @name.setter
    def name(self, name):
        self._name = name
    @type.setter
    def type(self, type):
        self._type = type
    @ofCity.setter
    def ofCity(self, ofCity):
        self._ofCity = ofCity
    @ofCountry.setter
    def ofCountry(self, ofCountry):
        self._ofCountry = ofCountry