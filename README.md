# Home Assistant Domain Entity Counter

[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg?style=for-the-badge)](https://github.com/custom-components/hacs)
<br><a href="https://www.buymeacoffee.com/Petro31" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-black.png" width="150px" height="35px" alt="Buy Me A Coffee" style="height: 35px !important;width: 150px !important;" ></a>

_Domain Entity Counter app for AppDaemon._

Adds sensors that count the number of entities inside a domain.

## Installation

Download the `count_entities` directory from inside the `apps` directory here to your local `apps` directory, then add the configuration to enable the `hacs` module.

## Example App configuration

#### Basic
```yaml
# Creates a sensor for all domains.
count_entities:
  module: count_entities
  class: CountEntities
```

#### Advanced
```yaml
# Creates a sensor for all domains except the excluded list
count_entities:
  module: count_entities
  class: CountEntities
  exclude:
  - sun
  - input_select
  - input_text
  - input_number
  - image_processing
  - persistent_notification
  - weather
  - remote
  log_level: INFO
```

#### App Configuration
key | optional | type | default | description
-- | -- | -- | -- | --
`module` | False | string | count_entities | The module name of the app.
`class` | False | string | CountEntities | The name of the Class.
`exclude` | True | list | | A list of domain names to exclude.  You cannot combine this with include.
`include` | True | list | | A list of domain names to include.  You cannot combine this with exclude.
`log_level` | True | `'INFO'` &#124; `'DEBUG'` | `'INFO'` | Switches log level.