from flask import Flask, request

app = Flask(__name__)

# TODO - improvements:
#   * What responses to return in case of failures
#   * Scale?
#   * tests (empty picture list, picture with no faces, very long list, very loaded picture..)


@app.route('/most-common-face', methods=['POST'])
def most_common_face_route():
    request_data = request.get_json()
    if request_data is None:
        pass  # TODO - throw indicative exception (like missing images list)
    print(request_data)
    return "test"


if __name__ == '__main__':
    # TODO - initialize Face Client and store in config
    app.run(host='0.0.0.0', port=8001)  # TODO - move port to configuration
