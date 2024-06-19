import flask
from viggocore.common import exception, utils
from viggocore.common.subsystem import controller


class Controller(controller.Controller):

    MIMETYPE_JSON = 'application/json'

    def __init__(self, manager, resource_wrap, collection_wrap):
        super().__init__(manager, resource_wrap, collection_wrap)

    def list(self):
        filters = self._filters_parse()

        try:
            filters = self._parse_list_options(filters)
            entities, total_rows, vl_total = self.manager.list(**filters)

            page = filters.get('page', None)
            page_size = filters.get('page_size', None)
        except exception.ViggoCoreException as exc:
            return flask.Response(response=exc.message,
                                  status=exc.status)
        except ValueError:
            raise exception.BadRequest('page or page_size is invalid')

        collection = self._entities_to_dict(
            entities, self._get_include_dicts_vex(filters))

        response = {
            self.collection_wrap: collection,
            'valor_total_contratos': vl_total
        }

        if total_rows is not None:
            response.update({'pagination': {'page': int(page),
                                            'page_size': int(page_size),
                                            'total': total_rows}})

        return flask.Response(response=utils.to_json(response),
                              status=200,
                              mimetype="application/json")

    def add_termo_aceite(self, id):
        data = flask.request.get_json()
        try:
            result = self.manager.add_termo_aceite(id=id, **data)

            response = {'contrato_viggo': result.to_dict()}
        except exception.ViggoCoreException as exc:
            return flask.Response(response=exc.message,
                                  status=exc.status)
        return flask.Response(response=utils.to_json(response),
                              status=201,
                              mimetype=self.MIMETYPE_JSON)

    def rem_termo_aceite(self, id):
        data = flask.request.get_json()
        try:
            result = self.manager.rem_termo_aceite(id=id, **data)

            response = {'contrato_viggo': result.to_dict()}
        except exception.ViggoCoreException as exc:
            return flask.Response(response=exc.message,
                                  status=exc.status)
        return flask.Response(response=utils.to_json(response),
                              status=201,
                              mimetype=self.MIMETYPE_JSON)
