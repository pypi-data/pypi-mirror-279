# Preservation Status Database Builder
Returns the preservation status of a Crossref DOI matched against mainstream digital preservation platforms.

![license](https://img.shields.io/gitlab/license/crossref/labs/preservation-database) ![activity](https://img.shields.io/gitlab/last-commit/crossref/labs/preservation-database) <a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>

![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white) ![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white) ![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white) ![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black) ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

This application allows you to build a database of digital preservation sources and then to match a DOI against common digital preservation systems.

## Installation
The easiest install is via pip:
    
    pip install preservation-database

Then add "preservationdatabase" (no hyphen) to your list of INSTALLED_APPS.

## Usage

    export DJANGO_SETTINGS_MODULE=import_settings.settings

    Usage: python -m preservationdatabase.cli [OPTIONS] COMMAND [ARGS]...
    
    Options:
      --help  Show this message and exit.
    
    Commands:
        clear-cache                    Clear the import cache
        import-all                     Download and import all data (excluding...
        import-cariniana               Download and import data from Cariniana
        import-clockss                 Download and import data from CLOCKSS
        import-hathi                   Import data from Hathi (requires local...
        import-internet-archive        Import data from Internet Archive...
        import-internet-archive-items  Import item data from Internet Archive
        import-issnl                   Import ISSN-L mappings
        import-lockss                  Download and import data from LOCKSS
        import-ocul                    Import data from Ocul (requires local...
        import-pkp                     Download and import data from PKP's...
        import-portico                 Download and import data from Portico
        random-samples                 Return random samples that occur in and...
        show-archives                  Clear the import cache
        show-cache                     Show last fill date/times and cache status
        show-issn                      Show preservation items that match an ISSN
        show-preservation              Determine whether a DOI is preserved
        stamp-cache-today              Mark the latest imports as today

## Features
* Cariniana import.
* CLOCKSS import.
* HathiTrust import.
* Internet Archive import.
* Internet Archive item-level import.
* LOCKSS import.
* PKP PLN import.
* Portico import.
* Crossref DOI lookup.

## First-Run Setup
First, copy example_settings.py to settings.py and check settings.py to ensure that the database you want to use is set correctly. The default is db.sqlite. You should carefully read and check all of settings.py.

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

Next, run the database build commands:

    python3 manage.py makemigrations
    python3 manage.py makemigrations preservation-database
    python3 manage.py migrate 

You should then have a working database into which you can import new preservation data.

## Archive Notes

### Internet Archive
The Internet Archive gives a KBART file for the Keepers Registry that we use as a primary ingest source: https://archive.org/details/ia-keepers-registry-kbart. However, this source is not the total coverage of the Internet Archive. However, sadly, the Internet Archive snapshots do not contain external identifiers and the container-level snapshots do not present coverage extent. While it is possible to download the entire 217GB FATCAT database snapshot, this will not be viable for many users. We have therefore stuck with the KBART file that Keepers uses. Extent of coverage in the Internet Archive may, therefore, be under-reported.

# Credits
* [Django](https://www.djangoproject.com/) for the ORM.
* [Git](https://git-scm.com/) from Linus Torvalds _et al_.
* [.gitignore](https://github.com/github/gitignore) from Github.
* [Rich](https://github.com/Textualize/rich) from Textualize.

&copy; Crossref 2023