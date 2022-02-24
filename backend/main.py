from app import create_app
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

if __name__ == "__main__":

    application = create_app()
    
    # application.debug = True
    
    application.run(host=config['server']['host'], port=config['server']['port'], debug = True)
