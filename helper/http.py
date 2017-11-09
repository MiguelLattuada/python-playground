# line break and inline space helper variables
l_b = '\n'
l_s = ' '

# predefined status and http default protocol
STATUS_OK = ('200', 'OK')
http_protocol_version = 'HTTP/1.1'


def get_header_start(response_status):
    """
    Generates first line of response header
    Ex. HTTP/1.1 200 OK
    :param tuple response_status: Status code definition represented as a tuple Ex. (200, OK)
    :return:
    """
    return '{protocol}{space}{status[0]}{space}{status[1]}'.format(
        protocol=http_protocol_version,
        space=l_s,
        status=response_status
    )


def get_header_fields(header_fields):
    """
    :param dict header_fields:
    :return:
    """
    header_fields_string = ''
    for field, field_value in header_fields.items():
        header_fields_string += '{}: {}{}'.format(field, field_value, l_b)
    return header_fields_string


def status_ok_response(response_body):
    """
    Get 200 OK response
    :param str response_body:
    :return:
    """
    return '{header_top}{line_break}{header_fields}{line_break}{body}'.format(
        header_top=get_header_start(STATUS_OK),
        line_break=l_b,
        header_fields=get_header_fields({
            'Content-Type': 'text/html; charset=utf-8',
            'Connection': 'keep-alive'
        }),
        body=response_body
    )
