import json, os, logging, base64

import pagerlib

import logconf

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromiumService
from selenium.webdriver.common.print_page_options import PrintOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)
logger.setLevel(logconf.loggerLevel)

logger.debug("Loading ChromeDriver")
driver = webdriver.Chrome(service=ChromiumService(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()))

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

book_width = pagerJson["bookSize"]["width"]
book_height = pagerJson["bookSize"]["height"]

pages = pagerJson["pages"]

for page_name, page_contents in pages.items():
    logger.debug("Processing page " + page_name)
    try:
        page_number = int(page_name)
    except ValueError:
        # Not a page we can process. Skip.
        logger.warning("Skipping page " + page_name + " as it is not a number")
        continue

    pagenumber_padded = str(page_number).zfill(4)

    if (not os.path.exists(os.path.join("output", bookId, pagenumber_padded + ".html"))):
        logger.error("Page " + page_name + " does not exist.")
        continue
    
    logger.debug("Opening page " + page_name)
    page_url = "file://" + os.path.join(os.getcwd(), "output", bookId, pagenumber_padded + ".html")
    driver.get(page_url)
    driver.implicitly_wait(0.5)
    print_options = PrintOptions()
    print_options.page_width = float(book_width) / 72 # 72 PPI (Converted up later)
    print_options.page_height = float(book_height) / 72 # 72 PPI (Converted up later)
    print_options.margin_bottom = 0
    print_options.margin_top = 0
    print_options.margin_left = 0
    print_options.margin_right = 0
    print_options.shrink_to_fit = True # Just in case of rounding errors
    # print_options.scale = 1.54 # 1 inch = 2.54 cm
    print_options.page_ranges = [1] # Just in case of rounding errors
    print_options.background = True
    logger.debug("Printing page " + page_name)
    base64_pdf = driver.print_page(print_options)
    logger.debug("Saving page " + page_name)
    with open(os.path.join("output", bookId, pagenumber_padded + ".pdf"), "wb") as pdfFile:
        pdfFile.write(base64.b64decode(base64_pdf))
        pdfFile.close()

logger.info("Closing ChromeDriver")
driver.quit()
logger.info("Done!")