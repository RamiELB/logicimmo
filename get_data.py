#! /usr/bin/python3
#coding:utf-8
from bs4 import BeautifulSoup
from requests import *
import sys
import datetime

#sinon, on a une erreur qui dit que notre navigateur est trop ancien
headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36'}


dict_ville = {
    'montpellier' : '239',
    'rouen' : '304',
    'amiens' : '16',
    'angers' : '18',
    'orleans' : '262',
    'lille' : '193',
    'rennes' : '294',
    'grenoble' : '144',
    'nantes' : '240',
    'saint-etienne' : '319',
    'clermont-ferrand' : '91'
    'caen' : '56',
    'nantes' : '240',
    'cannes' : '59'
}

def make_url(ville, locaouvente):
    url = 'https://www.logic-immo.com/'+locaouvente+'-immobilier-'+ville+'-tous-codes-postaux,'+dict_ville[ville]+'_99/options/groupprptypesids=1,2,6,7,12'
    return url

def get_nb_pages(url):
    r = get(url, headers = headers, timeout = 5)   
    page = BeautifulSoup(r.text,'html.parser')
    l = page.find_all('a', {'class' : 'btn btn-lightgrey'})
    try:
        l = [int(x.text) for x in l]
        nbpages = max(l)
    except:
        print('Erreur dans nbpages')
        sys.exit()

    return nbpages

def one_page(url, res):
    eurosign = 	u'\u20AC'
    liste_prix = []
    liste_surface = []
    r = get(url, headers = headers, timeout = 5)   
    page = BeautifulSoup(r.text,'html.parser')

    for item in page.find_all('div', {'class' : 'offer-block'}):
        try : 
            prix = int(item.find('p', {'class' : 'offer-price'}).find('span').text.replace(eurosign, '').replace(' ', ''))
            surface = int(item.find('span', {'class' : 'offer-area-number'}).text)
            if(prix != '' and surface != ''):
                liste_prix.append(prix)
                liste_surface.append(surface)
        except :
            pass
    
    for i in range(len(liste_prix)):
        if liste_prix[i] != '' and liste_surface[i] != '':
            res.append({
                'prix' : liste_prix[i],
                'surface' : liste_surface[i]
            })

def main():
    print('Villes disponibles : rouen, cannes, montpellier, amiens, angers, orleans, lille, rennes, grenoble, caen, nantes, saint-etienne, clermont-ferrand'')
    ville = input('Merci de donner une ville dans la liste\n')
    locaouvente = input('Voir les prix de vente ou de location? (écrire location ou vente)\n')
    url = make_url(ville, locaouvente)
    nbpages = get_nb_pages(url)
    url += '/page='
    res = []
    for p in range(1,nbpages+1):
        print('Page {}/{}...'.format(p,nbpages))
        one_page(url+str(p), res)


    somprix = 0
    somsurface = 0
    for i in range(len(res)):
        somprix = somprix + res[i]['prix']
        somsurface = somsurface + res[i]['surface']
    try :
        moyenne = somprix / somsurface
    except:
        print('Il n\'y a aucun résultat pour cette recherche')
        sys.exit()

    choix = input('(1) Afficher le résultat ou (2) L\'enregistrer dans un fichier? (Entrez 1 ou 2)\n')


    if choix == 1:    
        for i in range(len(res)):
            print(res[i]['prix'], res[i]['surface'])
        print('{} annonces au total'.format(i+1))
        print('Prix moyen au m²: {}€'.format(int(moyenne)))

    else:
        namefile = ville+'_'+locaouvente+'_'+str(datetime.datetime.today().strftime('%Y-%m-%d'))
        with open(namefile, 'w') as f:
            f.write('{} annonces au total\n'.format(i+1))
            f.write('Prix moyen au m²: {}€\n'.format(int(moyenne)))
            f.write('Prix Surface\n')
            for i in range(len(res)):
                f.write(str(res[i]['prix'])+' '+str(res[i]['surface'])+'\n')

if __name__ == '__main__':
    main()