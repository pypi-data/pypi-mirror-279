# rwend-tools
A collection of helper functions designed to consolidate some useful utilities I often use, and to gain experience with publishing packages. This package includes various functions for common tasks such as data manipulation, file handling, logging and more.
## Installation Instructions
```bash
pip install rwend_tools
```
## Package Structure
```bash
.
├── rwend_tools
│   ├── custom_logging.py
│   ├── google_helpers.py
│   └── utils.py
```

## Usage Guide
### 1. custom_logging
  - This module helps create custom logging and email notifications
  - Prerequisites:
    - gmail_app_pwd needs to be set/defined as an environmental variable. This should be an app password you obtain from google if you want to use the email functionality of this module. Without this you can still use this to create log files but won't be able to send log files over email.
  - Usage:
    ```python
    import rwend_tools.utils as ru
    import rwend_tools.google_helpers as rg
    from rwend_tools.custom_logging import set_logging, send_log_over_email
    
    log_email = 'user.email@gmail.com'
    process_id = '001'
    process_name = 'Test'

    subject_success = f'Success -- {process_id} -- {process_name} Ran'
    subject_error   = f'Error -- {process_id} -- {process_name} Failed'
    
    logger = set_logging(log_console=False, log_email=True)
    logger.info('Test')
    
    try:
        logger.info(f'First line of logging')
        logger.info(f'Second line of logging')
        logger.info(f'Third line of logging')
    
        send_log_over_email(
            logger,
            fromaddr=log_email,
            toaddr=log_email,
            subject=subject_success
        )
    except Exception as e:
        logger.info(f'Process failed with error: {e}')
        send_log_over_email(
            logger,
            fromaddr=log_email,
            toaddr=log_email,
            subject=subject_error
        )
    ```
