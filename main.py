from getRedOakfiles import getRedOakfiles
# import regex
configPath = r'C:\Projects\redoak_file_insight\config.ini'


def main():
    if __name__=='__main__':
        print('Getting list of all files..')
        getRedOakfiles(configPath)
        print('Data written to log files')


main()
