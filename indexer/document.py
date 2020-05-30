class Document(object):

    """
    main document class
    """

    def __init__(self, doc_string):
        self.doc_string = doc_string

    def transformed_string(self):
        raise NotImplementedError



class NormalDocument(Document):
    __string = None

    def __init__(self, doc_string, name):
        super(NormalDocument, self).__init__(doc_string)
        self.tokens = None
        self.name = name

    @property
    def transformed_string(self):
        if not self.__string:
            self.__string = self.doc_string.lower()
        return self.__string

