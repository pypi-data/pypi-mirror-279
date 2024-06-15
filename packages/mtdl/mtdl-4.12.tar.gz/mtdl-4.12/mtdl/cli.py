from mtdl.downloader import MultiThreadDownloader, abort_if_exception
from mtdl.metadata import format_metadata, __author_email__, __version__
import logging
import argparse
import json

logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)

SUPPORT_TEXT = format_metadata()
SUPPORT_TEXT_BEFORE = \
f"""
If you found any bug, contact {__author_email__}, if you like it, you can donate me.
"""

@abort_if_exception
def main():
    parser = argparse.ArgumentParser(epilog=SUPPORT_TEXT_BEFORE)
    parser.add_argument("url", help="", action="store")
    
    parser.add_argument("-o", "--output", type=str, default=None, help="The output file name, dafault to the url base.", dest="out_filename")
    
    parser.add_argument("-c", "--chunk", type=int, default=1000000, help="The chunk size to split, default to a million.", dest="chunk_size")
    
    parser.add_argument("-v", "--version", action="version", version=__version__, help="Show version")
    
    parser.add_argument("--header", type=str, help="The extra headers for request. (Please write in JSON format.)", dest="header")
    
    args = parser.parse_args()
    
    print(SUPPORT_TEXT)
    
    process = MultiThreadDownloader(args.url, args.chunk_size, args.out_filename, extra_headers=json.loads(args.header))
    
    process.start()
    
    print(SUPPORT_TEXT_BEFORE)
    
if __name__ == "__main__":
    main()
    