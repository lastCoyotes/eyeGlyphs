import matplotlib.pyplot as plt
import numpy as np
import collections


# takes RAW message
def listifyMessage(message: list[str]) -> list[int]:
    result = []
    for i in range(len(message)):
        for c in message[i]:
            result.append(int(c))
    return result


# takes RAW message
def shiftEyeGlyph(message: list[str]) -> list[int]:
    # take message from google docs and shift it by two to follow PAM5 encoding
    # 0 becomes -2, 4 becomes 2
    result = []
    for i in range(len(message)):
        for c in message[i]:
            result.append((int(c) - 2))

    return result


# 3 -> -1, 4 -> -2
# takes listified message
def eyeGlyphAlpha(message: list[str]) -> list[int]:
    result = []
    for i in range(len(message)):
        for c in message[i]:
            if int(c) < 3:
                result.append(int(c))
            elif int(c) == 3:
                result.append(-1)
            else:
                result.append(-2)
    return result


# takes listified message
def eyeGlyphBeta(message: list[str]) -> list[int]:
    result = []
    for i in range(len(message)):
        for c in message[i]:
            if int(c) == 0:
                result.append(0)
            elif int(c) == 1:
                result.append(2)
            elif int(c) == 2:
                result.append(1)
            elif int(c) == 3:
                result.append(-2)
            else:
                result.append(-1)
    return result


def diffBTElements(data: list[int]) -> list[int]:
    result = []
    # find the difference in 'voltage' between each Eye
    for i in range(len(data) - 1):
        result.append(data[i + 1] - data[i])
    return result


def decode2B1Q(data: list[int]) -> str:
    result = ""
    # assuming positive prev level, use this table
    # next bits | prev: + | prev: -
    # 00        | +1      | -1
    # 01        | +2      | -2
    # 10        | -1      | +1
    # 11        | -2      | +2
    prev = 1
    for i in data:
        if i == 1:
            result += '00' if prev >= 0 else '10'
        elif i == 2:
            result += '01' if prev >= 0 else '11'
        elif i == -1:
            result += '10' if prev >= 0 else '00'
        elif i == -2:
            result += '11' if prev >= 0 else '01'
        else:
            # not sure what to do when it encounters 0's so for now set prev to 1 for assume positive
            # in these models 0 is meant for forward error correction so implement than when possible
            prev = 1
        prev = i

    return result


def plotSignal(data: list[int], title: str) -> None:
    plt.rcParams["figure.figsize"] = [20, 5]
    plt.rcParams["figure.autolayout"] = True

    x = range(len(data))
    fig, axs = plt.subplots()
    axs.set_title(title)
    axs.step(x, data, color='C0')
    axs.set_xlabel("Index")
    axs.set_ylabel("State")

    plt.show()


def formatTrigram(data: list[str]) -> list[str]:
    result = []
    stretchedString = ""
    # all messages have Even number of lines.
    # i have a hunch that the trigrams can be encoded in a zig-zag fashion instead of how it is in the docs
    for i in range(0, len(data) - 1, 2):
        listA = collections.deque(data[i])
        listB = collections.deque(data[i + 1])
        while listA and listB:
            stretchedString += listA.popleft()
            stretchedString += listB.popleft()
        if listA:
            stretchedString += listA.popleft()
        if listB:
            stretchedString += listB.popleft()
        i += 2

    trigram = ""
    for i in range(0, len(stretchedString) - 2, 3):
        trigram = stretchedString[i] + stretchedString[i + 1] + stretchedString[i + 2]
        result.append(trigram)

    return result


other2dec = lambda n, other: sum([(int(v) * other ** i) for i, v in enumerate(list(str(n))[::-1])])


def base5to10(data: list[str]) -> list[int]:
    result = []
    for d in data:
        result.append(other2dec(d, 5))

    return result


if __name__ == "__main__":
    # formatted this way in case i need to preserve the trigram nature of them for other decoding methods
    # east 1
    message0 = ["201013223304041130232114313033004024000",
                "032041220001422242122220110003201341113",
                "310221044000200104040144142033022034241",
                "231313130031132120142231331441341441211",
                "014003212114130041110100241241004031001",
                "040331432341122101010040120412442442402",
                "13331220330103113111211210322314",
                "1310424224130304110203123204313"]

    # west 1
    message1 = ["311013223304041130232114313033004024004",
                "032041220001422242122220110003201341101",
                "020201044000104044040144142033022034131",
                "111213130001102020142231331441341441401",
                "212223303244000243231110221231031022043",
                "403431401222111340210301413341221330132",
                "02414221422203024200123212402323201403",
                "3101322112130203222200422310313224113"]

    # east 2
    message2 = ["121013223304041130232114313033004024004",
                "132041220001422242122220110003201341132",
                "302013230044210143001214140311024104223",
                "102441113222231403330130231010322441422",
                "014113030144102020311114241034232132112",
                "141120120040103022122402040000103221040",
                "001132210042231043242013103010200300221",
                "020142240312031330231000103310441201422",
                "034201043101100200124",
                "131402022020141322311"]

    # west 2
    message3 = ["301014304231111130103200114211142042144",
                "132041002441200222141013240022220120402",
                "110120210044012022014100202130013243312",
                "401130112010322313431422313213031100003",
                "143110223024224201021223142200103111223",
                "203401230041222213132220230242140211440",
                "122201000012143101233312010224203221",
                "011010101321231103032030241320322030"]

    # east 3
    message4 = ["221014304000100302220231222232144144211",
                "332041002222431341003242000010220042431",
                "313223312120134004141302310001231043130",
                "020020140002021212311100003112220110032",
                "140214222023042001214241211223104010034",
                "003021031300212210310000312332003240422",
                "001240241020232043043031224131312301142",
                "232311130211021020222341412113240321230",
                "001030124221224033003211024213133231001",
                "410210103300432031412111422330403400041",
                "04124012304",
                "0423010104"]

    # west 3
    message5 = ["111014304044023101033232120113240032023",
                "432041002342120301441212222401420211130",
                "033031134224144111303003142234042131112",
                "431413200210141202112431230203111430021",
                "103133214200230011143034143033110122120",
                "101132211120442310131321231020311022200",
                "120120123130011024014133021023002220044",
                "210312220001440122003232142141332131220",
                "120224022234203033120244040200",
                "002121100141102242103402411442"]

    # east 4
    message6 = ["101014304000100000010213233120142133003",
                "232041002222431212430430300110203421130",
                "101004223210034300144214224022200300022",
                "303411022313202403302030222441142010141",
                "143234300120242230110301302001040030130",
                "012332401341341302441301412412222303322",
                "212222143130302013102113102230003103232",
                "432331411032403200122103112431440120231",
                "12202423010131123221303",
                "3421210220100323034034"]

    # west 4
    message7 = ["301014304000100000010213233120140040002",
                "232041002222431212430430300110222113142",
                "211310214001032122241124300100131223313",
                "030221230132301430413420300032332421140",
                "040210240103202210243021012103012033232",
                "402211103132412102142440311122021431141",
                "204233241203302023301041204241012232101",
                "311140311421232122410240132440030221440",
                "224314114042121114140130",
                "020231000031000102140011"]

    # east 5
    message8 = ["111014304000100000010213233120143044133",
                "332041002222431212430430300110211112430",
                "101214223302024014144212222230212213233",
                "303411022401202041302002242420240341202",
                "014110114103111010240110204010013100130",
                "211211130110441211112403410122040041213",
                "102041041221134130133013243011042010221",
                "020203002240010120442311042111142031102",
                "131224220222041",
                "232442101331431"]

    # for bulk processing each message
    messageList = [message0, message1, message2, message3, message4, message5, message6, message7, message8]

    # count each message for number of eyes
    result = []
    for message in messageList:
        for line in message:
            for c in line:
                result.append(int(c))
        print(len(result))
        result.clear()

    #wrt to message # 0-8:
    #297 eyes
    #309 eyes
    #354 eyes
    #306 eyes
    #411 eyes
    #372 eyes
    #357 eyes
    #360 eyes
    #342 eyes
