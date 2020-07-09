from flask import Flask, render_template,request,redirect
from edit_ontol import *

app = Flask(__name__)

onto = get_ontology("F:\Raouf\Licence\L3\Web sémantique\Projet\sortiefinal.owl").load()
ns = "http://sararaouf.org/onto.owl#"
dict_fiches=[]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/consultation',methods =['GET','POST'])
def consultationform():
    if request.method =='POST':
        create_patient(request.form['nom'],request.form['prenom'],int(request.form['age']),float(request.form['poids']),float(request.form['taille']),request.form['sexe'],request.form['maladies'],request.form['traitement'],request.form['situationfam'],int(request.form['dureevoyage']),int(request.form['dureesymp']),request.form['daira'],request.form['wilaya'],request.form['symptomes'])
        return redirect('/')
    else:
        return render_template('Inscription.html')



@app.route('/med',methods=['GET','POST'])
def med():
    if request.method =='POST':
        create_medecin(request.form['nom'],request.form['prenom'],request.form['sexe'],request.form['specialite'])
        return redirect('/')
    else:
        return render_template('medecin.html')


if __name__ == "__main__":
    app.run(debug=True)

 


