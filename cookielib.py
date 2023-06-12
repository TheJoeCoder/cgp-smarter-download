import os, logging
import logconf

logger = logging.getLogger(__name__)
logger.setLevel(logconf.loggerLevel)

cookies = {}

logger.debug("Opening Cookies")
with open("cookies.txt", "r") as cookiesFile:
    cookies_contents = cookiesFile.read()
    cookies_array = cookies_contents.split(";")
    logger.info("Loading " + str(len(cookies_array)) + " cookies")
    for cookie in cookies_array:
        cookie_split = cookie.split("=")
        cookies[cookie_split[0].strip()] = cookie_split[1]
    cookiesFile.close()
logger.info("Cookies loaded")