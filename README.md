# cgp-smarter-download
## Disclaimer
This software is provided for the sole purpose of personal use of offline and private copies of the CGP books. Do not distribute any copyrighted files downloaded by this program. All property downloaded remains the copyright of CGP or the respected author. The author of this software does not condone copyright infringement and will not take any responsibility for any actions of any user of this software. Please note that you can only download books you already own on the CGP Online platform with this software. Books which you do not own cannot be downloaded.

## Introduction
This is a version of my other cgp-download script, completely re-written in Python, which seeks to convert into PDFs instead of just cloning the web server.
This is by no means finished, but is slightly more polished than cgp-download (no more random scripts all over the place!).

## Running
Documentation is currently not finished and the software is still a work-in-progress, but here's a quick rundown:
* Install Python and Git if you don't already have them.
* Clone the repo: `git clone https://github.com/TheJoeCoder/cgp-smarter-download`
* CD into directory: `cd cgp-smarter-download`
* Download the manifest file from [here](https://library.cgpbooks.co.uk/digitalcontent/ACEHR42DF/assets/pager.js). Please note you must own the online edition of "Edexcel Anthology of Poetry: Conflict" and be signed into your account for this link to work, otherwise you can download the `pager.js` file from another book, noting the book's ID (the string which looks similar to `ACEHR42DF`, `CAR46DF`, etc.)
* Rename this file to `pager.json` and put it in the git directory.
* If you have downloaded another book than the Edexcel Conflict anthology, edit the line of the `gen_download_links.py` script near the top starting with `bookId = ` to include your book's ID instead of `ACEHR42DF`
* Run the script: `python gen_download_links.py`
* Wait a few minutes for the script to finish and you should have HTML files containing the pages and some images and svg files in the `output` folder!
* To convert to PDF, install wkhtmltopdf, cd to the `output/ACEHR42DF` directory (change based on book ID), and run `wkhtmltopdf --enable-local-file-access .\0005.html .\0005.pdf` (where 0005 is replaced by the page number). (**Note**: This doesn't work completely yet.)