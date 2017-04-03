import glob, os

class Segment:
    def __init__(self, lines):
        self.source = lines;
        self.commands = []

        for text in lines:
            buffer = ""
            deepness = 0
            if (text == "" or text == "\n"):
                self.commands.append(Command(""))
                continue

            while (text.find("]]]]") != -1):
                text = text.replace("]]]]", "]];]]");

            while (text.find(" ;") != -1):
                text = text.replace(" ;", ";");

            while (text[-1] == "\n" or text[-1] == " "):
                text = text[:-1]
        
            if (text[-1] != ";"):
                text += ";"
            
            for i in range(0, len(text)):
                if (text[i] == "[" and text[i + 1] == "["):
                    deepness += 1
                    buffer += text[i]
                elif (text[i] == "]" and text[i + 1] == "]"):
                    deepness -= 1
                    buffer += text[i]
                elif (text[i] == ";" and deepness == 0):
                    self.commands.append(Command(buffer))
                    buffer = ""
                else:
                    buffer += text[i]
    def output(self):
        return self.output("")
    def output(self, prefix):
        out = ""
        for data in self.commands:
            out += data.output(prefix)
        return out

class Command:
    def __init__(self, work):
        self.work = work
        self.type = "normal"
        if work.find("ELAGAZAS") == 0:
            cntstart = work.find("[[")
            self.cond = work[9:(cntstart-1)]
            self.content = work[(cntstart+2):-2]
            self.subsegment = Segment([self.content]);
            self.type = "condition"
        if work.find("CIKLUS") == 0:
            cntstart = work.find("[[")
            self.cond = work[7:(cntstart-1)]
            self.content = work[(cntstart+2):-2]
            self.subsegment = Segment([self.content]);
            self.type = "cicle"
    def output(self, prefix):
        out = ""
        if (self.type == "normal"):
            out = prefix + self.work + "\n"
        elif (self.type == "condition"):
            out = prefix + "if " + self.cond + " :\n"
            out += self.subsegment.output(prefix + "    ")
        elif (self.type == "cicle"):
            out = prefix + "for " + self.cond + " :\n"
            out += self.subsegment.output(prefix + "    ")
        return out

dir_path = os.path.dirname(os.path.realpath(__file__))
for ff in os.listdir(dir_path):
    if ff.endswith(".prog"):
        td = file(ff, "r");
        sg = Segment(td.readlines())
        o = file(ff.replace(".prog", ".py"), "w")
        o.write(sg.output(""))
        o.close();
