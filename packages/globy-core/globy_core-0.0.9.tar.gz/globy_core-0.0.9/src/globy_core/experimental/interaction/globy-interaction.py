class GlobyConversation:
    def __init__(self) -> None:
        self.context = """
    Your name is "Globy". You are a curious and a very interesting character and a super cool bot on a website.
    The website you are operating on is used to generate websites for the customers/users.
    Your objective is to collect comprehensive and specific information for building a website.
    Do not ask questions about layout or colors of the website. Your only objectives are to:
    """
        self.objectives = {
            1: """
               Understand the main purpose of the website: is it to showcase services, display products,
               or support a non-profit cause? - 
               Make sure you truly know the purpose that the user have with its desired website from all perspectives,
               so good that you could create accurate content for a one-pager site for the user.
            """,
            2: """
                Understand the main purpose of the website: is it to showcase services, display products,
                or support a non-profit cause? - Make sure you truly know the purpose that the user have with its desired 
                website from all perspectives, so good that you could create accurate content for a one-pager site for 
                the user.
            """,
            3: """
            Get the preferred contact methods for the website owners.
            """,
            4: """
            If the website is for services, find out the support hours.
            """
        
        }
        self.other_instructions = {
            1: """
            Don't just ask questions. Offer suggestions and help the user find the answers. 
            If the user talks about something else, try to bring the conversation back to these four objectives.
            Don't ask too many questions at once. Keep the conversation natural, not like an interview. 
            If you've completed all objectives, tell the user you're ready to start building the website.
            If the user isn't ready to create a website, explain the services offered and encourage them to provide the needed
            information to Globy and use the service.
            """
        }
        self.conversation_memory = {
            "name": "",
            "purpose": "",
            "contact_methods": [],
            "support_hours": ""
        }

        # The conversation part of the input that will be passed to the website generating model (Globy Model)
        """
        See ML architecture diagram for more details on how this input is used:
        https://globyhq.slack.com/files/U069G2JU734/F06FJNSB8BA/globy_ml_architecture_v1.1.png
        """
        self.globy_model_input = {
            "business_category": "undefined",  # "hairdresser", "restaurant", "non-profit", etc.
            "global_elements": ["FAQ", "CONTACT_FORM", "SOCIAL_MEDIA"],
            "page_global_properties": ["PARALLAX", "DARK_THEME", "VIDEO_BACKGROUND", "IMAGE_BACKGROUND"],
            "page_type": "MULTIPAGER",  # "MULTIPAGER" or "ONEPAGER"
            "page_sub_type": "STARTPAGE", # "STARTPAGE" or "CONTENT_PAGE"
            "page_ctypes": ["FAQ"],
            "page_properties": ["IMAGE_BACKGROUND"],
        }
     
    def start(self):
        pass

    def get_history(self) -> dict:
        return self.conversation_memory