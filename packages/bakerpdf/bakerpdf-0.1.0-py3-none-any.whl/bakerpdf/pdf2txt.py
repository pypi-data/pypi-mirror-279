""" This module is used to convert PDF to TXT """


class PDF2TXT:
    """ 
    A class used to convert PDF to TXT

    Parameters:
    path (str): The path of the PDF file
    """

    def __init__(self, path):
        print("PDF2TXT.__init__()", path)

    def pdf2txt(self, path):
        """
        This function is used to convert PDF to TXT 

        Parameters:
        path (str): The path of the PDF file

        Returns:
        str: The text content of the PDF file
        """
        print("pdf2txt()", path)
