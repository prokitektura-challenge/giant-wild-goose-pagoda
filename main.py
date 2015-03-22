from pro import *

offset1 = 0.2
offsetHeight1 = 0.1

mainOffset = 0#param(0.3)
mainHeight = param(3.5)

columnWidth = param(0.8)
columnDepth = param(0.1)

#numColumns = (5, 5, 4, 4, 3, 3, 3)

numParts = 7

def init():
    global partIndex
    partIndex = 0


@rule
def Begin():
    init()
    rectangle(25, 25, replace=True)
    Basement()


@rule
def Basement():
    inset2(
        0.5, 5 >> BasementMaterial(),
        -offset1, 0 >> BasementMaterial(),
        0, offsetHeight1 >> BasementMaterial(),
        -offset1, 0 >> BasementMaterial(),
        0, offsetHeight1 >> BasementMaterial(),
        offset1, 0 >> BasementMaterial(),
        0, offsetHeight1 >> BasementMaterial(),
        1.5, 0 >> BasementMaterial(),
        cap>>Part()
    )

@rule
def BasementMaterial():
    return
    texture("MarekBrick004.jpg", 0.625, 0.625)


@rule
def PagodaMaterial():
    return
    texture("pagoda01.jpg", 0.5, 0.5)


@rule
def Part():
    global partIndex
    
    partIndex += 1
    
    inset2(
        mainOffset, mainHeight>>Side(partIndex),
        cap>>ConnectionBottom(partIndex)
    )


@rule
def Side(partIndex):
    windowSectionMargin = 1-partIndex*0.1
    
    PagodaMaterial()
    
    split(y,
        flt() >> split(x,
            flt() >> SideContent(partIndex, True),
            2+2*windowSectionMargin>>WindowSection(partIndex, windowSectionMargin),
            flt() >> SideContent(partIndex, False)
        ),
        rel(0.05)>>join(left, extrude(0.9*columnDepth), all>>PagodaMaterial())
    )


@rule
def SideContent(partIndex, locatedToTheLeft):
    if locatedToTheLeft:
        split(x,
            0.9*columnWidth>>join(left, extrude(columnDepth), all>>PagodaMaterial()),
            repeat(
                flt() >> BetweenColumns(),
                columnWidth>>extrude(columnDepth)
            )
        )
    else:
        split(x,
            repeat(
                columnWidth>>extrude(columnDepth),
                flt() >> BetweenColumns()
            ),
            0.9*columnWidth
        )


@rule
def BetweenColumns():
    split(y,
        flt(),
        rel(0.1) >> BetweenColumnsUpper()
    )


@rule
def BetweenColumnsUpper():
    split(y,
        flt() >> extrude(0.9*columnDepth),
        flt() >> split(x,
            flt(),
            rel(0.3) >> extrude(0.9*columnDepth),
            flt()
        )
    )


@rule
def WindowSection(partIndex, windowSectionMargin):
    if partIndex>1:
        split(y,
            flt() >> split(x,
                windowSectionMargin,
                flt()>> extrude(-0.7,
                    top>>extrude2(
                        0,1>>delete(), # it's hidden
                        0.1, 0.8,
                        0.2, 0.6,
                        0.5, 0.5,
                        cap2>>delete() # it's hidden
                    )
                ),
                windowSectionMargin
            ),
            rel(0.1) >> BetweenColumnsUpper()
        )
    else:
        BetweenColumns()


@rule
def ConnectionBottom(partIndex):
    insets = []
    for i in range(12):
        insets.extend((
            -0.1, 0 >> PagodaMaterial(),
            0, 0.1 >> PagodaMaterial()
        ))
    if partIndex<numParts:
        # call ConnectionUpper()
        insets.append(cap>>ConnectionUpper())
    
    inset2(
        *insets
    )


@rule
def ConnectionUpper():
    insets = []
    for i in range(12):
        insets.extend((
            0.2, 0 >> PagodaMaterial(),
            0, 0.1 >> PagodaMaterial()
        ))
        
    insets.append(cap>>Part())
    
    inset2(
        *insets
    )