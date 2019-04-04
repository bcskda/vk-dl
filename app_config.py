from typing import List
from urllib.parse import urlencode

App_id = '6872420'
Api_version = '5.92'


Auth_redir = {'netloc': 'oauth.vk.com', 'path': '/blank.html'}


_auth_params = {'client_id': App_id}
_auth_params['display'] = 'popup'
_auth_params['response_type'] = 'token'
_auth_params['revoke'] = 1
_auth_params['redirect_uri'] = 'https://oauth.vk.com/blank.html'
_auth_params['v'] = Api_version
_auth_params = urlencode(_auth_params)
_auth_url = 'https://oauth.vk.com/authorize?' + _auth_params


def make_auth_url(scope: List[str]):
    return _auth_url + urlencode({'scope': ','.join(scope)})


photo_size_priority = ['w', 'z', 'y', 'x', 'm', 's', 'r', 'q', 'p', 'o']
extract_sources = ['im']
source_url = {}
_dev_exec_params = {'params[v]': Api_version}
source_url['im'] = 'https://vk.com/dev/execute?' + urlencode(_dev_exec_params)


jsinject_dep = r':/qtwebchannel/qwebchannel.js'
_jsinject_code_path = 'jsinject/{}.js'
jsinject_code = {}
for source in extract_sources:
    try:
        with open(_jsinject_code_path.format(source)) as code_file:
            jsinject_code[source] = code_file.read()
    except OSError:
        print(f'Warning: missing injection file for source {source}')


local_filename_templ = 'dest/{}_{}'
