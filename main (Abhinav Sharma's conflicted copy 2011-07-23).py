from subprocess import Popen, PIPE, STDOUT

import json


class FBCircles(object):
    def __init__(self):
        self.userDict = dict()
        self.groups = []

    def runDemo(self, GDFfilename):
        self.runGDF(GDFfilename)
        Q=self.runFirstPass(GDFfilename + '.pairs')
        self.runSecondPass(GDFfilename + '.pairs', Q)
        print json.dumps(self.readGroups(GDFfilename))
    
    def readGroups(self, filename):
        f = open(filename + '-fc_second_run.groups','r')
        lines = f.readlines()
        
        groups = []
        currentGroup = []
    
        for line in lines:
            if line[:5] == 'GROUP':
                if len(currentGroup) > 0:
                    groups.append({
                        "type": 'group',
                        "id": len(groups),
                        "group": currentGroup
                    })
                    currentGroup = []
                print line
            else:
                print self.userDict[int(line.strip())]
                currentGroup.append({
                    "type": 'person',
                    "id": int(line.strip()),
                    "name": self.userDict[int(line.strip())],
                    "pic_url": "http://www.facebook.com/placeholder.jpg"
                })
    
    
        f.close()
        
        self.groups = groups
        
        return groups

    def runFirstPass(self, filename):
        cmd = "././native/FastCommunityMH -f %s -l first_run" % filename
        p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
        out = p.stdout.read()
        # Hilarious string split hackery
        Qvalue = out.split('\n')[-3].split(']')[0].split('[')[1]
        return Qvalue
    
    def runSecondPass(self, filename, Qvalue):
        cmd = "././native/FastCommunityMH -f %s -l second_run -c %s" % (filename,int(int(Qvalue)))
        p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
        out = p.stdout.read()    

    def runGDF(self, filename, write_dict_to_fs=False):
        f = open(filename,'r')
    
        fo = open(filename + '.pairs','w')
    
        lines = f.readlines()
    
        self.userDict = dict()
    
        for line in lines:
            if '>' in line:
                continue
            if ',' in line:
                #edge
                nodesConnected = line.strip().split(',')

                nodeIDs = [str(self.userDict[i]) for i in nodesConnected]
            
                if None in nodeIDs:
                    print "Error!"
                    print nodesConnected
                    return

                fo.write('\t'.join(nodeIDs) + '\n')
            else:
                curIdx = len(self.userDict)
                self.userDict[line.strip()] = curIdx

    
        f.close()
        fo.close()
    
        if write_dict_to_fs:
            fo2 = open(filename + '.dict','w')

            for nodeName,nodeID in self.userDict.items():
                fo2.write("%s,%s\n" % (nodeName,nodeID))
            fo2.close()
        else:
            for nodeName,nodeID in self.userDict.items():
                self.userDict[int(nodeID)] = nodeName
        # print self.userDict
        

if __name__ == '__main__':
    circles = FBCircles()
    circles.runDemo('abinav.gdf')
