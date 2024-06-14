
from assembly_payments.services.base import BaseService
from assembly_payments.types import User, UserRequest, WalletAccount, BankAccount, SetDisbursementRequest, \
    UserItemFilters, Item


class UserService(BaseService):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.endpoint = "/users"

    def get(self, user_id):
        response = self._execute(UserService.GET, f"{self.endpoint}/{user_id}")
        return User(**response['users'])

    def list(self, *args, **kwargs):
        response = self._execute(UserService.GET, self.endpoint)
        return list(map(lambda x: User(**x), response.get("users", [])))

    def create(self, **kwargs):
        data = UserRequest(**kwargs)
        response = self._execute(UserService.POST, self.endpoint, data=data.model_dump())
        return User(**response['users'])

    def update(self, **kwargs):
        data = UserRequest(**kwargs)
        response = self._execute(UserService.PATCH, f"{self.endpoint}/{data.id}", data=data.model_dump(exclude_none=True))
        return User(**response['users'])

    def get_wallet_account(self, user_id):
        response = self._execute(UserService.GET, f"{self.endpoint}/{user_id}/wallet_accounts")
        return WalletAccount(**response['wallet_accounts'])

    def get_bank_account(self, user_id):
        response = self._execute(UserService.GET, f"{self.endpoint}/{user_id}/bank_accounts")
        return BankAccount(**response['bank_accounts'])

    def set_disbursement_account(self, user_id, **kwargs):
        data = SetDisbursementRequest(**kwargs)
        response = self._execute(UserService.PATCH, f"{self.endpoint}/{user_id}/disbursement_account", data=data.model_dump())
        return User(**response['users'])

    def list_user_items(self, user_id, **kwargs):
        filters = UserItemFilters(**kwargs).model_dump(exclude_none=True)

        endpoint = f"{self.endpoint}/{user_id}/items"
        if filters:
            endpoint = self.append_query_params(endpoint, filters)

        response = self._execute(UserService.GET, endpoint)
        return list(map(lambda x: Item(**x), response.get("items", [])))
