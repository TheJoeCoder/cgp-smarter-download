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
* Download the pager file from [here](https://library.cgpbooks.co.uk/digitalcontent/CAR46DF/assets/pager.js), replacing `CAR46DF` in the URL with the ID of the book you're trying to download.
* Rename this file to `pager.json` and put it in the git directory.
* In the same manner, download the workspace file from [here](https://library.cgpbooks.co.uk/digitalcontent/CAR46DF/assets/workspace.js), rename to workspace.json, and place into the same directory. Again, change the URL with a different ID for a different book
* Copy the `book.py.example` file to `book.py`, and then change the book id to the book ID you're trying to download e.g. `bookId = "CAR46DF"`
* Put your cookies into a `cookies.txt` file. Guide [here](https://github.com/TheJoeCoder/cgp-download/blob/master/README.md#how-to-get-cookies) until I move it over to this page.
* Run the script: `python download.py`
* Wait a few minutes for the script to finish and you should have HTML files containing the pages and some images and svg files in the `output` folder! (**Note:** If you see a lot of 403 errors, this means your cookies have expired or are invalid. Try getting the cookies again.)
* To convert each page to a PDF form, run `python convert.py`.
* To merge all pages into one PDF, run `python merge.py` (work-in-progress).

## Programming Progress
- [x] Parse pager.js manifest
- [x] Download books
- [x] Download pager.js and workspace.js manifests from web
- [x] Convert HTML to PDF
- [x] Merge PDFs
- [ ] Add page labels (FC, IFC, Contents-i, etc.)
- [x] Add bookmarks
- [ ] Add Links
- [ ] Make code cleaner (especially download.py)
- [ ] Book browser/selection (userguid and signature collection)
- [ ] Remove collecting cookie dependency (username+password login to gain userguid and signature)
- [ ] Book Frontend page parsing (/digitalaccess/{id}/Online/: useful info contained within...)
- [ ] Fancy GUI
- [ ] 403 Forbidden (Cookie expiration/Access Denied) handling