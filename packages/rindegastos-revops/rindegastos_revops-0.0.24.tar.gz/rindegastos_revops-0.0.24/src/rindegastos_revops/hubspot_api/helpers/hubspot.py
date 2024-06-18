from enum import Enum

class Endpoints(Enum):
    """
    ### Endpoints Objetos
    Endpoints para extracción de registros de Objetos en Hubspot ver siguiente URL 
    [View a model of your CRM object and activity relationships](https://knowledge.hubspot.com/data-management/view-a-model-of-your-crm-object-and-activity-relationships)

    #### Objetos del CRM
    * Contacts
    * Companies
    * Tickets

    ### Objetos de Personalizados
    * Holdings (No requerido)
    
    ### Objetos de Ventas
    * Cotizaciones (No requerido)
    * Elementos de Pedido (No requerido)
    * Leads [No disponible mediante API](https://community.hubspot.com/t5/APIs-Integrations/Leads-Object-API/m-p/955434#M72538)
    * Deals

    ### Actividades
    * Postal mail (No requerido)
    * Emails
    * Linkedin Messages (No requerido)
    * Calls
    * Notas
    * Meetings
    * SMS (No requerido)
    * Tasks
    * WhatsApp Messages (No requerido)

    # Lista
    /crm/v3/lists/

    """

    ### Objetos del CRM ###
    # Contacts
    CONTACTS = "objects/contacts"
    CONTACTS_SEARCH = "objects/contacts/search"
    # Companies
    COMPANIES = "objects/companies"
    COMPANIES_SEARCH = "objects/companies/search"
    # Tickets
    TICKETS = "objects/tickets"
    TICKETS_SEARCH = "objects/tickets/search"

    ### Objetos de Ventas ###
    # Deals
    DEALS = "objects/deals"
    DEALS_SEARCH = "objects/deals/search"

    ### Actividades ###
    # Calls
    CALLS = "objects/calls"
    CALLS_SEARCH = "objects/calls/search"
    # Tasks
    TASKS = "objects/tasks"
    TASKS_SEARCH = "objects/tasks/search"
    # Emails
    EMAILS= "objects/emails"
    EMAILS_SEARCH = "objects/emails/search"
    # Meetings
    MEETINGS = "objects/meetings"
    MEETINGS_SEARCH = "objects/meetings/search"
    # Notes
    NOTES = "objects/notes"
    NOTES_SEARCH = "objects/notes/search"

    # Users
    USERS = "objects/users"

    # Extraer Propiedades de los Objetos
    PROPERTIES_CONTACTS = "properties/contacts"
    PROPERTIES_COMPANIES = "properties/companies"
    PROPERTIES_TICKETS = "properties/tickets"
    PROPERTIES_DEALS = "properties/deals"
    PROPERTIES_CALLS = "properties/calls"
    PROPERTIES_TASKS = "properties/tasks"
    PROPERTIES_EMAILS = "properties/emails"
    PROPERTIES_MEETINGS = "properties/meetings"
    PROPERTIES_NOTES = "properties/notes"
    PROPERTIES_USERS = "properties/users"

    # Lists
    LISTS = "lists"

    # Owners
    OWNERS = "owners/"

class ObjectTypeId(Enum):
    CONTACTS = "0-1"
    COMPANIES = "0-2"
    DEALS = "0-3"
    TICKETS = "0-5"
    CALLS = "0-48"
    EMAILS = "0-49"
    MEETINGS = "0-47"
    NOTES = "0-4"
    TASKS = "0-27"
    
class HubspotConnectorApi:
    def __init__(self, hubspot_api_key):
        self.base_url = "https://api.hubapi.com/crm/v3"

        self.headers = {
            'accept': "application/json",
            'content-type': "application/json",
            'authorization': f"Bearer {hubspot_api_key}"
        }
    def endpoint(self, endpoint:Endpoints):
        return f"{self.base_url}/{endpoint.value}"
