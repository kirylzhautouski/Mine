from flask import abort


def get_int_arg(request, arg_name, default):
    try:
        arg = int(request.args.get(arg_name))
    except TypeError:
        arg = default  # if request.args.get returns None
    except ValueError:
        return abort(400, f'GET param {arg_name} should be an integer.')

    return arg
