from trac.core import *
from trac.web.api import IRequestFilter
from trac.web.chrome import ITemplateProvider, add_stylesheet, add_script
from trac.ticket.api import ITicketManipulator

from pkg_resources import resource_filename

class DuplicatesModule(Component):
  implements(IRequestFilter, ITemplateProvider, ITickerManipulator)
  
  # IRequestFilter methods
  def pre_process_request(self, req, handler):
      return handler
      
  def post_process_request(self, req, template, content_type):
    raise TracError(Error)
    return template, content_type
    
  # ITemplateProvider
  def get_htdocs_dirs():
    return [('duplicates', resource_filename(__name__, 'htdocs'))]
  
  def get_template_dirs():
    return [('duplicates', resource_filename(__name__, 'templates'))]
  
  # ITicketManipulator
  def prepare_ticket(self, req, ticket, fields, actions):
    return handler
  
  def validate_ticket(self, req, ticket):
    pass