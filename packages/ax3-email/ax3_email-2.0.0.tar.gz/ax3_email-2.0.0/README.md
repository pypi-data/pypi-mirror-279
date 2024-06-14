# AX3 Email

AX3 Email is a Django application designed to send emails using Huey tasks.

## Installation

You can easily install AX3 Email from the PyPI package using the following command:

```bash
pip install ax3-email
```

After the package is installed, you need to configure your project settings. Specifically, you need to add `ax3_email` to your `INSTALLED_APPS`:

```python
INSTALLED_APPS += ['ax3_email']
```

## Configuration

Next, you need to add the email backend settings. Here's how you can do it:

```python
# app/settings.py
EMAIL_BACKEND = 'ax3_email.backends.AX3EmailBackend'
```

You can also specify additional settings for AX3 Email:

```python
# app/settings.py
AX3_EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend' # Optional - Default is smtp (django). This is the Django Email that actually sends the emails.
AX3_EMAIL_RETRIES  # Optional - Default is 3. This is the maximum number of times to retry sending an email.
AX3_EMAIL_DELAY # Optional - Default is 600. This is the time in seconds between attempts to send an email.
AX3_EMAIL_BACKUP_LIST # Optional - This is a list of emails to send a BCC backup copy of each email.
AX3_ONLY_BACKUP_LIST # Optional - If set to True, emails will only be sent to the backup list.
EMAIL_SUBJECT # Optional - This is a string format for all email subjects. For example, you can use '[ax3_prefix] {} ' as a prefix.
```

## Publish package

To build the package, you need to run the following command:

```bash
rye build && rye publish

```
