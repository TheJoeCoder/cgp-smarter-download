import json, os, requests, logging

import pagerlib

import logconf

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)
logger.setLevel(logconf.loggerLevel)

from book import bookId

logger.debug("Opening template file base.html")
with open("template/base.html", "r") as baseFile:
    baseHtml = baseFile.read()
    baseFile.close()

logger.debug("Opening template file background.html")
with open("template/background.html", "r") as backgroundFile:
    backgroundHtml = backgroundFile.read()
    backgroundFile.close()

logger.debug("Opening template file text-layer.html")
with open("template/text-layer.html", "r") as textLayerFile:
    textLayerHtml = textLayerFile.read()
    textLayerFile.close()

logger.debug("Opening template file svg.html")
with open("template/svg.html", "r") as vectorLayerFile:
    vectorLayerHtml = vectorLayerFile.read()
    vectorLayerFile.close()

logger.debug("Opening template file link.html")
with open("template/link.html", "r") as linkFile:
    linkHtml = linkFile.read()
    linkFile.close()

from cookielib import cookies

if (not os.path.exists("output")):
    os.mkdir("output")
    logger.debug("Created output directory")

bookPath = os.path.join("output", bookId)

if (not os.path.exists(bookPath)):
    os.mkdir(bookPath)
    logger.debug("Created book output directory")

failed_downloads = []

# Download a file
# Unless force is true, will not download if file already exists
# Returns the full path and relative path of the downloaded file
def download(url, force=False):
    logger.debug("Downloading " + url)
    urlbase = "https://library.cgpbooks.co.uk/digitalcontent/" + bookId + "/"
    # Get filename
    filename_replaced = url.replace(urlbase, "")
    save_filename = os.path.join(bookPath, filename_replaced)
    save_dir = os.path.dirname(save_filename)
    if (os.path.exists(save_filename) and not force):
        logger.debug("File already exists, skipping")
        return save_filename, filename_replaced
    # Make request
    res = requests.get(url, cookies=cookies)
    logger.debug("Response code: " + str(res.status_code))
    logger.debug("Response length: " + str(len(res.content)))
    if (res.status_code == 200):
        # Status was OK
        # Create directory if not exists
        os.makedirs(save_dir, exist_ok=True)
        # Save file
        with open(save_filename, "wb") as saveFile:
            saveFile.write(res.content)
            saveFile.close()
        logger.debug("Saved file to " + save_filename)
        return save_filename, filename_replaced
    # If we're still here, download has failed
    logger.error("Download failed of file " + url)
    failed_downloads.append(url)
    return None, None

# pager.js provides all data about pages, substrates, text links, etc
# pager is located in one of two places:
# https://library.cgpbooks.co.uk/digitalcontent/{bookId}/assets/pager.js
# https://library.cgpbooks.co.uk/digitalcontent/{bookId}/assets/common/pager.js
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

if ("links" in pagerJson):
    if("color" in pagerJson["links"]):
        link_hover_colour = pagerJson["links"]["color"]
    else:
        link_hover_colour = "rgba(0, 0, 0, 0)"
    if "target" in pagerJson["links"]:
        link_target = pagerJson["links"]["target"]
    else:
        link_target = "_blank"

pages = pagerJson["pages"]

default_background_image_width = 0
default_background_image_height = 0
default_content_width = 0
default_width = 0
default_height = 0
default_thumbnail_format = ""
default_has_textlayer = False
default_has_vectortext = False
default_substrate_format = ""
default_is_stub = False
default_contentscale = 0
default_slidedelay = 0
default_background_colour = ""
default_is_wide = False
default_pageresize = ""
default_shadowdepth = 0
default_substratesizes = []
default_substratesizesready = 0
default_textsizes = []
default_righttoleft_content = False
default_has_textblocks = False
default_has_notext = False
default_blocks = []
default_displayname = ""
default_urlheader = ""
default_links = []

if ("defaults" in pages):
    logger.debug("Parsing default page attributes")
    page_contents = pages["defaults"]
    # edit default attributes
    if ("backgroundImageWidth" in page_contents):
        default_background_image_width = page_contents["backgroundImageWidth"]
    if ("backgroundImageHeight" in page_contents):
        default_background_image_height = page_contents["backgroundImageHeight"]
    if ("contentWidth" in page_contents):
        default_content_width = page_contents["contentWidth"]
    if ("width" in page_contents):
        default_width = page_contents["width"]
    if ("height" in page_contents):
        default_height = page_contents["height"]
    if ("thFormat" in page_contents):
        default_thumbnail_format = page_contents["thFormat"]
    if ("textLayer" in page_contents):
        default_has_textlayer = page_contents["textLayer"]
    if ("vectorText" in page_contents):
        default_has_vectortext = page_contents["vectorText"]
    if ("substrateFormat" in page_contents):
        default_substrate_format = page_contents["substrateFormat"]
    if ("stub" in page_contents):
        default_is_stub = page_contents["stub"]
    if ("contentScale" in page_contents):
        default_contentscale = page_contents["contentScale"]
    if ("slideDelay" in page_contents):
        default_slidedelay = page_contents["slideDelay"]
    if ("backgroundColor" in page_contents):
        default_background_colour = page_contents["backgroundColor"]
    if ("wide" in page_contents):
        default_is_wide = page_contents["slideDelay"]
    if ("pageResize" in page_contents):
        default_pageresize = page_contents["pageResize"]
    if ("shadowDepth" in page_contents):
        default_shadowdepth = page_contents["shadowDepth"]
    if ("substrateSizes" in page_contents):
        default_substratesizes = page_contents["substrateSizes"]
    if ("substrateSizesReady" in page_contents):
        default_substratesizesready = page_contents["substrateSizesReady"]
    if ("textSizes" in page_contents):
        default_textsizes = page_contents["textSizes"]
    if ("rtlContent" in page_contents):
        default_righttoleft_content = page_contents["rtlContent"]
    if ("textBlocks" in page_contents):
        default_has_textblocks = page_contents["textBlocks"]
    if ("hasNoText" in page_contents):
        default_has_notext = page_contents["hasNoText"]
    if ("blocks" in page_contents):
        default_blocks = page_contents["blocks"]
    if ("displayName" in page_contents):
        default_displayname = page_contents["displayName"]
    if ("urlHeader" in page_contents):
        default_urlheader = page_contents["urlHeader"]
    if ("links" in page_contents):
        default_links = page_contents["links"]
else:
    logger.warning("No default page attributes found")

for page_name, page_contents in pages.items():
    logger.debug("Processing page " + page_name)
    if (page_name == "defaults"):
        # Default page. Already processed, so skip.
        logger.debug("Skipping default page")
        continue
    try:
        page_number = int(page_name)
    except ValueError:
        # Not a page we can process. Skip.
        logger.warning("Skipping page " + page_name + " as it is not a number")
        continue
    # Get page data from json into variables
    background_image_width = default_background_image_width
    background_image_height = default_background_image_height
    content_width = default_content_width
    width = default_width
    height = default_height
    thumbnail_format = default_thumbnail_format
    has_textlayer = default_has_textlayer
    has_vectortext = default_has_vectortext
    substrate_format = default_substrate_format
    is_stub = default_is_stub
    contentscale = default_contentscale
    slidedelay = default_slidedelay
    background_colour = default_background_colour
    is_wide = default_is_wide
    pageresize = default_pageresize
    shadowdepth = default_shadowdepth
    substratesizes = default_substratesizes
    substratesizesready = default_substratesizesready
    textsizes = default_textsizes
    righttoleft_content = default_righttoleft_content
    has_textblocks = default_has_textblocks
    has_notext = default_has_notext
    blocks = default_blocks
    displayname = default_displayname
    urlheader = default_urlheader
    links = default_links
    if ("backgroundImageWidth" in page_contents):
        background_image_width = page_contents["backgroundImageWidth"]
    if ("backgroundImageHeight" in page_contents):
        background_image_height = page_contents["backgroundImageHeight"]
    if ("contentWidth" in page_contents):
        content_width = page_contents["contentWidth"]
    if ("width" in page_contents):
        width = page_contents["width"]
    if ("height" in page_contents):
        height = page_contents["height"]
    if ("thFormat" in page_contents):
        thumbnail_format = page_contents["thFormat"]
    if ("textLayer" in page_contents):
        has_textlayer = page_contents["textLayer"]
    if ("vectorText" in page_contents):
        has_vectortext = page_contents["vectorText"]
    if ("substrateFormat" in page_contents):
        substrate_format = page_contents["substrateFormat"]
    if ("stub" in page_contents):
        is_stub = page_contents["stub"]
    if ("contentScale" in page_contents):
        contentscale = page_contents["contentScale"]
    if ("slideDelay" in page_contents):
        slidedelay = page_contents["slideDelay"]
    if ("backgroundColor" in page_contents):
        background_colour = page_contents["backgroundColor"]
    if ("wide" in page_contents):
        is_wide = page_contents["slideDelay"]
    if ("pageResize" in page_contents):
        pageresize = page_contents["pageResize"]
    if ("shadowDepth" in page_contents):
        shadowdepth = page_contents["shadowDepth"]
    if ("substrateSizes" in page_contents):
        substratesizes = page_contents["substrateSizes"]
    if ("substrateSizesReady" in page_contents):
        substratesizesready = page_contents["substrateSizesReady"]
    if ("textSizes" in page_contents):
        textsizes = page_contents["textSizes"]
    if ("rtlContent" in page_contents):
        righttoleft_content = page_contents["rtlContent"]
    if ("textBlocks" in page_contents):
        has_textblocks = page_contents["textBlocks"]
    if ("hasNoText" in page_contents):
        has_notext = page_contents["hasNoText"]
    if ("blocks" in page_contents):
        blocks = page_contents["blocks"]
    if ("displayName" in page_contents):
        displayname = page_contents["displayName"]
    if ("urlHeader" in page_contents):
        urlheader = page_contents["urlHeader"]
    if ("links" in page_contents):
        links = page_contents["links"]
    # generate template
    max_substrate_level = len(substratesizes)
    pagenumber_padded = str(page_number).zfill(4)
    substrate_url = "https://library.cgpbooks.co.uk/digitalcontent/" + bookId + "/assets/common/page-html5-substrates/page" + pagenumber_padded + "_" + str(max_substrate_level) + "." + substrate_format
    fpath1_full, fpath_rel = download(substrate_url)
    if (fpath1_full != None):
        substrate_url = "./" + fpath_rel
        logger.debug("Using substrate url " + substrate_url)
    doText = (not has_notext) and has_textlayer and (not has_vectortext)
    if (doText):
        max_text_level = len(textsizes)
        text_url = "https://library.cgpbooks.co.uk/digitalcontent/" + bookId + "/assets/common/page-textlayers/page" + pagenumber_padded + "_" + str(max_text_level) + "." + "png" # + substrate_format
        fpath2_full, fpath_rel = download(text_url)
        if (fpath2_full != None):
            text_url = "./" + fpath_rel
            logger.debug("Using text url " + text_url)
    doVectorText = (not has_notext) and has_textlayer and has_vectortext
    if doVectorText:
        vector_url = "https://library.cgpbooks.co.uk/digitalcontent/" + bookId + "/assets/common/page-vectorlayers/" + pagenumber_padded + ".svg"
        fpath3_full, fpath_rel = download(vector_url)
        if (fpath3_full != None):
            vector_url = "./" + fpath_rel
            logger.debug("Using vector url " + vector_url)
    # Generate page template
    logger.debug("Generating page template")
    page_template = baseHtml.replace("%BACKGROUND%", backgroundHtml)
    page_template = page_template.replace("%PAGE_SUBSTRATE%", substrate_url)
    if (doText):
        page_template = page_template.replace("%TEXTLAYER%", textLayerHtml)
        page_template = page_template.replace("%TEXT_SUBSTRATE%", text_url)
    else:
        page_template = page_template.replace("%TEXTLAYER%", "")
    if(doVectorText):
        page_template = page_template.replace("%SVG%", vectorLayerHtml)
        page_template = page_template.replace("%VECTOR_LAYER%", vector_url)
    else:
        page_template = page_template.replace("%SVG%", "")
    page_template = page_template.replace("%URLTITLE%", urlheader)
    page_template = page_template.replace("%DISPLAYNAME%", displayname)
    page_template = page_template.replace("%WIDTH%", str(width))# / 72)) # 72 PPI
    page_template = page_template.replace("%HEIGHT%", str(height))# / 72))
    page_template = page_template.replace("%BACKGROUNDCOLOR%", background_colour)
    page_template = page_template.replace("%HOVER_COLOUR%", str(link_hover_colour))
    links_text = ""
    for link in links:
        lnk_width = link["rect"][0]
        lnk_height = link["rect"][1]
        lnk_x = link["rect"][2]
        lnk_y = link["rect"][3]
        lnk_url = link["url"]
        lnk_zindex = link["zIndex"]
        link_template = linkHtml.replace("%WIDTH%", str(lnk_width))
        link_template = link_template.replace("%HEIGHT%", str(lnk_height))
        link_template = link_template.replace("%X%", str(lnk_x))
        link_template = link_template.replace("%Y%", str(lnk_y))
        link_template = link_template.replace("%URL%", lnk_url)
        link_template = link_template.replace("%TARGET%", link_target)
        link_template = link_template.replace("%ZINDEX%", str(lnk_zindex))
        links_text += link_template
        logger.debug("Generated link attribute for " + lnk_url)
    # page_template = page_template.replace("%LINKS%", links_text)
    page_template = page_template.replace("%LINKS%", "") # TODO: fix links
    # write page template to file
    logger.debug("Writing page template to file")
    with open(os.path.join(bookPath, pagenumber_padded + ".html"), "w") as f:
        f.write(page_template)
        f.close()

logger.info("Done!")
logger.info("Failed Downloads: " + str(len(failed_downloads)))
for download in failed_downloads:
    logger.info(download)

###
# substrate/text layer size is the 1-based index of the size in the sizes array
# e.g. first in list = 1, second = 2, etc

# background image url:
# https://library.cgpbooks.co.uk/digitalcontent/{bookId}/assets/common/page-html5-substrates/page{page}_{substrate_size}.{substrate_format}

# Image text layers:
# https://library.cgpbooks.co.uk/digitalcontent/{bookId}/assets/common/page-textlayers/page{page}_{textlayer_size}.{textlayer_format}

# image vector layers:
# https://library.cgpbooks.co.uk/digitalcontent/{bookId}/assets/common/page-vectorlayers/{page}.svg

# thumbnail:
# https://library.cgpbooks.co.uk/digitalcontent/{bookId}/assets/flash/pages/page{page}_s.{thumbnail_format}

# search index:
# https://library.cgpbooks.co.uk/digitalcontent/{bookId}/assets/mobile/search/search{page}.xml

# text blocks:
# https://library.cgpbooks.co.uk/digitalcontent/{bookId}/assets/textblocks/page{page}.xml

###
