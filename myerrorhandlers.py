from app import app

@app.errorhandler(400)
def invalid_request(error):
    return make_response(jsonify({'error': 'Bad Request', 'source': 'Errorhandler 400', 'request':request.url}), 400)
    
@app.errorhandler(404)
def resource_not_found(error):
    return make_response(jsonify({'error': 'Ressource ist nicht vorhanden', 'source': 'Errorhandler 404', 'request':request.url}),404)
    
@app.errorhandler(405)
def method_not_implemented(error):
    return make_response(jsonify({'error': f'Methode:{request.method} ist nicht implementiert', 'source': 'Errorhandler 405', 'request':request.url}), 405)
    
@app.errorhandler(409)
def invalid_request(error):
    return make_response(jsonify({'error': 'Conflict', 'source': 'Errorhandler 409', 'request':request.url}), 409)
    