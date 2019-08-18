from app import create_app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=8001)  # TODO - move port to server configuration


# TODO - improvements:
#   * responses in case of failures  - How to test server side???
#   * requirements.txt file
#   * Logger
#   * tests (picture with no faces, very long list (repeating image), very loaded picture..)

