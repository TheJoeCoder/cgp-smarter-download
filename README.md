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
* Download the manifest file from [here](https://library.cgpbooks.co.uk/digitalcontent/ACEHR42DF/assets/pager.js). Please note you must own the online edition of "Edexcel Anthology of Poetry: Conflict" and be signed into your account for this link to work, otherwise you can download the `pager.js` file from another book, noting the book's ID (the string which looks similar to `ACEHR42DF`, `CAR46DF`, etc.)
* Rename this file to `pager.json` and put it in the git directory.
* If you have downloaded another book than the Edexcel Conflict anthology, edit the line of the `download.py`, `convert.py`, and `merge.py` scripts near the top starting with `bookId = ` to include your book's ID instead of `ACEHR42DF` (temporary solution - args coming soon)
* Put your cookies into a `cookies.txt` file. Guide [here](https://github.com/TheJoeCoder/cgp-download/blob/master/README.md#how-to-get-cookies).
* Run the script: `python download.py`
* Wait a few minutes for the script to finish and you should have HTML files containing the pages and some images and svg files in the `output` folder!
* To convert each page to a PDF form, run `python convert.py`.
* To merge all pages into one PDF, run `python merge.py` (work-in-progress).

## Programming Progress
- [x] Parse pager.js manifest
- [x] Download books
- [ ] Download pager.js manifest from web
- [x] Convert HTML to PDF
- [x] Merge PDFs
- [ ] Add page labels (FC, IFC, Contents-i, etc.)
- [ ] Add bookmarks
- [ ] Make code cleaner
- [ ] Book autoselection
- [ ] Fancy GUI