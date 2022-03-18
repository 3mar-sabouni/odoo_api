# API Connector
# XMLRPC Style for Odoo
# Main Dev: Ignacio Buioli <ibuioli@gmail.com>
# Codize - https://www.codize.ar

# -*- coding: utf-8 -*-
import odoo
from odoo import http
from odoo.http import request
import re

CORS = '*'

class OdooApiXMLRPC(http.Controller):
    # version #
    @http.route('/odoo-api/common/version', type="json", auth='none', cors=CORS)
    def odoo_api_version(self, **kw):
        version = odoo.release.version.split('.')
        # Try int ( error on Odoo 12 )
        try:
            server_version_info = [int(version[0]), int(version[1]), 0, "final", 0]
        except:
            server_version_info = [str(version[0]), str(version[1]), 0, "final", 0]

        return {
            "server_version": version[0] + "." + version[1],
            "server_version_info": server_version_info,
            "server_serie": version[0] + "." + version[1],
            "protocol_version": 1,
        }

    # login #
    @http.route('/odoo-api/common/login', type="json", auth='none', cors=CORS)
    def odoo_api_login(self, db=None, login=None, password=None, **kw):
        try:
            uid = request.session.authenticate(db, login, password)
            return {
                "user_uid": uid,
                "authentification": True
            }
        except Exception as e:
            return {'status': False, 'error': str(e)}

    # fields_get #
    @http.route('/odoo-api/object/fields_get', type="json", auth='none', cors=CORS)
    def odoo_api_fields_get(self, model, db=None, login=None, password=None, keys={}, **kw):
        try:
            uid = request.session.authenticate(db, login, password)
            if uid:
                attributes=None
                allfields=None
                if 'attributes' in keys.keys():
                    attributes=keys['attributes']
                if 'allfields' in keys.keys():
                    allfields=keys['allfields']

                return request.env[model].browse(uid).fields_get(attributes=attributes, allfields=allfields)
        except Exception as e:
            return {'status': False, 'error': str(e)}

    # search_count #
    @http.route('/odoo-api/object/search_count', type="json", auth='none', cors=CORS)
    def odoo_api_search_count(self, model, filters=None, db=None, login=None, password=None, **kw):
        try:
            uid = request.session.authenticate(db, login, password)
            if uid:
                return request.env[model].browse(uid).search_count(filters)
        except Exception as e:
            return {'status': False, 'error': str(e)}

    # search #
    @http.route('/odoo-api/object/search', type="json", auth='none', cors=CORS)
    def odoo_api_search(self, model, filters=None, keys={}, db=None, login=None, password=None, attributes=None, **kw):
        try:
            uid = request.session.authenticate(db, login, password)
            if uid:
                limit=None
                offset=None
                order=None
                count=False

                if 'limit' in keys.keys():
                    limit=keys['limit']
                if 'offset' in keys.keys():
                    offset=keys['offset']
                if 'order' in keys.keys():
                    order=keys['order']
                if 'count' in keys.keys():
                    count=keys['count']

                ans = []
                model = request.env[model].browse(uid).search(filters, limit=limit, offset=offset, order=order, count=count)
                for m in model:
                    ans.append(m.id)
                return ans
        except Exception as e:
            return {'status': False, 'error': str(e)}

    # read #
    @http.route('/odoo-api/object/read', type="json", auth='none', cors=CORS)
    def odoo_api_read(self, model, ids=None, keys={}, db=None, login=None, password=None, attributes=None, **kw):
        try:
            uid = request.session.authenticate(db, login, password)
            if uid:
                fields=None

                if 'fields' in keys.keys():
                    fields=keys['fields']

                model = request.env[model].browse(uid).browse(ids).read(fields=fields)
                return model
        except Exception as e:
            return {'status': False, 'error': str(e)}

    # search_read #
    @http.route('/odoo-api/object/search_read', type="json", auth='none', cors=CORS)
    def odoo_api_search_read(self, model, filters=None, keys={}, db=None, login=None, password=None, attributes=None, **kw):
        try:
            uid = request.session.authenticate(db, login, password)
            if uid:
                limit=None
                offset=0
                order=None
                fields=None

                if 'limit' in keys.keys():
                    limit=keys['limit']
                if 'offset' in keys.keys():
                    offset=keys['offset']
                if 'order' in keys.keys():
                    order=keys['order']
                if 'fields' in keys.keys():
                    fields=keys['fields']

                model = request.env[model].browse(uid).search_read(filters, limit=limit, offset=offset, order=order, fields=fields)
                return model
        except Exception as e:
            return {'status': False, 'error': str(e)}

    # write #
    @http.route('/odoo-api/object/write', type="json", auth='none', cors=CORS)
    def odoo_api_write(self, model, id=None, vals={}, db=None, login=None, password=None, attributes=None, **kw):
        """
              ``(0, 0, values)``
              adds a new record created from the provided ``value`` dict.
          ``(1, id, values)``
              updates an existing record of id ``id`` with the values in
              ``values``. Can not be used in :meth:`~.create`.
          ``(2, id, 0)``
              removes the record of id ``id`` from the set, then deletes it
              (from the database). Can not be used in :meth:`~.create`.
          ``(3, id, 0)``
              removes the record of id ``id`` from the set, but does not
              delete it. Can not be used in
              :meth:`~.create`.
          ``(4, id, 0)``
              adds an existing record of id ``id`` to the set.
          ``(5, 0, 0)``
              removes all records from the set, equivalent to using the
              command ``3`` on every record explicitly. Can not be used in
              :meth:`~.create`.
          ``(6, 0, ids)``
              replaces all existing records in the set by the ``ids`` list,
              equivalent to using the command ``5`` followed by a command
              ``4`` for each ``id`` in ``ids``.
        """
        try:
            uid = request.session.authenticate(db, login, password)
            if uid:
                model = request.env[model].browse(uid).browse(id).write(vals)
                return model
        except Exception as e:
            return {'status': False, 'error': str(e)}

    # create #
    @http.route('/odoo-api/object/create', type="json", auth='none', cors=CORS)
    def odoo_api_create(self, model, vals={}, db=None, login=None, password=None, attributes=None, **kw):
        try:
            uid = request.session.authenticate(db, login, password)
            if uid:
                model = request.env[model].browse(uid).create(vals)
                return model.id
        except Exception as e:
            return {'status': False, 'error': str(e)}

    # unlink #
    @http.route('/odoo-api/object/unlink', type="json", auth='none', cors=CORS)
    def odoo_api_unlink(self, model, id=None, db=None, login=None, password=None, attributes=None, **kw):
        try:
            uid = request.session.authenticate(db, login, password)
            if uid:
                model = request.env[model].browse(uid).browse(id).unlink()
                return model
        except Exception as e:
            return {'status': False, 'error': str(e)}
