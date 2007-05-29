from trac.core import *
from trac.web.api import IRequestFilter
from trac.web.chrome import ITemplateProvider, add_stylesheet, add_script
from trac.ticket.api import ITicketManipulator
from trac.ticket.model import Ticket

from pkg_resources import resource_filename

class TicketProxy:
  def __init__(self, dupe_id, ticket):
    self._dupe_id = dupe_id
    self._ticket = ticket
    ticket._proxy_old_save = ticket.save_changes
    ticket.save_changes = self.save_changes
  
  def save_changes(self, author, comment, when=0, db=None, cnum=''):
    dupeticket = Ticket(self._ticket.env, self._dupe_id, db=db)
    dupeticket.save_changes(
      author,
      "*** Ticket #%d marked duplicate of this one ***" % self._ticket.id,
      when=when,
      db=db
      )
    if not comment or not len(comment.strip()):
      comment = ""
    else:
      comment += "\n\n"
    comment += "*** Marked duplicate of #%d ***" % self._dupe_id
    return self._ticket._proxy_old_save(author, comment, when=when, db=db, cnum=cnum)    

class DuplicatesModule(Component):
  implements(IRequestFilter, ITemplateProvider, ITicketManipulator)
  
  # IRequestFilter methods
  def pre_process_request(self, req, handler):
    if not req.path_info.startswith('/ticket/') or not req.method == 'POST':
      return handler

    if not req.args.has_key('preview'):
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
    return template, content_type
    
  # ITemplateProvider
  def get_htdocs_dirs(self):
    return []
  
  def get_templates_dirs(self):
    return [resource_filename(__name__, 'templates')]
  
  # ITicketManipulator
  def prepare_ticket(self, req, ticket, fields, actions):
    return handler
  
  def validate_ticket(self, req, ticket):
    """ Somewhat hacky; what if we later fail... Anyway :p """
  
    if req.args.get('is_duped'):
      db = self.env.get_db_cnx()
      comment = req.args.get('comment')
      try:
        dupeid = int(req.args.get('duplicate_id'))
        Ticket(self.env, dupeid, db=db)
        TicketProxy(dupeid, ticket)
      except (ValueError, TypeError, TracError):
        yield None, "Invalid Duplicate Ticket Id"
