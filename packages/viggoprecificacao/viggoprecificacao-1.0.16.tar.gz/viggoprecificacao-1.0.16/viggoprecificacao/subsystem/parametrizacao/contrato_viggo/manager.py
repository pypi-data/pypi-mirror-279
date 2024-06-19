from viggocore.common.subsystem import operation
from viggocore.common import manager, utils
from viggoprecificacao.subsystem.parametrizacao.contrato_viggo.resource \
    import ContratoViggo
from viggoprecificacao.subsystem.parametrizacao.contrato_viggo.sql import \
    get_vl_total_contratos

from viggocore.common.subsystem.pagination import Pagination


class Create(operation.Create):

    def get_codigo(self):
        domains = self.manager.api.domains().list(name='default')
        if len(domains) == 0:
            return None

        domain_id = domains[0].id
        return self.manager.api.domain_sequences().\
            get_nextval(id=domain_id, name=ContratoViggo.CODIGO_SEQUENCE)

    def pre(self, session, **kwargs):
        nome = kwargs.get('nome', None)
        domain_id = kwargs.pop('domain_id', None)
        if nome is None:
            raise ValueError('Nome do contrato não informado.')
        if domain_id is None:
            raise ValueError('Domain do contrato não informado.')

        kwargs['id'] = domain_id
        kwargs['codigo'] = self.get_codigo()
        return super().pre(session=session, **kwargs)


class Update(operation.Update):
    def pre(self, session, id, **kwargs):
        kwargs.pop('domain_id', None)
        return super().pre(session, id, **kwargs)


class List(operation.List):
    def _get_vl_total_contratos(self, session):
        rs = session.execute(get_vl_total_contratos.query.format(where=''))
        result = [r for r in rs]

        if len(result) > 0:
            return utils.to_decimal(result[0])
        else:
            return utils.to_decimal('0')

    def do(self, session, **kwargs):
        query = session.query(ContratoViggo)

        query = self.manager.apply_filters(query, ContratoViggo, **kwargs)
        query = query.distinct()

        total_rows = None
        if self.manager.with_pagination(**kwargs):
            total_rows = query.count()

        pagination = Pagination.get_pagination(ContratoViggo, **kwargs)
        if pagination.order_by is not None:
            pagination.adjust_order_by(ContratoViggo)
        query = self.driver.apply_pagination(query, pagination)
        result = query.all()

        vl_total = self._get_vl_total_contratos(session)

        return (result, total_rows, vl_total)


class AddTermoAceite(operation.Update):

    def pre(self, session, id, **kwargs):
        self.termo_aceite_id = kwargs.get('termo_aceite_id', None)
        return super().pre(session=session, id=id, **kwargs)

    def do(self, session, **kwargs):
        self.entity.add_termo_aceite(self.termo_aceite_id)
        return super().do(session=session)


class RemTermoAceite(operation.Update):
    def pre(self, session, id, **kwargs):
        self.termo_aceite_id = kwargs.get('termo_aceite_id', None)
        return super().pre(session=session, id=id, **kwargs)

    def do(self, session, **kwargs):
        self.entity.rem_termo_aceite(self.termo_aceite_id)
        return super().do(session=session)


class Manager(manager.CommonManager):

    def __init__(self, driver):
        super(Manager, self).__init__(driver)
        self.create = Create(self)
        self.update = Update(self)
        self.list = List(self)
        self.add_termo_aceite = AddTermoAceite(self)
        self.rem_termo_aceite = RemTermoAceite(self)
