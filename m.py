# -*- coding: utf-8 -*-
P = r"D:\wechat_moments\index.html"
lines = open(P, encoding="utf-8", newline="").read().split("\r\n")

def idx(sub):
    for i, ln in enumerate(lines):
        if sub in ln:
            return i
    raise SystemExit("NOT FOUND: " + sub)

# 1) head：补 PWA 相关 meta / link
i = idx('<meta name="apple-mobile-web-app-status-bar-style"')
lines[i] = (lines[i] + "\r\n"
    '<meta name="mobile-web-app-capable" content="yes">\r\n'
    '<meta name="apple-mobile-web-app-title" content="朋友圈">\r\n'
    '<meta name="application-name" content="朋友圈">\r\n'
    '<link rel="manifest" href="manifest.webmanifest?v=4">\r\n'
    '<link rel="apple-touch-icon" href="apple-touch-icon.png?v=4">\r\n'
    '<link rel="icon" type="image/png" href="icon-192.png?v=4">')

# 2) JS：首次交互时尝试进入全屏（Android Chrome 有效，iPhone 会静默失败）
i = idx("if (location.hash === '#detail') showDetail();")
lines.insert(i, (
    "  // 首次交互时尝试进入全屏（Android Chrome 可隐藏地址栏；iOS 需添加到主屏幕）\r\n"
    "  (function () {\r\n"
    "    var done = false;\r\n"
    "    function enterFs() {\r\n"
    "      if (done) return;\r\n"
    "      done = true;\r\n"
    "      var el = document.documentElement;\r\n"
    "      var fn = el.requestFullscreen || el.webkitRequestFullscreen || el.msRequestFullscreen;\r\n"
    "      if (fn) { try { var p = fn.call(el); if (p && p.catch) p.catch(function(){}); } catch (e) {} }\r\n"
    "    }\r\n"
    "    ['click', 'touchend'].forEach(function (ev) {\r\n"
    "      document.addEventListener(ev, enterFs, { once: true, passive: true });\r\n"
    "    });\r\n"
    "  })();\r\n"))

txt = "\r\n".join(lines)
open(P, "w", encoding="utf-8", newline="").write(txt)

print("--- head ---")
for ln in txt.split("\r\n")[:22]:
    print("  ", ln)
print("\n大括号配平:", txt.count("{") - txt.count("}"))
print("含 requestFullscreen:", "requestFullscreen" in txt)
