import os

from flask import Flask, render_template, redirect, request

from uuid import uuid1

from fastcommunity import FBCircles

app = Flask(__name__)

@app.route("/",methods=['GET','POST'])
def main():
    if request.method == 'POST':
        if not(os.path.exists('userdata/')):
            os.mkdir('userdata')
        
        f = request.files['gdf_file']
        # Save to random file.
        
        randomUUID = str(uuid1())
        GDFfilename = '/tmp/' + 'temp.gdf'#randomUUID + '.gdf'
        
        f.save(GDFfilename)
        
        circlesObj = FBCircles()
        
        circlesObj.runGDF(GDFfilename)
        Q=circlesObj.runFirstPass(GDFfilename + '.pairs')
        
        os.mkdir('userdata/' + randomUUID)
        
        for i in range(9):
            circlesObj.runSecondPass(GDFfilename + '.pairs', int(Q*((i+1)/9.0)))
            fo = open('userdata/%s/%s.json' % (randomUUID,i),'w')
            fo.write(circlesObj.readGroups(GDFfilename))
            fo.close()
        # print json.dumps(self.readGroups(GDFfilename))
        
        return redirect('view/' + randomUUID)
    else:
        return render_template("main.html")

@app.route("/view/<uuid>")
def view(uuid):
    return render_template('view.html', userUUID = uuid)
    
@app.route("/fetch/<user>/<int:stage>")
def fetch(user,stage):
    filepath = "userdata/%s/%s.json" % (user,stage)
    if os.path.exists(filepath):
        f = open(filepath,'r')
        filedata = f.read()
        f.close()
        
        return filedata
    return "Doesn't exist. :("

if __name__ == "__main__":
    app.config.update(DEBUG=True,PROPAGATE_EXCEPTIONS=True,TESTING=True)
    app.run()