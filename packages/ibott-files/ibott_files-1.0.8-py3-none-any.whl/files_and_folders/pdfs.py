import PyPDF2
from PyPDF2 import PdfFileMerger
from .files import File
import fitz


class PDF(File):
    """
    PDF Class Heritates from File Class
        Arguments:
            file_path (str): Path of the file
            Attributes:
                file_path (str): Path of the file
                pages (int): number of pages in the file
                info (str): info of the file
                Methods:
                    read_pages(page_num, encoding=None): Returns a string with the text in the page
                    append(pdf_document2,merge_path): Appends a pdf document to the current document
                    split(): split pdf into several pdfs
    """

    def __init__(self, path):
        super().__init__(path)
        self.pages = self.get_pages()
        self.info = self.get_info()

    def get_pages(self):
        file = open(self.path, "rb")
        page_num = len(PyPDF2.PdfReader(file).pages) - 1
        file.close()
        return page_num

    def get_info(self):
        file = open(self.path, "rb")
        meta = PyPDF2.PdfReader(file).metadata
        file.close()
        return meta

    def read_page(self, page_num, encoding="utf-8"):
        """
        Read page from PDF, receives number of page to receive and encoding
        Arguments:
            page_num (int): number of page to receive
            encoding (str): encoding of the text
        Returns:
            str: text of the page
        """
        file = open(self.path, "rb")
        reader = PyPDF2.PdfReader(file)
        page = reader.pages[page_num]
        text = page.extract_text()
        file.close()
        return text
        # PyMuPDF

    def read_pdf(self):
        doc = fitz.open(self.path)
        num_pages = doc.page_count
        text = ""
        for page_num in range(num_pages):
            page = doc[page_num]
            text += page.get_text()
        doc.close()
        return text

    def read_file(self):
        file = open(self.path, "rb")
        reader = PyPDF2.PdfReader(file)
        text = ""
        for i in range(self.pages):
            page = reader.pages[i]
            text = text + page.extract_text()
        file.close()
        return text

    def append(self, pdf_document2, merged_path):
        """
        Append new pdf to current and store it as a new one.
        Arguments:
            pdf_document2 (PDF): PDF to append
            merged_path (str): Path to store the new PDF
        """
        pdfs = [str(self.path), str(pdf_document2)]
        merger = PdfFileMerger()
        for pdf in pdfs:
            merger.append(pdf)
            merger.write(merged_path)

    def spit(self):
        """Split pdf into multiple pages with format: pdfName_n.pdf
        """
        pdf = PyPDF2.PdfFileReader(self.path)
        for page in range(self.pages):
            pdf_writer = PyPDF2.PdfWriter()
            pdf_writer.addPage(pdf.getPage(page))
            output_filename = '{}_page_{}.pdf'.format(self.file_name, page + 1)
            with open(output_filename, 'wb') as out:
                pdf_writer.write(out)


