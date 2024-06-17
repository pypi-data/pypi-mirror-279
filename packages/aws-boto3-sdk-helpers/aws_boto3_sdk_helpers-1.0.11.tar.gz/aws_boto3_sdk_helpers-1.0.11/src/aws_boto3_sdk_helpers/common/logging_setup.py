import os, logging.config
import yaml

with open(f"{os.getcwd()}/../common/logging_definition.yaml", 'rt') as f:
    config = yaml.safe_load(f.read())

logging.config.dictConfig(config)
logger = logging.getLogger("development") # Use one of the defined logger in the logging.yaml file

## You can now emit log meesage based on the selected Logger:
## logger.info('MESSAGE')
