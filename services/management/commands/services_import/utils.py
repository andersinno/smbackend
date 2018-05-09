import os
import requests
from django.conf import settings
from django.utils.http import urlencode

from services.management.commands.utils.text import clean_text

URL_BASE = 'http://www.hel.fi/palvelukarttaws/rest/v4/'


def pk_get(resource_name, res_id=None, params=None):
    url = "%s%s/" % (URL_BASE, resource_name)
    if res_id is not None:
        url = "%s%s/" % (url, res_id)
    if params:
        url += '?' + urlencode(params)
    print("CALLING URL >>> ", url)
    resp = requests.get(url)
    assert resp.status_code == 200, 'fuu status code {}'.format(resp.status_code)
    return resp.json()


def save_translated_field(obj, obj_field_name, info, info_field_name, max_length=None):
    has_changed = False
    for lang in ('fi', 'sv', 'en'):
        key = '%s_%s' % (info_field_name, lang)
        if key in info:
            val = clean_text(info[key])
        else:
            val = None
        if max_length and val and len(val) > max_length:
            # if self.verbosity:
            #     self.logger.warning("%s: field '%s' too long" % (obj, obj_field_name))
            val = None
        obj_key = '%s_%s' % (obj_field_name, lang)
        obj_val = getattr(obj, obj_key)
        if obj_val == val:
            continue

        if getattr(obj, obj_key) != val:
            setattr(obj, obj_key, val)
            has_changed = True
        if lang == 'fi':
            setattr(obj, obj_field_name, val)
    return has_changed


def postcodes():
    path = os.path.join(settings.BASE_DIR, 'data', 'fi', 'postcodes.txt')
    postcodes = {}
    f = open(path, 'r', encoding='utf-8')
    for l in f.readlines():
        code, muni = l.split(',')
        postcodes[code] = muni.strip()
    return postcodes
