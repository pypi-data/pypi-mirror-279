from datetime import datetime
from typing import Union, Optional

from pydantic.main import BaseModel


class TokenRequest(BaseModel):
    grant_type: Union[None, str]
    client_id: Union[None, str]
    client_secret: Union[None, str]
    scope: Union[None, str]


class Token(BaseModel):
    access_token: str
    expires_in: int
    token_type: str
    expires_at: float


class UserBase(BaseModel):
    id: str
    first_name: str
    last_name: Optional[str] = None
    email: str
    country: Optional[str] = None


class UserRequest(UserBase):
    pass


class User(UserBase):
    full_name: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    location: Optional[str] = None
    related: Optional[dict] = None


class CompanyBase(BaseModel):
    name: str
    legal_name: str
    tax_number: str


class CompanyRequest(CompanyBase):
    user_id: str
    country: str


class Company(CompanyBase):
    id: str
    charge_tax: Optional[str] = None
    address_line_1: Optional[str] = None
    address_line_2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip: Optional[str] = None
    phone: Optional[str] = None


class CompanyUpdateRequest(CompanyRequest):
    pass


class WalletAccount(BaseModel):
    id: str
    active: bool
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    balance: int
    currency: str


class NppDetails(BaseModel):
    pay_id: str
    reference: str
    amount: str
    currency: str


class BpayDetails(BaseModel):
    biller_code: str
    reference: str
    amount: str
    currency: str


class VirtualAccountBase(BaseModel):
    id: str
    wallet_account_id: str


class VirtualAccount(VirtualAccountBase):
    routing_number: int
    account_number: int
    currency: str
    status: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    user_external_id: str


class BankAccountBase(BaseModel):
    bank_name: str
    country: str
    account_name: str
    routing_number: str
    account_number: str
    holder_type: str
    account_type: str


class BankDetails(BankAccountBase):
    direct_debit_authority_status: Optional[str] = None


class BankAccountRequest(BankAccountBase):
    user_id: str


class BankAccount(BaseModel):
    id: str
    active: bool
    verification_status: str
    currency: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    bank: Optional[BankDetails] = None


class SetDisbursementRequest(BaseModel):
    account_id: str


class Disbursement(BaseModel):
    id: str
    amount: int
    currency: str
    batch_id: Optional[int] = None
    cuscal_payment_transaction_id: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    state: str


class Transaction(BaseModel):
    id: str
    description: str
    type: str
    type_method: str
    state: str
    user_id: str
    user_name: str
    account_id: str
    item_name: Optional[str] = None
    dynamic_descriptor: Optional[str] = None
    amount: int
    currency: str
    debit_credit: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class TransactionSupplementaryData(BaseModel):
    id: str
    debtor_name: str
    debtor_account: str
    creditor_account: str
    creditor_name: str
    remittance_information: str
    type: str
    type_method: str
    npp_details: Optional[dict] = None


class ItemBase(BaseModel):
    id: str
    name: str
    amount: int
    description: Optional[str] = None


class ItemRequest(ItemBase):
    payment_type: int
    buyer_id: str
    seller_id: str


class Item(ItemBase):
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    state: str
    payment_type_id: int
    status: int
    deposit_reference: str
    buyer_name: str
    buyer_country: str
    buyer_email: str
    seller_name: str
    seller_country: str
    seller_email: str
    tds_check_state: Optional[str] = None
    currency: str


class PaginationFilters(BaseModel):
    offset: Optional[int] = None
    limit: Optional[int] = None


class UserItemFilters(PaginationFilters):
    pass


class ItemFilters(PaginationFilters):
    search: Optional[str] = None
    created_before: Optional[datetime] = None
    created_after: Optional[datetime] = None


class MakePaymentRequest(BaseModel):
    account_id: str


class RefundPaymentRequest(BaseModel):
    refund_amount: Optional[int] = None
    refund_message: Optional[str] = None
    account_id: Optional[str] = None


class AuthorizePaymentRequest(BaseModel):
    account_id: str
    cvv: Optional[str] = None


class WebhookBase(BaseModel):
    http_method: str
    url: str
    description: Optional[str] = None


class WebhookRequest(WebhookBase):
    object_type: str


class WebhookUpdateRequest(WebhookBase):
    pass


class Webhook(WebhookBase):
    uuid: str
    enabled: bool
    created_at: str
    updated_at: str
    object_type: str


class Job(BaseModel):
    hashed_payload: str
    updated_at: str
    created_at: str
    webhook_uuid: str
    uuid: str
    payload: dict
    request_responses: list[dict]


class DirectDebitAuthority(BaseModel):
    id: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    amount: int
    bank_bsb: str
    debit_user_id: str
    state: str


class DirectDebitAuthorityFilters(PaginationFilters):
    account_id: str


class DirectDebitAuthorityRequest(BaseModel):
    amount: int
    account_id: str


class WithdrawFundsRequest(BaseModel):
    account_id: str
    amount: int
    custom_descriptor: Optional[str] = None


class BillPaymentRequest(BaseModel):
    account_id: str
    amount: int


class ProcessNppPaymentRequest(BaseModel):
    crn: str
    payid: str
    amount: int
    payee_name: str
    trn: str
    clearing_system_transaction_id: str
    debtor_name: str
    debtor_legal_name: str
    debtor_bsb: str
    debtor_account: str
    remittance_information: str
    pay_id_type: str
    end_to_end_id: str
    npp_payin_internal_id: str
    pay_id: str


class TransactionStatesRequest(BaseModel):
    exported_ids: list[str]
    state: int


class CallbackBase(BaseModel):
    description: str
    url: str
    object_type: str
    enabled: bool


class Callback(CallbackBase):
    id: str
    authorization_token: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    description: Optional[str] = None


class CallbackRequest(CallbackBase):
    pass


class CallbackUpdateRequest(CallbackBase):
    pass


class BatchTransaction(BaseModel):
    created_at: str
    updated_at: str
    id: int
    uuid: str
    external_reference: Optional[str] = None
    user_email: str
    first_name: str
    last_name: str
    user_external_id: str
    type: str
    type_method: str
    batch_id: int
    reference: Optional[str] = None
    deposit_reference: Optional[str] = None
    state: str
    status: int
    user_id: str
    account_id: str
    from_user_name: str
    from_user_id: int
    amount: int
    currency: str
    debit_credit: str
    description: str


class BPayDetailsBase(BaseModel):
    account_name: str
    biller_code: int


class BPayDetails(BPayDetailsBase):
    biller_name: str
    crn: int


class BPayAccount(BaseModel):
    id: str
    active: bool
    created_at: str
    updated_at: str
    verification_status: str
    currency: str
    bpay_details: BPayDetails


class BPayAccountRequest(BPayDetailsBase):
    user_id: str
    bpay_crn: str
