#! /bin/bash

#ratio vente/location : plus il est bas, plus la ville est rentable

 liste_villes=$(ls ventes/ | cut -d'_' -f1)

for ville in $liste_villes ; do
    location=$(ls locations/ | grep $ville)
    vente=$(ls ventes/ | grep $ville)
    for i in 1 2 ; do
        read prix_vente
    done < "ventes/$vente"
    prix_vente=$(echo $prix_vente | cut -d' ' -f5)
    prix_vente=${prix_vente%?}

   for i in 1 2 ; do
        read prix_location
    done < "locations/$location"
    prix_location=$(echo $prix_location | cut -d' ' -f5)
    prix_location=${prix_location%?} 
    ratio=$(($prix_vente/$prix_location))
    echo $ville $ratio
done