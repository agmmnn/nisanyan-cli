![screenshot](https://github.com/agmmnn/nisanyan-cli/assets/16024979/c19b628b-c0c3-4ca9-aef2-4172bbc53a7d)

<div align="center">
<a href="https://github.com/agmmnn/nisanyan-cli">
<img alt="GitHub release (latest by date)" src="https://img.shields.io/github/v/release/agmmnn/nisanyan-cli"></a>
<a href="https://pypi.org/project/nisanyan-cli/">
<img alt="PyPI" src="https://img.shields.io/pypi/v/nisanyan-cli"></a> 
<a href="https://pepy.tech/project/nisanyan-cli">
<img alt="Total Downloads" src="https://static.pepy.tech/personalized-badge/nisanyan-cli?period=total&units=international_system&left_color=black&right_color=orange&left_text=Downloads"></a>

CLI tool for Turkish etymological dictionary, [nisanyansozluk.com](https://www.nisanyansozluk.com/).

</div>

## Install

```
pip install nisanyan-cli
```

## Usage

```
$ nis anadolu
```

![nisanyan-cli](https://github.com/agmmnn/nisanyan-cli/assets/16024979/1fef51dc-caec-42cf-82ad-4dca8ac4ca71)

### Etymology Tree (`--tree`, `-t`):

```
$ nis çikolata --tree
çikolata (Günümüz Türkçesi)
└── cioccolata (İtalyanca): kakao yağı ve şekerle imal edilen yiyecek maddesi.
    └── chocolate (İspanyolca): ~.
        └── xocolatl (Aztekçe): kakaodan yapılan içecek.
            ├── xocolli (Aztekçe): acı.
            └── atl (Aztekçe): su.
```

![Turkish Etymology Tree](https://github.com/agmmnn/nisanyan-cli/assets/16024979/c19b628b-c0c3-4ca9-aef2-4172bbc53a7d)

### Random Word (`--random`, `-r`):

```
$ nis -r -t
menekşe (Günümüz Türkçesi)
└── banafşe ‹بنفشه› (Farsça): aynı anlam.
    └── vanavşag (Orta Farsça 1300—1500): aynı anlam.
        └── *vana-vaxşa- (Avestaca MÖ.2000): orman otu.
            └── vaxşaiti, vaxş- (Avestaca MÖ.2000): yetişmek, bitmek (bitki).
```

### Adlar (`-ad`):

```
$ nis gökçe -ad
```

![NisanyanAdlar](https://github.com/agmmnn/nisanyan-cli/assets/16024979/75bca210-904a-410b-9de7-f5cb0aaf2396)

Also you can use `--random`, `-r` argument with `-ad` argument: `nis -ad -r`

## Arguments

```
positional arguments:
    <word>

options:
    -h, --help     show this help message and exit
    -t, --tree     show result as etymology tree
    -r, --random   selects a random word and brings the result
    -p, --plain    plain text output
    -ad            show result from nisanyanadlar.com
    -v, --version  show program's version number and exit
```




## Dependencies

- [rich](https://pypi.org/project/rich/)
- [poetry](https://python-poetry.org/docs/)

## Initialize Developer Environment

1. Install [Poetry](https://python-poetry.org/docs/)
2. Install dependencies:
   ```bash
   poetry install
   ```
3. Run the CLI:
   ```bash
   poetry run nis <word>
   ```

## TODO

- [ ] Köken metninin sitedeki gibi görünmesi için Api'dan dönen sonucun işlenmesi.
- [ ] Ek açıklama metnindeki kısaltmaların normal hallerine çevrilmesi.