
from assembly_payments.services.base import BaseService
from assembly_payments.types import DirectDebitAuthority, DirectDebitAuthorityRequest, DirectDebitAuthorityFilters


class DirectDebitAuthorityService(BaseService):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.endpoint = "/direct_debit_authorities"

    def get(self, debit_authority_id):
        response = self._execute(
            DirectDebitAuthorityService.GET, f"{self.endpoint}/{debit_authority_id}"
        )
        return DirectDebitAuthority(**response["direct_debit_authorities"])

    def list(self, account_id, **kwargs):
        filters = DirectDebitAuthorityFilters(account_id=account_id, **kwargs).model_dump(exclude_none=True)

        endpoint = self.endpoint
        if filters:
            endpoint = self.append_query_params(endpoint, filters)

        response = self._execute(DirectDebitAuthorityService.GET, endpoint)
        return list(map(lambda x: DirectDebitAuthority(**x), response.get("direct_debit_authorities", [])))

    def create(self, **kwargs):
        data = DirectDebitAuthorityRequest(**kwargs)
        response = self._execute(
            DirectDebitAuthorityService.POST, self.endpoint, data=data.model_dump()
        )
        return DirectDebitAuthority(**response["direct_debit_authorities"])
