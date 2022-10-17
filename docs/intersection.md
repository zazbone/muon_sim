# Calcule des points d'intersections

On a une droite définie par un point $(x_0, y_0, z_0)$ et un vecteur directeur $(dx, dy, dz)$.

On paramétrise la droite par $\lambda$

On choisit d'exprimer la trajectoire en coordonnées cartésiennes.

- $x = x_0 + \lambda dx$
- $y = y_0 + \lambda dy$
- $z = z_0 + \lambda dz$

## Intersection sur l'un des disques

$$z(\lambda_I) = h = z_0 + \lambda cos(\theta)$$

$$\Rightarrow \lambda_I = \frac{h - z_0}{cos(\theta)}$$

Vérifier la condition de validité de la racine :
$$\sqrt{x^2(\lambda_I) + y^2(\lambda_I)} \leq R$$


*Remarque* : Peut diverger sur $\theta = \frac{\pi}{2} (Improbable pour les muons) 
## Intersection sur le cylindre

$$x^2(\lambda_{\pm}) + y^2(\lambda_{\pm}) = R^2$$

$$\Rightarrow (x_0 + \lambda_{\pm} dx)^2 + (y_0 + \lambda_{\pm} dy)^2$$

$$\Rightarrow \lambda_{\pm}^2(dx^2 + dy^2) + 2\lambda_{\pm}(x_0dx + y_0dy) + x_0^2 + y_0^2 - R^2 = 0$$

Polynôme du second degré 0 à deux racines réelles.

Vérifier la condition de validité des racines :
$$z(\lambda_{\pm}) \in [h_1, h_2]$$

*Remarque* : Peut également diverger pour les muons strictement verticaux pour lesquels $x^2_0 + y^2_0 = R^2$ (On supposera également ces cas comme improbables).
