import unicodedata

from time import time
from docx import Document
from lxml import etree
import zipfile
ooXMLns = {'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}


if __name__ == "__main__":
    doc_name = "PLINE-8-annotéIPL.docx"

    doc_obj = Document(doc_name)
    docxZip = zipfile.ZipFile(doc_name)
    etd = etree.XML(docxZip.read("word/document.xml"))
    alpha = time()
    commentsXML = etree.XML(docxZip.read("word/comments.xml"))
    commentNumber = etd.xpath("//w:commentRangeStart/@w:id", namespaces=ooXMLns)
    all_mentions = []
    for i in commentNumber:
        mention = list()
        # Je veux tous les noeuds ayant pour id = x, étant précédé par commentRangeStart et étant les suivants de commentRangeEnd
        # Le path est très tricky
        resp = etd.xpath(
        f"//w:r[preceding::w:commentRangeStart[@w:id='{i}'] and following::w:commentRangeEnd[@w:id='{i}']]/w:t",
        namespaces=ooXMLns)
        for elt in resp:
            mention.append(elt.text)
        all_mentions.append("".join(mention).strip())
    print(time() - alpha)
    exit(0)
    para_content = [p.text for p in doc_obj.paragraphs]
    refs = list(map(lambda x: x.strip(),
                    [para_content[0].split("]]")[-1], para_content[1].split("]]")[-1], para_content[2].split("]]")[-1]]))
    paragraph = ["".join(p.split("]]")[-1]).strip() for p in para_content[3:] if p != ""]
    print(len(paragraph))