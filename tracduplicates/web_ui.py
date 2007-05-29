from time import time

from trac.core import *
from trac.web.api import IRequestFilter
from trac.web.chrome import ITemplateProvider, add_stylesheet, add_script
from trac.ticket.api import ITicketManipulator
from trac.ticket.model import Ticket
from trac.util import get_reporter_id

from pkg_resources import resource_filename

class DuplicatesModule(Component):
  implements(IRequestFilter, ITemplateProvider, ITicketManipulator)
  
  # IRequestFilter methods
  def pre_process_request(self, req, handler):
    if req.path_info.startswith('/ticket/') and req.method == 'POST' and not req.args.has_key('preview'):
      if req.args.get('action') == 'duplicate':
        req.args['action'] = 'resolve'
        req.args['resolve_resolution'] = 'duplicate'
        req.args['is_duped'] = True
      else:
        req.args['is_duped'] = False

    return handler
      
  def post_process_request(self, req, template, content_type):
    if template == 'ticket.cs':
      template = 'duplicates_ticket.cs'
      add_script(req, 'duplicates/duplicates.js')
      if req.hdf.get('ticket.actions.resolve'):
        req.hdf['ticket.actions.duplicate'] = 1
        if req.args.get('duplicate_id'):
          req.hdf['ticket.duplicate_id'] = req.args.get('duplicate_id')
        req.hdf.pop('ticket.fields.resolution.options.duplicate')
        
    return template, content_type
    
  # ITemplateProvider
  def get_htdocs_dirs(self):
    return [('duplicates', resource_filename(__name__, 'htdocs'))]
  
  def get_templates_dirs(self):
    return [resource_filename(__name__, 'templates')]
  
  # ITicketManipulator
  def prepare_ticket(self, req, ticket, fields, actions):
    return handler
  
  def validate_ticket(self, req, ticket):
    """ Somewhat hacky; what if we later fail... Anyway :p """
    if req.args.get('is_duped'):
      now = int(time())
      db = self.env.get_db_cnx()
      comment = req.args.get('comment')
      try:
        dupeid = int(req.args.get('duplicate_id'))
        dupeticket = Ticket(self.env, dupeid, db=db)
        dupeticket.save_changes(
          get_reporter_id(req, 'author'),
          "*** Ticket #%d marked duplicate of this one ***" % dupeid,
          when=now,
          db=db
          )
        if not comment or not len(comment.strip()):
          comment = ""
        else:
          comment += "\n\n"
        comment += "*** Marked duplicate of #%d ***" % dupeid
        req.args['comment'] = comment
      except (ValueError, TypeError, TracError):
        yield None, "Invalid Duplicate Ticket Id"
      
