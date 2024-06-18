from dataclasses import dataclass
from typing import Optional, Tuple
from enum import Enum
from ..errors import CarmenAPIConfigError
from ..models import CloudServiceRegion

@dataclass(frozen=True)
class SelectedServices:
    """
    Specifies the recognition services to call on the input image. At least one
    service must be selected.

    Attributes
    ----------
    anpr : Optional[bool]
        True if ANPR (Automatic Number Plate Recognition) should be performed
        on the input image, False otherwise.
    mmr : Optional[bool]
        True if MMR (Make and Model Recognition) should be performed on the input
        image, False otherwise.
    adr : Optional[bool]
        True if ADR (Dangerous Goods plate recognition) should be performed on
        the input image, False otherwise.
    """
    anpr: Optional[bool] = False
    mmr: Optional[bool] = False
    adr: Optional[bool] = False

    def __post_init__(self):
        if not any([self.anpr, self.mmr, self.adr]):
            raise CarmenAPIConfigError("At least one service must be selected.")

@dataclass
class InputImageLocation:
    """
    Represents the geographic location where the input image was taken.
    """
    region: str
    location: Optional[str] = None

@dataclass
class RegionOfInterest:
    """
    Represents the region of interest to be analyzed in the input image.
    The coordinates are given as `(x, y)` pairs.
    """
    top_left: Tuple[float, float]
    top_right: Tuple[float, float]
    bottom_right: Tuple[float, float]
    bottom_left: Tuple[float, float]

class Europe:
    Hungary = InputImageLocation(region="eur", location="hun")
    Austria = InputImageLocation(region="eur", location="aut")
    Slovakia = InputImageLocation(region="eur", location="svk")
    Czechia = InputImageLocation(region="eur", location="cze")
    Slovenia = InputImageLocation(region="eur", location="svn")
    Poland = InputImageLocation(region="eur", location="pol")
    Estonia = InputImageLocation(region="eur", location="est")
    Latvia = InputImageLocation(region="eur", location="lva")
    Lithuania = InputImageLocation(region="eur", location="ltu")
    Romania = InputImageLocation(region="eur", location="rou")
    Bulgaria = InputImageLocation(region="eur", location="bgr")
    Croatia = InputImageLocation(region="eur", location="hrv")
    BosniaHerzegovina = InputImageLocation(region="eur", location="bih")
    Serbia = InputImageLocation(region="eur", location="srb")
    NorthMacedonia = InputImageLocation(region="eur", location="mkd")
    Montenegro = InputImageLocation(region="eur", location="mne")
    Albania = InputImageLocation(region="eur", location="alb")
    Greece = InputImageLocation(region="eur", location="grc")
    Turkey = InputImageLocation(region="eur", location="tur")
    Netherlands = InputImageLocation(region="eur", location="nld")
    Luxembourg = InputImageLocation(region="eur", location="lux")
    Germany = InputImageLocation(region="eur", location="deu")
    Belgium = InputImageLocation(region="eur", location="bel")
    France = InputImageLocation(region="eur", location="fra")
    FranceOverseasTerritories = InputImageLocation(region="eur", location="fra_ot")
    Switzerland = InputImageLocation(region="eur", location="che")
    Italy = InputImageLocation(region="eur", location="ita")
    Portugal = InputImageLocation(region="eur", location="prt")
    Spain = InputImageLocation(region="eur", location="esp")
    EuropeanOrganization = InputImageLocation(region="eur", location="none")
    Denmark = InputImageLocation(region="eur", location="dnk")
    DenmarkFaroe = InputImageLocation(region="eur", location="fro")
    DenmarkGreenland = InputImageLocation(region="eur", location="grl")
    Norway = InputImageLocation(region="eur", location="nor")
    Sweden = InputImageLocation(region="eur", location="swe")
    Finland = InputImageLocation(region="eur", location="fin")
    FinlandAland = InputImageLocation(region="eur", location="fin")
    GreatBritain = InputImageLocation(region="eur", location="gbr")
    Gibraltar = InputImageLocation(region="eur", location="gib")
    IsleOfMan = InputImageLocation(region="eur", location="imn")
    Jersey = InputImageLocation(region="eur", location="jey")
    Guernsey = InputImageLocation(region="eur", location="ggy")
    Alderney = InputImageLocation(region="eur", location="ald")
    GreatBritainNorthernIreland = InputImageLocation(region="eur", location="nir")
    Ireland = InputImageLocation(region="eur", location="irl")
    Russia = InputImageLocation(region="eur", location="rus")
    Ukraine = InputImageLocation(region="eur", location="ukr")
    UkraineLuhansk = InputImageLocation(region="eur", location="ukr")
    UkraineDonetsk = InputImageLocation(region="eur", location="ukr")
    Moldova = InputImageLocation(region="eur", location="mda")
    MoldovaTransnistria = InputImageLocation(region="eur", location="mda")
    Belarus = InputImageLocation(region="eur", location="blr")
    Georgia = InputImageLocation(region="eur", location="geo")
    GeorgiaAbkhazia = InputImageLocation(region="eur", location="geo")
    GeorgiaSouthOssetia = InputImageLocation(region="eur", location="geo")
    Azerbaijan = InputImageLocation(region="eur", location="aze")
    Armenia = InputImageLocation(region="eur", location="arm")
    Kazakhstan = InputImageLocation(region="cas", location="kaz")
    Andorra = InputImageLocation(region="eur", location="and")
    Monaco = InputImageLocation(region="eur", location="mco")
    Liechtenstein = InputImageLocation(region="eur", location="lie")
    SanMarino = InputImageLocation(region="eur", location="smr")
    VaticanCity = InputImageLocation(region="eur", location="vat")
    Kosovo = InputImageLocation(region="eur", location="rks")
    Iceland = InputImageLocation(region="eur", location="isl")
    Malta = InputImageLocation(region="eur", location="mlt")
    CyprusSouthCyprus = InputImageLocation(region="eur", location="cyp")
    CyprusUNCyprus = InputImageLocation(region="eur", location="none")
    CyprusNorthCyprus = InputImageLocation(region="eur", location="cyp")
    SvalbardAndJanMayen = InputImageLocation(region="eur", location="sjm")

class NorthAmerica:
    UnitedStatesOfAmericaGovernment = InputImageLocation(region="nam", location="none")
    UnitedStatesOfAmericaColumbia = InputImageLocation(region="nam", location="us-dc")
    UnitedStatesOfAmericaAlaska = InputImageLocation(region="nam", location="us-ak")
    UnitedStatesOfAmericaWashington = InputImageLocation(region="nam", location="us-wa")
    UnitedStatesOfAmericaOregon = InputImageLocation(region="nam", location="us-or")
    UnitedStatesOfAmericaCalifornia = InputImageLocation(region="nam", location="us-ca")
    UnitedStatesOfAmericaIdaho = InputImageLocation(region="nam", location="us-id")
    UnitedStatesOfAmericaNevada = InputImageLocation(region="nam", location="us-nv")
    UnitedStatesOfAmericaMontana = InputImageLocation(region="nam", location="us-mt")
    UnitedStatesOfAmericaWyoming = InputImageLocation(region="nam", location="us-wy")
    UnitedStatesOfAmericaUtah = InputImageLocation(region="nam", location="us-ut")
    UnitedStatesOfAmericaArizona = InputImageLocation(region="nam", location="us-az")
    UnitedStatesOfAmericaNorthDakota = InputImageLocation(region="nam", location="us-nd")
    UnitedStatesOfAmericaSouthDakota = InputImageLocation(region="nam", location="us-sd")
    UnitedStatesOfAmericaNebraska = InputImageLocation(region="nam", location="us-ne")
    UnitedStatesOfAmericaColorado = InputImageLocation(region="nam", location="us-co")
    UnitedStatesOfAmericaNewMexico = InputImageLocation(region="nam", location="us-nm")
    UnitedStatesOfAmericaKansas = InputImageLocation(region="nam", location="us-ks")
    UnitedStatesOfAmericaOklahoma = InputImageLocation(region="nam", location="us-ok")
    UnitedStatesOfAmericaTexas = InputImageLocation(region="nam", location="us-tx")
    UnitedStatesOfAmericaArkansas = InputImageLocation(region="nam", location="us-ar")
    UnitedStatesOfAmericaMinnesota = InputImageLocation(region="nam", location="us-mn")
    UnitedStatesOfAmericaWisconsin = InputImageLocation(region="nam", location="us-wi")
    UnitedStatesOfAmericaIowa = InputImageLocation(region="nam", location="us-ia")
    UnitedStatesOfAmericaIllinois = InputImageLocation(region="nam", location="us-il")
    UnitedStatesOfAmericaMissouri = InputImageLocation(region="nam", location="us-mo")
    UnitedStatesOfAmericaMichigan = InputImageLocation(region="nam", location="us-mi")
    UnitedStatesOfAmericaIndiana = InputImageLocation(region="nam", location="us-in")
    UnitedStatesOfAmericaOhio = InputImageLocation(region="nam", location="us-oh")
    UnitedStatesOfAmericaKentucky = InputImageLocation(region="nam", location="us-ky")
    UnitedStatesOfAmericaAlabama = InputImageLocation(region="nam", location="us-al")
    UnitedStatesOfAmericaTennessee = InputImageLocation(region="nam", location="us-tn")
    UnitedStatesOfAmericaLouisiana = InputImageLocation(region="nam", location="us-la")
    UnitedStatesOfAmericaMississippi = InputImageLocation(region="nam", location="us-ms")
    UnitedStatesOfAmericaMaine = InputImageLocation(region="nam", location="us-me")
    UnitedStatesOfAmericaVermont = InputImageLocation(region="nam", location="us-vt")
    UnitedStatesOfAmericaNewHampshire = InputImageLocation(region="nam", location="us-nh")
    UnitedStatesOfAmericaConnecticut = InputImageLocation(region="nam", location="us-ct")
    UnitedStatesOfAmericaMassachusetts = InputImageLocation(region="nam", location="us-ma")
    UnitedStatesOfAmericaRhodeIsland = InputImageLocation(region="nam", location="us-ri")
    UnitedStatesOfAmericaNewYork = InputImageLocation(region="nam", location="us-ny")
    UnitedStatesOfAmericaNewJersey = InputImageLocation(region="nam", location="us-nj")
    UnitedStatesOfAmericaDelaware = InputImageLocation(region="nam", location="us-de")
    UnitedStatesOfAmericaPennsylvania = InputImageLocation(region="nam", location="us-pa")
    UnitedStatesOfAmericaMaryland = InputImageLocation(region="nam", location="us-md")
    UnitedStatesOfAmericaVirginia = InputImageLocation(region="nam", location="us-va")
    UnitedStatesOfAmericaWestVirginia = InputImageLocation(region="nam", location="us-wv")
    UnitedStatesOfAmericaNorthCarolina = InputImageLocation(region="nam", location="us-nc")
    UnitedStatesOfAmericaSouthCarolina = InputImageLocation(region="nam", location="us-sc")
    UnitedStatesOfAmericaGeorgia = InputImageLocation(region="nam", location="us-ga")
    UnitedStatesOfAmericaFlorida = InputImageLocation(region="nam", location="us-fl")
    UnitedStatesOfAmericaHawaii = InputImageLocation(region="nam", location="us-hi")
    UnitedStatesOfAmericaPuertoRico = InputImageLocation(region="nam", location="us-pr")
    UnitedStatesOfAmericaGuam = InputImageLocation(region="nam", location="us-gu")
    UnitedStatesOfAmericaAmericanSamoa = InputImageLocation(region="nam", location="us-as")
    UnitedStatesOfAmericaVirginIslands = InputImageLocation(region="nam", location="us-vi")
    UnitedStatesOfAmericaNorthernMarianaIslands = InputImageLocation(region="nam", location="us-mp")
    CanadaFederal = InputImageLocation(region="nam", location="none")
    CanadaBritishColumbia = InputImageLocation(region="nam", location="ca-bc")
    CanadaAlberta = InputImageLocation(region="nam", location="ca-ab")
    CanadaSaskatchewan = InputImageLocation(region="nam", location="ca-sk")
    CanadaManitoba = InputImageLocation(region="nam", location="ca-mb")
    CanadaOntario = InputImageLocation(region="nam", location="ca-on")
    CanadaQuebec = InputImageLocation(region="nam", location="ca-qc")
    CanadaNovaScotia = InputImageLocation(region="nam", location="ca-ns")
    CanadaNewBrunswick = InputImageLocation(region="nam", location="ca-nb")
    CanadaNewfoundlandLabrador = InputImageLocation(region="nam", location="ca-nl")
    CanadaNorthWestTerritories = InputImageLocation(region="nam", location="ca-nt")
    CanadaNunavut = InputImageLocation(region="nam", location="ca-nu")
    CanadaPrinceEdouardIsland = InputImageLocation(region="nam", location="ca-pe")
    CanadaYukon = InputImageLocation(region="nam", location="ca-yt")

class CentralAmerica:
    Guatemala = InputImageLocation(region="cam", location="gtm")
    Belize = InputImageLocation(region="cam", location="blz")
    ElSalvador = InputImageLocation(region="cam", location="slv")
    Nicaragua = InputImageLocation(region="cam", location="nic")
    Honduras = InputImageLocation(region="cam", location="hnd")
    CostaRica = InputImageLocation(region="cam", location="cri")
    Panama = InputImageLocation(region="cam", location="pan")
    Mexico = InputImageLocation(region="cam", location="mex")

class SouthAmerica:
    Colombia = InputImageLocation(region="sam", location="col")
    Venezuela = InputImageLocation(region="sam", location="ven")
    Guyana = InputImageLocation(region="sam", location="guy")
    Suriname = InputImageLocation(region="sam", location="sur")
    Peru = InputImageLocation(region="sam", location="per")
    Brazil = InputImageLocation(region="sam", location="bra")
    Ecuador = InputImageLocation(region="sam", location="ecu")
    Bolivia = InputImageLocation(region="sam", location="bol")
    Paraguay = InputImageLocation(region="sam", location="pry")
    Chile = InputImageLocation(region="sam", location="chl")
    Argentina = InputImageLocation(region="sam", location="arg")
    Uruguay = InputImageLocation(region="sam", location="ury")
    FalklandIslands = InputImageLocation(region="sam", location="flk")

class CentralAsia:
    Uzbekistan = InputImageLocation(region="cas", location="uzb")
    Turkmenistan = InputImageLocation(region="cas", location="tkm")
    Tajikistan = InputImageLocation(region="cas", location="tjk")
    Kyrgyzstan = InputImageLocation(region="cas", location="kgz")
    Mongolia = InputImageLocation(region="cas", location="mng")
    Afghanistan = InputImageLocation(region="cas", location="afg")

class EastAsia:
    China = InputImageLocation(region="eas", location="chn")
    HongKong = InputImageLocation(region="eas", location="hkg")
    Macau = InputImageLocation(region="eas", location="mac")
    KoreaSouth = InputImageLocation(region="eas", location="kor")
    KoreaNorth = InputImageLocation(region="eas", location="prk")

class SouthAsia:
    Thailand = InputImageLocation(region="sas", location="tha")
    Malaysia = InputImageLocation(region="sas", location="mys")
    Singapore = InputImageLocation(region="sas", location="sgp")
    Myanmar = InputImageLocation(region="sas", location="mmr")
    Laos = InputImageLocation(region="sas", location="lao")
    Cambodia = InputImageLocation(region="sas", location="khm")
    Vietnam = InputImageLocation(region="sas", location="vnm")
    Brunei = InputImageLocation(region="sas", location="brn")
    ChristmasIsland = InputImageLocation(region="sas", location="cxr")
    KeelingIslands = InputImageLocation(region="sas", location="cck")

class MiddleEast:
    Syria = InputImageLocation(region="me", location="syr")
    Lebanon = InputImageLocation(region="me", location="lbn")
    Jordan = InputImageLocation(region="me", location="jor")
    SaudiArabia = InputImageLocation(region="me", location="sau")
    Kuwait = InputImageLocation(region="me", location="kwt")
    UnitedArabEmirates = InputImageLocation(region="me", location="are")
    Qatar = InputImageLocation(region="me", location="qat")
    Bahrain = InputImageLocation(region="me", location="bhr")
    Oman = InputImageLocation(region="me", location="omn")
    Yemen = InputImageLocation(region="me", location="yem")

class AustraliaAndOceania:
    AustraliaUnknown = InputImageLocation(region="aus", location="none")
    AustraliaFederalInterstate = InputImageLocation(region="aus", location="none")
    AustraliaGovernment = InputImageLocation(region="aus", location="none")
    AustraliaCapitalTerritory = InputImageLocation(region="aus", location="au-act")
    AustraliaNorthernTerritory = InputImageLocation(region="aus", location="au-nt")
    AustraliaNewSouthWales = InputImageLocation(region="aus", location="au-nsw")
    AustraliaQueensland = InputImageLocation(region="aus", location="au-qld")
    AustraliaSouthAustralia = InputImageLocation(region="aus", location="au-sa")
    AustraliaTasmania = InputImageLocation(region="aus", location="au-tas")
    AustraliaVictoria = InputImageLocation(region="aus", location="au-vic")
    AustraliaWesternAustralia = InputImageLocation(region="aus", location="au-wa")

class Locations:
    """
    An object which contains all accepted region/location pairs.
    """
    Europe = Europe
    NorthAmerica = NorthAmerica
    CentralAmerica = CentralAmerica
    SouthAmerica = SouthAmerica
    CentralAsia = CentralAsia
    EastAsia = EastAsia
    SouthAsia = SouthAsia
    MiddleEast = MiddleEast
    AustraliaAndOceania = AustraliaAndOceania

@dataclass
class VehicleAPIOptions:
    """
    An object containing configuration options for the Vehicle API client.

    Attributes
    ----------
    api_key : str
        The API key to be used for authentication.
    endpoint : Optional[str]
        The URL of the API endpoint to call. Optional if `cloud_service_region`
        is also set. Overrides `cloud_service_region` if both properties are set.
    cloud_service_region : Optional[CloudServiceRegion]
        The cloud service region to use - `"EU"` for Europe and `"US"` for the
        United States. Has no effect if `endpoint` is also set.
    input_image_location : InputImageLocation
        The expected geographic region of the license plates in the uploaded image.
        You can either use one of the presets in the `Locations` object or provide
        your own settings in an `InputImageLocation(region="", location="")` object.
        `region` is required but `location` is optional.
    region_of_interest : Optional[RegionOfInterest]
        The region of interest in the image to be analyzed.
    services : SelectedServices
        The services to use. At least one of `anpr` (Automated Number Plate
        Recognition), `mmr` (Make and Model Recognition) and `adr` (Dangerous Goods
        Pictogram Recognition) must be specified.
    disable_call_statistics : Optional[bool] = False
        The service uses your call statistics, which were generated based on the
        list of locations (countries and states) determined when reading your
        previously sent images, to decide which ANPR engines should be run when
        processing your uploaded images. If you want the service to ignore your call
        statistics, for example because you use the service with images from
        different locations around the world, you can turn this feature off by
        setting the property value to `true`.
    disable_image_resizing : Optional[bool] = False
        The service resizes large images to Full HD resolution by bicubic
        interpolation. Resizing can make reading many times faster, but it can reduce
        the recognition efficiency. If you don't want the service to resize your
        images, turn this feature on by setting the property value to `true`. By
        disabling image resizing, you may also need to enable wide range analysis.
    enable_wide_range_analysis : Optional[bool] = False
        If you cannot guarantee that the uploaded image meets all the required
        parameters (see the Input Images tab on the How To Use page), you can turn
        on the wide-range analysis by setting this property's value to `true`.
        Attention! The duration of the analysis may increase several times.
    enable_unidentified_license_plate : Optional[bool] = False
        If you want to receive text results read from unidentified license plate
        types as well, you can turn this feature on by setting the property value to
        true. Attention! The number of false positives can be much higher.
    max_reads : Optional[int] = 1
        An optional parameter, it specifies the maximum number of vehicle/license
        plate searches per image. Use this parameter carefully, because every
        search increases the processing time. The system will stop searching when
        there is no more vehicle/license plate in the image, or the number of
        searches reaches the value of `max_reads`. Its value is `1` by default,
        the maximum is `5`.
    retry_count : Optional[int] = 3
        How many times the request should be retried in case of a 5XX response
        status code. Default: 3.
    """
    api_key: str
    input_image_location: InputImageLocation
    services: SelectedServices
    endpoint: Optional[str] = None
    cloud_service_region: Optional[CloudServiceRegion] = None
    region_of_interest: Optional[RegionOfInterest] = None
    disable_call_statistics: Optional[bool] = False
    disable_image_resizing: Optional[bool] = False
    enable_wide_range_analysis: Optional[bool] = False
    enable_unidentified_license_plate: Optional[bool] = False
    max_reads: Optional[int] = 1
    retry_count: Optional[int] = 3
