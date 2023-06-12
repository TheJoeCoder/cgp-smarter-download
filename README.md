# cgp-smarter-download
## Disclaimer
This software is provided for the sole purpose of personal use of offline and private copies of the CGP books. Do not distribute any copyrighted files downloaded by this program. All property downloaded remains the copyright of CGP or the respected author. The author of this software does not condone copyright infringement and will not take any responsibility for any actions of any user of this software. Please note that you can only download books you already own on the CGP Online platform with this software. Books which you do not own cannot be downloaded.

## Introduction
This is a version of my other cgp-download script, completely re-written in Python, which seeks to convert into PDFs instead of just cloning the web server.
This is by no means finished, but is slightly more polished than cgp-download (no more random scripts all over the place!).

This software could also potentially be modified to download books from any other service that uses FlippingBook publisher, since that's what CGP uses.

## Running
Documentation is currently not finished and the software is still a work-in-progress, but here's a quick rundown:
* Install Python and Git if you don't already have them.
* Clone the repo: `git clone https://github.com/TheJoeCoder/cgp-smarter-download`
* CD into directory: `cd cgp-smarter-download`
* Copy the `book.py.example` file to `book.py`, and then change the book id to the book ID you're trying to download e.g. `bookId = "CAR46DF"`
* Put your cookies into a `cookies.txt` file. Guide [here](https://github.com/TheJoeCoder/cgp-download/blob/master/README.md#how-to-get-cookies) until I move it over to this page. (**Note:** Due to how the website is programmed, cookies are only valid on a per-book basis - you must capture your cookies every time you download a new book.)
* Run the script: `python download.py`
* Wait a few minutes for the script to finish and you should have HTML files containing the pages and some images and svg files in the `output` folder! (**Note:** If you see a lot of 403 errors, this means your cookies have expired or are invalid. Try getting the cookies again.)
* To convert each page to a PDF form, run `python convert.py`. This will download and open an instance of Chromium controlled by Python. Don't close it - just wait for it to finish going through all the pages.
* To merge all pages into one PDF, run `python merge.py` (work-in-progress).

## Programming Progress
Ordered in level of importance/difficulty
- [ ] Add page labels (FC, IFC, Contents-i, etc.)
- [ ] Add Links
- [ ] Order page based on "structure" pager page def, not on order of pages
- [ ] 403 Forbidden (Cookie expiration/Access Denied) handling
- [ ] Book browser/selection (userguid and signature collection)
- [ ] Remove collecting cookie dependency (username+password login to gain userguid and signature)
- [ ] For that matter, work out how userguids and signatures work at all
- [ ] Book Frontend page + flippingbook index page parsing (/digitalaccess/{id}/Online/ and /digitalcontent/{id}/index.html: useful info contained within...)
- [ ] Fancy GUI
- [ ] Make code cleaner (especially download.py)
- [x] Parse pager.js manifest
- [x] Download books
- [x] Download pager.js and workspace.js manifests from web
- [x] Convert HTML to PDF
- [x] Merge PDFs
- [x] Add bookmarks
