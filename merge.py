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
merger.set_page_mode("/UseOutlines")

def bookmark(children, parent):
    for child in children:
        logger.debug("Adding bookmark " + child["title"])
        title = child["title"]
        zeropage = child["page"] - 1 # Needed because pypdf numbering starts at 0, whereas the workspace.json numbering starts at 1
        if (parent != None):
            # Parent exists
            new_parent = merger.add_outline_item(title, zeropage, parent=parent)
        else:
            # Parent does not exist
            new_parent = merger.add_outline_item(title, zeropage)
        if ("children" in child):
            bookmark(child["children"], new_parent)

# Merge pdfs into one
for pdf in os.listdir(os.path.join("output", bookId)):
    if (pdf.endswith(".pdf")):
        logger.debug("Merging " + pdf)
        merger.append(os.path.join("output", bookId, pdf))

# TODO: Page labels (pager.json)

# Add bookmarks
bookmark(workspaceJson["toc"]["children"], None)

logger.debug("Writing output file")
merger.write(os.path.join("output", bookId + ".pdf"))
logger.debug("Closing PdfWriter")
merger.close()
logger.info("Done!")