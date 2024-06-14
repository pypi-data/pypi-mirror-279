#%%
import logging  
import os 
import smtplib  
from email.mime.text import MIMEText  
from email.mime.multipart import MIMEMultipart  
from logging.handlers import BufferingHandler  

# Define a custom logging handler that buffers log records and sends them via email
class EmailBufferingHandler(BufferingHandler):
    # Initialize the handler with email configuration and buffering capacity
    def __init__(self, capacity, fromaddr, toaddr, subject, smtp_server, smtp_port, login, password):
        super().__init__(capacity)  # Initialize the base class with the capacity
        self.fromaddr = fromaddr  
        self.toaddr = toaddr  
        self.subject = subject  
        self.smtp_server = smtp_server  
        self.smtp_port = smtp_port  
        self.login = login  
        self.password = password  
        self.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))  # Set the log format

    # Flush the buffer and send the buffered log records via email
    def flush(self):
        if self.buffer:  # Check if there are any log records in the buffer
            try:
                body = '\n'.join(self.format(record) for record in self.buffer)  # Format the log records
                self._send_email(body)  # Send the formatted log records via email
            except Exception as e:
                self.handleError(None)  
            self.buffer = []  # Clear the buffer after sending

    # Send an email with the specified body content
    def _send_email(self, body):
        msg = MIMEMultipart()  
        msg['From'] = self.fromaddr  
        msg['To'] = self.toaddr  
        msg['Subject'] = self.subject  

        msg.attach(MIMEText(body, 'plain'))  # Attach the log records as plain text to the email
        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:  
            server.starttls() 
            server.login(self.login, self.password)  
            server.sendmail(self.fromaddr, self.toaddr.split(','), msg.as_string()) 

# Configure logging with options for console, file, and email logging
def configure_logging(log_console=True, console_level=logging.DEBUG,
                      log_file=True, log_folder='logs', log_file_name='log.log', file_level=logging.DEBUG,
                      log_email=False, email_level=logging.DEBUG, email_config=None):
    logger = logging.getLogger()  
    logger.setLevel(logging.DEBUG)  

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')  

    if log_console: 
        console_handler = logging.StreamHandler()  
        console_handler.setLevel(console_level)  
        console_handler.setFormatter(formatter) 
        logger.addHandler(console_handler)  

    if log_file:  
        # Check if the log folder exists, create it if not
        if not os.path.exists(log_folder):  
            os.makedirs(log_folder)  
        file_handler = logging.FileHandler(os.path.join(log_folder, log_file_name))  
        file_handler.setLevel(file_level) 
        file_handler.setFormatter(formatter)  
        logger.addHandler(file_handler)  

    if log_email and email_config:  
        email_handler = EmailBufferingHandler(
            capacity=email_config.get('capacity', 1000),  
            fromaddr=email_config['fromaddr'], 
            toaddr=email_config['toaddr'],  
            subject=email_config['subject'],  
            smtp_server=email_config.get('smtp_server', 'smtp.gmail.com'),  
            smtp_port=email_config.get('smtp_port', 587),  
            login=email_config['login'],  
            password=email_config['password']  
        )
        email_handler.setLevel(email_level)  
        logger.addHandler(email_handler)  

    return logger  

# Send the buffered log records via email
def send_log_over_email(logger_obj, fromaddr, toaddr, subject, body=''):
    for handler in logger_obj.handlers:  
        if isinstance(handler, EmailBufferingHandler):  
            handler.subject = subject 
            handler.flush()  # Flush the buffer and send the email