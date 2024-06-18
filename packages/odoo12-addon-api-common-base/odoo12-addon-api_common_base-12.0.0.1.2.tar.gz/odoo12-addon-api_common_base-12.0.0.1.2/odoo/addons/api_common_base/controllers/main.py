from odoo.addons.base_rest.controllers import main


class CommonAPIController(main.RestController):
    _root_path = '/api/'
    _collection_name = 'api_common_base.services'
    _default_auth = 'api_key'
