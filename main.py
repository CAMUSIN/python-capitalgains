import os
import sys
from App import App
from Services.Processor import TaxProcessor
from Services.Rules import TaxRules
from Services.Sender import TaxSender

if __name__ == '__main__':
    rules = TaxRules()
    processor = TaxProcessor(rules)
    sender = TaxSender()
    app = App(processor,sender)
    
    if len(sys.argv[1:]) > 0:
        if os.path.exists(str(sys.argv[1:])):
            file = open(str(sys.argv[1:]), "r")
            app.Run(file.readline())
        else:
            print("EOF")
    else:
        args = input()
        app.Run(args)


