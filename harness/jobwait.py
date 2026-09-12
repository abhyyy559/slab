import json
import time
import urllib.request

BASE = "http://127.0.0.1:8765"


def post(path, body):
    q = urllib.request.Request(BASE + path, data=json.dumps(body).encode(),
                               headers={"Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(q, timeout=15))


def get(path):
    return json.load(urllib.request.urlopen(BASE + path, timeout=15))


if __name__ == "__main__":
    import sys
    body = json.loads(sys.argv[1]) if len(sys.argv) > 1 else {"action": "gauntlet"}
    jid = post("/api/run", body)["id"]
    print("job:", jid, flush=True)
    for _ in range(40):
        time.sleep(10)
        runs = get("/api/history")["runs"]
        match = [x for x in runs if x["id"] == jid]
        if match and match[0].get("ended"):
            r = match[0]
            print(r.get("verdict"), "|", r.get("result_status"),
                  "| extra:", r.get("extra_steps"), flush=True)
            break
    else:
        print("TIMEOUT waiting for job", flush=True)
