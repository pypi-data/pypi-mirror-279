from enum import Enum
from typing import List, Optional

from pydantic import BaseModel


class TokenType(str, Enum):
    """The three types of tokens that can be issued.
    METRICS - Metrics token, used for gathering data.
    SIGN - Sign token, used for verifying the challenge.
    STRICT - Strict token, used for strict verification.
    """

    METRICS = "metrics"
    SIGN = "sign"
    STRICT = "strict"


class ActionType(str, Enum):
    """Translates the risk level into an action to take.
    ALLOW - Allow the visitor to continue.
    REDIRECT - Redirect the visitor to a different page. Or have them perform another form of verification.
    BLOCK - Block the visitor from accessing
    """

    ALLOW = 0
    REDIRECT = 1
    BLOCK = 2


class RiskLevel(str, Enum):
    """Risk level of the visitor. Simplified for ease of use.
    Under certain circumstances, you may want to use the risk score.
    """

    LOW = 0
    MEDIUM = 1
    HIGH = 2


class BaseResponse(BaseModel):
    """
    For representing 401, 409
    success: bool = False
    """

    message: str


class Device(BaseModel):
    """Device model, contains core information relating
    to the visitor device.

    model (Optional[str]): The model of the device, if available.
    brand (str): The brand of the device.
    os (str): The operating system of the device.
    version (str): The version of the operating system.
    """

    model: Optional[str] = None
    brand: str
    os: str
    version: str


class Browser(BaseModel):
    """Browser being used, can be null if the browser could not be
    identified. (next to impossible)

    name (str): The name of the browser.
    version (str): The version of the browser.
    """

    name: str
    version: str


class IpData(BaseModel):
    """IpData model, contains information about the IP address

    is_vpn (bool): If the IP address is a VPN.
    is_proxy (bool): If the IP address is a proxy.
    is_tor (bool): If the IP address is a TOR node.
    is_relay (bool): If the IP address is a relay.
    asn (str): The ASN of the IP address.
    """

    is_vpn: bool
    is_proxy: bool
    is_tor: bool
    is_relay: bool
    asn: str


class Location(BaseModel):
    """IP Location

    city (str): The city of the IP address.
    region (str): The region of the IP address.
    country (str): The country of the IP address.
    region_code (str): The region code of the IP address.
    country_code (str): The country code of the IP address.
    latitude (float): The latitude of the IP address.
    longitude (float): The longitude of the IP address.
    """

    city: str
    region: str
    country: str
    region_code: str
    country_code: str
    latitude: float
    longitude: float


class LookupResponse(BaseModel):
    """Response model for the lookup endpoint.

    token (str): The token of the visitor.
    token_type (str): The type of token that was issued (metrics, sign, strict)
    session (str): The persistent session of the visitor, will not change.
    device (Optional[Device]): The device information of the visitor.
    browser (Optional[Browser]): The browser information of the visitor.
    ip (str): The IP address of the visitor.
    ip_data (Optional[IpData]): The IP data of the visitor.
    location (Optional[Location]): The location of the visitor.
    page (Optional[str]): The page the visitor is on.
    risk_score (int): The risk score of the visitor.
    is_incognito (bool): If the visitor is in incognito mode.
    is_bot (bool): If the visitor is a bot.
    is_vm (bool): If the visitor is using a VM.
    is_farm (bool): If the visitor is using a device farm.
    solved (Optional[bool]): If the visitor has solved the captcha. (if applicable, GetMetricsToken will be null)
    consumed (bool): If the token has been consumed. AKA you used it before. Prevents abuse.
    """

    token: str
    token_type: TokenType
    session: str
    device: Optional[Device] = None
    browser: Optional[Browser] = None
    ip: str
    ip_data: Optional[IpData] = None
    location: Optional[Location] = None
    page: Optional[str] = None
    risk_score: int
    is_incognito: bool
    is_bot: bool
    is_farm: bool
    is_vm: bool
    solved: Optional[bool] = None
    consumed: Optional[bool] = None

    @property
    def risk_level(self) -> RiskLevel:
        if self.risk_score < 20:
            return RiskLevel.LOW
        elif self.risk_score < 50:
            return RiskLevel.MEDIUM
        else:
            return RiskLevel.HIGH


class VisitResponse(BaseModel):
    session: str
    visits: List[LookupResponse]
    has_next: bool


class DeleteResponse(BaseResponse):
    """Response model for the delete endpoint. Inherits from BaseResponse.

    message (str): Message from the server.
    """
