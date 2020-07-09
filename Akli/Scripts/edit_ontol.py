from owlready2 import *
import rdflib
import pandas as pd
import  csv

#On inovque cette fonction afin de pouvoir ordonner les classes de notre ontologie dans une liste afin de pouvoir instancier les classes directement
def ordonner_classe(ontol):
    d = {}
    for i in ontol.classes():
        d[i.name] = i
    d = sorted(d.items(), key=lambda x: x[0])

    L = []
    for i in range(len(d)):
        L.append(d[i][1])
    return L

#Fonction pour pouvoir énumerer les classes de notre ontologie et nous les afficher
def enum_class(onto):
    liste = ordonner_classe(onto)
    cpt = 0
    for i in liste:
        print(cpt, '-', str(i).split('.')[-1])
        cpt += 1
    return liste

#Cette fonction nous permet de créer un patient dans notre ontologie
def create_patient(nom, prenom, age,poids,taille, sexe, maladiechronique, traitement, situationfam, dureederniervoyage,dureedepuisappsymp, daira, wilaya, symptomes):
    #On recupere la classe "Patient" de notre liste
    class_patient = onto.Patient
    #On instancie un objet de la classe
    P = class_patient()

    #A partir de la on va instancier les valeurs des attributs de notre objet patient
    P.patientID = P.iri.split('#')[-1]
    P.Nom = nom
    P.Prenom.append(prenom)
    P.Age = age
    P.Sexe = sexe
    P.Poids = poids
    P.taille = taille

    P.Traitement.append(traitement)

    P.SituationFamiliale.append(situationfam)
    P.DureeDepuisDernierVoyage.append(dureederniervoyage)
    P.DureeDepuisApparitionDesSymptomes.append(dureedepuisappsymp)


    #On utilise une requete sparql afin de trouver la daira et wilaya de notre patient et lié notre patient a eux via une relation "estLocalise"
    requete = """
    prefix ns1: <http://sararaouf.org/onto.owl#> 
    prefix ns2: <http://www.w3.org/2002/07/owl#> 
    prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
    prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
    prefix xml: <http://www.w3.org/XML/1998/namespace> 
    prefix xsd: <http://www.w3.org/2001/XMLSchema#> 
    SELECT     ?d ?w
    WHERE{
    ?d rdf:type ns1:Daira .
    ?d ns1:nomDaira ?nd .
    ?w rdf:type ns1:Wilaya .
    ?w ns1:nomWilaya ?wn .
    ?d ns1:communeDe ?w . 
    FILTER regex(?nd,"var1")  
    FILTER regex(?wn,"var2")
    }
    """.replace("var1", daira).replace("var2",wilaya)
    result = graph.query(requete)
    for i in result:
        print(i)
        P.estLocalise.append(onto.search(iri=i[0])[0])

    #Au lieu d'utiliser une requete sparql , on utilise la fonction search de owlready afin de pouvoir trouver les maladies chroniques de patient existante dans notre base rdf pour les lier , et si il n'existe pas on le crée puis on les lie
    list_maladiechronique = maladiechronique.split(',')
    for j in list_maladiechronique:
        requete = """
                    prefix ns1: <http://sararaouf.org/onto.owl#> 
                    prefix ns2: <http://www.w3.org/2002/07/owl#> 
                    prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
                    prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
                    prefix xml: <http://www.w3.org/XML/1998/namespace> 
                    prefix xsd: <http://www.w3.org/2001/XMLSchema#> 
                    SELECT     ?m ?mn
                    WHERE{
                    ?m rdf:type ns1:MaladieChronique .
                    ?m ns1:nomMaladie ?mn.
                     FILTER regex(?mn,"var")  
                    }
                    """.replace("var", j.replace(" ", "_"))
        result = graph.query(requete)
        if (list(result) == []):
            class_mch = onto.MaladieChronique
            M = class_mch()
            M.iri = ns + j.replace(" ", "_")
            M.nomMaladie = j.replace(" ", "_")
            P.estMaladeDe.append(M)
        else:
            P.estMaladeDe.append(onto.search(iri=list(result)[0][0])[0])

    #Meme procede que les maladies chroniques pour les symptomes
    list_symptomes = symptomes.split(',')
    for j in list_symptomes:
        requete = """
            prefix ns1: <http://sararaouf.org/onto.owl#> 
            prefix ns2: <http://www.w3.org/2002/07/owl#> 
            prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
            prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
            prefix xml: <http://www.w3.org/XML/1998/namespace> 
            prefix xsd: <http://www.w3.org/2001/XMLSchema#> 
            SELECT     ?s ?sn
            WHERE{
            ?s rdf:type ns1:Symptomes .
            ?s ns1:nomSymptomes ?sn.
             FILTER regex(?sn,"var")  
            }
            """.replace("var",j.replace(" ","_"))
        result = graph.query(requete)
        if (list(result) == []):
            requete = """
                        prefix ns1: <http://sararaouf.org/onto.owl#> 
                        prefix ns2: <http://www.w3.org/2002/07/owl#> 
                        prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
                        prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
                        prefix xml: <http://www.w3.org/XML/1998/namespace> 
                        prefix xsd: <http://www.w3.org/2001/XMLSchema#> 
                        SELECT     ?s ?sn
                        WHERE{
                        ?s rdf:type ns1:SymptomesCovid .
                        ?s ns1:nomSymptomes ?sn.
                        FILTER regex(?sn,"var")  
                        }
                        """.replace("var",j.replace(" ","_"))
            result = graph.query(requete)
            if(list(result)==[]):
                class_symp = onto.Symptomes
                S = class_symp()
                S.nomSymptomes = j.replace(" ", "_")
                P.aSymptomes.append(S)
            else:
                P.aSymptomes.append(onto.search(iri=list(result)[0][0])[0])
        else:
            P.aSymptomes.append(onto.search(iri=list(result)[0][0])[0])
    synchro()
    onto.save("sortiefinal.owl", format="ntriples")

#Cette fonction quant a elle nous permets de créer un objet medecin dans notre base rdf
def create_medecin(nom, prenom, sexe,specialite):
    class_medecin = onto.Medecin
    M = class_medecin()
    M.medecinID = M.iri.split('#')[-1]
    M.Nom = nom
    M.Prenom.append(prenom)
    M.Sexe = sexe
    requete = """
    prefix ns1: <http://sararaouf.org/onto.owl#> 
    prefix ns2: <http://www.w3.org/2002/07/owl#> 
    prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
    prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
    prefix xml: <http://www.w3.org/XML/1998/namespace> 
    prefix xsd: <http://www.w3.org/2001/XMLSchema#> 
    SELECT     ?s ?ns
    WHERE{
    ?d rdf:type ns1:Specialite .
    ?s ns1:nomSpecialite ?ns .
    FILTER regex(?ns,"var1")  
    }
    """.replace("var1", specialite)
    result = graph.query(requete)
    M.estSpecialise.append(onto.search(iri=list(result)[0][0])[0])

#Cette fonction nous permets de traduire un fichier csv et l'inserer dans notre base rdf
def fromcsvtordf(path):
    patients = pd.read_csv(path,encoding='latin-1')
    for i in range(len(patients)):
        patient = patients.iloc[i]
        create_patient( patient[1], patient[2], int(patient[3]),float(patient[4]),float(patient[5]), patient[6], patient[7], patient[8],
                       patient[9], int(patient[10]), int(patient[11]), patient[12], patient[13],patient[14])


#Les fonctions d'enrichissements

#Cette fonction nous a permit d'enrichir notre base rdf en insérant les wilayas quand on  a pu trouvé dans un fichier csv qu'un saint samaritain nous a donné
def enrichissementwilaya(path):
    wilayas = pd.read_csv(path)
    for i in range(len(wilayas)):
        class_wilaya = onto.Wilaya
        W = class_wilaya()
        nom_wilaya = wilayas.iloc[i]['nom'].replace(" ", "_")
        W.iri = ns + "wilaya" + str(wilayas.iloc[i]['code'])
        W.nomWilaya = nom_wilaya
        code_wilaya = wilayas.iloc[i]['code']
        W.idWilaya = str(code_wilaya)

#Meme chose pour les dairas , sauf qu'en plus de ca , on lie les Dairas a leur Wilayas respectives
def enrichissementdaira(path):
    dairas = pd.read_csv(path)
    for i in range(len(dairas)):
        class_daira = onto.Daira
        D = class_daira()
        # Le if suivant est pour reglé le probleme des communes dont l'id commence par un 0
        if len(str(dairas.iloc[i]['code_postal'])) == 4:
            D.iri = ns + "0" + str(dairas.iloc[i]['code_postal'])
        else:
            D.iri = ns + str(dairas.iloc[i]['code_postal'])
        # print(D.iri)
        D.nomDaira = dairas.iloc[i]['nom'].replace(" ", "_")
        D.communeDe.append(onto.search(iri="*" +"wilaya"+ str(dairas.iloc[i]['wilaya_id']))[0])

#On enrichit notre base de donnés avec les symptomes fréquents du covid trouvés sur internet
def enrichissementsympcov(path):
    f = open(path,"r")
    sympcov = f.readlines()
    for i in sympcov:
        class_sympcov = onto.SymptomesCovid
        SC = class_sympcov()
        SC.nomSymptomes = i.capitalize().replace(" ","_").replace("\n","")

#Quand a ceux la , ce sont les symptomes qui n'ont pas de rapports avec le covid
def enrichissementsymp(path):
    f = open(path,"r",encoding="utf-8")
    symp = f.readlines()
    for i in symp:
        class_symp = onto.Symptomes
        S = class_symp()
        S.nomSymptomes = i.capitalize().replace(" ","_").replace("\n","")
    pass

#Enrichissement des maladies chroniques
def enrichissementmaladiechronique(path):
    f = open(path,"r",encoding="utf-8")
    maladies = f.readlines()
    for i in maladies:
        class_maladiechro = onto.MaladieChronique
        M = class_maladiechro()
        M.nomMaladie = i.capitalize().replace(" ","_").replace("\n","")


def enrichissementspecialite(path):
    f = open(path,"r",encoding="utf-8")
    specialites = f.readlines()
    for i in specialites:
        class_spe = onto.Specialite
        SP = class_spe()
        SP.nomSpecialite = i[0:-1]

def enrichissementhopital(path):
    f = open(path,"r",encoding="latin-1")
    specialites = f.readlines()
    for i in specialites:
        class_H = onto.Hopital
        H = class_H()
        H.nomHopital = i[0:-1]







#Cette fonction nous permets de relié l'orientation donné par un medecin sur un patient donné
def orientation(type_orientation,IDmedecin,IDpatient):
    patient = onto.search(iri=ns + "patient" + str(IDpatient))[0]
    medecin = onto.search(iri=ns + "medecin" + str(IDmedecin))[0]
    if type_orientation == "Prise en charge a domicile":
        class_pec = onto.PCDomicile
        pec = class_pec()
        pec.nomOrientation.append(type_orientation)
        patient.estConcerneParOrientation.append(pec)
        medecin.prescritOrientation.append(pec)
        print("orientation faite")

    if type_orientation == "Redirection vers hopital":
        class_hop = onto.Hopital
        hop = class_hop()
        hop.nomOrientation.append(type_orientation)
        patient.estConcerneParOrientation.append(hop)
        medecin.prescritOrientation.append(hop)
        print("orientation faite")

    if type_orientation == "Prise de rendez-vous":
        class_rdv = onto.RDV
        rdv = class_rdv()
        rdv.nomOrientation.append(type_orientation)
        patient.estConcerneParOrientation.append(rdv)
        medecin.prescritOrientation.append(rdv)
        print("orientation faite")


#Cette fonction nous permets de créer une fiche pour un patient en recoltant ses informations via une requete sparql
def créationfiche(IDpatient):

    dic_info={}
    list_info = []
    list_symp = []
    list_malad = []
    list_med = []
    requete = """
    prefix ns1: <http://sararaouf.org/onto.owl#> 
    prefix ns2: <http://www.w3.org/2002/07/owl#> 
    prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    prefix xml: <http://www.w3.org/XML/1998/namespace>
    prefix xsd: <http://www.w3.org/2001/XMLSchema#>
    SELECT  ?id ?nom ?prenom  ?age ?sexe  ?situationfam ?dureevoyage ?dureesymp   ?traitement   ?ndaira  ?nwilaya ?poids ?taille ?s ?maladiechronique ?norientation ?idmed ?nommed
    WHERE{
    ?p rdf:type ns1:Patient .
    ?p ns1:patientID ?id .
    ?p ns1:Nom ?nom .
    ?p ns1:Age ?age .
    ?p ns1:Sexe ?sexe .
    ?p ns1:DureeDepuisDernierVoyage ?dureevoyage .
    ?p ns1:DureeDepuisApparitionDesSymptomes ?dureesymp .
    ?p ns1:Prenom ?prenom .
    ?p ns1:Poids ?poids .
    ?p ns1:Taille ?taille .
    ?p ns1:estMaladeDe ?maladiechronique .
    ?p ns1:Traitement ?traitement .
    ?p ns1:SituationFamiliale ?situationfam .
    ?p ns1:aSymptomes ?s .
    ?p ns1:estLocalise ?daira .
    ?daira ns1:communeDe ?wilaya .
    ?daira ns1:nomDaira ?ndaira .
    ?wilaya ns1:nomWilaya ?nwilaya .
    ?p ns1:estConcerneParOrientation ?orientation .
    ?m ns1:prescritOrientation ?orientation .
    ?orientation ns1:nomOrientation ?norientation .
    ?m ns1:medecinID ?idmed .
    ?m ns1:Nom ?nommed .
    FILTER regex(?id , "^var")
    }
        """.replace("var", IDpatient)
    result = graph.query(requete)
    for i in result:
        print(i)
    # Ici on receuille les infos fixes du patient ( pourquoi fixe ?car un patient peut avoir plusieurs symptomes / maladie chronique et donc le résultat de  la requete sparql sera sur plusieurs lignes)
    for i in range(13):
        list_info.append(list(result)[0][i])

    #Donc on utilise cette fonction pour receuillir les maladies chroniques
    for i in result:
        if str(i[12]).split('#')[1] not in list_malad:
            list_malad.append(str(i[12]).split('#')[1])

    #Et celle la pour les symptomes
    for i in result:
        if str(i[11]).split('#')[1] not in list_symp:
            list_symp.append(str(i[11]).split('#')[1])

    for i in range(13,16):
        list_med.append(list(result)[0][i])


#?id ?nom ?prenom  ?age ?sexe ?situationfam ?dureevoyage ?dureesymp   ?traitement   ?ndaira  ?nwilaya ?s ?maladiechronique ?orientation ?idmed ?nommed
    dic_info['Id'] = list_info[0]
    dic_info['Nom'] = list_info[1]
    dic_info['Prenom'] = list_info[2]
    dic_info['Age'] = list_info[3]
    dic_info['Sexe'] = list_info[4]
    dic_info['Situation familiale'] = list_info[5]
    dic_info['Durée depuis dernier voyage'] = list_info[6]
    dic_info['Durée depuis apparition des symptomes'] = list_info[7]
    dic_info['Traitement suivi'] = list_info[8]
    dic_info['Daira de résidence'] = list_info[9]
    dic_info['Wilaya de résidence'] = list_info[10]
    dic_info['Poids'] = list_info[11]
    dic_info['Taille'] = list_info[12]

    dic_info['Maladies chroniques'] = list_malad
    dic_info['Symptomes'] = list_symp
    dic_info['Orientation prescrite'] = list_med[0]
    dic_info['Id  medecin en charge'] = list_med[1]
    dic_info['Nom du medecin en charge'] = list_med[2]

    dict_fiches.append(dic_info)
    return dic_info.keys()


#Cette fonction nous permettra de générer un fichier csv contenant l'ensemble des patients avec leurs informations personnels en plus de leur orientation et le medecin en charge de l'orientation
def générationfiches():
    requete = """
        prefix ns1: <http://sararaouf.org/onto.owl#> 
        prefix ns2: <http://www.w3.org/2002/07/owl#> 
        prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        prefix xml: <http://www.w3.org/XML/1998/namespace>
        prefix xsd: <http://www.w3.org/2001/XMLSchema#>
        SELECT  ?p
        WHERE{
        ?p rdf:type ns1:Patient     
        }
         """
    result = graph.query(requete)
    for i in result:
        print(i)
    for i in range(len(list(result))):
        col = créationfiche(str(i+1))
    csv_file = "fiches.csv"
    csv_columns = col
    with open(csv_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for data in dict_fiches:
            writer.writerow(data)


def enrichissement():
    enrichissementwilaya("../ressources/wilaya.csv")
    enrichissementdaira("../ressources/communes.csv")
    enrichissementsymp("../ressources/sym.txt")
    enrichissementsympcov("../ressources/sym_covid.txt")
    enrichissementmaladiechronique("../ressources/maladie_chronique.txt")
    enrichissementspecialite("../ressources/specialite_medecine.txt")
    enrichissementhopital("../ressources/hopital.txt")



def synchro():
    with onto:
        sync_reasoner()
#--------------------------------------------------------------------------------------------------------------------------------
#Main


#On recupere notre ontologie

onto = get_ontology(".\sortiefinal.owl").load()
ns = "http://sararaouf.org/onto.owl#"
dict_fiches=[]
owlready2.JAVA_EXE = "C:\\Program Files (x86)\\Common Files\\Oracle\\Java\\javapath\\java.exe"


#on utilise rdflib afin de concevoir le graph sur lequel nous appliquerons nos requetes
graph = rdflib.Graph()
graph.parse("sortiefinal.owl",format="turtle")
open("sortieturtle.rdf","w")
graph.serialize("sortieturtle.rdf",format="turtle")

#Cette fonction appelle les multiples enrichissements
#enrichissement()

#On utilise cette fonction pour prendre les données d'un fichier csv et les mettres dans notre ontologie
#fromcsvtordf("../ressources/test.csv")

#create_medecin("Bakir","Djamal","Homme","Pédiatrie")

#orientation("Redirection vers hopital","0002",2)
#orientation("Prise en charge a domicile","0002",1)

#générationfiches()

#On invoque le raisonneur Hermit
#synchro()



#On sauvegarde notre ontologie
onto.save("sortiefinal.owl", format="ntriples")
graph.serialize("sortieturtle.rdf",format="turtle")
