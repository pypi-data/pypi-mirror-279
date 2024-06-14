# flake8: noqa

# import all models into this package
# if you have many models here with many references from one model to another this may
# raise a RecursionError
# to avoid this, import only the models that you directly need like:
# from from eis.claim.model.pet import Pet
# or import this package, but before doing it, use:
# import sys
# sys.setrecursionlimit(n)

from eis.claim.model.claim_class import ClaimClass
from eis.claim.model.claim_partner_class import ClaimPartnerClass
from eis.claim.model.claim_partner_role_class import ClaimPartnerRoleClass
from eis.claim.model.claim_status_class import ClaimStatusClass
from eis.claim.model.create_claim_partner_request_dto import CreateClaimPartnerRequestDto
from eis.claim.model.create_claim_partner_response_class import CreateClaimPartnerResponseClass
from eis.claim.model.create_claim_partner_role_request_dto import CreateClaimPartnerRoleRequestDto
from eis.claim.model.create_claim_partner_role_response_class import CreateClaimPartnerRoleResponseClass
from eis.claim.model.create_claim_request_dto import CreateClaimRequestDto
from eis.claim.model.create_claim_response_class import CreateClaimResponseClass
from eis.claim.model.create_claim_status_request_dto import CreateClaimStatusRequestDto
from eis.claim.model.create_claim_status_response_class import CreateClaimStatusResponseClass
from eis.claim.model.create_settlement_request_dto import CreateSettlementRequestDto
from eis.claim.model.create_settlement_response_class import CreateSettlementResponseClass
from eis.claim.model.get_claim_partner_response_class import GetClaimPartnerResponseClass
from eis.claim.model.get_claim_partner_role_response_class import GetClaimPartnerRoleResponseClass
from eis.claim.model.get_claim_response_class import GetClaimResponseClass
from eis.claim.model.get_claim_status_response_class import GetClaimStatusResponseClass
from eis.claim.model.get_settlement_response_class import GetSettlementResponseClass
from eis.claim.model.inline_response200 import InlineResponse200
from eis.claim.model.inline_response503 import InlineResponse503
from eis.claim.model.list_claim_partner_roles_response_class import ListClaimPartnerRolesResponseClass
from eis.claim.model.list_claim_partners_response_class import ListClaimPartnersResponseClass
from eis.claim.model.list_claim_statuses_response_class import ListClaimStatusesResponseClass
from eis.claim.model.list_claims_response_class import ListClaimsResponseClass
from eis.claim.model.list_settlements_response_class import ListSettlementsResponseClass
from eis.claim.model.patch_claim_request_dto import PatchClaimRequestDto
from eis.claim.model.patch_claim_response_class import PatchClaimResponseClass
from eis.claim.model.settlement_class import SettlementClass
from eis.claim.model.update_claim_partner_role_request_dto import UpdateClaimPartnerRoleRequestDto
from eis.claim.model.update_claim_partner_role_response_class import UpdateClaimPartnerRoleResponseClass
from eis.claim.model.update_claim_request_dto import UpdateClaimRequestDto
from eis.claim.model.update_claim_response_class import UpdateClaimResponseClass
from eis.claim.model.update_settlement_request_dto import UpdateSettlementRequestDto
from eis.claim.model.update_settlement_response_class import UpdateSettlementResponseClass
