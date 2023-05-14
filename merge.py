import json, os, logging
from charset_normalizer import from_path

from pypdf import PdfWriter

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

bookId = "CAR46DF"

if (not os.path.exists(os.path.join("output", bookId))):
    logger.error("Output folder does not exist. Please run the download.py script first.")
    exit()

logger.debug("Opening pager.json file")
with open("pager.json", "r") as pagerFile:
    pagerJson = json.loads(pagerFile.read())
    pagerFile.close()

logger.debug("Opening workspace.json file")
workspaceJson = json.loads(str(from_path("workspace.json").best()))

logger.debug("Creating PdfWriter")
merger = PdfWriter()

# Merge pdfs into one
for pdf in os.listdir(os.path.join("output", bookId)):
    if (pdf.endswith(".pdf")):
        logger.debug("Merging " + pdf)
        merger.append(os.path.join("output", bookId, pdf))

# TODO: Page labels (pager.json)

# Add bookmarks
for bookmark in workspaceJson["toc"]["children"]:
    title = bookmark["title"]
    page = bookmark["page"]
    zero_page = page - 1
    logger.debug("Adding bookmark " + title)
    merger.add_outline_item(title, zero_page) # TODO: Add children bookmarks

logger.debug("Writing output file")
merger.write(os.path.join("output", bookId + ".pdf"))
logger.debug("Closing PdfWriter")
merger.close()
logger.info("Done!")