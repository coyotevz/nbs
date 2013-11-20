# -*- coding: utf-8 -*-

import requests
import json

class NobixConnection(object):

    def __init__(self, url, private_token=None):
        self._url = url
        headers = {
            'Content-Type': u'application/json',
            'Accept': u'application/json',
        }
        if private_token:
            headers['Private-Token'] = private_token

        self._s = requests.Session()
        self._s.headers.update(headers)

    def raw_post(self, path, data):
        url = '{0}{1}'.format(self._url, path)
        try:
            resp = self._s.post(url, json.dumps(data), stream=False)
        except:
            raise
            raise Exception("Can't connect to Nobix Application"
                            " Server({})".format(self._url))
        return resp

    def api_post(self, path, data):
        return self.raw_post('/api' + path, data)


products = [
    {'sku': u'20120' ,'description': u'CODO 90° HH Ø20 GEN FUSION' ,'price': '2.21'},
    {'sku': u'20125' ,'description': u'CODO 90° HH Ø25 GEN FUSION' ,'price': '3.82'},
    {'sku': u'20132' ,'description': u'CODO 90° HH Ø32 GEN FUSION' ,'price': '5.32'},
    {'sku': u'20140' ,'description': u'CODO 90° HH Ø40 GEN FUSION' ,'price': '11.78'},
    {'sku': u'20150' ,'description': u'CODO 90° HH Ø50 GEN FUSION' ,'price': '22.14'},
    {'sku': u'20163' ,'description': u'CODO 90° HH Ø63 GEN FUSION' ,'price': '33.24'},
    {'sku': u'20175' ,'description': u'CODO 90° HH Ø75 GEN FUSION' ,'price': '87.51'},
    {'sku': u'20190' ,'description': u'CODO 90° HH Ø90 GEN FUSION' ,'price': '181.19'},
    {'sku': u'20320' ,'description': u'TE HHH Ø20 GEN FUSION'      ,'price': '2.92'},
    {'sku': u'20325' ,'description': u'TE HHH Ø25 GEN FUSION'      ,'price': '5.51'},
    {'sku': u'20332' ,'description': u'TE HHH Ø32 GEN FUSION'      ,'price': '8.04'},
    {'sku': u'20340' ,'description': u'TE HHH Ø40 GEN FUSION'      ,'price': '17.64'},
    {'sku': u'20350' ,'description': u'TE HHH Ø50 GEN FUSION'      ,'price': '31.85'},
    {'sku': u'20363' ,'description': u'TE HHH Ø63 GEN FUSION'      ,'price': '46.24'},
    {'sku': u'20375' ,'description': u'TE HHH Ø75 GEN FUSION'      ,'price': '104.02'},
    {'sku': u'20390' ,'description': u'TE HHH Ø90 GEN FUSION'      ,'price': '222.05'},
    {'sku': u'20520' ,'description': u'CUPLA HH Ø20 GEN FUSION'    ,'price': '1.64'},
    {'sku': u'20525' ,'description': u'CUPLA HH Ø25 GEN FUSION'    ,'price': '2.92'},
    {'sku': u'20532' ,'description': u'CUPLA HH Ø32 GEN FUSION'    ,'price': '4.06'},
    {'sku': u'20540' ,'description': u'CUPLA HH Ø40 GEN FUSION'    ,'price': '9.22'},
    {'sku': u'20550' ,'description': u'CUPLA HH Ø50 GEN FUSION'    ,'price': '15.49'},
    {'sku': u'20563' ,'description': u'CUPLA HH Ø63 GEN FUSION'    ,'price': '27.21'},
    {'sku': u'20575' ,'description': u'CUPLA HH Ø75 GEN FUSION'    ,'price': '60.71'},
    {'sku': u'20590' ,'description': u'CUPLA HH Ø90 GEN FUSION'    ,'price': '102.19'},
]

branches = [
    {'name': u'Casa Central'},
    {'name': u'Sucursal Godoy Cruz'},
    {'name': u'Depósito Guaymallén'},
]

connection = NobixConnection('http://localhost:5000')

for product in products:
    result = connection.api_post('/product', product)
    if result.status_code != 201:
        print "ERROR[{1}]: {0}".format(product, result.status_code)
