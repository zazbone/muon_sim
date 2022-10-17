# Identifier les v.a. correspondantes aux états initiaux de nos muons

- `(x, y, z)` : paramètres d'approche, garantissent que le muon passera par ces coordonnées durant son parcours.

- `(dx, dy, dz)` : paramètres d'impact, vecteur directeur de la trajectoire du muon.

-  $E_0$ : Énergie initiale du muon (énergie à l'approche de détecteur pas à la création)

# Génération des v.a.

- `(x, y)` : uniforme dans le disque correspondant au sommet de la cuve. $(x - cx)^2 + (y - cy)^2 \leq R_{cuve}$

- `z` : uniforme selon la hauteur de la cuve $z \in [h_1, h_2]$

- `(dx, dy, dz)` : dépendant de $\phi$ et $\theta$ les angles d'incidence des muons. Générer via mcmc à partir de fit de données expérimentales des spectres énergétiques et angulaire des muons.

	- $dx = cos(\theta)$
	- $dy = sin(\theta)cos(\phi)$
	- $dz = sin(\theta)sin(\phi)$

- $E_0$ : Fit de spectres expérimentaux ou uniforme dans la range [50 MeV, 700 MeV]

# Calculer la distance de parcours dans la cuve

Longueur géométrique uniquement. Calcule analytique des intersections de la trajectoire du muon avec la surface de la cuve, à partir des paramètres de la trajectoire `(x, y, z)` | `(dx, dy, dz)`

__Méthode__ :

Paramétrisation de la trajectoire avec $\lambda$.

Trouver les potentielles racines des $lambda$ pour lesquels la trajectoire intersecte soit la surface du cylindre soit un des deux disques.

Une fois les potentiels $\lambda_1$ $\lambda_2$ trouvé, calculer $\Delta l = (x(\lambda_2) - x(\lambda_1))^2 + (y(\lambda_2) - y(\lambda_1))^2 + (z(\lambda_2) - z(\lambda_1))^2$

$\Delta l \doteq$ La longueur géométrique de parcours dans la cuve

La distance de parcours physique du muon peut être inférieur si elle $\Delta l$ est suffisant pour qu'il perde toute son énergie.

# Intégrer $dE$ et $dN_{\gamma}$

Intégrer numériquement la perte d'énergie du muon fonction de la distance et le nombre de photons de scintillations produits sur le trajet.
Jusqu'a E=0 ou l > $\Delta l$

# Faire des stats :smirk:
