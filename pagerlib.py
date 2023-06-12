import os, requests, logging
import logconf

logger = logging.getLogger(__name__)
logger.setLevel(logconf.loggerLevel)

from cookielib import cookies

workspace_try_urls = [
    "https://library.cgpbooks.co.uk/digitalcontent/{id}/assets/html/workspace.js",
    "https://library.cgpbooks.co.uk/digitalcontent/{id}/assets/workspace.js"
]

pager_try_urls = [
    "https://library.cgpbooks.co.uk/digitalcontent/{id}/assets/common/pager.js",
    "https://library.cgpbooks.co.uk/digitalcontent/{id}/assets/pager.js"
]

if (not os.path.exists('pagers')):
    os.mkdir('pagers')

def get_book_dir(book):
    dirr = os.path.join('pagers', book)
    if (not os.path.exists(dirr)):
        os.mkdir(dirr)
    return dirr

def get_file_contents(filename):
    contents = None
    try:
        with open(filename, "r") as file:
            contents = file.read()
            file.close()
    except:
        pass
    return contents

def download_file_test_url(urls, bookid, output_file):
    for url in urls:
        try:
            book_url = url.replace("{id}", bookid)
            logger.debug("Trying " + book_url)
            workspace = requests.get(book_url, cookies=cookies).text
            if "NoSuchKey" in workspace:
                logger.info("Failed to get workspace file from " + book_url)
                continue
            logger.debug("Writing to " + output_file)
            with open(output_file, 'w') as workspace_file:
                workspace_file.write(workspace)
            return output_file
        except:
            logger.info("Failed to get workspace file from " + book_url)
            continue
    logger.error("Failed to get file file for " + bookid + " from any URL (tried " + str(len(urls)) + ")")
    return None

def get_workspace_file(book):
    # Return the workspace file for the given book.
    workspace_path = os.path.join(get_book_dir(book), 'workspace.js')
    if os.path.exists(workspace_path):
        return workspace_path
    return download_file_test_url(workspace_try_urls, book, workspace_path)

def get_pager_file(book):
    # Return the pager file for the given book.
    pager_path = os.path.join(get_book_dir(book), 'pager.js')
    if os.path.exists(pager_path):
        return pager_path
    return download_file_test_url(pager_try_urls, book, pager_path)
