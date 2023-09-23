import json 
import base64 
import services 
import services

def checkGLSNames(api, names):
    passed = api.checkNameLength(names)
    print(passed)
    ans = api.adjustNameFields(*names)
    print(ans)
    passed = api.checkNameLength(ans)
    print(passed)

def testGLSNames():
    api = services.buildAPI(debug=True)
    names = [
        "I provided professional IT support our online editor can",
        "Peter Mueller",
        "1G"
    ]
    checkGLSNames(api, names)

    names = [
        "I provided program",
        "text from another program over into the online editor above",
        "Peter"
    ]
    checkGLSNames(api, names)

    names = [
        "I provided program",
        "text from another program over into the online editor above",
        ""
    ]
    checkGLSNames(api, names)

    names = [
        "text from another program over into the online editor above",
        "text from another program over into the online ",
        "1G"
    ]
    checkGLSNames(api, names)

    names = [
        "text from another program over into the online editor above",
        "",
        ""
    ]
    checkGLSNames(api, names)

    names = [
        "aa",
        "text from another program over into the online editor above",
        "text can be important. For example, if an author has to write a minimum or maximum"
    ]
    checkGLSNames(api, names)

    names = [
        "aa",
        "bb",
        "vv"
    ]
    checkGLSNames(api, names)

if __name__ == '__main__':

    # services.glsLabel()
    testGLSNames()
