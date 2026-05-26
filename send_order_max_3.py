import runtime_warnings

from env_config import get_device_id, get_integration_token, get_location_id
from order_templates import print_order_summary, run_minimal_order


result = run_minimal_order(
    token=get_integration_token(),
    location_id=get_location_id(),
    device_id=get_device_id(),
    max_items=3,
    qty_choices=[1, 3],
)
print_order_summary(result)
