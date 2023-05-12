import json, os, logging

from pypdf import PdfWriter

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

bookId = "ACEHR42DF"

if (not os.path.exists(os.path.join("output", bookId))):
    logger.error("Output folder does not exist. Please run the download.py script first.")
    exit()

merger = PdfWriter()

for pdf in os.listdir(os.path.join("output", bookId)):
    if (pdf.endswith(".pdf")):
        logger.debug("Merging " + pdf)
        merger.append(os.path.join("output", bookId, pdf))    

merger.write(os.path.join("output", bookId + ".pdf"))
merger.close()