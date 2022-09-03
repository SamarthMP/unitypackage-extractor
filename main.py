import argparse



def main():

    parser = argparse.ArgumentParser(description='UnityPackage Extractor')

    parser.add_argument('pkgpath', type=str, nargs='?', help='Path To The UnityPackage')
    parser.add_argument('--extractmeta', action='store_true', help='Enable Extraction Of Meta Files')

    args = parser.parse_args()

    if (args.pkgpath != None):
        #Run In CLI Mode
        import extract
        extract.extract(args.pkgpath, args.extractmeta, None, None)
    else:
        #Run In GUI Mode
        import gui

if (__name__ == "__main__"):
    main()