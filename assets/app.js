(function () {
  "use strict";
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  /* ---------- Circuito de portada: Y = A·B + C' ---------- */
  var hero = $("#hero");
  if (hero) {
    var st = { A: 0, B: 0, C: 0 };
    var setOn = function (el, v) { if (el) { el.classList.toggle("on", !!v); } };
    var renderHero = function () {
      var AB = st.A & st.B, nC = st.C ? 0 : 1, Y = AB | nC;
      setOn($("#wA"), st.A); setOn($("#wB"), st.B); setOn($("#wC"), st.C);
      setOn($("#wAB"), AB); setOn($("#wNC"), nC); setOn($("#wY"), Y);
      setOn($("#lamp"), Y);
      ["A", "B", "C"].forEach(function (k) {
        var g = $("#sw" + k);
        setOn(g, st[k]);
        g.setAttribute("aria-checked", st[k] ? "true" : "false");
        $("text", g).textContent = k + "=" + st[k];
      });
      var idx = st.A * 4 + st.B * 2 + st.C;
      $$("#hero-tt tr[data-i]").forEach(function (tr) {
        tr.classList.toggle("hl", Number(tr.getAttribute("data-i")) === idx);
      });
      $("#hero-read").textContent =
        "A=" + st.A + ", B=" + st.B + ", C=" + st.C + "  →  A·B = " + AB + ", C' = " + nC + ", Y = " + Y;
    };
    $$(".sw", hero).forEach(function (g) {
      var flip = function () { var k = g.getAttribute("data-v"); st[k] = st[k] ? 0 : 1; renderHero(); };
      g.addEventListener("click", flip);
      g.addEventListener("keydown", function (e) {
        if (e.key === "Enter" || e.key === " ") { e.preventDefault(); flip(); }
      });
    });
    renderHero();
  }

  /* ---------- Conversor de bases ---------- */
  var conv = $("#conv");
  if (conv) {
    var valid = { 2: /^[01]+$/, 8: /^[0-7]+$/, 10: /^[0-9]+$/, 16: /^[0-9a-f]+$/i };
    var group = function (s, n) {
      var out = [];
      while (s.length % n) { s = "0" + s; }
      for (var i = 0; i < s.length; i += n) { out.push(s.slice(i, i + n)); }
      return out.join(" ");
    };
    var runConv = function () {
      var txt = $("#conv-in").value.trim();
      var base = Number($("#conv-base").value);
      var out = $("#conv-out");
      if (!txt) { out.textContent = "Escribe un número."; return; }
      if (!valid[base].test(txt)) { out.textContent = "Ese número no es válido en base " + base + "."; return; }
      var n = parseInt(txt, base);
      if (n > 4294967295) { out.textContent = "Usa un número menor que 4 294 967 296."; return; }
      var b = n.toString(2);
      out.textContent =
        "Decimal : " + n + "\n" +
        "Binario : " + group(b, 4) + "\n" +
        "Octal   : " + n.toString(8) + "\n" +
        "Hex     : " + n.toString(16).toUpperCase();
    };
    $("#conv-in").addEventListener("input", runConv);
    $("#conv-base").addEventListener("change", runConv);
    runConv();
  }

  /* ---------- Sumador / restador de 4 bits ---------- */
  var add = $("#adder");
  if (add) {
    var sg = function (x) { return x >= 8 ? x - 16 : x; };
    var bits4 = function (x) { var s = (x & 15).toString(2); while (s.length < 4) { s = "0" + s; } return s; };
    var runAdd = function () {
      var A = Number($("#ad-a").value), B = Number($("#ad-b").value), M = Number($("#ad-m").value);
      var out = $("#ad-out");
      if (!(A >= 0 && A <= 15 && B >= 0 && B <= 15) || A % 1 || B % 1) {
        out.innerHTML = "<p>Escribe A y B entre 0 y 15.</p>"; return;
      }
      var c = M, rows = "", S = 0, carries = [M];
      for (var i = 0; i < 4; i++) {
        var a = (A >> i) & 1, bb = (B >> i) & 1, bx = bb ^ M;
        var s = a ^ bx ^ c, co = (a & bx) | (a & c) | (bx & c);
        S |= s << i;
        rows += "<tr><td>" + i + "</td><td>" + a + "</td><td>" + bx + "</td><td>" + c + "</td><td>" + (a + bx + c) +
                "</td><td>" + s + "</td><td>" + co + "</td></tr>";
        c = co; carries.push(co);
      }
      var C3 = carries[3], C4 = carries[4], V = C3 ^ C4;
      var esperado = M ? sg(A) - sg(B) : sg(A) + sg(B);
      out.innerHTML =
        "<div class='wide'><table class='tt'><tr><th>Etapa</th><th>A</th><th>B⊕M</th><th>Cin</th><th># de 1</th><th>S</th><th>Cout</th></tr>" +
        rows + "</table></div>" +
        "<span class='out'>" + bits4(A) + (M ? " − " : " + ") + bits4(B) + " = " + bits4(S) + "  (Cout = " + C4 + ")<br>" +
        "Sin signo: " + A + (M ? " − " : " + ") + B + " → resultado " + S + "<br>" +
        "Con signo: " + sg(A) + (M ? " − " : " + ") + sg(B) + " = " + esperado + " → el circuito da " + sg(S) + "<br>" +
        "V = C3 ⊕ C4 = " + C3 + " ⊕ " + C4 + " = " + V + (V ? "  → hay overflow con signo" : "  → sin overflow con signo") + "</span>";
    };
    ["ad-a", "ad-b"].forEach(function (id) { $("#" + id).addEventListener("input", runAdd); });
    $("#ad-m").addEventListener("change", runAdd);
    runAdd();
  }
})();
