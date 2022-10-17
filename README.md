# Muon Sim

Simulation Monte Carlos d'événements muon passant dans un cylindre.

Utiliser pour estimer un nombre de photons de scintillation produit et un taux d'arrêt dans un détecteur, pour une expérience de mesure de temps de vie.

## Installation

### Cloner le projet

```bash
git clone https://github.com/zazbone/muon_sim.git 
cd muon_sim
```

### Créer un venv dédié (Optionnel)

**Linux MacOs**
```bash
python3 -m venv .env
```

**Windows**

```bash
py -m venv .env
```

### Installation

Il est recommander d'installer le module en ajoutant le flag -e à la commande pip install

**Linux MacOs**
```bash
.env/bin/pip install -e .
```

(Si pas de venv)
```bash
python3 -m pip install -e .
```

**Windows**

```bash
.env/Scripts/pip install -e .
```

(Si pas de venv)
```bash
py -m pip install -e .
```