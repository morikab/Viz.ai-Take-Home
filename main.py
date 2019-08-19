from vizapp import create_app

if __name__ == '__main__':
    app = create_app(config_filename="config.cfg")
    app.run(host=app.config['HOST'], port=app.config['PORT'])
