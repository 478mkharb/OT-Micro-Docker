FROM scylladb/scylla:6.1

LABEL authors="Opstree Solution" \
      application="Scylla Init" \
      version="v0.1.0"

WORKDIR /

COPY init.cql /init.cql
COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]