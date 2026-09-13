/* How-a-vote-works extras: year charts stay CSS-only. This file only
   drives the teaching compass (visitor mark) and the Dewan Rakyat
   Seat simulator. The page must still read without this script — every
   control has a static fallback in the HTML. */

(function () {
  var TOTAL = 222;
  var MAJORITY = 112;
  var CODES = ["PH", "PN", "BN", "GPS", "GRS", "OTHER"];
  var COLORS = {
    PH: "#d7263d",
    PN: "#15387c",
    BN: "#1f9bd6",
    GPS: "#b8332e",
    GRS: "#e8772e",
    OTHER: "#5d6b7d",
  };

  var PRESETS = {
    ge15: { PH: 82, PN: 74, BN: 30, GPS: 23, GRS: 6, OTHER: 7 },
    ge14: { PH: 113, PN: 0, BN: 79, GPS: 0, GRS: 0, OTHER: 30 },
    majority: { PH: 70, PN: 60, BN: 30, GPS: 12, GRS: 6, OTHER: 44 },
  };

  function lang() {
    return document.documentElement.lang === "ms" ? "ms" : "en";
  }

  function t(en, ms) {
    return lang() === "ms" ? ms : en;
  }

  function initCompass() {
    var board = document.getElementById("vote-compass");
    if (!board) return;
    var you = document.getElementById("vote-compass-you");
    var note = document.getElementById("vote-compass-note");
    var xInput = document.getElementById("vote-compass-x");
    var yInput = document.getElementById("vote-compass-y");
    if (!you || !note) return;

    function place(xPct, yPct) {
      var x = Math.max(2, Math.min(98, xPct));
      var y = Math.max(2, Math.min(98, yPct));
      you.style.left = x + "%";
      you.style.top = y + "%";
      you.hidden = false;
      if (xInput) xInput.value = String(Math.round(x));
      if (yInput) yInput.value = String(Math.round(y));
      note.textContent = t(
        "Your mark. This page does not name a Coalition for you.",
        "Tanda anda. Laman ini tidak menamakan Gabungan untuk anda.",
      );
    }

    board.addEventListener("click", function (event) {
      var rect = board.getBoundingClientRect();
      if (!rect.width || !rect.height) return;
      place(
        ((event.clientX - rect.left) / rect.width) * 100,
        ((event.clientY - rect.top) / rect.height) * 100,
      );
    });

    function fromSliders() {
      if (!xInput || !yInput) return;
      place(Number(xInput.value), Number(yInput.value));
    }
    if (xInput) xInput.addEventListener("input", fromSliders);
    if (yInput) yInput.addEventListener("input", fromSliders);
  }

  function readSeats(root) {
    var seats = {};
    CODES.forEach(function (code) {
      var input = root.querySelector('[data-sim-seats="' + code + '"]');
      var value = input ? parseInt(input.value, 10) : 0;
      seats[code] = Number.isFinite(value) ? Math.max(0, value) : 0;
    });
    return seats;
  }

  function writeSeats(root, seats) {
    CODES.forEach(function (code) {
      var input = root.querySelector('[data-sim-seats="' + code + '"]');
      if (input) input.value = String(seats[code] || 0);
    });
  }

  function governmentCodes(root) {
    return CODES.filter(function (code) {
      var box = root.querySelector('[data-sim-gov="' + code + '"]');
      return box && box.checked;
    });
  }

  function sum(seats) {
    return CODES.reduce(function (n, code) {
      return n + (seats[code] || 0);
    }, 0);
  }

  function paintChamber(root, seats) {
    var chamber = root.querySelector("[data-sim-chamber]");
    if (!chamber) return;
    var dots = [];
    CODES.forEach(function (code) {
      var n = seats[code] || 0;
      for (var i = 0; i < n; i += 1) {
        dots.push(
          '<i class="sim-dot" style="background:' +
            COLORS[code] +
            '" title="' +
            code +
            '"></i>',
        );
      }
    });
    chamber.innerHTML = dots.join("");
  }

  function paintStack(root, seats) {
    var stack = root.querySelector("[data-sim-stack]");
    if (!stack) return;
    var html = CODES.map(function (code) {
      var n = seats[code] || 0;
      if (!n) return "";
      return (
        '<span class="stack-seg" style="width:' +
        ((n / TOTAL) * 100).toFixed(2) +
        "%;background:" +
        COLORS[code] +
        '" title="' +
        code +
        " " +
        n +
        '"></span>'
      );
    }).join("");
    html +=
      '<i class="majority-tick" style="left:' +
      ((MAJORITY / TOTAL) * 100).toFixed(2) +
      '%"></i>';
    stack.innerHTML = html;
  }

  function renderSim(root) {
    var seats = readSeats(root);
    var total = sum(seats);
    var gov = governmentCodes(root);
    var govSeats = gov.reduce(function (n, code) {
      return n + (seats[code] || 0);
    }, 0);
    var status = root.querySelector("[data-sim-status]");
    var totalEl = root.querySelector("[data-sim-total]");
    if (totalEl) {
      totalEl.textContent = String(total);
    }
    paintChamber(root, seats);
    paintStack(root, seats);

    if (!status) return;
    if (total !== TOTAL) {
      status.dataset.state = "warn";
      status.textContent = t(
        "Give the house 222 Seats first. This house has " + total + ".",
        "Berikan dewan 222 Kerusi dahulu. Dewan ini ada " + total + ".",
      );
      return;
    }
    if (govSeats >= MAJORITY) {
      status.dataset.state = "pass";
      status.textContent = t(
        "This house has a Majority (" +
          govSeats +
          " of 222). If every Government Coalition Seat votes yes, a Bill can pass a Division.",
        "Dewan ini mempunyai Majoriti (" +
          govSeats +
          " daripada 222). Jika setiap Kerusi Gabungan Kerajaan mengundi ya, Rang Undang-Undang boleh lulus suatu Bahagian.",
      );
      return;
    }
    status.dataset.state = "hung";
    status.textContent = t(
      "This house does not have a Majority (" +
        govSeats +
        " of 222). A Bill still needs 112 yes votes on a Division.",
      "Dewan ini tidak mempunyai Majoriti (" +
        govSeats +
        " daripada 222). Rang Undang-Undang masih memerlukan 112 undi ya dalam suatu Bahagian.",
    );
  }

  function initSimulator() {
    var root = document.getElementById("vote-sim");
    if (!root) return;

    root.addEventListener("input", function (event) {
      var target = event.target;
      if (target && target.hasAttribute("data-sim-seats")) {
        var next = parseInt(target.value, 10);
        if (!Number.isFinite(next) || next < 0) target.value = "0";
        if (next > TOTAL) target.value = String(TOTAL);
      }
      renderSim(root);
    });

    root.addEventListener("click", function (event) {
      var btn = event.target.closest("[data-sim-step]");
      if (btn) {
        var code = btn.getAttribute("data-sim-step-code");
        var delta = Number(btn.getAttribute("data-sim-step"));
        var input = root.querySelector('[data-sim-seats="' + code + '"]');
        if (input) {
          var next = (parseInt(input.value, 10) || 0) + delta;
          input.value = String(Math.max(0, Math.min(TOTAL, next)));
          renderSim(root);
        }
        return;
      }
      var preset = event.target.closest("[data-sim-preset]");
      if (preset) {
        var name = preset.getAttribute("data-sim-preset");
        if (PRESETS[name]) writeSeats(root, PRESETS[name]);
        if (name === "ge15" || name === "majority") {
          ["PH", "BN", "GPS", "GRS"].forEach(function (code) {
            var box = root.querySelector('[data-sim-gov="' + code + '"]');
            if (box) box.checked = true;
          });
          ["PN", "OTHER"].forEach(function (code) {
            var box = root.querySelector('[data-sim-gov="' + code + '"]');
            if (box) box.checked = false;
          });
        }
        if (name === "ge14") {
          var ph = root.querySelector('[data-sim-gov="PH"]');
          if (ph) ph.checked = true;
          ["PN", "BN", "GPS", "GRS", "OTHER"].forEach(function (code) {
            var box = root.querySelector('[data-sim-gov="' + code + '"]');
            if (box) box.checked = false;
          });
        }
        renderSim(root);
      }
    });

    renderSim(root);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function () {
      initCompass();
      initSimulator();
    });
  } else {
    initCompass();
    initSimulator();
  }
})();
