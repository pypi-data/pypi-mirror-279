#!/usr/bin/env python

from operator import itemgetter

########################################################################################################################


def get_html_table(header, rows):
    html_table = f"""<table bordercolor='black' border='2'>
    <thead>
    <tr style='background-color : Teal; color: White'>
"""
    for h in header:
        html_table += f"""        <th>{h}</th>
"""

    html_table += f"""    </tr>
    </thead>
    <tbody>
{rows}    </tbody>
</table>
"""
    return html_table


def get_html_row(row):
    html_row = f"    <tr>"
    for item in row:
        html_row += f"""
        <td>{item}</td>"""
    html_row += """
    </tr>"""
    if row:
        return html_row


class Report(object):
    def __init__(self, certs, warning, critical,
                 ok_symbol=":white_check_mark:",
                 warning_symbol=":warning:",
                 critical_symbol=":bangbang:",
                 error_symbol=":no_entry:",
                 expired_symbol=":rotating_light:",
                 unknown_symbol=":question:",
                 ok_txt="OK",
                 warning_txt="Warning",
                 critical_txt="CRITICAL",
                 error_txt="Error!",
                 expired_txt="EXPIRED!!",
                 unknown_txt="Unknown",
                 title="SSL certificates report",
                 html_header=None,
                skip_ok = False):

        if html_header is None:
            html_header = ["Status", "SSL Cert", "Message", "Expiration date"]

        self.certs = certs
        self.warning = warning
        self.critical = critical

        self.ok_symbol = ok_symbol
        self.warning_symbol = warning_symbol
        self.critical_symbol = critical_symbol
        self.error_symbol = error_symbol
        self.expired_symbol = expired_symbol
        self.unknown_symbol = unknown_symbol

        self.ok_txt = ok_txt
        self.warning_txt = warning_txt
        self.critical_txt = critical_txt
        self.error_txt = error_txt
        self.expired_txt = expired_txt
        self.unknown_txt = unknown_txt

        self.ok_code = 0
        self.warning_code = 1
        self.critical_code = 2
        self.error_code = 3
        self.expired_code = 4
        self.unknown_code = 5

        self.title = title
        self.html_header = html_header
        self.skip_ok = skip_ok

        self.report = []
        self.report_json = []
        self.html_rows = []
        self.slack_rows = []

    def gen_report(self):
        for c in self.certs:
            name = c.get("name")
            expire_date = c.get("notAfter")
            days = c.get("expire_age")
            error_message = c.get("error_message")
            crt = {"name": name,
                   "expire_date": expire_date,
                   "expire_age": days,
                   "comment": error_message,
                   "status": self.unknown_txt,
                   "code": self.unknown_code
                   }

            if error_message:
                expire_date = "-"
                slack_row = f"{self.error_symbol} *{name}* - {error_message}"
                html_row = [self.error_txt, name, error_message, expire_date]
                crt["status"] = self.error_txt
                crt["code"] = self.error_code

            elif not error_message and isinstance(days, int) and days < 0:
                comment = f"Will expire in {abs(days)} days"
                slack_row = f"*{name}* - {comment} ({expire_date})."
                html_row = [name, comment, expire_date]
                crt["comment"] = comment

                if abs(days) <= self.critical:
                    slack_row = f"{self.critical_symbol} {slack_row}"
                    html_row = [self.critical_txt] + html_row
                    crt["status"] = self.critical_txt
                    crt["code"] = self.critical_code
                elif self.warning >= abs(days) > self.critical:
                    slack_row = f"{self.warning_symbol} {slack_row}"
                    html_row = [self.warning_txt] + html_row
                    crt["status"] = self.warning_txt
                    crt["code"] = self.warning_code
                elif self.skip_ok:
                    continue
                else:
                    html_row = [self.ok_txt] + html_row
                    slack_row = f"{self.ok_symbol} {slack_row}"
                    crt["status"] = self.ok_txt
                    crt["code"] = self.ok_code

            elif not error_message and isinstance(days, int) and days >= 0:
                comment = f"Has already expired. Expired {abs(days)} days ago."
                slack_row = f"{self.expired_symbol} *{name}* - {comment} ({expire_date})."
                html_row = [self.expired_txt, name, comment, expire_date]
                crt["comment"] = comment
                crt["status"] = self.critical_txt
                crt["code"] = self.critical_code
            else:
                comment = f"Unknown state for cert **{name}**."
                slack_row = f"{self.unknown_symbol} - *{name}* - {comment} ({expire_date})."
                html_row = [self.unknown_txt, name, comment, "-"]
                crt["comment"] = comment
                crt["status"] = self.unknown_txt
                crt["code"] = self.unknown_code

            code = crt.get("code")

            if html_row:
                html_syntax = get_html_row(html_row)
                self.html_rows.append([code, days, html_syntax])

            if slack_row:
                self.slack_rows.append([code, days, slack_row])

            self.report_json.append(crt)

    def get_slack_report(self):
        rows = ""
        for row in sorted(self.slack_rows, key=itemgetter(0, 1, 2), reverse=True):
            rows += f"{row[-1]}\n"

        if rows:
            return f"*{self.title}*\n{rows}"

    def get_html_report(self):
        rows = ""
        for row in sorted(self.html_rows, key=itemgetter(0, 1, 2), reverse=True):
            rows += f"{row[-1]}\n"

        if rows:
            return self.title, get_html_table(self.html_header, rows)

        return None, None

    def get_report_json(self):
        return self.report_json
