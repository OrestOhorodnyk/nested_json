from dynamic_nested_dict import DynamicNestedDict
from connexion.exceptions import OAuthScopeProblem, Unauthorized
from connexion.decorators.security import validate_scope
from flask import current_app
from flask import abort


def health():
    return {'status': 'OK'}


def basic_auth(username, password, required_scopes=None):
    if username == 'admin' and password == 'admin':
        info = {'sub': 'admin', 'scope': 'secret'}
    else:
        raise Unauthorized(f'Incorrect username: {username} or password: {password}')

    if required_scopes is not None and not validate_scope(required_scopes, info['scope']):
        raise OAuthScopeProblem(
            description='Provided user doesn\'t have the required access rights',
            required_scopes=required_scopes,
            token_scopes=info['scope']
        )

    return info


def nest(**args):
    current_app.logger.debug(f"Start processing params: {args}")
    result = dict()
    input_dict = args['body']
    keys = args['keys']
    dd = DynamicNestedDict()
    try:
        for i in input_dict:
            nested_keys = [i.pop(w) for w in keys]
            dd.set_from_list(nested_keys, [i])
            result.update(dd.to_regular_dict())
    except KeyError as e:
        current_app.logger.error(f'Key {e.args[0]} not present in the input JSON')
        abort(422, f'Key {e.args[0]} not present in the input JSON')
    current_app.logger.debug(f"Successfully finished processing {result}")
    return result
