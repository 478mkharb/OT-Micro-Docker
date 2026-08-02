import os
import time
import requests
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from elasticsearch import Elasticsearch

# ==================================================
# Configuration
# ==================================================

SCYLLA_HOST = os.getenv("SCYLLA_HOST", "scylladb")
SCYLLA_PORT = int(os.getenv("SCYLLA_PORT", "9042"))
SCYLLA_USER = os.getenv("SCYLLA_USERNAME", "scylladb")
SCYLLA_PASS = os.getenv("SCYLLA_PASSWORD", "password")
SCYLLA_KEYSPACE = os.getenv("SCYLLA_KEYSPACE", "employee_db")

ES_HOST = os.getenv("ES_HOST", "http://elasticsearch:9200")
ES_INDEX = os.getenv("ES_INDEX", "employee_index")

NOTIFICATION_URL = os.getenv(
    "NOTIFICATION_URL",
    "http://notification-api:8085/api/v1/notification/send/all"
)

SYNC_INTERVAL = int(os.getenv("SYNC_INTERVAL", "5"))

# ==================================================
# Wait for ScyllaDB
# ==================================================

print("Waiting for ScyllaDB...")

while True:
    try:
        auth_provider = PlainTextAuthProvider(
            username=SCYLLA_USER,
            password=SCYLLA_PASS
        )

        cluster = Cluster(
            [SCYLLA_HOST],
            port=SCYLLA_PORT,
            auth_provider=auth_provider
        )

        session = cluster.connect(SCYLLA_KEYSPACE)

        print("Connected to ScyllaDB")
        break

    except Exception as e:
        print(f"ScyllaDB not ready: {e}")
        time.sleep(5)

# ==================================================
# Wait for Elasticsearch
# ==================================================

print("Waiting for Elasticsearch...")

while True:

    try:

        es = Elasticsearch(ES_HOST)

        if es.ping():
            print("Connected to Elasticsearch")
            break

    except Exception as e:
        print(f"Elasticsearch not ready: {e}")

    time.sleep(5)

print("==================================================")
print("ScyllaDB → Elasticsearch Sync Started")
print("==================================================")


# ==================================================
# Sync Function
# ==================================================

def sync_data():

    try:

        salary_rows = session.execute(
            """
            SELECT id,
                   process_date,
                   name,
                   salary,
                   status
            FROM employee_salary
            """
        )

        synced = 0

        for salary in salary_rows:

            employee = session.execute(
                """
                SELECT id,
                       name,
                       email,
                       designation
                FROM employee_info
                WHERE id=%s
                """,
                [salary.id]
            ).one()

            if employee is None:

                print(f"Employee {salary.id} not found.")
                continue

            if es.exists(index=ES_INDEX, id=employee.email):

                continue

            document = {
                "employee_id": employee.id,
                "name": employee.name,
                "email_id": employee.email,
                "designation": employee.designation,
                "salary": salary.salary,
                "process_date": str(salary.process_date),
                "status": salary.status,
                "notified": False
            }

            es.index(
                index=ES_INDEX,
                id=employee.email,
                document=document,
                refresh=True
            )

            synced += 1

            print(f"Indexed Employee : {employee.name}")

        if synced > 0:

            print(f"{synced} employee(s) indexed.")

            try:

                response = requests.post(
                    NOTIFICATION_URL,
                    timeout=30
                )

                print(
                    f"Notification API Response : "
                    f"{response.status_code}"
                )

            except Exception as exc:

                print(f"Notification API Error : {exc}")

        else:

            print("No new records to synchronize.")

    except Exception as exc:

        print(f"Synchronization Error : {exc}")


# ==================================================
# Main Loop
# ==================================================

if __name__ == "__main__":

    while True:

        sync_data()

        time.sleep(SYNC_INTERVAL)