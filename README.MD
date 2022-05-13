![screenshot](https://user-images.githubusercontent.com/16024979/162843362-4050c114-dc82-49eb-ac43-dd6cef79382a.png)

<div align="center">
<a href="https://github.com/agmmnn/nisanyan-cli">
<img alt="GitHub release (latest by date)" src="https://img.shields.io/github/v/release/agmmnn/nisanyan-cli"></a>
<a href="https://pypi.org/project/nisanyan-cli/">
<img alt="PyPI" src="https://img.shields.io/pypi/v/nisanyan-cli"></a>

CLI tool for Turkish etymological dictionary, [nisanyansozluk.com](https://www.nisanyansozluk.com/).

_Not: 0.3 sürümü itibariyle 'yavaş selenium' yerine artık direkt nisanyan sözlüğün api endpoint'i[\*](https://github.com/agmmnn/Radyal-api#nisanyan-decrypt) kullanılmaktadır._

</div>

## Install

```
pip install nisanyan-cli
```

## Usege

```
$ nis yakamoz
```

![](https://user-images.githubusercontent.com/16024979/162844886-7831aebc-8efe-4018-9df5-b26babcc1ca3.png)

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

![](https://user-images.githubusercontent.com/16024979/164780578-0d51d1b1-31b6-48a4-a09e-b42aa6b6c515.png)

### Random Word (`--random`, `-r`):

```
$ nis -r -t
menekşe (Günümüz Türkçesi)
└── banafşe ‹بنفشه› (Farsça): aynı anlam.
    └── vanavşag (Orta Farsça 1300—1500): aynı anlam.
        └── *vana-vaxşa- (Avestaca MÖ.2000): orman otu.
            └── vaxşaiti, vaxş- (Avestaca MÖ.2000): yetişmek, bitmek (bitki).
```

## Arguments

```
  <word>
  -h, --help     show this help message and exit
  -t, --tree     show result as etymology tree
  -r, --random   selects a random word and brings the result
  -v, --version  show program's version number and exit
```

## Dependencies

- [rich](https://pypi.org/project/rich/)
