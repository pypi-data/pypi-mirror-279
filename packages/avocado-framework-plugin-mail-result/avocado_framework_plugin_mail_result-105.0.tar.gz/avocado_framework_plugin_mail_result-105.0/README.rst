Avocado Job Notification Mail Plugin
====================================

The Avocado Job Notification plugin enables you to receive email notifications for job start and completion events within the Avocado testing framework.

*Currently Only Supports Gmail*

Installation
------------

To install the Mail Results plugin from pip, use:

.. code-block:: bash

   $ pip install avocado-framework-plugin-mail

Configuration
-------------

To use the Avocado Job Notification plugin, you need to configure it in the Avocado settings file
(`avocado.conf` - located at /etc/avocado/ if not present you can create the file.).
Below is an example configuration:

.. code-block:: ini

   [plugins.mail]

   # The email address to which job notification emails will be sent.
   recipient = avocado@local.com

   # The subject header for the job notification emails.
   header = [AVOCADO JOB NOTIFICATION]

   # The email address from which the job notification emails will be sent.
   sender = avocado@local.com

   # The SMTP server address for sending the emails.
   server = smtp.gmail.com

   # The SMTP server port for sending the emails.
   port = 587

   # The application-specific password for the sender email address.
   password = abcd efgh ijkl mnop

   # The detail level of the email content.
   # Set to false for a summary with essential details or true for detailed information about each failed test.
   detail_level = false

Usage
-----

Once configured, the Avocado Job Notification plugin will automatically send email notifications for job start and completion events based on the specified settings.

Obtaining an App Password for Gmail
-----------------------------------

Please follow these steps to generate an App Password:

Create & use app passwords

Important: To create an app password, you need 2-Step Verification on your Google Account.

#. Go to your Google Account.
#. Select Security.
#. Under "How you sign in to Google," select 2-Step Verification.
#. At the bottom of the page, select App passwords.
#. Enter a name that helps you remember where you’ll use the app password.
#. Select Generate.
#. To enter the app password, follow the instructions on your screen. The app password is the 16-character code that generates on your device.
#. Select Done.

Enter the App Password inside of the avocado configuration file.

Remember to keep this App Password secure and don't share it with anyone. If you suspect it has been compromised, you can always revoke it and generate a new one.
