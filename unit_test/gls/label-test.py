import os, sys
sys.path.append(".")
import json
from pylib.ioutils import *

def test_watermark():
    path = r"G:\hansagt\tampermonkey\temp\prod"
    with open(path+r"\gls-028-2162491-7793901.json", 'r') as f:
        label = json.load(f)
        b64parcel = label['labels'][0]

    b64Watermark = createPdfWatermark("123456", pagesize=getPdfPageSize(b64parcel),
                                      textPosition=(10 * mm, 75 * mm),
                                      textColor=(0, 0, 0, 0.9),
                                      fontSize=7)
    ret = addWatermarkToPdf(b64parcel, b64Watermark)

    props = DocumentProperties()
    props.title = "028-2162491-7793901"
    props.subject = "GLS-parcel"
    props['data'] = json.dumps(dict(orderId = "028-2162491-779是3901", trackingId=None), ensure_ascii=False)
    ret = setPdfDocumentProperties(ret, props)
    with open(path + r"\res.pdf", 'wb') as f:
        f.write(base64ToPdf(ret))


if __name__ == '__main__':
    test_watermark()