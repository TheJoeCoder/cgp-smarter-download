import json, os, logging
from charset_normalizer import from_path

import pagerlib

import logconf

from pypdf import PdfWriter, PdfReader

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)
logger.setLevel(logconf.loggerLevel)

from book import bookId

if (not os.path.exists(os.path.join("output", bookId))):
    logger.error("Output folder does not exist. Please run the download.py script first.")
    exit()

logger.debug("Opening pager.json file")
pagerfile_path = pagerlib.get_pager_file(bookId)
if (pagerfile_path is None):
    logger.error("Could not find pager file")
    exit(1)
with open(pagerfile_path, "r") as pagerFile:
    pagerJson = json.loads(pagerFile.read())
    pagerFile.close()

logger.debug("Opening workspace.json file")
workspacefile_path = pagerlib.get_workspace_file(bookId)
if (workspacefile_path is None):
    logger.error("Could not find workspace file")
    exit(1)
with open(workspacefile_path, "r") as workspaceFile:
    workspaceJson = json.loads(workspaceFile.read())
    workspaceFile.close()

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
        # Read file
        pg_rd = PdfReader(os.path.join("output", bookId, pdf))
        pg = pg_rd.pages[0]
        # And now, a hacky inches-printed-as-cm to inches conversion
        pg.scale_by(2.54)
        # Append pdf to merger
        merger.add_page(pg)

# TODO: Page labels (pager.json)

# Add bookmarks
bookmark(workspaceJson["toc"]["children"], None)

logger.debug("Writing output file")
merger.write(os.path.join("output", bookId + ".pdf"))
logger.debug("Closing PdfWriter")
merger.close()
logger.info("Done!")