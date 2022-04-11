![screenshot](https://user-images.githubusercontent.com/16024979/162843362-4050c114-dc82-49eb-ac43-dd6cef79382a.png)

<div align="center">
<a href="https://github.com/agmmnn/nisanyan-cli">
<img alt="GitHub release (latest by date)" src="https://img.shields.io/github/v/release/agmmnn/nisanyan-cli"></a>
<a href="https://pypi.org/project/nisanyan-cli/">
<img alt="PyPI" src="https://img.shields.io/pypi/v/nisanyan-cli"></a>

CLI tool for Turkish etymological dictionary, [nisanyansozluk.com](https://www.nisanyansozluk.com/).

_Not: Site yeni güncellemeyle birlikte dinamik hale geldiği için kodda da [selenium](https://github.com/SeleniumHQ/selenium) kullanmak elzem oldu, [ChromeDriver](https://chromedriver.chromium.org/)'ı indirip sistem path dizinlerinden birine ya da kodu çalıştırdığınız dizine kopyalamanız yeterli._

</div>

## Install

`pip install nisanyan-cli`

## Usege

- `nis <word>`

### Example Usage:

- `nis yakamoz`

![](https://user-images.githubusercontent.com/16024979/162844886-7831aebc-8efe-4018-9df5-b26babcc1ca3.png)

## Arguments

```
  <word>
  -h, --help     show this help message and exit
  -v, --version  show program's version number and exit
```

## Dependencies

- [selenium](https://pypi.org/project/selenium/)
- [rich](https://pypi.org/project/rich/)

_Note: Be aware when this code was published. If the site will be updated in the future this code may not work properly._
