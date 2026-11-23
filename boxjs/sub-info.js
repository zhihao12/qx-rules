(function () {
  var name = $prefs.valueForKey("subinfo_name") || "订阅";
  var url = $prefs.valueForKey("subinfo_url");

  function notify(title, body) {
    $notify(title, "", body);
  }

  try {
    if (!url) {
      notify("订阅信息", "还没有填订阅链接，请先在 BoxJS 的「订阅信息」应用里填入机场订阅链接");
      $done();
      return;
    }

    $task.fetch({
      url: url,
      method: "GET",
      headers: { "User-Agent": "Quantumult X" }
    }).then(function (response) {
      var headers = response.headers || {};
      var info = null;
      Object.keys(headers).some(function (key) {
        if (key.toLowerCase() === "subscription-userinfo") {
          info = headers[key];
          return true;
        }
        return false;
      });

      if (!info) {
        notify(name + " 订阅信息", "该订阅没有返回流量信息（面板未提供 subscription-userinfo）");
        return;
      }

      var values = {};
      String(info).split(";").forEach(function (part) {
        var pair = part.trim().split("=");
        if (pair.length >= 2) values[pair[0].trim()] = Number(pair.slice(1).join("=").trim());
      });

      var upload = values.upload || 0;
      var download = values.download || 0;
      var total = values.total || 0;
      var used = upload + download;
      var remaining = Math.max(0, total - used);
      var percent = total > 0 ? (used / total * 100).toFixed(1) : "0.0";
      var gb = 1024 * 1024 * 1024;
      var lines = [
        "已用 " + (used / gb).toFixed(2) + " GB / 共 " + (total / gb).toFixed(2) + " GB（" + percent + "%）",
        "剩余 " + (remaining / gb).toFixed(2) + " GB"
      ];

      if (values.expire > 0) {
        var expiry = new Date(values.expire * 1000);
        var year = expiry.getFullYear();
        var month = String(expiry.getMonth() + 1).padStart(2, "0");
        var day = String(expiry.getDate()).padStart(2, "0");
        var days = Math.max(0, Math.ceil((values.expire * 1000 - Date.now()) / 86400000));
        lines.push("到期 " + year + "-" + month + "-" + day + "（剩 " + days + " 天）");
      }

      notify(name + " 订阅信息", lines.join("\n"));
    }).catch(function (error) {
      notify(name + " 订阅信息", "查询失败，请检查订阅链接是否有效");
    }).then(function () {
      $done();
    }, function () {
      $done();
    });
  } catch (error) {
    try {
      notify(name + " 订阅信息", "查询失败，请检查订阅链接是否有效");
    } finally {
      $done();
    }
  }
})();
