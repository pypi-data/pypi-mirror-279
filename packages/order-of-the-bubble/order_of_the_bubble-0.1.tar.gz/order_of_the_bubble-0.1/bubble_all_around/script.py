"""Program code for bubbleorder function"""

def bubbleorder(arrayval):
    """Code for creating bubbleorder"""
    for i in range(0,len(arrayval)-1):
        for j in range(1,len(arrayval)-1-i):
            if arrayval[j] > arrayval[j+1]:
                arrayval[j] = arrayval[j+1]
    return arrayval

