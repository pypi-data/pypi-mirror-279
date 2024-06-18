from enum import Enum
from typing import List, Any, Dict
import json
from pydantic import BaseModel, Field, field_validator
from enum import Enum

class BusinessTypes(Enum):
    """
    Business types are used to categorize different types of businesses.
    """
    SERVICE = "SERVICE"
    PRODUCT_SERVICE = "PRODUCT_SERVICE"
    PRODUCT = "PRODUCT"
    INFORMATION = "INFORMATION"

class BusinessCategories(Enum):
    """
    Business categories are used to categorize different types of businesses.
    If some business category is not listed here, Globy officially does not support it.
    """
    EXERCISE = "EXERCISE"
    COMPUTER_SCIENCE = "COMPUTER_SCIENCE"
    LAW = "LAW"
    INTERIOR_DECORATION = "INTERIOR_DECORATION"
    IT_CONSULTING = "IT_CONSULTING"
    MARKETING = "MARKETING"
    HEALTH_PRODUCTS = "HEALTH_PRODUCTS"
    GROCERIES = "GROCERIES"
    FOOD = "FOOD"
    FILM = "FILM"
    CULTURE = "CULTURE"
    GRAPHIC_DESIGN = "GRAPHIC_DESIGN"
    BUILDING_MATERIALS = "BUILDING_MATERIALS"
    EVENTS = "EVENTS"
    SKIN_CARE = "SKIN_CARE"
    HEALTH = "HEALTH"
    ART = "ART"
    ELECTRONICS = "ELECTRONICS"
    FINANCE = "FINANCE"
    HOME_DECOR = "HOME_DECOR"
    INSURANCE = "INSURANCE"
    ARCHITECTURE = "ARCHITECTURE"
    POLITICS = "POLITICS"
    BEAUTY = "BEAUTY"
    MUSIC = "MUSIC"
    DENTAL_CARE = "DENTAL_CARE"
    RESTAURANT = "RESTAURANT"
    RELIGION = "RELIGION"
    SPORTS = "SPORTS"
    REAL_ESTATE_AGENT = "REAL_ESTATE_AGENT"
    HEALTHCARE = "HEALTHCARE"
    TRAVEL = "TRAVEL"
    PHOTOGRAPHY = "PHOTOGRAPHY"
    EDUCATION = "EDUCATION"
    PET_PRODUCTS = "PET_PRODUCTS"
    CONSTRUCTION_COMPANY = "CONSTRUCTION_COMPANY"
    FASHION = "FASHION"
    WEB_DEVELOPMENT = "WEB_DEVELOPMENT"
    CONSULTING = "CONSULTING"
    MEDICINE = "MEDICINE"
    HAIRDRESSER = "HAIRDRESSER"
    ENVIRONMENTAL_CARE = "ENVIRONMENTAL_CARE"
    GARDEN_PRODUCTS = "GARDEN_PRODUCTS"
    INDUSTRY = "INDUSTRY"
    AGRICULTURE = "AGRICULTURE"
    CAR_WORKSHOP = "CAR_WORKSHOP"
    TRANSPORT = "TRANSPORT"
    ENERGY = "ENERGY"
    ENTERTAINMENT = "ENTERTAINMENT"
    UNKNOWN_BUSINESS_CATEGORY = "UNKNOWN_BUSINESS_CATEGORY"

# Type of site
class SiteTypes(Enum):
    """
    Site type is used to distinguish between different types of websites.
    """
    MULTIPAGER = "MULTIPAGER"
    ONEPAGER = "ONEPAGER"

# Type of page
class PageTypes(Enum):
    """
    Page type is used to distinguish between main/start pages and content pages (sub pages).
    """
    STARTPAGE = "STARTPAGE"
    CONTENT_PAGE = "CONTENT_PAGE"

# Content types that can be added to a page or a site
class PageContentTypes(Enum):
    """
    The page content describes the type of content that is shown on the page.
    May also be used in a list to describe the content of a page within that a certain site.
    """
    SOCIAL_MEDIA = "SOCIAL_MEDIA"
    ABOUT_US = "ABOUT_US"
    SERVICES = "SERVICES"
    PRODUCTS = "PRODUCTS"
    GALLERY = "GALLERY"
    TEAM = "TEAM"
    PRICING = "PRICING"
    BLOG = "BLOG"
    EVENTS = "EVENTS"
    PORTFOLIO = "PORTFOLIO"
    NEWS = "NEWS"
    CAREERS = "CAREERS"
    TERMS = "TERMS"
    PRIVACY = "PRIVACY"
    REFUND = "REFUND"
    SHIPPING = "SHIPPING"
    FAQ = "FAQ"
    CONTACT = "CONTACT"

# Properties that can be set for a page or a site
class PageProperties(Enum):
    """
    Page properties may describe anything from the layout of the page to the content it contains.
    """
    PARALLAX = "PARALLAX"
    DARK_THEME = "DARK_THEME"
    VIDEO_BACKGROUND = "VIDEO_BACKGROUND"
    IMAGE_BACKGROUND = "IMAGE_BACKGROUND"
    PARAGRAPH_HEAVY = "PARAGRAPH_HEAVY"
    IMAGE_HEAVY = "IMAGE_HEAVY"
    VIDEO_HEAVY = "VIDEO_HEAVY"
    TESTIMONIALS = "TESTIMONIALS"
    GENERIC = "GENERIC"
    FAQ = "FAQ"
    CONTACT = "CONTACT"

# Constants
VALID_BUSINESS_CATEGORIES = {item.value for item in BusinessCategories}
VALID_GLOBAL_CONTENT_TYPES = {item.value for item in PageContentTypes}
VALID_GLOBAL_PROPERTIES = {item.value for item in PageProperties}
VALID_SITE_TYPES = {item.value for item in SiteTypes}
VALID_PAGE_TYPES = {item.value for item in PageTypes}
VALID_PAGE_CTYPES = {item.value for item in PageContentTypes}
VALID_PAGE_PROPERTIES = {item.value for item in PageProperties}

class WordPressMetaData(BaseModel):
    """
    Meta data related to WordPress specifically
    """
    redux: Any = None
    settings: Any = None

class ModelMetaData(BaseModel):
    """
    Meta data gathered from inference process
    """
    pass

class GlobySiteDataModel(BaseModel):
    
    # Actual used fields
    business_categories: List[BusinessCategories] = Field(default_factory=list)
    global_content_types: List[PageContentTypes] = Field(default_factory=list)
    global_properties: List[PageProperties] = Field(default_factory=list)
    site_type: List[SiteTypes] = Field(default_factory=list)
    page_types: List[PageTypes] = Field(default_factory=list)
    page_ctypes: List[PageContentTypes] = Field(default_factory=list)
    page_properties: List[PageProperties] = Field(default_factory=list)

    @field_validator('business_categories', mode='before')
    def validate_business_category(cls, v):
        if not all(item.value in VALID_BUSINESS_CATEGORIES for item in v):
            raise ValueError(f"Invalid business category: {v}")
        return v

    @field_validator('global_content_types', mode='before')
    def validate_global_content_type(cls, v):
        if not all(item.value in VALID_GLOBAL_CONTENT_TYPES for item in v):
            raise ValueError(f"Invalid global content type: {v}")
        return v

    @field_validator('global_properties', mode='before')
    def validate_global_property(cls, v):
        if not all(item.value in VALID_GLOBAL_PROPERTIES for item in v):
            raise ValueError(f"Invalid global property: {v}")
        return v

    @field_validator('site_type', mode='before')
    def validate_site_type(cls, v):
        if not all(item.value in VALID_SITE_TYPES for item in v):
            raise ValueError(f"Invalid site type: {v}")
        return v

    @field_validator('page_types', mode='before')
    def validate_page_type(cls, v):
        if not all(item.value in VALID_PAGE_TYPES for item in v):
            raise ValueError(f"Invalid page type: {v}")
        return v

    @field_validator('page_ctypes', mode='before')
    def validate_page_ctype(cls, v):
        if not all(item.value in VALID_PAGE_CTYPES for item in v):
            raise ValueError(f"Invalid page content type: {v}")
        return v

    @field_validator('page_properties', mode='before')
    def validate_page_property(cls, v):
        if not all(item.value in VALID_PAGE_PROPERTIES for item in v):
            raise ValueError(f"Invalid page property: {v}")
        return v

class GlobySite(GlobySiteDataModel):
    """
    Use this when operating on a Globy user site.
    """
    site_name: str

    def to_json(self) -> str:
        return json.dumps(self.model_dump(), default=lambda o: o.value if isinstance(o, Enum) else o)

    def model_dump(self, *args, **kwargs) -> Dict[str, Any]:
        return super().model_dump(*args, **kwargs)
