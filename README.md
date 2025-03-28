# OutSystems Ninja

## Overview

Pentesting an OutSystems-based web application follows many of the same methodologies as traditional web pentesting. Common vulnerabilities, can still be found, so manual testing is still essential.

However, I noticed that many patterns are present in these systems, making some basic automation possible. This tool assists pentesters in performing OutSystems-specific tasks.

## Features

The script provides the following functionalities:

- [Recursively scan for module references](docs/modulereferences.md)
- Check modules for [**application definitions**](docs/appdefinitions.md) and [**language resources**](docs/languageresources.md)
- Identify modules with `Default.aspx` [**default entry point**](docs/defaultentries.md)
- Check for [**module service**](docs/moduleservices.md) endpoints
- Inspect module assets for [**screen service**](docs/screenservices.md) endpoints
- Generate an [**OpenAPI specification**](docs/openapi.md) from screen service endpoints
- There are many TODO-s, check Issues, give ideas, and if possible, help making them reality.
 