FROM grafana/grafana:11.2.0

# Copy the exported dashboard JSON file
COPY fraud_detection_dashboard.json /var/lib/grafana/dashboards/

# Copy the datasource configuration file
COPY datasource.yaml /etc/grafana/provisioning/datasources/

# Copy the dashboard provisioning configuration
COPY dashboard-provider.yaml /etc/grafana/provisioning/dashboards/

# Switch to root to set permissions
USER root

# Determine the user ID and group ID for Grafana
RUN id grafana || echo "Grafana user not found, using UID=472" \
    && chown -R 472:472 /etc/grafana /var/lib/grafana

# Switch back to Grafana user (use 472, which is the default UID/GID for Grafana in Docker)
USER 472
