# coding: utf-8

import os
import requests
import tempfile
import urllib
import json

from contextlib import contextmanager


coldstar_url = os.getenv('TEST_COLDSTAR_URL', 'http://127.0.0.1:6098')
devourer_url = os.getenv('TEST_DEVOURER_URL', 'http://127.0.0.1:6900')
auth_token_name = 'CastielAuthToken'

login = os.getenv('TEST_LOGIN', u'ВнешСис')
password = os.getenv('TEST_PASSWORD', '')


def get_token(login, password):
    url = u'%s/cas/api/acquire' % coldstar_url
    result = requests.post(
        url,
        {
            'login': login,
            'password': password
        }
    )
    j = result.json()
    if not j['success']:
        print j
        raise Exception(j['exception'])
    return j['token']


def release_token(token):
    url = u'%s/cas/api/release' % coldstar_url
    result = requests.post(
        url,
        {
            'token': token,
        }
    )
    j = result.json()
    if not j['success']:
        print j
        raise Exception(j['exception'])


@contextmanager
def make_login():
    token = get_token(login, password)
    print ' > auth token: ', token

    try:
        yield token
    finally:
        release_token(token)


def make_api_request(method, url, session, json_data=None, url_args=None):
    token = session
    result = getattr(requests, method)(
        devourer_url + url,
        json=json_data,
        params=url_args,
        cookies={auth_token_name: token}
    )
    if result.status_code != 200:
        try:
            j = result.json()
            message = u'{0}: {1}'.format(j['meta']['code'], j['meta']['name'])
        except Exception, e:
            # raise e
            message = u'Unknown ({0})'.format(unicode(result))
        raise Exception(unicode(u'Api Error: {0}'.format(message)).encode('utf-8'))
    return result


def test_auth(login, password):
    print 'Coldstar: ', coldstar_url, ', Devourer: ', devourer_url
    with make_login() as token:
        print ' > auth token: ', token


def test_api_download(token, id_):
    res = make_api_request('get', '/api/0/download/{fileid}'.format(fileid=id_), token)
    fname = urllib.unquote(res.headers['content-disposition'].partition("filename*=UTF-8''")[2])
    fpath = os.path.join(tempfile.gettempdir(), '{0}_{1}'.format(id_, fname))
    print 'new file:', fpath
    with open(fpath, 'wb') as tf:
        tf.write(res.content)


def test_api_fileupload(token):
    test_file = tempfile.NamedTemporaryFile(suffix='test_upload_file.txt')
    with test_file:
        test_file.write('This is a test file to upload')
        test_file.seek(0)

        info = {
            'files_info': [
                {'name': 'test1.txt', 'note': u'заметка'}
            ]
        }
        files = {
            'files': ('test_upload_file.txt', test_file),
            'info': ('', json.dumps(info))
        }
        res = requests.post(
            devourer_url + '/api/0/upload',
            files=files,
            cookies={auth_token_name: token}
        )
        print res
    return res.json()


def test_api_fileupload_multiple(token):
    test_file1 = tempfile.NamedTemporaryFile(suffix='test_upload_file1.txt')
    test_file2 = tempfile.NamedTemporaryFile(suffix='test_upload_file2.txt')
    try:
        test_file1.write('This is a test file to upload')
        test_file1.seek(0)
        test_file2.write('This is second test file to upload')
        test_file2.seek(0)

        info = {
            'files_info': [
                {'name': 'testm1.txt', 'note': u'заметка'},
                {'name': 'testm2.txt'}
            ],
            # 'attach_data': {'attach_type': 1, 'errand_id': 1, 'set_person_id': 1}
        }
        files = [
            ('files', ('test_upload_file.txt', test_file1)),
            ('files', ('test_upload_file2.txt', test_file2)),
            ('info', ('', json.dumps(info)))
        ]
        res = requests.post(
            devourer_url + '/api/0/upload',
            files=files,
            cookies={auth_token_name: token}
        )
        print res
    finally:
        test_file1.close()
        test_file2.close()
    return res.json()


if __name__ == '__main__':
    # test_auth(login, password)

    with make_login() as token:
        # test_api_download(token, 'af861f33fa0f4e729d33a8dd3ea958ba')

        # res = test_api_fileupload(token)
        # print unicode(res).decode('unicode-escape')

        res = test_api_fileupload_multiple(token)
        print unicode(res).decode('unicode-escape')