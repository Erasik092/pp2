import json


def parse_sample_json():
    """Parse sample-data.json and print a formatted interface status table."""
    fname = "sample-data.json"
    with open(fname) as f:
        data = json.load(f)

    print("Interface Status")
    print("=" * 80)
    header = (
        f"{'DN':<50} {'Description':<20} {'Speed':<6} {'MTU':<6}"
    )
    print(header)
    print("-" * 50 + " " + "-" * 20 + " " + "-" * 6 + " " + "-" * 6)

    for entry in data.get("imdata", []):
        attrs = entry.get("l1PhysIf", {}).get("attributes", {})
        dn = attrs.get("dn", "")
        descr = attrs.get("descr", "")
        speed = attrs.get("speed", "")
        mtu = attrs.get("mtu", "")

        line = f"{dn:<50} {descr:<20} {speed:<6} {mtu:<6}"
        print(line)


if __name__ == "__main__":
    parse_sample_json()