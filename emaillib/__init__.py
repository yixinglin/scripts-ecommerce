from common import SmtpEmail, EmailApplication
from common import customer_list_to_send, setup_logger, load_yaml
from email.message import Message
from pylib.ioutils import current_date, current_time, base64encode_urlsafe, base64decode_urlsafe
