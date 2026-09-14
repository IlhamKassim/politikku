/* How-a-vote-works plays: one Seat race, a Majority house, one Bill
   walk, and an optional compass. The page must still read without this
   script — every control has a static fallback in the HTML. */

(function () {
  var TOTAL = 222;
  var MAJORITY = 112;
  var CODES = ["PH", "PN", "BN", "GPS", "GRS", "OTHER"];
  var YEARS = {
    ge13: {
      seats: { PH: 0, PN: 0, BN: 133, GPS: 0, GRS: 0, OTHER: 89 },
      show: ["BN", "OTHER"],
      otherLabel: { en: "Pakatan Rakyat", ms: "Pakatan Rakyat" },
    },
    ge14: {
      seats: { PH: 113, PN: 0, BN: 79, GPS: 0, GRS: 0, OTHER: 30 },
      show: ["PH", "BN", "OTHER"],
      otherLabel: { en: "Others", ms: "Lain-lain" },
    },
    ge15: {
      seats: { PH: 82, PN: 74, BN: 30, GPS: 23, GRS: 6, OTHER: 7 },
      show: CODES,
      otherLabel: { en: "Others", ms: "Lain-lain" },
    },
  };

  function lang() {
    return document.documentElement.lang === "ms" ? "ms" : "en";
  }

  function t(en, ms) {
    return lang() === "ms" ? ms : en;
  }

  function color(code) {
    return "var(--vote-" + code.toLowerCase() + ")";
  }

  function initRace() {
    var root = document.getElementById("vote-race");
    if (!root) return;
    var result = root.querySelector("[data-race-result]");
    root.addEventListener("click", function (event) {
      var btn = event.target.closest("[data-race]");
      if (!btn || !result) return;
      var pick = btn.getAttribute("data-race");
      root.querySelectorAll("[data-race]").forEach(function (el) {
        el.removeAttribute("data-on");
        el.setAttribute("aria-pressed", "false");
      });
      btn.setAttribute("data-on", "true");
      btn.setAttribute("aria-pressed", "true");
      if (pick === "rizal") {
        result.dataset.state = "pass";
        result.textContent = t(
          "Yes. Rizal has the most votes in this Seat, so Rizal wins it.",
          "Ya. Rizal ada undi terbanyak dalam Kerusi ini, jadi Rizal memenanginya.",
        );
      } else {
        result.dataset.state = "hung";
        result.textContent = t(
          "Not this person. Most votes in this Seat win it. Rizal has 5,100.",
          "Bukan orang ini. Undi terbanyak dalam Kerusi ini memenanginya. Rizal ada 5,100.",
        );
      }
    });
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
      var count = root.querySelector('[data-sim-count="' + code + '"]');
      if (input) input.value = String(seats[code] || 0);
      if (count) count.textContent = String(seats[code] || 0);
    });
  }

  function governmentCodes(root) {
    return CODES.filter(function (code) {
      var box = root.querySelector('[data-sim-gov="' + code + '"]');
      return box && box.checked;
    });
  }

  function govSeatsOf(root) {
    var seats = readSeats(root);
    return governmentCodes(root).reduce(function (n, code) {
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
            color(code) +
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
        color(code) +
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
    stack.innerHTML = '<div class="stack-bar">' + html + "</div>";
  }

  function applyYear(root, name) {
    var year = YEARS[name];
    if (!year) return;
    writeSeats(root, year.seats);
    CODES.forEach(function (code) {
      var row = root.querySelector('[data-sim-row="' + code + '"]');
      if (row) row.hidden = year.show.indexOf(code) === -1;
      var box = root.querySelector('[data-sim-gov="' + code + '"]');
      if (box) box.checked = false;
    });
    var otherName = root.querySelector("[data-sim-other-name]");
    if (otherName) otherName.textContent = year.otherLabel[lang()];
    root.querySelectorAll("[data-sim-year]").forEach(function (btn) {
      btn.setAttribute(
        "aria-pressed",
        btn.getAttribute("data-sim-year") === name ? "true" : "false",
      );
    });
  }

  function renderSim(root) {
    var seats = readSeats(root);
    var govSeats = govSeatsOf(root);
    var status = root.querySelector("[data-sim-status]");
    paintChamber(root, seats);
    paintStack(root, seats);
    if (!status) return;
    if (govSeats >= MAJORITY) {
      status.dataset.state = "pass";
      status.textContent = t(
        "You have a Majority (" + govSeats + "). In this teaching house, that side holds more than half of all 222 Seats.",
        "Anda ada Majoriti (" + govSeats + "). Dalam dewan pengajaran ini, pihak itu memegang lebih separuh daripada semua 222 Kerusi.",
      );
    } else {
      status.dataset.state = "hung";
      status.textContent = t(
        "Not yet. You have " + govSeats + ". Tick Coalitions until you hold 112.",
        "Belum. Anda ada " + govSeats + ". Tanda Gabungan sampai anda pegang 112.",
      );
    }
  }

  function initSimulator() {
    var root = document.getElementById("vote-sim");
    if (!root) return;

    root.addEventListener("change", function () {
      renderSim(root);
    });

    root.addEventListener("click", function (event) {
      var yearBtn = event.target.closest("[data-sim-year]");
      if (yearBtn) {
        applyYear(root, yearBtn.getAttribute("data-sim-year"));
        renderSim(root);
      }
    });

    applyYear(root, "ge15");
    renderSim(root);
  }

  function paintDots(container, seats, fallbackCount, fallbackColor) {
    if (!container) return;
    var html = "";
    if (seats) {
      CODES.forEach(function (code) {
        var n = seats[code] || 0;
        for (var i = 0; i < n; i += 1) {
          html +=
            '<i class="sim-dot" style="background:' +
            color(code) +
            '" title="' +
            code +
            '"></i>';
        }
      });
    } else {
      for (var j = 0; j < fallbackCount; j += 1) {
        html +=
          '<i class="sim-dot" style="background:' + fallbackColor + '"></i>';
      }
    }
    container.innerHTML = html;
  }

  function readBillHouse(force) {
    var lime = "var(--accent)";
    var mute = "var(--ink-faint)";
    if (force === "fail") {
      return { yes: 82, no: 140, yesSeats: null, noSeats: null, lime: lime, mute: mute, kind: "fail" };
    }
    if (force === "pass") {
      return { yes: 112, no: 110, yesSeats: null, noSeats: null, lime: lime, mute: mute, kind: "pass" };
    }
    var sim = document.getElementById("vote-sim");
    if (!sim) {
      return { yes: 112, no: 110, yesSeats: null, noSeats: null, lime: lime, mute: mute, kind: "default" };
    }
    var gov = governmentCodes(sim);
    if (!gov.length) {
      return { yes: 112, no: 110, yesSeats: null, noSeats: null, lime: lime, mute: mute, kind: "default" };
    }
    var seats = readSeats(sim);
    var yesSeats = {};
    var noSeats = {};
    var yes = 0;
    var no = 0;
    CODES.forEach(function (code) {
      var n = seats[code] || 0;
      if (gov.indexOf(code) !== -1) {
        yesSeats[code] = n;
        yes += n;
      } else {
        noSeats[code] = n;
        no += n;
      }
    });
    return {
      yes: yes,
      no: no,
      yesSeats: yesSeats,
      noSeats: noSeats,
      lime: lime,
      mute: mute,
      kind: "play3",
    };
  }

  function initBill() {
    var root = document.getElementById("vote-bill");
    if (!root) return;
    var next = root.querySelector("[data-bill-next]");
    var failBtn = root.querySelector("[data-bill-fail]");
    var passBtn = root.querySelector("[data-bill-if-pass]");
    var floor = root.querySelector("[data-div-floor]");
    var live = root.querySelector("[data-div-live]");
    var stage = "reading";
    var divided = false;
    var force = "";
    var PASS = ["reading", "gov", "opp", "division", "senate", "assent", "law", "coda"];
    var CHIP = {
      reading: "reading",
      gov: "debate",
      opp: "debate",
      division: "division",
      senate: "senate",
      assent: "assent",
      law: "end",
      failed: "end",
      coda: "end",
    };

    function house() {
      return readBillHouse(force);
    }

    function paintPool() {
      if (!floor) return;
      var h = house();
      floor.setAttribute("data-split", "false");
      var pool = root.querySelector("[data-div-pool-dots]");
      if (h.yesSeats && h.noSeats) {
        var all = {};
        CODES.forEach(function (code) {
          all[code] = (h.yesSeats[code] || 0) + (h.noSeats[code] || 0);
        });
        paintDots(pool, all, 0, h.lime);
      } else {
        paintDots(pool, null, 222, h.mute);
      }
      if (live) {
        live.textContent = t(
          "Not yet counted. Press to split the 222 Seats.",
          "Belum dikira. Tekan untuk memecahkan 222 Kerusi.",
        );
      }
    }

    function splitFloor() {
      if (!floor) return;
      var h = house();
      floor.setAttribute("data-split", "true");
      paintDots(root.querySelector("[data-div-yes-dots]"), h.yesSeats, h.yes, h.lime);
      paintDots(root.querySelector("[data-div-no-dots]"), h.noSeats, h.no, h.mute);
      var yesN = root.querySelector("[data-div-yes-n]");
      var noN = root.querySelector("[data-div-no-n]");
      if (yesN) yesN.textContent = String(h.yes);
      if (noN) noN.textContent = String(h.no);
      var passed = h.yes >= MAJORITY;
      if (live) {
        live.textContent = passed
          ? t(
              "Yes " + h.yes + ". No " + h.no + ". This play counts all 222 MPs, so 112 yes votes pass the Bill.",
              "Ya " + h.yes + ". Tidak " + h.no + ". Permainan ini mengira semua 222 Ahli Parlimen, jadi 112 undi ya meluluskan Rang Undang-Undang.",
            )
          : t(
              "Yes " + h.yes + ". No " + h.no + ". This play counts all 222 MPs, so the Bill does not have more votes.",
              "Ya " + h.yes + ". Tidak " + h.no + ". Permainan ini mengira semua 222 Ahli Parlimen, jadi Rang Undang-Undang tidak mendapat undi lebih.",
            );
      }
      return passed;
    }

    function show(shouldFocus) {
      root.querySelectorAll("[data-bill-stage]").forEach(function (el) {
        el.classList.toggle("is-on", el.getAttribute("data-bill-stage") === stage);
      });
      var chip = CHIP[stage] || "end";
      root.querySelectorAll("[data-bill-chip]").forEach(function (el) {
        var isCurrent = el.getAttribute("data-bill-chip") === chip;
        el.setAttribute("data-on", isCurrent ? "true" : "false");
        if (isCurrent) el.setAttribute("aria-current", "step");
        else el.removeAttribute("aria-current");
      });
      if (stage === "division" && !divided) paintPool();
      if (next) {
        var hideNext = stage === "coda";
        next.hidden = hideNext;
        if (stage === "division" && !divided) {
          next.textContent = next.getAttribute("data-label-divide") || t("Divide the house", "Pecahkan dewan");
        } else {
          next.textContent = next.getAttribute("data-label-continue") || t("Continue", "Teruskan");
        }
      }
      if (failBtn) failBtn.hidden = stage !== "law";
      if (passBtn) passBtn.hidden = stage !== "failed";
      var panel = root.querySelector('[data-bill-stage="' + stage + '"]');
      if (panel && shouldFocus) {
        panel.focus();
      }
    }

    if (next) {
      next.addEventListener("click", function () {
        if (stage === "division" && !divided) {
          divided = true;
          splitFloor();
          show(true);
          return;
        }
        if (stage === "reading") stage = "gov";
        else if (stage === "gov") stage = "opp";
        else if (stage === "opp") {
          stage = "division";
          divided = false;
        } else if (stage === "division") {
          stage = house().yes >= MAJORITY ? "senate" : "failed";
        } else if (stage === "senate") stage = "assent";
        else if (stage === "assent") stage = "law";
        else if (stage === "law") stage = "coda";
        else if (stage === "failed") stage = "coda";
        show(true);
      });
    }
    if (failBtn) {
      failBtn.addEventListener("click", function () {
        force = "fail";
        divided = true;
        stage = "failed";
        splitFloor();
        show(true);
      });
    }
    if (passBtn) {
      passBtn.addEventListener("click", function () {
        force = "pass";
        divided = true;
        stage = "senate";
        splitFloor();
        show(true);
      });
    }
    show(false);
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

  function start() {
    document.documentElement.classList.add("js-ready");
    initRace();
    initSimulator();
    initBill();
    initCompass();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", start);
  } else {
    start();
  }
})();
