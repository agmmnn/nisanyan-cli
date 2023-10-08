![screenshot](https://user-images.githubusercontent.com/16024979/162843362-4050c114-dc82-49eb-ac43-dd6cef79382a.png)

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

## Usege

```
$ nis yakamoz
```

![nisanyan-cli](https://user-images.githubusercontent.com/16024979/162844886-7831aebc-8efe-4018-9df5-b26babcc1ca3.png)

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

![Etymology Tree](https://user-images.githubusercontent.com/16024979/164780578-0d51d1b1-31b6-48a4-a09e-b42aa6b6c515.png)

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

<img src="https://user-images.githubusercontent.com/16024979/208524422-115cf48b-b2db-4e3e-880f-d43784ed48c6.png" alt="NisanyanAdlar" width="540"/>

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
    -ad            show result from nisanyanadlar
    -v, --version  show program's version number and exit
```

## TODO

- [ ] Köken metninin sitedeki gibi görünmesi için Api'dan dönen sonucun işlenmesi.
- [ ] Ek açıklama metnindeki kısaltmaların normal hallerine çevrilmesi.

## Dependencies

- [rich](https://pypi.org/project/rich/)
