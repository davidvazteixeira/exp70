class Book():
    def __init__(self, rfid, title='', author='', description='', image_file=''):
        self.rfid = rfid
        self.description = description
        self.title = title
        self.author = author
        self.image_file = image_file
        self.counter = 0

    def show(self):
        return {'title': self.title, 'author': seld.author, 'ifid': self.rfid, 'description': self.description, 'counter': self.counter, 'image_file':self.image}

    def touch(self):
        self.counter += 1

