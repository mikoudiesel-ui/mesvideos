---
workflow: general-video
flow: automation
storyboard: no
message: "Bikini Shop (@daya_na990) : des maillots tendance à petits prix, présentés en live et commandés en un message."
destination: tiktok
aspect: 1080x1920
language: fr
audience: "Jeunes femmes d'Abidjan qui cherchent un maillot pour la plage, la piscine ou les vacances"
length: 40s
angle: "Présentation de marque en motion design : ce que fait la boutique, pour qui, et pourquoi commander chez elle"
voice: ff_siwis
---

## Intent

Paroles de l'utilisateur : « crée une nouvelle vidéo en motion design pour présenter cette boutique sur TikTok qui
vend des bikinis en ligne… présenter ce que la boutique fait, dire à qui elle s'adresse, quelle est la proposition
de valeur… Choisir une voix off adaptée pour une vidéo en motion design pour faire les descriptions. »
Ton : solaire, féminin, rythmé, très TikTok. Récupérer l'ADN graphique de la page (couleurs, style, images).

## Assets

- assets/img/t-*.jpg — miniatures des vidéos TikTok de la boutique, découpées dans les 2 captures du profil (tools/crop_screens.py).
- assets/img/avatar.png — photo de profil de la boutique (bikinis sur cintres), découpée dans la capture.

## Customizations

- Voix off française (Kokoro, voix « ff_siwis », locale) sur toute la vidéo.
- ADN graphique tiré des captures : mur orange des shootings, mannequins dorés et noirs laqués, fleurs d'hibiscus,
  rose vif, turquoise, imprimés (crochet, fleurs bleues, léopard), feuilles d'automne en décor.
- Infos réelles de la page : « Bikinis shop », @daya_na990, 2 863 followers, 14,5K J'aime, bio « disponible pour tous
  vos achats de maillot et haut top », 07 99 00 45 50, arrivages annoncés « en live », prix « de 1000 à 3000 »,
  « Top basique 2.500 », « Yop 📍 ».

## Notes

- Les liens Pinterest (pin.it/4uzJEXLLm, pin.it/6QcfIKgtI, pin.it/MEN6bLgyB) et la page TikTok sont bloqués par le
  proxy de l'environnement : ni les inspirations ni les vidéos n'ont pu être ouvertes. Seules les 2 captures servent de source.
- « Yop » est lu comme Yopougon (Abidjan) et les prix comme des francs CFA : déductions à faire valider.
- La livraison à domicile vient du brief de la vidéo précédente (daya-livraison-iso), pas de la page.
