import sys
sys.path.insert(0, '../src')

from globy_core.ml.datamodel import GlobySite, PageContentTypes, PageProperties, BusinessCategories, SiteTypes

if __name__ == "__main__":
    site = GlobySite(site_name="some hairdresser AB")


    ### This example demonstrates how to use the GlobySite class to create a datamodel object for a hairdresser website
    # Adding a valid site type
    try:
        site.add_site_type(SiteTypes.MULTIPAGER)
    except ValueError as e:
        print(f"Error: {e}")

    # Adding a valid business category
    try:
        site.add_business_category(BusinessCategories.HAIRDRESSER)
    except ValueError as e:
        print(f"Error: {e}")

    # Adding a valid global content type
    try:
        site.add_global_content_type(PageContentTypes.ABOUT_US)
        site.add_global_content_type(PageContentTypes.GALLERY)
        site.add_global_content_type(PageContentTypes.SOCIAL_MEDIA)
        site.add_global_content_type(PageContentTypes.CONTACT)
    except ValueError as e:
        print(f"Error: {e}")

    # Adding a valid global property
    try:
        site.add_global_property(PageProperties.IMAGE_HEAVY)
        site.add_page_property(PageProperties.IMAGE_BACKGROUND)
    except ValueError as e:
        print(f"Error: {e}")

    # print(site.to_json())

    ### Same example again, but this time we create the datamodel object using a dictionary as input
    site = GlobySite(
        site_name="some hairdresser AB",
        site_type=[SiteTypes.MULTIPAGER],
        business_categories=[BusinessCategories.HAIRDRESSER],
        global_content_types=[ 
            PageContentTypes.ABOUT_US,
            PageContentTypes.GALLERY,
            PageContentTypes.SOCIAL_MEDIA,
            PageContentTypes.CONTACT
            ],
        global_properties=[
            PageProperties.IMAGE_HEAVY,
            PageProperties.IMAGE_BACKGROUND,
            ]
    )
    print(site.to_json())
