from enum import Enum


class DocumentStatus(Enum):
    INTEGRATED = 'INTEGRADO'
    PENDING_INTEGRATION = 'PENDENTE_INTEGRACAO'
    CONVERTER_ERROR = 'ERRO_CONVERSAO'


class DocumentMovementType(Enum):
    INPUT = 'E',
    OUTPUT = 'S'


class ResponsibleMovement(Enum):
    ISSUER = 'EMITENTE'
    RECIPIENT = 'DESTINATARIO'


class Origin(Enum):
    JDE = "JDE"
    ABADI = "ABADI"


class DocumentType(Enum):
    SERVICE = 'SERV'
    PRODUCT = 'PROD'
    ISS_SERVICE = "SERV_ISS"


class TaxType:
    PIS = "PIS"
    IPI = "IPI"
    ISS = "ISS"
    INSS = "INSS"
    COFINS = "COFINS"
    ISSRET = "ISSRET"
    ICMS = "ICMS"
    ICMSST = "ICMSST"
    ICMSFCP = "ICMSFCP"
    ICMSFCPST = "ICMSFCPST"
    ICMSMONORETEN = "ICMSMONORETEN"
    ICMSMONOPROP = "ICMSMONOPROP"
    ICMSMONODIFER = "ICMSMONODIFER"
    ICMSMONORET = "ICMSMONORET"
