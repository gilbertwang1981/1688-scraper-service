import ruamel.yaml


yaml = ruamel.yaml.YAML(typ='rt')

with open('aliCookieMonitor.yaml', 'r') as file:
    config = yaml.load(file)

