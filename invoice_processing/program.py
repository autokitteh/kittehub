"""Invoice processing system module."""

from datetime import datetime, UTC
import os
import time

import autokitteh

import process_gmails


def main(event):
    """Main entry point for the invoice processing system"""
    invoices = []

    polling_interval = int(os.getenv("POLLING_INTERVAL_MINUTES", "60")) * 60

    start_date = os.getenv("START_DATE")
    if start_date is None:
        start_date = datetime.now(UTC).replace(day=1)
        start_date = start_date.strftime("%Y-%m-%d")

    last_check_time = int(time.mktime(time.strptime(start_date, "%Y-%m-%d")))

    # Subscribe to send_mail events.
    send_mail_webhook = autokitteh.subscribe("send_mail", "true")

    # Initial scan.
    new_invoices = process_gmails.handle_scan(last_check_time)
    invoices.extend(new_invoices)
    last_check_time = int(time.time())

    while True:
        # Wait for send_mail event or timeout.
        send_mail_req = autokitteh.next_event(
            send_mail_webhook, timeout=polling_interval
        )

        if send_mail_req:
            # Send invoice report on demand.
            print("Received send_mail event - sending invoice report")
            process_gmails.send_invoices(invoices)
        else:
            # Check for new invoices.
            new_invoices = process_gmails.handle_scan(last_check_time)

            if new_invoices:
                print(f"Found {len(new_invoices)} new invoices")
                invoices.extend(new_invoices)
            else:
                print("No new invoices found")

            last_check_time = int(time.time())
