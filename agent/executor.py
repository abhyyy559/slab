"""Executor: WebCMD browser actions + pre/post state hashes.
Uses WebCMD CLI (webcmd browser run / session create / session close) for all browser operations.
"""
import hashlib, json, os, pathlib, shutil, subprocess, time
from .logger import log_action

DEFAULT_TIMEOUT_MS = 3000
WEBCMD_BIN = shutil.which("webcmd") or "webcmd"

def state_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()

def page_state(page) -> str:
    try:
        return page.content()
    except Exception:
        try:
            return page.evaluate("() => document.documentElement ? document.documentElement.outerHTML : ''") or ""
        except Exception as e:
            return f"<snapshot-failed:{e}>"

class WebcmdLocator:
    def __init__(self, page, loc_type: str, selector: str, extra: dict | None = None):
        self.page = page
        self.loc_type = loc_type
        self.selector = selector
        self.extra = extra or {}

    @property
    def first(self):
        return self

    def _js_target(self) -> str:
        if self.loc_type == "css":
            return f"page.locator({json.dumps(self.selector)})"
        elif self.loc_type == "role":
            role = self.extra.get("role", "")
            name = self.extra.get("name")
            if name:
                return f"page.getByRole({json.dumps(role)}, {{ name: {json.dumps(name)} }})"
            return f"page.getByRole({json.dumps(role)})"
        elif self.loc_type == "text":
            return f"page.getByText({json.dumps(self.selector)})"
        return f"page.locator({json.dumps(self.selector)})"

    def count(self) -> int:
        code = f"""
        try {{
            const loc = {self._js_target()};
            return await loc.count();
        }} catch (e) {{
            return 0;
        }}
        """
        res = self.page.run_js(code)
        return int(res.get("result", 0)) if isinstance(res, dict) and "result" in res else 0

    def is_visible(self) -> bool:
        code = f"""
        try {{
            const loc = {self._js_target()};
            const n = await loc.count();
            if (n < 1) return false;
            return await loc.isVisible();
        }} catch (e) {{
            return false;
        }}
        """
        res = self.page.run_js(code)
        return bool(res.get("result", False)) if isinstance(res, dict) and "result" in res else False

    def click(self, timeout: int = DEFAULT_TIMEOUT_MS):
        code = f"""
        const loc = {self._js_target()};
        await loc.click({{ timeout: {timeout} }});
        return true;
        """
        res = self.page.run_js(code, timeout_ms=timeout + 2000)
        if not res.get("ok"):
            err = res.get("error", {})
            msg = err.get("message", "click failed") if isinstance(err, dict) else str(err)
            raise RuntimeError(f"WebCMD click error: {msg}")
        return True

    def fill(self, value: str, timeout: int = DEFAULT_TIMEOUT_MS):
        code = f"""
        const loc = {self._js_target()};
        await loc.fill({json.dumps(value)}, {{ timeout: {timeout} }});
        return true;
        """
        res = self.page.run_js(code, timeout_ms=timeout + 2000)
        if not res.get("ok"):
            err = res.get("error", {})
            msg = err.get("message", "fill failed") if isinstance(err, dict) else str(err)
            raise RuntimeError(f"WebCMD fill error: {msg}")
        return True

    def press(self, key: str = "Enter", timeout: int = DEFAULT_TIMEOUT_MS):
        code = f"""
        const loc = {self._js_target()};
        await loc.press({json.dumps(key)}, {{ timeout: {timeout} }});
        return true;
        """
        res = self.page.run_js(code, timeout_ms=timeout + 2000)
        if not res.get("ok"):
            err = res.get("error", {})
            msg = err.get("message", "press failed") if isinstance(err, dict) else str(err)
            raise RuntimeError(f"WebCMD press error: {msg}")
        return True

    def inner_text(self) -> str:
        code = f"""
        const loc = {self._js_target()};
        return await loc.innerText();
        """
        res = self.page.run_js(code)
        return str(res.get("result", "")) if isinstance(res, dict) and "result" in res else ""


class WebcmdPage:
    def __init__(self, session_id: str, profile: str | None = None):
        self.session_id = session_id
        self.profile = profile

    def run_js(self, js_code: str, timeout_ms: int = 15000) -> dict:
        timeout_sec = max(2, int(timeout_ms / 1000))
        cmd = [WEBCMD_BIN]
        if self.profile:
            cmd.extend(["--profile", self.profile])
        cmd.extend(["--session", self.session_id, "browser", "run", "--stdin", "--no-snapshot-diff", "-f", "json", "--timeout", str(timeout_sec)])
        try:
            proc = subprocess.run(cmd, input=js_code, text=True, capture_output=True, encoding="utf-8", check=False)
            out = proc.stdout.strip()
            if not out:
                return {"ok": False, "error": f"Empty output from webcmd (stderr: {proc.stderr[:200]})"}
            return json.loads(out)
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def goto(self, url: str, wait_until: str = "domcontentloaded", timeout: int = DEFAULT_TIMEOUT_MS):
        code = f"""
        await page.goto({json.dumps(url)}, {{ waitUntil: {json.dumps(wait_until)}, timeout: {timeout} }});
        return {{ url: page.url(), title: await page.title() }};
        """
        res = self.run_js(code, timeout_ms=timeout + 3000)
        if not res.get("ok"):
            err = res.get("error", {})
            msg = err.get("message", "goto failed") if isinstance(err, dict) else str(err)
            raise RuntimeError(f"WebCMD goto error: {msg}")
        return res.get("result")

    def content(self) -> str:
        code = """
        return await page.content();
        """
        res = self.run_js(code)
        return res.get("result", "") if isinstance(res, dict) else ""

    def title(self) -> str:
        code = """
        return await page.title();
        """
        res = self.run_js(code)
        return res.get("result", "") if isinstance(res, dict) else ""

    def url(self) -> str:
        code = """
        return page.url();
        """
        res = self.run_js(code)
        return res.get("result", "") if isinstance(res, dict) else ""

    def wait_for_timeout(self, ms: int):
        code = f"""
        await page.waitForTimeout({int(ms)});
        return true;
        """
        return self.run_js(code, timeout_ms=ms + 3000)

    def fill(self, selector: str, value: str, timeout: int = DEFAULT_TIMEOUT_MS):
        return self.locator(selector).fill(value, timeout=timeout)

    def inner_text(self, selector: str) -> str:
        return self.locator(selector).inner_text()

    def locator(self, selector: str) -> WebcmdLocator:
        return WebcmdLocator(self, loc_type="css", selector=selector)

    def get_by_role(self, role: str, name: str | None = None) -> WebcmdLocator:
        return WebcmdLocator(self, loc_type="role", selector="", extra={"role": role, "name": name})

    def get_by_text(self, text: str) -> WebcmdLocator:
        return WebcmdLocator(self, loc_type="text", selector=text)

    def evaluate(self, js_expr: str, arg: any = None) -> any:
        if arg is not None:
            code = f"""
            const fn = {js_expr};
            return await page.evaluate(fn, {json.dumps(arg)});
            """
        else:
            code = f"""
            const fn = {js_expr};
            return await page.evaluate(fn);
            """
        res = self.run_js(code)
        if isinstance(res, dict) and "result" in res:
            return res["result"]
        return None


class WebcmdSession:
    """Manages WebCMD browser session lifecycle with action logging."""
    def __init__(self, name: str = "sentry", profile: str | None = None):
        self.name = name
        self.profile = profile
        self.session_id = None
        self.page = None

    def __enter__(self):
        cmd = [WEBCMD_BIN]
        if self.profile:
            cmd.extend(["--profile", self.profile])
        cmd.extend(["session", "create", self.name, "-f", "json"])
        proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", check=False)
        out = proc.stdout.strip()
        try:
            data = json.loads(out)
            self.session_id = data.get("id")
        except Exception:
            # parse non-json fallback
            for line in out.splitlines():
                if line.startswith("id:"):
                    self.session_id = line.split(":", 1)[1].strip()
        if not self.session_id:
            raise RuntimeError(f"Failed to create WebCMD session: {out} (stderr: {proc.stderr})")

        log_action(event="SESSION_CREATED", session_id=self.session_id, profile=self.profile or "default", name=self.name)
        self.page = WebcmdPage(self.session_id, profile=self.profile)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.session_id:
            cmd = [WEBCMD_BIN]
            if self.profile:
                cmd.extend(["--profile", self.profile])
            cmd.extend(["session", "close", self.session_id])
            subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", check=False)
            log_action(event="SESSION_CLOSED", session_id=self.session_id, profile=self.profile or "default")


def do_action(page, action: str, locator, value: str | None = None, timeout_ms: int = DEFAULT_TIMEOUT_MS):
    """Execute action via WebCMD browser commands and compute pre/post state hashes."""
    t0 = time.time()
    before = state_hash(page_state(page))
    result = "ok"
    try:
        if action == "goto":
            page.goto(value, wait_until="domcontentloaded", timeout=timeout_ms)
        elif action == "click":
            locator.click(timeout=timeout_ms)
        elif action == "fill":
            locator.fill(value or "", timeout=timeout_ms)
        elif action == "press":
            locator.press(value or "Enter", timeout=timeout_ms)
        else:
            raise ValueError(f"unknown action {action}")
    except Exception as e:
        result = f"timeout_or_error: {type(e).__name__}: {e}"
        try:
            snap = page_state(page)
            before = state_hash(snap)
        except Exception:
            pass
    after = state_hash(page_state(page))
    return {
        "state_before_hash": before,
        "state_after_hash": after,
        "duration_ms": int((time.time() - t0) * 1000),
        "result": result
    }
