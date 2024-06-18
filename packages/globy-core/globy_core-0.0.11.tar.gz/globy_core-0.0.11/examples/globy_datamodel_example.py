import sys
sys.path.insert(0, '../src')

from globy_core.ml.datamodel import GlobySite, PageContentTypes, PageProperties, BusinessCategories, SiteTypes

if __name__ == "__main__":
    site = GlobySite(site_name="some hairdresser AB")

    ### This example demonstrates how to use the GlobySite class to create a datamodel object for a hairdresser website
    # Adding a valid site type
    try:
        site.site_type.append(SiteTypes.MULTIPAGER)
    except ValueError as e:
        print(f"Error: {e}")

    # Adding a valid business category
    try:
        site.business_categories.append(BusinessCategories.HAIRDRESSER)
    except ValueError as e:
        print(f"Error: {e}")

    # Adding a valid global content type
    try:
        site.global_content_types.append(PageContentTypes.ABOUT_US)
        site.global_content_types.append(PageContentTypes.GALLERY)
        site.global_content_types.append(PageContentTypes.SOCIAL_MEDIA)
        site.global_content_types.append(PageContentTypes.CONTACT)
    except ValueError as e:
        print(f"Error: {e}")

    # Adding a valid global property
    try:
        site.global_properties.append(PageProperties.IMAGE_HEAVY)
        site.page_properties.append(PageProperties.IMAGE_BACKGROUND)
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
