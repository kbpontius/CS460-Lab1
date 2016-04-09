class Parser(object):
    inputFile = file

    def __init__(self, fileName):
        self.inputFile = open(fileName)
        input = self.inputFile.readline()

        # Read in lines.
        for line in input:
            print line

        self.inputFile.close()