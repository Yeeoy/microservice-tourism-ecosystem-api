import time
import consul
import os
import requests
from requests.exceptions import RequestException
from django.conf import settings

def register_service():
    if not settings.CONSUL_ENABLED:
        print("Skipping Consul registration as it is disabled.")
        return

    max_retries = 5
    retry_delay = 5

    for attempt in range(max_retries):
        try:
            consul_host = os.environ.get('CONSUL_HOST', 'consul')
            consul_client = consul.Consul(host=consul_host)

            service_host = os.environ.get('SERVICE_HOST', 'accommodation-service')
            service_port = int(os.environ.get('SERVICE_PORT', 8000))

            consul_client.agent.service.register(
                name="accommodation-service",
                service_id="accommodation-service-1",
                address=service_host,
                port=service_port,
                tags=["web", "django"],
                check=consul.Check().http(
                    f'http://{service_host}:{service_port}/api/accommodation/health/',
                    interval="10s",
                    timeout="5s"
                )
            )
            print("Service registered with Consul")
            return
        except (RequestException, consul.ConsulException) as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                print("Failed to register service with Consul after multiple attempts")
