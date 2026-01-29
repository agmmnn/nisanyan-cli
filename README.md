# Nişanyan CLI

<div align="center">

![screenshot](https://github.com/agmmnn/nisanyan-cli/assets/16024979/c19b628b-c0c3-4ca9-aef2-4172bbc53a7d)

[![GitHub release](https://img.shields.io/github/v/release/agmmnn/nisanyan-cli?style=flat-square)](https://github.com/agmmnn/nisanyan-cli)
[![PyPI](https://img.shields.io/pypi/v/nisanyan-cli?style=flat-square)](https://pypi.org/project/nisanyan-cli/)
[![Downloads](https://static.pepy.tech/personalized-badge/nisanyan-cli?period=total&units=international_system&left_color=black&right_color=orange&left_text=Downloads&style=flat-square)](https://pepy.tech/project/nisanyan-cli)

**CLI tool for the Turkish etymological dictionary, [nisanyansozluk.com](https://www.nisanyansozluk.com/).**

</div>

Explore the origins, history, and development of Turkish words directly from your terminal. This tool provides access to Sevan Nişanyan's comprehensive etymological database, including the "Adlar" (names) dictionary.

- **Etymology Tree**: Visualize the lineage of words with the `--tree` flag.
- **Random Word**: Discover new words and their origins with `--random`.
- **Adlar Support**: Access the Turkish names dictionary ([nisanyanadlar.com](https://www.nisanyanadlar.com/)) using `-ad`.
- **Rich Output**: Beautifully formatted terminal output thanks to [Rich](https://github.com/Textualize/rich).
- **Plain Mode**: Clean, unformatted text output for scripts and piping.

## Installation

```bash
pip install nisanyan-cli
```

or

```bash
uv tool install nisanyan-cli
```

## Usage

### Basic Search

Simply provide the word you want to look up:

```bash
nis anadolu
```

![Usage Screenshot](https://github.com/agmmnn/nisanyan-cli/assets/16024979/1fef51dc-caec-42cf-82ad-4dca8ac4ca71)

### Etymology Tree (`-t`, `--tree`)

View the word's history as a hierarchical tree:

```bash
nis çikolata --tree
```

**Output Example:**

```text
çikolata (Günümüz Türkçesi)
└── cioccolata (İtalyanca): kakao yağı ve şekerle imal edilen yiyecek maddesi.
    └── chocolate (İspanyolca): ~.
        └── xocolatl (Aztekçe): kakaodan yapılan içecek.
            ├── xocolli (Aztekçe): acı.
            └── atl (Aztekçe): su.
```

![Tree Screenshot](https://github.com/agmmnn/nisanyan-cli/assets/16024979/c19b628b-c0c3-4ca9-aef2-4172bbc53a7d)

### Nişanyan Adlar (`-ad`)

Query the names dictionary for meanings and origins:

```bash
nis gökçe -ad
```

![Adlar Screenshot](https://github.com/agmmnn/nisanyan-cli/assets/16024979/75bca210-904a-410b-9de7-f5cb0aaf2396)

_Combine with random for inspiration:_ `nis -ad -r`

### Discover Random Words (`-r`, `--random`)

Explore the dictionary randomly:

```bash
nis -r -t
```

## Commands & Arguments

| Argument | Long Flag   | Description                               |
| :------- | :---------- | :---------------------------------------- |
| `<word>` |             | The word to search for (positional).      |
| `-h`     | `--help`    | Show help message and exit.               |
| `-t`     | `--tree`    | Show result as an etymology tree.         |
| `-r`     | `--random`  | Select a random word and display results. |
| `-p`     | `--plain`   | Output plain text (no styling).           |
| `-ad`    |             | Fetch results from nisanyanadlar.com.     |
| `-v`     | `--version` | Show program's version number and exit.   |

## Development

### Prerequisites

- [Poetry](https://python-poetry.org/docs/) (Dependency Management)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/agmmnn/nisanyan-cli.git
   cd nisanyan-cli
   ```
2. Install dependencies:
   ```bash
   poetry install
   ```
3. Run the CLI in development mode:
   ```bash
   poetry run nis <word>
   ```

## TODO

- [ ] Better processing of API results for better alignment with the website's format.
- [ ] Expansion of abbreviations in supplementary descriptions to their full forms.

## Dependencies

- [Rich](https://pypi.org/project/rich/) - Terminal formatting.
- [importlib-metadata](https://pypi.org/project/importlib-metadata/) - Version management.
