import base64
from typing import Tuple, List, Dict
from reportlab.pdfgen import canvas
import reportlab.lib.pagesizes as pagesizes
from reportlab.lib.units import mm
from PyPDF2 import PdfReader, PdfWriter
from io import BytesIO
from datetime import datetime


def base64decode_urlsafe(b64: str) -> str:
    return base64.urlsafe_b64decode(b64).decode("utf-8")


def base64encode_urlsafe(text: str) -> str:
    b64 = base64.urlsafe_b64encode(text.encode("utf-8"))
    return b64.decode('utf-8')


def base64ToPdf(b64) -> bytes:
    bytes_ = base64.b64decode(b64, validate=True)
    return bytes_


def pdfToBase64(bytes_) -> str:
    b64 = base64.b64encode(bytes_).decode("utf-8")
    return b64


def createPdfWatermark(text: str,
                       pagesize: Tuple[int, int] = pagesizes.A4,
                       textPosition: Tuple[int, int] = (2 * mm, 4 * mm),
                       textColor: Tuple[int, int, int, int] = (1, 0, 0, 0.9),
                       fontSize=9) -> str:
    x, y = textPosition
    w, h = pagesize
    buffer = BytesIO()
    can = canvas.Canvas(buffer, pagesize=(w, h), bottomup=0)
    can.setFont("Helvetica", fontSize)
    can.setStrokeColorRGB(*textColor)
    can.setFillColorRGB(*textColor)
    textObj = can.beginText(x, y)
    textObj.setFont("Helvetica", fontSize)
    for t in text.split('\n'):
        textObj.textLine(t.strip())
    can.drawText(textObj)
    can.save()
    bytes_ = buffer.getvalue()
    b64 = pdfToBase64(bytes_)
    return b64  # A Pdf encoded by Base64


def addWatermarkToPdf(b64Pdf: str, b64Watermark: str) -> str:
    bufferPdf = BytesIO()
    bufferWatermark = BytesIO()
    bufferOut = BytesIO()
    bufferPdf.write(base64ToPdf(b64Pdf))
    bufferWatermark.write(base64ToPdf(b64Watermark))
    pdf = PdfReader(bufferPdf)
    watermark = PdfReader(bufferWatermark)
    mediaBox = pdf.pages[0].mediabox
    print(mediaBox.width, mediaBox.height)
    out = PdfWriter()
    for page in pdf.pages:
        page.merge_page(watermark.pages[0])
        out.add_page(page)
    out.write(bufferOut)
    bytes_ = bufferOut.getvalue()
    b64 = pdfToBase64(bytes_)
    return b64  # A Pdf encoded by Base64


def getPdfPageSize(b64Pdf: str, index: int = 0):
    bufferPdf = BytesIO()
    bufferPdf.write(base64ToPdf(b64Pdf))
    pdf = PdfReader(bufferPdf)
    mediabox = pdf.pages[index].mediabox
    return mediabox.width, mediabox.height


# DocumentProperties of a PDF file.
class DocumentProperties:
    title: str = ""
    subject: str = ""
    author: str = ""
    keywords: str = ""
    custom: List[Dict] = list()

    def __setitem__(self, key: str, value: object):
        k = key.capitalize()
        self.custom.append({"/" + k: value})

    def getDescription(self):
        res = {'/Author': self.author, '/Title': self.title, "/Subject": self.subject,
               "/Keywords": self.keywords}
        for c in self.custom:
            res.update(c)
        return res


def setPdfDocumentProperties(b64Pdf: str, properties: DocumentProperties):
    br = BytesIO()
    br.write(base64ToPdf(b64Pdf))
    reader = PdfReader(br)
    out = PdfWriter()
    out.append_pages_from_reader(reader)
    out.add_metadata(properties.getDescription())
    bw = BytesIO()
    out.write(bw)
    bytes_ = bw.getvalue()
    b64out = pdfToBase64(bytes_)
    return b64out


def current_time(format_="%Y%m%d %H%M%S"):
    return datetime.today().strftime(format_)


def current_date(format=r"%Y%m%d"):
    return datetime.datetime.today().strftime(format)
