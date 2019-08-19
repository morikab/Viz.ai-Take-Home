from vizapp import create_app

if __name__ == '__main__':
    app = create_app("config.cfg")
    app.run(host=app.config['HOST'], port=app.config['PORT'])

# TODO - improvements:
#   * responses in case of failures  - How to test server side??? - Add error handlers -> handle all cases!
#   * Logger
#   * Configuration!!!!!!

#   * requirements.txt file
#   * README file
#   * tests (picture with no faces, very loaded picture?, )
#   * mock face_client for unit testing of most_common_face methods

