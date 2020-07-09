from owlready2 import *
import rdflib


default_world.set_backend(filename="file_back3.sqlite3", exclusive=False)

onto = get_ontology("http://sararaouf.org/onto.owl")
Url = "http://sararaouf.oms/Covid_ont#"

with onto:
    # Class and Data Property
    class Humain(Thing):
        pass


    class Sexe(DataProperty, FunctionalProperty):
        range = [str]
        domain = [Humain]


    class Age(DataProperty, FunctionalProperty):
        range = [int]
        domain = [Humain]


    class Nom(DataProperty, FunctionalProperty):
        range = [str]
        domain = [Humain]


    class Prenom(DataProperty):
        range = [str]
        domain = [Humain]


    class Patient(Humain):
        pass

    class Poids(DataProperty, FunctionalProperty):  # Unicité a questionner
        range = [float]
        domain = [Patient]
        pass

    class Taille(DataProperty, FunctionalProperty):  # Unicité a questionner
        range = [float]
        domain = [Patient]
        pass

    class patientID(DataProperty, FunctionalProperty):  # Unicité a questionner
        range = [str]
        domain = [Patient]
        pass


    class TrancheAge(Patient >> str):
        pass


    class MaladieChronique(Thing):
        pass

    class nomMaladie(DataProperty,FunctionalProperty):
        domain = [MaladieChronique]
        range = [str]
        pass

    class estMaladeDe(Patient >> MaladieChronique):
        pass




    class Traitement(Patient >> str):
        pass


    class SituationFamiliale(Patient >> str):
        pass


    class DureeDepuisDernierVoyage(Patient >> int):  # Jour
        pass


    class DureeDepuisApparitionDesSymptomes(Patient >> int):  # Jour
        pass


    class Medecin(Humain):
        pass


    class medecinID(DataProperty, FunctionalProperty):
        domain = [Medecin]
        range = [str]
        pass



    class Specialite(Thing):
        pass

    class nomSpecialite(DataProperty, FunctionalProperty):
        domain = [Specialite]
        range = [str]
        pass

    class estSpecialise(Medecin >> Specialite):
        pass

    class Localisation(Thing):
        pass


    class Wilaya(Localisation):
        pass


    class nomWilaya(DataProperty,FunctionalProperty):
        domain = [Wilaya]
        range = [str]

    class idWilaya(DataProperty,FunctionalProperty):
        domain = [Wilaya]
        range = [str]
        pass


    class Daira(Localisation):
        pass




    class nomDaira(DataProperty,FunctionalProperty):
        domain = [Daira]
        range = [str]


    class communeDe(Daira >> Wilaya):
        pass



    class estLocalise(Thing >> Localisation):
        pass


    class Symptomes(Thing):
        pass


    class SymptomesCovid(Symptomes):
        pass

    class nomSymptomes(DataProperty,FunctionalProperty):
        domain = [Symptomes]
        range = [str]

    class aSymptomes(Patient >> Symptomes):
        pass


    class SuspectCovid(Thing):
        equivalent_to = [Patient & aSymptomes.min(2,SymptomesCovid)]

    class Orientation(Thing):
        pass


    class Hopital(Thing):
        pass

    class nomHopital(DataProperty,FunctionalProperty):
        domain = [Hopital]
        range = [str]




    class RDV(Orientation):
        pass

    class dateRDV(RDV >> str):
        pass

    #Prise en charge
    class PCDomicile(Orientation):
        pass

    class nomOrientation(Orientation >> str):
        pass

    class Fiche(Thing):
        pass


    class patientConcerne(Fiche >> Patient):
        pass


    class medecinConcerne(Fiche >> Medecin):
        pass





    class estConcerneParOrientation(Patient >> Orientation):
        pass

    class estRedirigeVersHopital(Patient >> Hopital):
        pass

    class prescritOrientation(Medecin >> Orientation):
        pass

    AllDisjoint([Daira, Wilaya,Specialite,Symptomes,MaladieChronique,Patient,Medecin,Orientation,])


onto.save("sortie.owl", format="ntriples")





