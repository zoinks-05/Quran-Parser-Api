# Quran Parser API

A lightweight **FastAPI-based Quran API** that parses, compiles, and serves Quranic text, Surah information, verses, and translations through a simple REST API.

The project is designed to provide an easy-to-use backend for applications such as iOS, Android, web applications, desktop applications, and other projects that need structured Quranic data.

## Features

* REST API built with **FastAPI**
* Quran text served as structured JSON
* Retrieve the complete Quran
* Retrieve individual Surahs
* Retrieve individual verses
* Retrieve Surah metadata
* Retrieve ranges of Surah names and metadata
* Discover available translations
* Retrieve translations by language and author
* UTF-8 JSON responses
* Automatic compilation of Quran data
* Translation compression/decompression system
* CORS support for web applications
* Designed to be consumed by mobile and frontend applications

---

## Data Source

The Quranic text used by this project was sourced from **[Tanzil.net](https://tanzil.net/)**.

Tanzil is an established Quranic project focused on providing highly verified and precise Quranic text in Unicode. It provides both Uthmani and Imlaei Quran text, along with various formatting and text options.

The repository currently contains processed/compiled versions of this data for use by the API.

### Attribution

> Quran text data sourced from Tanzil.net.

Please refer to **[Tanzil's documentation](https://tanzil.net/docs/)** and the relevant Tanzil terms/conditions before redistributing or modifying the underlying Quranic text.

---

## Repository Structure

```text
Quran-Parser-Api/
│
├── data/
│
├── translations/
│   ├── data/
│   │   └── Compressed/
│   │
│   └── encryptionLogic.py
│
├── compiledQuran.json
├── compiler.py
├── main.py
├── quranParser.py
├── quran-simple.txt
└── README.md
```

### Main files

#### `main.py`

Contains the FastAPI application and REST endpoints.

#### `compiler.py`

Responsible for compiling/processing the Quran data into the structure consumed by the API.

#### `quranParser.py`

Contains Quran parsing functionality used during the compilation process.

#### `compiledQuran.json`

The compiled Quran dataset consumed by the API.

#### `quran-simple.txt`

Plain-text Quran data used by the current data-processing pipeline.

#### `translations/`

Contains translation data and the current translation compression/decompression logic.

---

# Installation

## Requirements

* Python 3.9+
* pip
* FastAPI
* Uvicorn

Install the Python dependencies:

```bash
pip install fastapi uvicorn
```

If the project gains additional dependencies, install them with:

```bash
pip install -r requirements.txt
```

---

# Running the API

Start the FastAPI server with:

```bash
uvicorn main:app --reload
```

The API will normally be available at:

```text
http://127.0.0.1:8000
```

FastAPI's interactive API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

The alternative ReDoc interface is available at:

```text
http://127.0.0.1:8000/redoc
```

For access from another device on your local network, run:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

---

# API

## Root

### `GET /`

Returns a simple API status message.

Example:

```json
{
    "message": "Welcome to the Quran Parser API"
}
```

---

## Get the Complete Quran

### `GET /quran`

Returns the complete compiled Quran dataset.

Example:

```text
GET /quran
```

---

## Get Available Translations

### `GET /quran/translations`

Returns the translations currently available to the API.

Example:

```text
GET /quran/translations
```

Response:

```json
[
    {
        "language": "en",
        "author": "example"
    }
]
```

The exact available languages and authors depend on the translation files currently installed in the repository.

---

## Get a Translation

### `GET /quran/translations/{language}/{author}`

Returns a specific Quran translation.

Example:

```text
GET /quran/translations/en/example
```

The response contains the Surahs and their translated verses.

Example structure:

```json
[
    {
        "1": {
            "name": "...",
            "nameAr": "...",
            "nameEng": "...",
            "verses": [
                {
                    "number": 1,
                    "data": {
                        "language": "en",
                        "author": "example",
                        "translation": "...",
                        "base": false
                    }
                }
            ]
        }
    }
]
```

If the requested translation does not exist:

```json
{
    "error": "Translation not found"
}
```

with HTTP status:

```text
404
```

---

# Get a Surah

### `GET /quran/{surah}`

Returns information and verses for a specific Surah.

For example, to retrieve Al-Fatihah:

```text
GET /quran/1
```

A Surah contains metadata such as:

* Surah name
* Arabic name
* English name
* Number of verses
* Origin
* Juz information
* Verse data

---

# Get a Verse

### `GET /quran/{surah}/{ayah}`

Returns a specific verse.

For example:

```text
GET /quran/2/255
```

This can be used by applications that need to retrieve individual Ayahs rather than downloading an entire Surah or the complete Quran.

---

# Get Surah Names and Metadata

### `GET /quran/surahs/names/{start}/{end}`

Returns Surah metadata for a specified range.

For example:

```text
GET /quran/surahs/names/1/10
```

The response includes information such as:

```json
{
    "1": {
        "name": "...",
        "nameAr": "...",
        "nameEng": "...",
        "numberOfVerses": 7,
        "Origin": "...",
        "juz": "...",
        "size": 7
    }
}
```

This endpoint is useful for building Surah selection screens in applications.

---

# CORS

The API currently enables CORS:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

This allows the API to be accessed from browser-based applications and other clients.

For a production deployment, `allow_origins=["*"]` should be replaced with the specific origins that are intended to access the API.

---

# Current Translation System

Translations are currently stored locally and compressed into ZIP files.

The API:

1. Finds the requested translation.
2. Decompresses the translation.
3. Loads/compiles the Quran data.
4. Extracts the requested translation.
5. Returns it through the API.
6. Compresses the translation data again.

This system works for the current implementation but introduces unnecessary complexity for dynamically managing a growing collection of translations.

---

# Planned Translation System

A future version of the API should replace the current local compression/decompression workflow with a **Tanzil-based translation discovery and download system**.

The planned architecture is:

```text
                    Tanzil.net
                        │
                        ▼
              Discover available
                 translations
                        │
                        ▼
              Download translation
                        │
                        ▼
                 Parse / validate
                        │
                        ▼
              Store locally / cache
                        │
                        ▼
                   FastAPI
                        │
                        ▼
                Client Applications
```

## Planned functionality

The API should eventually be able to:

* Query Tanzil for available translations.
* Discover newly available translations.
* Retrieve translation metadata.
* Download translations directly from Tanzil.
* Parse downloaded translation files.
* Convert them into the API's internal format.
* Cache translations locally.
* Avoid repeatedly downloading the same translation.
* Update translations when the upstream source changes.
* Remove the dependency on the current ZIP-based translation workflow.

### Translation discovery

Instead of maintaining a manually curated list of translation ZIP files, the future system should obtain the available translation information from Tanzil.

For example, the API could eventually expose:

```text
GET /quran/translations
```

and dynamically build its response from the translations available from the upstream source.

---

# Future Data Synchronization

The long-term goal is to make the repository less dependent on manually maintained data.

A possible synchronization workflow would be:

```text
Tanzil
  │
  ├── Quran text
  │
  ├── Plain-text data
  │
  └── Translations
       │
       ▼
   Downloader
       │
       ▼
   Validator
       │
       ▼
     Parser
       │
       ▼
   Local Cache
       │
       ▼
  compiledQuran.json
       │
       ▼
     FastAPI
```

This would allow the project to keep its API stable while allowing the underlying data to be updated from the upstream source.

---

# Additional Data

Additional Quranic translations and plain-text Quran data should be sourced directly from **Tanzil.net** where available.

Rather than adding arbitrary third-party copies of Quranic text or translations to the repository, future data additions should preferably follow the upstream Tanzil source and its applicable usage requirements.

See:

[Tanzil.net](https://tanzil.net/?utm_source=chatgpt.com)

[Tanzil Documentation](https://tanzil.net/docs/?utm_source=chatgpt.com)

---

# Roadmap

### Current

* [x] FastAPI REST API
* [x] Quran JSON API
* [x] Surah endpoint
* [x] Verse endpoint
* [x] Surah metadata endpoint
* [x] Translation listing
* [x] Translation retrieval
* [x] Local translation storage
* [x] Translation compression/decompression

### Planned

* [ ] Tanzil translation discovery
* [ ] Automatic translation downloading
* [ ] Translation metadata synchronization
* [ ] Translation caching
* [ ] Automatic translation updates
* [ ] Remove ZIP-based translation management
* [ ] Automatic Quran text synchronization
* [ ] Better validation of downloaded data
* [ ] Background synchronization jobs
* [ ] Translation version tracking
* [ ] Improved API error handling
* [ ] API versioning
* [ ] Production deployment configuration
* [ ] Automated tests
* [ ] Docker support

---

# Contributing

Contributions are welcome.

When adding or modifying Quranic text or translations, please ensure that the source and applicable licensing/usage requirements are respected.

For new data sources, prefer authoritative upstream sources and document the source clearly.

---

# Disclaimer

This project is a software/API project for accessing and processing Quranic data.

The Quranic text currently used by the project was sourced from Tanzil.net. Please consult Tanzil's documentation and terms for the authoritative information regarding the use and redistribution of its data.

This project is not affiliated with or endorsed by Tanzil unless explicitly stated otherwise.

---

# License

See the repository's license information for the terms governing the source code.

Data contained within the project may be subject to separate attribution, licensing, or usage requirements from their respective sources.

---

## Project

**Quran Parser API**

GitHub:
[https://github.com/zoinks-05/Quran-Parser-Api](https://github.com/zoinks-05/Quran-Parser-Api?utm_source=chatgpt.com)
