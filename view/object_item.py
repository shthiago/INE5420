from PyQt5.QtGui import QStandardItem


class ObjectItem(QStandardItem):
    def __init__(self, object):
        super().__init__(object.name)
        self._object = object

        self.setEditable(False)

    @property
    def object(self):
        return self._object

    @property
    def name(self):
        return self.text()

    @name.setter
    def name(self, name):
        self.setText(name)
