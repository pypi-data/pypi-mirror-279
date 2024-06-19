"""
Create a new Project
"""
from phases.commands.run import Run

from pyPhases import Project


class Explain(Run):
    """create a Phase-Project"""

    def parseRunOptions(self):
        super().parseRunOptions()

        if "<dataid>" in self.options:
            self.what = self.options["<dataid>"]

    def runProject(self, project: Project):
        self.explain(project, self.what)

    def explainString(self, values, fieldNames):
        valueLength = [len(v) + 1 for v in values]
        valuePositions = [sum(valueLength[:(i)]) for i in range(len(values))]
        # valueLength[0] = 0
        linePositions = [0]
        fieldLines = [""]
        for valueIndex, valuePosition in enumerate(valuePositions):
            useLine = -1
            # find empty spots in current lines
            for index, linePosition in enumerate(linePositions):
                if valuePosition > linePosition or linePositions == 0:
                    useLine = index
                    break
                    
            # create new Line if neccessary
            if useLine == -1:
                useLine = len(fieldLines)
                fieldLines.append("")
                linePositions.append(0)
            
            # fill the line to current position
            if valuePosition > 0:
                fieldLines[useLine] += " " * (valuePosition - linePositions[useLine] - 1)
            
            name = fieldNames[valueIndex]
            if valuePosition > 0:
                name = "|" + name
                # fieldLines[useLine] += "|"
            fieldLines[useLine] += name
            # update positions
            # for i in range(useLine):

            linePositions[useLine] = len(fieldLines[useLine])
            # print("-".join(values))
            # print("\n".join(fieldLines))
        return "\n".join(fieldLines)

    def explain(self, project:Project, what):
        self.log("Try to explain: %s"%what)
        try:
            phase = project.getPhaseForData(what)
            if phase is not None:
                self.log(f"data is generated in phase: {phase.name}")

            self.log("\tit depends on following config values:")
            dataObj = project.getDataFromName(what)
            fields = []
            for f, v in dataObj.getDependencyDict().items():
                self.log("%s: \t%s"%(f, v))
                if v is not None:
                    fields.append(f)
            self.log("data id: %s"%dataObj.getDataId())
            dataId, version = dataObj.getDataId().split("--")
            # dataId = dataObj.getDataId()
            values = dataId.split("-")
            fields = list(dataObj.getDependencyDict().keys())

            valueString = "-".join(values)
            explainBlock = self.explainString(values, fields)
            self.log("Current value string looks like this:")
            print(valueString)
            print(explainBlock)
        except:
            pass

        if what in project.phaseMap:
            self.log(f"{what} is a phase")
