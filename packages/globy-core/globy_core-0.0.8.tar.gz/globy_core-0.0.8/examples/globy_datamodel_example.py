import sys
sys.path.append('../src')

from globy_core.ml.datamodel import GlobySite, PageContentTypes, PageProperties, BusinessCategories

if __name__ == "__main__":
    site = GlobySite(site_name="globy_site")

    # Adding a valid business category
    try:
        site.add_business_category(BusinessCategories.HAIRDRESSER)
        print(site.as_dict())
        print(site.to_json())
    except ValueError as e:
        print(f"Error: {e}")

    # Adding a valid global content type
    try:
        site.add_global_content_type(PageContentTypes.ABOUT_US)
        print(site.as_dict())
        print(site.to_json())
    except ValueError as e:
        print(f"Error: {e}")

    # Adding a valid page property
    try:
        site.add_page_property(PageProperties.PARAGRAPH_HEAVY)
        print(site.as_dict())
        print(site.to_json())
    except ValueError as e:
        print(f"Error: {e}")
