import configparser

config = configparser.ConfigParser()
config['general'] = {'margen': 3, 'iniciar_activado': 0, 'pid': 12345}
with open('config.ini', 'w') as f:
    config.write(f)
    
config2 = configparser.ConfigParser()
config2.read('config.ini')

print(config2['general']['margen'])