import os
import sys

NativeNames = set()
Args = []
NativeDict = dict()
StartString = "{"
TemplateMidleString = \
    """
    "%s": {
        "prefix": "%s", 
        "body": "%s",
        "description": [
            "%s"
        ]
    },
    """
EndString = "}"
FinalString = ""
EnabledDocs = False


def GetNextLine(tab, idx):
    return tab[idx + 1] if len(tab) - 1 >= idx + 1 else "native"

File = open("AllFiveMNatives.lua", "r" , encoding="utf8")
Line = File.readlines()
for idx , l in enumerate(Line):
    if l.find("native") != -1:
        Native = l.split(" ")[1].replace("\"", "").split("_")
        _Final = ""
        for t in Native:
            _Final += t.lower().capitalize()
        print(_Final)
        NativeNames.add(_Final.rstrip("\n"))
        NativeDict[_Final.rstrip("\n")] = {
            "hasArgs": False,
            "hasDocs": False,
            "Args": set(),
            "Docs": ""
        }
        TempIdx = idx
        while GetNextLine(Line, TempIdx).find("native") == -1:

            if GetNextLine(Line, TempIdx).find("arguments") != -1:
                
                NativeDict[_Final.rstrip("\n")]["hasArgs"] = True

                TempArgs = set()
                AnotherIdx = TempIdx + 1
                while GetNextLine(Line, AnotherIdx).find("}") == -1:
                    TempArgs.add(
                        GetNextLine(Line, AnotherIdx)
                        .replace(" " , "" ) # Remove space
                        .replace("\"", "_") # Remove ""
                        .replace("," , "") # Remove ,
                        .replace("\t" , "") # Remove tabulation
                        .rstrip("\n") # Remove EOL
                        .replace("_", "(" , 1) # Open
                        .replace("_" , ")" , 1) # Close
                        )
                    AnotherIdx += 1
                
                NativeDict[_Final.rstrip("\n")]["Args"] = TempArgs
            
            if GetNextLine(Line, TempIdx).find("doc") != -1:
                if GetNextLine(Line, TempIdx + 1).find("summary") != -1:
                    NativeDict[_Final.rstrip("\n")]["hasDocs"] = True
                    TempDocs = ""
                    AgainAnotherIdx = TempIdx + 3
                    while GetNextLine(Line, AgainAnotherIdx).find("]]") == -1:
                        TempDocs += GetNextLine(Line, AgainAnotherIdx).replace("\"", "'")
                        # print(TempDocs)
                        AgainAnotherIdx += 1
                    
                    NativeDict[_Final.rstrip("\n")]["Docs"] = TempDocs



            TempIdx += 1


for key, value in NativeDict.items():
    print(key)
    print(value)

JsonFile = open("__Final.json", "w", encoding="utf8")
FinalString += StartString
ArgsString = ""
IdxArgs = 0
for key , value in NativeDict.items():
    print("Key : " + key)
    if value["hasArgs"]:
        TempString = ""
        ArgsString = "(%s)"
        for args in value["Args"]:
            if (IdxArgs + 1) != len(value["Args"]):
                TempString += "${%s: %s}," % (str(IdxArgs + 1), args)
            else:
                TempString += "${%s: %s}" % (str(IdxArgs + 1), args)
            IdxArgs += 1
        
        if TempString != "":
            ArgsString = ArgsString % TempString
        else:
            ArgsString = ArgsString % ""

        IdxArgs = 0
        # print(ArgsString)
    else:
        ArgsString = "()"
    

    FinalString += TemplateMidleString % (key, key, "%s%s" % (key, ArgsString), value["Docs"].replace("\n", "\",\"") if value["Docs"] and EnabledDocs else "")

FinalString += EndString
# print(FinalString)
JsonFile.write(FinalString)
JsonFile.close()