################################################################################
import sys
import os
################################################################################

def opts(args):
    if len(args) == 1:
        print 'Please give an operation.'
        return
    operation = args.pop(0)
    if operation == 'add':
        print 'add'
    elif operation == 'mv':
        print 'add'
    elif operation == 'update':
        print 'add'
    elif operation == 'recent':
        print 'add'
    return







if __name__ == "__main__":
    main(sys.argv)
