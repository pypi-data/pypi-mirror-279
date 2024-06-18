import json
import os
import smtplib
import time
from email.mime.text import MIMEText

from avocado.core.output import LOG_UI
from avocado.core.plugin_interfaces import Init, JobPost, JobPre
from avocado.core.settings import settings


class MailInit(Init):
    name = "mail-init"
    description = "Mail plugin initialization"

    def initialize(self):
        help_msg = "Mail recipient."
        settings.register_option(
            section="plugins.mail",
            key="recipient",
            default="root@localhost.localdomain",
            help_msg=help_msg,
        )

        help_msg = "Mail header."
        settings.register_option(
            section="plugins.mail",
            key="header",
            default="[AVOCADO JOB NOTIFICATION]",
            help_msg=help_msg,
        )

        help_msg = "Mail sender."
        settings.register_option(
            section="plugins.mail",
            key="sender",
            default="avocado@localhost.localdomain",
            help_msg=help_msg,
        )

        help_msg = "Mail server."
        settings.register_option(
            section="plugins.mail",
            key="server",
            default="localhost",
            help_msg=help_msg,
        )

        help_msg = "Mail server port."
        settings.register_option(
            section="plugins.mail",
            key="port",
            default=587,
            help_msg=help_msg,
        )

        help_msg = "Mail server Application Password."
        settings.register_option(
            section="plugins.mail",
            key="password",
            default="",
            help_msg=help_msg,
        )

        help_msg = "Email detail level."
        settings.register_option(
            section="plugins.mail",
            key="detail_level",
            default=False,
            help_msg=help_msg,
            key_type=bool,
        )


class Mail(JobPre, JobPost):
    name = "mail"
    description = "Sends mail to notify on job start/end"

    @staticmethod
    def _get_smtp_config(job):
        return (
            job.config.get("plugins.mail.server"),
            job.config.get("plugins.mail.port"),
            job.config.get("plugins.mail.sender"),
            job.config.get("plugins.mail.password", ""),
        )

    @staticmethod
    def _build_message(job, time_content, phase, finishedtime="", test_summary=""):
        if phase == "Post":
            body = f"""
            <html>
                <body>
                    <h2>Job Notification - Job {job.unique_id}</h2>
                    <p><strong>Job Total Time:</strong> {time_content}</p>
                    <p><strong>Job Finished At:</strong> {finishedtime}</p>
                    <p><strong>Results:</strong></p>
                    <ul>
                        <li>PASS: {job.result.passed}</li>
                        <li>ERROR: {job.result.errors}</li>
                        <li>FAIL: {job.result.failed}</li>
                        <li>SKIP: {job.result.skipped}</li>
                        <li>WARN: {job.result.warned}</li>
                        <li>INTERRUPT: {job.result.interrupted}</li>
                        <li>CANCEL: {job.result.cancelled}</li>
                    </ul>
                    <p><strong>Test Summary:</strong></p>
                    <pre>{test_summary}</pre>
                </body>
            </html>
            """
            msg = MIMEText(body, "html")
            msg["Subject"] = (
                f"{job.config.get('plugins.mail.header')} Job {job.unique_id} - Status: Job Completed"
            )
        else:
            body = f"""
            <html>
                <body>
                    <h2>Job Notification - Job {job.unique_id}</h2>
                    <p><strong>Job Started At:</strong> {time_content}</p>
                </body>
            </html>
            """
            msg = MIMEText(body, "html")
            msg["Subject"] = (
                f"{job.config.get('plugins.mail.header')} Job {job.unique_id} - Status: Job Started"
            )
        msg["From"] = job.config.get("plugins.mail.sender")
        msg["To"] = job.config.get("plugins.mail.recipient")
        return msg

    @staticmethod
    def _send_email(smtp, sender, rcpt, msg):
        try:
            smtp.sendmail(sender, [rcpt], msg.as_string())
            LOG_UI.info("EMAIL SENT TO: %s", rcpt)
        except Exception as e:  # pylint: disable=W0703
            LOG_UI.error(f"Failure to send email notification to {rcpt}: {e}")

    @staticmethod
    def _create_smtp_connection(server, port):
        try:
            smtp = smtplib.SMTP(server, port)
            smtp.starttls()  # Enable TLS
            return smtp
        except Exception as e:  # pylint: disable=W0703
            LOG_UI.error(f"Failed to establish SMTP connection to {server}:{port}: {e}")
            return None

    @staticmethod
    def _read_results_file(results_path):
        try:
            with open(results_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            LOG_UI.error("Test summary file not found at %s.", results_path)
        except json.JSONDecodeError:
            LOG_UI.error("Error decoding JSON from file %s.", results_path)
        except Exception as e:
            LOG_UI.error("Unexpected error while reading test summary: %s", str(e))
        return None

    @staticmethod
    def _format_test_details(test, advanced=False):
        if advanced:
            details = [
                f"<strong>Name:</strong> {test.get('name', '')}<br>",
                f"<strong>Status:</strong> {test.get('status', '')}<br>",
                f"<strong>Fail Reason:</strong> {test.get('fail_reason', '')}<br>",
                f"<strong>Actual Time Start:</strong> {test.get('actual_time_start', '')}<br>",
                f"<strong>Actual Time End:</strong> {test.get('actual_time_end', '')}<br>",
                f"<strong>ID:</strong> {test.get('id', '')}<br>",
                f"<strong>Log Directory:</strong> {test.get('logdir', '')}<br>",
                f"<strong>Log File:</strong> {test.get('logfile', '')}<br>",
                f"<strong>Time Elapsed:</strong> {test.get('time_elapsed', '')}<br>",
                f"<strong>Time Start:</strong> {test.get('time_start', '')}<br>",
                f"<strong>Time End:</strong> {test.get('time_end', '')}<br>",
                f"<strong>Tags:</strong> {test.get('tags', '')}<br>",
                f"<strong>Whiteboard:</strong> {test.get('whiteboard', '')}<br>",
            ]
        else:
            details = [
                f"<strong>Name:</strong> {test.get('name', '')}<br>",
                f"<strong>Fail Reason:</strong> {test.get('fail_reason', '')}<br>",
            ]
        return "".join(details)

    @staticmethod
    def _generate_test_summary(data, detail_level):
        test_summary = []

        def format_test_details(test):
            return Mail._format_test_details(test, advanced=detail_level)

        for test in data.get("tests", []):
            if test.get("status") == "FAIL":
                test_summary.append(format_test_details(test))

        return "\n\n".join(test_summary)

    @staticmethod
    def _get_test_summary(job):
        results_path = os.path.join(job.logdir, "results.json")
        data = Mail._read_results_file(results_path)
        if not data:
            return ""

        detail_level = job.config.get("plugins.mail.detail_level")
        return Mail._generate_test_summary(data, detail_level)

    def send_start_email(self, job):
        phase = "Start"
        server, port, sender, password = Mail._get_smtp_config(job)
        smtp = Mail._create_smtp_connection(server, port)
        if smtp:
            try:
                smtp.login(sender, password)
            except Exception as e:  # pylint: disable=W0703
                LOG_UI.error(f"SMTP login failed: {e}")
                return
            start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            time_content = f"{start_time}"

            msg = Mail._build_message(job, time_content, phase)
            Mail._send_email(
                smtp, sender, job.config.get("plugins.mail.recipient"), msg
            )
            smtp.quit()

    def pre(self, job):
        self.send_start_email(job)

    def post(self, job):
        phase = "Post"
        server, port, sender, password = Mail._get_smtp_config(job)
        smtp = Mail._create_smtp_connection(server, port)
        if smtp:
            try:
                smtp.login(sender, password)
            except Exception as e:  # pylint: disable=W0703
                LOG_UI.error(f"SMTP login failed: {e}")
                return
            time_elapsed_formatted = f"{job.time_elapsed:.2f}"
            time_content = f"{time_elapsed_formatted} Seconds"
            current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            finishedtime = f"{current_time}"

            test_summary = Mail._get_test_summary(job)

            msg = Mail._build_message(
                job, time_content, phase, finishedtime, test_summary
            )
            Mail._send_email(
                smtp, sender, job.config.get("plugins.mail.recipient"), msg
            )
            smtp.quit()
