from trac.core import *
from trac.web.api import IRequestFilter
from trac.web.chrome import ITemplateProvider, add_stylesheet, add_script
from trac.ticket.api import ITicketManipulator

from pkg_resources import resource_filename

class DuplicatesModule(Component):
  implements(IRequestFilter, ITemplateProvider, ITicketManipulator)
  
  # IRequestFilter methods
  def pre_process_request(self, req, handler):
    if req.path_info.startswith('/ticket/') and req.method == 'POST' and req.args.has_key('preview'):
      if req.args.get('accept') == 'dupe':
        req.args['accept'] = 'resolve'
        req.args['resolve_resolution'] = 'duplicate'


    return handler
      
  def post_process_request(self, req, template, content_type):
    if template == 'ticket.cs':
      template = 'duplicates/ticket.cs'
    return template, content_type
    
  # ITemplateProvider
  def get_htdocs_dirs(self):
    return [('duplicates', resource_filename(__name__, 'htdocs'))]
  
  def get_templates_dirs(self):
    return [('duplicates', resource_filename(__name__, 'templates'))]
  
  # ITicketManipulator
  def prepare_ticket(self, req, ticket, fields, actions):
    return handler
  
  def validate_ticket(self, req, ticket):
    if req.args.get('accept') == 'dupe':
      pass
