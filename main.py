import json
import os
import time
from lightstreamer.client import LightstreamerClient, Subscription, SubscriptionListener

CACHE_FILE = "urine_tank_cache.json"

print("hank")

def load_cached_value():
    #loads cached values from urine_tank_cache into memory
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return None


def save_cached_value(value, timestamp):
    # updates cache json when new vals received
    with open(CACHE_FILE, "w") as f:
        json.dump({"value": value, "timestamp": timestamp}, f)


class UrineTankListener(SubscriptionListener):
    # dont think i needed to make it a class
    def onUpdate(self, update):
        try:
            value = update.getValue("value")
            timestamp = update.getValue("timeStamp")
            if value:
                print(f"[LIVE {timestamp}] urine tank fill: {value}%")
                save_cached_value(value, timestamp)
        except Exception as e:
            print("error: ", e)


# print last known value immediatelly (probably not that accurate)
cached = load_cached_value()
if cached:
    print(f"[CACHED {cached['timestamp']}] uirine tank fill: {cached['value']}%")
else:
    print("no cached urine tank value found.")

# connect to lightstreamer
client = LightstreamerClient("https://push.lightstreamer.com", "DEMO")

sub = Subscription(mode="MERGE", items=["NODE3000005"], fields=["TimeStamp", "Value"])

sub.addListener(UrineTankListener())

client.connect()
client.subscribe(sub)

print("listening for live updates")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:  # like if ctrl + c
    print("disconnecting...")
finally:
    client.unsubscribe(sub)
    client.disconnect()
