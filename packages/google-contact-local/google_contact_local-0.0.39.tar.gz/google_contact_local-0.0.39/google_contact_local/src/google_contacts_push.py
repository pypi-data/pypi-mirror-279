from database_mysql_local.connector import Connector
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from .google_contacts import GoogleContacts, SCOPES
from .google_contacts_constants import GoogleContactConstants



# TODO: the inheritance of GoogleContactsPush from GoogleContacts is temporary
# we want to inherit from GoogleAccount class
class GoogleContactsPush(GoogleContacts):
    def __init__(self):
        super().__init__()

    def create_and_push_contact_by_contact_id(self, *, username: str, contact_id: int):
        self.logger.start('create_and_push_contact_by_contact_id', object={'contact_id': contact_id})
        try:
            google_contact_dict = self.get_google_contact_dict_by_contact_id(contact_id)
            self.create_contact_by_google_contact_dict(username=username, google_contact_dict=google_contact_dict)
        except Exception as exception:
            self.logger.exception('Exception in create_and_push_contact_by_contact_id', object={'exception': exception})
            raise exception
        self.logger.end('create_and_push_contact_by_contact_id')

    def create_contact_by_google_contact_dict(self, *, username: str, google_contact_dict: dict):
        token_data = self.user_externals_local.get_auth_details(  # TODO: fix typing
            username=username, system_id=GoogleContactConstants.GOOGLE_SYSTEM_ID,
            profile_id=self.user_context.get_effective_profile_id())
        if not token_data:
            self.logger.error("Token data not found in DB.")
            raise Exception("Token data not found in DB.")

        # Unpack the token_data tuple into its constituent parts
        access_token, refresh_token, expiry = token_data

        # Update the token_info dictionary with the unpacked values
        token_info = {
            'token': access_token,
            'refresh_token': refresh_token,
            'token_uri': self.google_token_uri,
            'client_id': self.google_client_id,
            'client_secret': self.google_client_secret,
            'scopes': SCOPES,
            'expiry': expiry  # Already in string format, no need to convert
        }

        # Create a Credentials object from the stored token
        self.creds = Credentials.from_authorized_user_info(token_info)

        # Print all attributes of self.creds for debugging
        for attr in dir(self.creds):
            if not attr.startswith("__"):
                print(f"{attr}: {getattr(self.creds, attr)}")

        if not self.creds.valid:
            self.logger.error("Stored credentials are not valid.", object={"token_info": token_info})
            self.update_by_column_and_value(
                schema_name="user_external", table_name="user_external_table",
                column_name="refresh_token", column_value=refresh_token,
                data_dict={"is_refresh_token_valid": False})
            raise Exception("Stored credentials are not valid.")
        service = build('people', 'v1', credentials=self.creds)
        service.people().createContact(body=google_contact_dict).execute()

    def get_contact_ids_with_no_google_people_api_resource_name(
            self, *, limit: int = 1, data_source_types_ids_list: list = None, 
            order_by: str = None) -> list[int]:
        self.logger.start('get_contact_ids_with_no_google_people_api_resource_name', object={'limit': limit})
        contacts_ids_list: list = []
        connection = Connector.connect('contact')
        params = []
        select_query = ''
        select_query_part1 = (
            'SELECT DISTINCT cv.contact_id FROM contact.contact_view AS cv JOIN'
            ' importer.importer_view AS iv JOIN contact_person.contact_person_view AS cpv'
            ' JOIN data_source_instance.data_source_instance_table AS dsigv'
            ' WHERE cv.contact_id = iv.entity_id AND cv.contact_id = cpv.contact_id AND'
            ' iv.google_people_api_resource_name IS NULL AND iv.end_timestamp IS NULL'
        )
        select_query += select_query_part1
        if data_source_types_ids_list:
            select_query += ' AND cv.data_source_instance_id = dsigv.data_source_instance_id AND ('
            for data_source_type_id in data_source_types_ids_list:
                condition = 'dsigv.data_source_type_id = %s OR '
                select_query += condition
                params.append(data_source_type_id)
            select_query = select_query[:-3]    # remove the last ' OR '
            select_query += ')'
        select_query_part2 = (
            ' AND NOT EXISTS (SELECT 1 FROM importer.importer_view AS iv2 JOIN'
            ' contact.contact_view AS cv2 JOIN contact_person.contact_person_view AS cpv2'
            ' WHERE cpv2.contact_id = cv2.contact_id AND cpv.person_id = cpv2.person_id'
            ' AND iv2.entity_id = cv2.contact_id AND iv2.google_people_api_resource_name IS NOT NULL)'
        )
        select_query += select_query_part2
        if order_by:
            select_query += ' ORDER BY %s'
            params.append(order_by)
        select_query += ' LIMIT %s'
        params.append(limit)
        self.logger.info('select_query', object={'select_query': select_query, 'params': params})
        cursor = connection.cursor()
        cursor.execute(select_query, params)
        results = cursor.fetchall()
        for result in results:
            contacts_ids_list.append(result[0])
        self.logger.end('get_contact_ids_with_no_google_people_api_resource_name',
                        object={'contacts_ids_list': contacts_ids_list})
        return contacts_ids_list

    # Get contact dict by contact id from the databse
    def get_google_contact_dict_by_contact_id(self, contact_id: int) -> dict:
        self.logger.start('get_contact_dict_by_contact_id', object={'contact_id': contact_id})
        google_contact_dict: dict = {}

        # Get the record from contact_view
        contact_view_select_result_dict: dict = self.select_one_dict_by_column_and_value(
            schema_name='contact', view_table_name='contact_view', column_name='contact_id', column_value=contact_id)
        if contact_view_select_result_dict is None:
            self.logger.info('No contact found with the given contact_id', object={'contact_id': contact_id})
            self.logger.end('get_contact_dict_by_contact_id', object={'contact_dict': google_contact_dict})
            return google_contact_dict
        self.__append_result_from_contact_view_to_google_contact_dict(
            contact_view_select_result_dict, google_contact_dict)
        self.logger.end('get_contact_dict_by_contact_id', object={'google_contact_dict': google_contact_dict})
        return google_contact_dict

    def __append_result_from_contact_view_to_google_contact_dict(self, contact_view_select_result_dict: dict,
                                                                 google_contact_dict: dict):
        google_contact_dict['names'] = [
            {
                'givenName': contact_view_select_result_dict['original_first_name'],    # TODO: Shall we use first_name?
                'familyName': contact_view_select_result_dict['original_last_name'],     # TODO: Shall we use last_name?
                'displayName': contact_view_select_result_dict['display_as'],    # TODO: Shall we use full_name?
            }
        ]
        google_contact_dict['phoneNumbers'] = [
            {
                'value': contact_view_select_result_dict['phone1'],
                # 'type': 'mobile',     # TODO: There is not phone type in the db, shall we add it?
            },
            {
                'value': contact_view_select_result_dict['phone2'],
                # 'type': 'mobile',     # TODO: There is not phone type in the db, shall we add it?
            },
            {
                'value': contact_view_select_result_dict['phone3'],
                # 'type': 'mobile',     # TODO: There is not phone type in the db, shall we add it?
            }
        ]
        google_contact_dict['emailAddresses'] = [
            {
                'value': contact_view_select_result_dict['email1'],
                # 'type': 'home',     # TODO: There is not email type in the db, shall we add it?
            },
            {
                'value': contact_view_select_result_dict['email2'],
                # 'type': 'home',     # TODO: There is not email type in the db, shall we add it?
            },
            {
                'value': contact_view_select_result_dict['email3'],
                # 'type': 'home',     # TODO: There is not email type in the db, shall we add it?
            }
        ]
        # TODO: use also organization_profile for this?
        google_contact_dict['organizations'] = [
            {
                'name': contact_view_select_result_dict['organization'],
                'title': contact_view_select_result_dict['title'],
                'jobDescription': contact_view_select_result_dict['job_title'],
            }
        ]
        google_contact_dict['occupations'] = [
            {
                'value': contact_view_select_result_dict['job_title'],
            }
        ]
        # TODO: use also contact_location for this?
        google_contact_dict['addresses'] = [
            {
                'streetAddress': contact_view_select_result_dict['address1_street'],
                'city': contact_view_select_result_dict['address1_city'],
                'region': contact_view_select_result_dict['address1_state'],    # This is the state in Google Contact
                'postalCode': contact_view_select_result_dict['address1_postal_code'],
                'country': contact_view_select_result_dict['address1_country'],
            },
            {
                'streetAddress': contact_view_select_result_dict['address2_street'],
                'city': contact_view_select_result_dict['address2_city'],
                'region': contact_view_select_result_dict['address2_state'],    # This is the state in Google Contact
                'postalCode': contact_view_select_result_dict['address2_postal_code'],
                'country': contact_view_select_result_dict['address2_country'],
            }
        ]
        google_contact_dict['birthdays'] = [
            {
                # 'date': contact_view_select_result_dict['birthday'], # TODO: we will have to convert it to date format
                'text': contact_view_select_result_dict['birthday'],
            }
        ]
        # TODO: if necessary get it also from url table
        google_contact_dict['urls'] = [
            {
                'value': contact_view_select_result_dict['website1'],
            },
            {
                'value': contact_view_select_result_dict['website2'],
            },
            {
                'value': contact_view_select_result_dict['website3'],
            }
        ]
        google_contact_dict['biographies'] = [
            {
                'value': contact_view_select_result_dict['notes'],
            }
        ]
