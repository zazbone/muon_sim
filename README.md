# Muon Sim

Simulation Monte Carlos d'événements muon passant dans un cylindre.

Utiliser pour estimer un nombre de photons de scintillation produit et un taux d'arrêt dans un détecteur, pour une expérience de mesure de temps de vie.

## Installation

### Cloner le projet

```bash
git clone https://github.com/zazbone/muon_sim.git 
cd muon_sim
```

### Créer un venv dédié

**Linux MacOs**

```bash
python3 -m venv .env
```

**Windows**

```bash
py -m venv .env
```

### Installation

Il est recommandé d'installer en mode développement avec [flit][flit_tutorial]

**Linux MacOs**
```bash
.env/bin/pip install flit
.env/bin/python3 -m flit install -s
```

**Windows**

```bash
.env/Scripts/pip install flit
.env/Scripts/python -m flit install -s
```

[flit_tutorial]: https://flit.pypa.io/en/stable/index.html