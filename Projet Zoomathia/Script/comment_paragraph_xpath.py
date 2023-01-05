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
    para_content = [p.text for p in doc_obj.paragraphs]
    refs = list(map(lambda x: x.strip(),
                    [para_content[0].split("]]")[-1], para_content[1].split("]]")[-1],
                     para_content[2].split("]]")[-1]]))
    paragraph = [[
        para_content[0].split("]]")[-1].strip(),
        para_content[1].split("]]")[-1].strip(),
        para_content[2].split("]]")[-1].strip(),
        "".join(p.split("]]")[0].split("[[")[-1]).strip(),
        "".join(p.split("]]")[-1]).strip()] for p in para_content[3:] if p != ""]
    print(paragraph)
    exit(0)
    etd = etree.XML(docxZip.read("word/document.xml"))
    alpha = time()
    commentsXML = etree.XML(docxZip.read("word/comments.xml"))
    commentNumber = etd.xpath("//w:commentRangeStart/@w:id", namespaces=ooXMLns)
    print(f"Nombres de commentaires à extraire: {len(commentNumber)}")
    all_extraction = []
    for i in commentNumber:
        if int(i) % 100 == 0:
            print(f"{i} éléments en {time() - alpha} secondes")
        # Je pars de w:commentRangeEnd ayant l'ID "x" et je veux tous les noeuds w:t qui le précède, si ils suivent w:commentRangeStart ayant l'id X
        # Le path est très tricky
        resp_text = etd.xpath(
            f"//w:commentRangeEnd[@w:id='{i}']/preceding::w:t[preceding::w:commentRangeStart[@w:id={i}]]",
            namespaces=ooXMLns)

        resp_comment = commentsXML.xpath(
            f"//w:comment[@w:id]/w:p/w:r/w:t",
            namespaces=ooXMLns
        )
        all_extraction.append(["".join(list(map(lambda x: x.text.replace(u"\xa0", ""), resp_comment))).strip(),
                               "".join(list(map(lambda x: x.text, resp_text)))])
        del resp_comment, resp_text
    print(f"Fin de l'execution. Durée totale: {time() - alpha} secondes")
    print(all_extraction)
    exit(0)
