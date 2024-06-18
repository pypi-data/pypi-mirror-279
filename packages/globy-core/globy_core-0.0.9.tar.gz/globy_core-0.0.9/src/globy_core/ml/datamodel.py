from enum import Enum
from dataclasses import dataclass, field
from typing import List, Dict, Any
import json

# Supported business categories
class BusinessCategories(Enum):
    """
    Business categories are used to categorize different types of businesses.
    If some business category is not listed here, Globy officially does not support it.
    """
    HAIRDRESSER = "hairdresser"
    RESTAURANT = "restaurant"

    # Globy may support any business category that is not listed here.
    # As long as we have a good fit based on the other information provided
    UNKNOWN = "unknown"

# Type of site
class SiteTypes(Enum):
    """
    Site type is used to destinguish between different types of websites.
    """
    MULTIPAGER = "MULTIPAGER"
    ONEPAGER = "ONEPAGER"

# Type of page
class PageTypes(Enum):
    """
    Page type is used to destinguish between main/start pages and content pages (sub pages).
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

    # Note that these may overlap with PageContentTypes since for example "FAQ" may be both a content type and a property
    FAQ = "FAQ"
    CONTACT = "CONTACT"


# These fields are used to customize the valid values if they differ depending on the context ("site" or "page" for example)
VALID_BUSINESS_CATEGORIES = list(BusinessCategories)
VALID_GLOBAL_CONTENT_TYPES = list(PageContentTypes)
VALID_GLOBAL_PROPERTIES = list(PageProperties)
VALID_SITE_TYPES = list(SiteTypes)

# These are optional and defined per sub page if needed
VALID_PAGE_TYPES = list(PageTypes)
VALID_PAGE_CTYPES = list(PageContentTypes)
VALID_PAGE_PROPERTIES = list(PageProperties)

@dataclass
class WordPressMetaData:
    """
    Meta data related to WordPress specifically
    """
    def __init__(self):
        self.redux = None
        self.settings = None

@dataclass
class ModelMetaData:
    """
    Meta data gathered from inference process
    """
    def __init__(self):
        pass

@dataclass
class GlobySiteDataModel:
    UNDEFINED_VALUE: str = "undefined"

    # Actual used fields
    business_categories: List[str] = field(default_factory=list)
    global_content_types: List[PageContentTypes] = field(default_factory=list)
    global_properties: List[PageProperties] = field(default_factory=list)
    site_type: List[SiteTypes] = field(default_factory=list)
    page_types: List[PageTypes] = field(default_factory=list)
    page_ctypes: List[PageContentTypes] = field(default_factory=list)
    page_properties: List[PageProperties] = field(default_factory=list)

    def add_business_category(self, category: str):
        if category in VALID_BUSINESS_CATEGORIES:
            self.business_categories.append(category)
        else:
            raise ValueError("Invalid business category")

    def add_global_content_type(self, element: PageContentTypes):
        if element in VALID_GLOBAL_CONTENT_TYPES:
            self.global_content_types.append(element)
        else:
            raise ValueError("Invalid global content type")

    def add_global_property(self, property: PageProperties):
        if property in VALID_GLOBAL_PROPERTIES:
            self.global_properties.append(property)
        else:
            raise ValueError("Invalid global property")

    def add_site_type(self, site_type: SiteTypes):
        if site_type in VALID_SITE_TYPES:
            self.site_type.append(site_type)
        else:
            raise ValueError("Invalid site type")

    def add_page_type(self, page_type: PageTypes):
        if page_type in VALID_PAGE_TYPES:
            self.page_types.append(page_type)
        else:
            raise ValueError("Invalid page type")

    def add_page_ctype(self, page_ctype: PageContentTypes):
        if page_ctype in VALID_PAGE_CTYPES:
            self.page_ctypes.append(page_ctype)
        else:
            raise ValueError("Invalid page content type")

    def add_page_property(self, property: PageProperties):
        if property in VALID_PAGE_PROPERTIES:
            self.page_properties.append(property)
        else:
            raise ValueError("Invalid page property")


class GlobySite(GlobySiteDataModel):
    """
    Use this when operating on a Globy user site.
    """
    def __init__(self, site_name: str, **kwargs):
        self.site_name = site_name
        super().__init__(**kwargs)

    def to_json(self) -> str:
        return json.dumps(self.as_dict(), default=lambda o: o.value if isinstance(o, Enum) else o)

    def as_dict(self) -> Dict[str, Any]:
        return {
            "site_name": self.site_name,
            "business_categories": self.business_categories,
            "global_content_types": [element.value for element in self.global_content_types],
            "global_properties": [prop.value for prop in self.global_properties],
            "site_type": [site_type.value for site_type in self.site_type],
            "page_types": [page_type.value for page_type in self.page_types],
            "page_ctypes": [page_ctype.value for page_ctype in self.page_ctypes],
            "page_properties": [prop.value for prop in self.page_properties],
        }