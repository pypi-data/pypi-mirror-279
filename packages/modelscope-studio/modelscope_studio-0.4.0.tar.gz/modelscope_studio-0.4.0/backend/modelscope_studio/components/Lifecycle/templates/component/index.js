function P() {
}
function nt(e) {
  return e();
}
function it(e) {
  e.forEach(nt);
}
function ot(e) {
  return typeof e == "function";
}
function at(e, t) {
  return e != e ? t == t : e !== t || e && typeof e == "object" || typeof e == "function";
}
function st(e, ...t) {
  if (e == null) {
    for (const n of t)
      n(void 0);
    return P;
  }
  const r = e.subscribe(...t);
  return r.unsubscribe ? () => r.unsubscribe() : r;
}
const A = [];
function ht(e, t) {
  return {
    subscribe: Q(e, t).subscribe
  };
}
function Q(e, t = P) {
  let r;
  const n = /* @__PURE__ */ new Set();
  function i(h) {
    if (at(e, h) && (e = h, r)) {
      const f = !A.length;
      for (const u of n)
        u[1](), A.push(u, e);
      if (f) {
        for (let u = 0; u < A.length; u += 2)
          A[u][0](A[u + 1]);
        A.length = 0;
      }
    }
  }
  function o(h) {
    i(h(e));
  }
  function a(h, f = P) {
    const u = [h, f];
    return n.add(u), n.size === 1 && (r = t(i, o) || P), h(e), () => {
      n.delete(u), n.size === 0 && r && (r(), r = null);
    };
  }
  return { set: i, update: o, subscribe: a };
}
function L(e, t, r) {
  const n = !Array.isArray(e), i = n ? [e] : e;
  if (!i.every(Boolean))
    throw new Error("derived() expects stores as input, got a falsy value");
  const o = t.length < 2;
  return ht(r, (a, h) => {
    let f = !1;
    const u = [];
    let s = 0, c = P;
    const l = () => {
      if (s)
        return;
      c();
      const x = t(n ? u[0] : u, a, h);
      o ? a(x) : c = ot(x) ? x : P;
    }, E = i.map(
      (x, d) => st(
        x,
        (y) => {
          u[d] = y, s &= ~(1 << d), f && l();
        },
        () => {
          s |= 1 << d;
        }
      )
    );
    return f = !0, l(), function() {
      it(E), c(), f = !1;
    };
  });
}
function ut(e) {
  return e && e.__esModule && Object.prototype.hasOwnProperty.call(e, "default") ? e.default : e;
}
var lt = function(t) {
  return ft(t) && !ct(t);
};
function ft(e) {
  return !!e && typeof e == "object";
}
function ct(e) {
  var t = Object.prototype.toString.call(e);
  return t === "[object RegExp]" || t === "[object Date]" || bt(e);
}
var mt = typeof Symbol == "function" && Symbol.for, pt = mt ? Symbol.for("react.element") : 60103;
function bt(e) {
  return e.$$typeof === pt;
}
function gt(e) {
  return Array.isArray(e) ? [] : {};
}
function G(e, t) {
  return t.clone !== !1 && t.isMergeableObject(e) ? N(gt(e), e, t) : e;
}
function Et(e, t, r) {
  return e.concat(t).map(function(n) {
    return G(n, r);
  });
}
function xt(e, t) {
  if (!t.customMerge)
    return N;
  var r = t.customMerge(e);
  return typeof r == "function" ? r : N;
}
function vt(e) {
  return Object.getOwnPropertySymbols ? Object.getOwnPropertySymbols(e).filter(function(t) {
    return Object.propertyIsEnumerable.call(e, t);
  }) : [];
}
function de(e) {
  return Object.keys(e).concat(vt(e));
}
function Ce(e, t) {
  try {
    return t in e;
  } catch {
    return !1;
  }
}
function dt(e, t) {
  return Ce(e, t) && !(Object.hasOwnProperty.call(e, t) && Object.propertyIsEnumerable.call(e, t));
}
function _t(e, t, r) {
  var n = {};
  return r.isMergeableObject(e) && de(e).forEach(function(i) {
    n[i] = G(e[i], r);
  }), de(t).forEach(function(i) {
    dt(e, i) || (Ce(e, i) && r.isMergeableObject(t[i]) ? n[i] = xt(i, r)(e[i], t[i], r) : n[i] = G(t[i], r));
  }), n;
}
function N(e, t, r) {
  r = r || {}, r.arrayMerge = r.arrayMerge || Et, r.isMergeableObject = r.isMergeableObject || lt, r.cloneUnlessOtherwiseSpecified = G;
  var n = Array.isArray(t), i = Array.isArray(e), o = n === i;
  return o ? n ? r.arrayMerge(e, t, r) : _t(e, t, r) : G(t, r);
}
N.all = function(t, r) {
  if (!Array.isArray(t))
    throw new Error("first argument should be an array");
  return t.reduce(function(n, i) {
    return N(n, i, r);
  }, {});
};
var yt = N, Ht = yt;
const Tt = /* @__PURE__ */ ut(Ht);
var ae = function(e, t) {
  return ae = Object.setPrototypeOf || { __proto__: [] } instanceof Array && function(r, n) {
    r.__proto__ = n;
  } || function(r, n) {
    for (var i in n)
      Object.prototype.hasOwnProperty.call(n, i) && (r[i] = n[i]);
  }, ae(e, t);
};
function q(e, t) {
  if (typeof t != "function" && t !== null)
    throw new TypeError("Class extends value " + String(t) + " is not a constructor or null");
  ae(e, t);
  function r() {
    this.constructor = e;
  }
  e.prototype = t === null ? Object.create(t) : (r.prototype = t.prototype, new r());
}
var b = function() {
  return b = Object.assign || function(t) {
    for (var r, n = 1, i = arguments.length; n < i; n++) {
      r = arguments[n];
      for (var o in r)
        Object.prototype.hasOwnProperty.call(r, o) && (t[o] = r[o]);
    }
    return t;
  }, b.apply(this, arguments);
};
function Bt(e, t) {
  var r = {};
  for (var n in e)
    Object.prototype.hasOwnProperty.call(e, n) && t.indexOf(n) < 0 && (r[n] = e[n]);
  if (e != null && typeof Object.getOwnPropertySymbols == "function")
    for (var i = 0, n = Object.getOwnPropertySymbols(e); i < n.length; i++)
      t.indexOf(n[i]) < 0 && Object.prototype.propertyIsEnumerable.call(e, n[i]) && (r[n[i]] = e[n[i]]);
  return r;
}
function $(e, t, r) {
  if (r || arguments.length === 2)
    for (var n = 0, i = t.length, o; n < i; n++)
      (o || !(n in t)) && (o || (o = Array.prototype.slice.call(t, 0, n)), o[n] = t[n]);
  return e.concat(o || Array.prototype.slice.call(t));
}
var m;
(function(e) {
  e[e.EXPECT_ARGUMENT_CLOSING_BRACE = 1] = "EXPECT_ARGUMENT_CLOSING_BRACE", e[e.EMPTY_ARGUMENT = 2] = "EMPTY_ARGUMENT", e[e.MALFORMED_ARGUMENT = 3] = "MALFORMED_ARGUMENT", e[e.EXPECT_ARGUMENT_TYPE = 4] = "EXPECT_ARGUMENT_TYPE", e[e.INVALID_ARGUMENT_TYPE = 5] = "INVALID_ARGUMENT_TYPE", e[e.EXPECT_ARGUMENT_STYLE = 6] = "EXPECT_ARGUMENT_STYLE", e[e.INVALID_NUMBER_SKELETON = 7] = "INVALID_NUMBER_SKELETON", e[e.INVALID_DATE_TIME_SKELETON = 8] = "INVALID_DATE_TIME_SKELETON", e[e.EXPECT_NUMBER_SKELETON = 9] = "EXPECT_NUMBER_SKELETON", e[e.EXPECT_DATE_TIME_SKELETON = 10] = "EXPECT_DATE_TIME_SKELETON", e[e.UNCLOSED_QUOTE_IN_ARGUMENT_STYLE = 11] = "UNCLOSED_QUOTE_IN_ARGUMENT_STYLE", e[e.EXPECT_SELECT_ARGUMENT_OPTIONS = 12] = "EXPECT_SELECT_ARGUMENT_OPTIONS", e[e.EXPECT_PLURAL_ARGUMENT_OFFSET_VALUE = 13] = "EXPECT_PLURAL_ARGUMENT_OFFSET_VALUE", e[e.INVALID_PLURAL_ARGUMENT_OFFSET_VALUE = 14] = "INVALID_PLURAL_ARGUMENT_OFFSET_VALUE", e[e.EXPECT_SELECT_ARGUMENT_SELECTOR = 15] = "EXPECT_SELECT_ARGUMENT_SELECTOR", e[e.EXPECT_PLURAL_ARGUMENT_SELECTOR = 16] = "EXPECT_PLURAL_ARGUMENT_SELECTOR", e[e.EXPECT_SELECT_ARGUMENT_SELECTOR_FRAGMENT = 17] = "EXPECT_SELECT_ARGUMENT_SELECTOR_FRAGMENT", e[e.EXPECT_PLURAL_ARGUMENT_SELECTOR_FRAGMENT = 18] = "EXPECT_PLURAL_ARGUMENT_SELECTOR_FRAGMENT", e[e.INVALID_PLURAL_ARGUMENT_SELECTOR = 19] = "INVALID_PLURAL_ARGUMENT_SELECTOR", e[e.DUPLICATE_PLURAL_ARGUMENT_SELECTOR = 20] = "DUPLICATE_PLURAL_ARGUMENT_SELECTOR", e[e.DUPLICATE_SELECT_ARGUMENT_SELECTOR = 21] = "DUPLICATE_SELECT_ARGUMENT_SELECTOR", e[e.MISSING_OTHER_CLAUSE = 22] = "MISSING_OTHER_CLAUSE", e[e.INVALID_TAG = 23] = "INVALID_TAG", e[e.INVALID_TAG_NAME = 25] = "INVALID_TAG_NAME", e[e.UNMATCHED_CLOSING_TAG = 26] = "UNMATCHED_CLOSING_TAG", e[e.UNCLOSED_TAG = 27] = "UNCLOSED_TAG";
})(m || (m = {}));
var g;
(function(e) {
  e[e.literal = 0] = "literal", e[e.argument = 1] = "argument", e[e.number = 2] = "number", e[e.date = 3] = "date", e[e.time = 4] = "time", e[e.select = 5] = "select", e[e.plural = 6] = "plural", e[e.pound = 7] = "pound", e[e.tag = 8] = "tag";
})(g || (g = {}));
var I;
(function(e) {
  e[e.number = 0] = "number", e[e.dateTime = 1] = "dateTime";
})(I || (I = {}));
function _e(e) {
  return e.type === g.literal;
}
function St(e) {
  return e.type === g.argument;
}
function Me(e) {
  return e.type === g.number;
}
function Re(e) {
  return e.type === g.date;
}
function Ue(e) {
  return e.type === g.time;
}
function Ge(e) {
  return e.type === g.select;
}
function De(e) {
  return e.type === g.plural;
}
function At(e) {
  return e.type === g.pound;
}
function Fe(e) {
  return e.type === g.tag;
}
function je(e) {
  return !!(e && typeof e == "object" && e.type === I.number);
}
function se(e) {
  return !!(e && typeof e == "object" && e.type === I.dateTime);
}
var Ve = /[ \xA0\u1680\u2000-\u200A\u202F\u205F\u3000]/, Pt = /(?:[Eec]{1,6}|G{1,5}|[Qq]{1,5}|(?:[yYur]+|U{1,5})|[ML]{1,5}|d{1,2}|D{1,3}|F{1}|[abB]{1,5}|[hkHK]{1,2}|w{1,2}|W{1}|m{1,2}|s{1,2}|[zZOvVxX]{1,4})(?=([^']*'[^']*')*[^']*$)/g;
function Nt(e) {
  var t = {};
  return e.replace(Pt, function(r) {
    var n = r.length;
    switch (r[0]) {
      case "G":
        t.era = n === 4 ? "long" : n === 5 ? "narrow" : "short";
        break;
      case "y":
        t.year = n === 2 ? "2-digit" : "numeric";
        break;
      case "Y":
      case "u":
      case "U":
      case "r":
        throw new RangeError("`Y/u/U/r` (year) patterns are not supported, use `y` instead");
      case "q":
      case "Q":
        throw new RangeError("`q/Q` (quarter) patterns are not supported");
      case "M":
      case "L":
        t.month = ["numeric", "2-digit", "short", "long", "narrow"][n - 1];
        break;
      case "w":
      case "W":
        throw new RangeError("`w/W` (week) patterns are not supported");
      case "d":
        t.day = ["numeric", "2-digit"][n - 1];
        break;
      case "D":
      case "F":
      case "g":
        throw new RangeError("`D/F/g` (day) patterns are not supported, use `d` instead");
      case "E":
        t.weekday = n === 4 ? "long" : n === 5 ? "narrow" : "short";
        break;
      case "e":
        if (n < 4)
          throw new RangeError("`e..eee` (weekday) patterns are not supported");
        t.weekday = ["short", "long", "narrow", "short"][n - 4];
        break;
      case "c":
        if (n < 4)
          throw new RangeError("`c..ccc` (weekday) patterns are not supported");
        t.weekday = ["short", "long", "narrow", "short"][n - 4];
        break;
      case "a":
        t.hour12 = !0;
        break;
      case "b":
      case "B":
        throw new RangeError("`b/B` (period) patterns are not supported, use `a` instead");
      case "h":
        t.hourCycle = "h12", t.hour = ["numeric", "2-digit"][n - 1];
        break;
      case "H":
        t.hourCycle = "h23", t.hour = ["numeric", "2-digit"][n - 1];
        break;
      case "K":
        t.hourCycle = "h11", t.hour = ["numeric", "2-digit"][n - 1];
        break;
      case "k":
        t.hourCycle = "h24", t.hour = ["numeric", "2-digit"][n - 1];
        break;
      case "j":
      case "J":
      case "C":
        throw new RangeError("`j/J/C` (hour) patterns are not supported, use `h/H/K/k` instead");
      case "m":
        t.minute = ["numeric", "2-digit"][n - 1];
        break;
      case "s":
        t.second = ["numeric", "2-digit"][n - 1];
        break;
      case "S":
      case "A":
        throw new RangeError("`S/A` (second) patterns are not supported, use `s` instead");
      case "z":
        t.timeZoneName = n < 4 ? "short" : "long";
        break;
      case "Z":
      case "O":
      case "v":
      case "V":
      case "X":
      case "x":
        throw new RangeError("`Z/O/v/V/X/x` (timeZone) patterns are not supported, use `z` instead");
    }
    return "";
  }), t;
}
var It = /[\t-\r \x85\u200E\u200F\u2028\u2029]/i;
function Ot(e) {
  if (e.length === 0)
    throw new Error("Number skeleton cannot be empty");
  for (var t = e.split(It).filter(function(l) {
    return l.length > 0;
  }), r = [], n = 0, i = t; n < i.length; n++) {
    var o = i[n], a = o.split("/");
    if (a.length === 0)
      throw new Error("Invalid number skeleton");
    for (var h = a[0], f = a.slice(1), u = 0, s = f; u < s.length; u++) {
      var c = s[u];
      if (c.length === 0)
        throw new Error("Invalid number skeleton");
    }
    r.push({ stem: h, options: f });
  }
  return r;
}
function wt(e) {
  return e.replace(/^(.*?)-/, "");
}
var ye = /^\.(?:(0+)(\*)?|(#+)|(0+)(#+))$/g, Xe = /^(@+)?(\+|#+)?[rs]?$/g, Lt = /(\*)(0+)|(#+)(0+)|(0+)/g, ke = /^(0+)$/;
function He(e) {
  var t = {};
  return e[e.length - 1] === "r" ? t.roundingPriority = "morePrecision" : e[e.length - 1] === "s" && (t.roundingPriority = "lessPrecision"), e.replace(Xe, function(r, n, i) {
    return typeof i != "string" ? (t.minimumSignificantDigits = n.length, t.maximumSignificantDigits = n.length) : i === "+" ? t.minimumSignificantDigits = n.length : n[0] === "#" ? t.maximumSignificantDigits = n.length : (t.minimumSignificantDigits = n.length, t.maximumSignificantDigits = n.length + (typeof i == "string" ? i.length : 0)), "";
  }), t;
}
function ze(e) {
  switch (e) {
    case "sign-auto":
      return {
        signDisplay: "auto"
      };
    case "sign-accounting":
    case "()":
      return {
        currencySign: "accounting"
      };
    case "sign-always":
    case "+!":
      return {
        signDisplay: "always"
      };
    case "sign-accounting-always":
    case "()!":
      return {
        signDisplay: "always",
        currencySign: "accounting"
      };
    case "sign-except-zero":
    case "+?":
      return {
        signDisplay: "exceptZero"
      };
    case "sign-accounting-except-zero":
    case "()?":
      return {
        signDisplay: "exceptZero",
        currencySign: "accounting"
      };
    case "sign-never":
    case "+_":
      return {
        signDisplay: "never"
      };
  }
}
function Ct(e) {
  var t;
  if (e[0] === "E" && e[1] === "E" ? (t = {
    notation: "engineering"
  }, e = e.slice(2)) : e[0] === "E" && (t = {
    notation: "scientific"
  }, e = e.slice(1)), t) {
    var r = e.slice(0, 2);
    if (r === "+!" ? (t.signDisplay = "always", e = e.slice(2)) : r === "+?" && (t.signDisplay = "exceptZero", e = e.slice(2)), !ke.test(e))
      throw new Error("Malformed concise eng/scientific notation");
    t.minimumIntegerDigits = e.length;
  }
  return t;
}
function Te(e) {
  var t = {}, r = ze(e);
  return r || t;
}
function Mt(e) {
  for (var t = {}, r = 0, n = e; r < n.length; r++) {
    var i = n[r];
    switch (i.stem) {
      case "percent":
      case "%":
        t.style = "percent";
        continue;
      case "%x100":
        t.style = "percent", t.scale = 100;
        continue;
      case "currency":
        t.style = "currency", t.currency = i.options[0];
        continue;
      case "group-off":
      case ",_":
        t.useGrouping = !1;
        continue;
      case "precision-integer":
      case ".":
        t.maximumFractionDigits = 0;
        continue;
      case "measure-unit":
      case "unit":
        t.style = "unit", t.unit = wt(i.options[0]);
        continue;
      case "compact-short":
      case "K":
        t.notation = "compact", t.compactDisplay = "short";
        continue;
      case "compact-long":
      case "KK":
        t.notation = "compact", t.compactDisplay = "long";
        continue;
      case "scientific":
        t = b(b(b({}, t), { notation: "scientific" }), i.options.reduce(function(f, u) {
          return b(b({}, f), Te(u));
        }, {}));
        continue;
      case "engineering":
        t = b(b(b({}, t), { notation: "engineering" }), i.options.reduce(function(f, u) {
          return b(b({}, f), Te(u));
        }, {}));
        continue;
      case "notation-simple":
        t.notation = "standard";
        continue;
      case "unit-width-narrow":
        t.currencyDisplay = "narrowSymbol", t.unitDisplay = "narrow";
        continue;
      case "unit-width-short":
        t.currencyDisplay = "code", t.unitDisplay = "short";
        continue;
      case "unit-width-full-name":
        t.currencyDisplay = "name", t.unitDisplay = "long";
        continue;
      case "unit-width-iso-code":
        t.currencyDisplay = "symbol";
        continue;
      case "scale":
        t.scale = parseFloat(i.options[0]);
        continue;
      case "integer-width":
        if (i.options.length > 1)
          throw new RangeError("integer-width stems only accept a single optional option");
        i.options[0].replace(Lt, function(f, u, s, c, l, E) {
          if (u)
            t.minimumIntegerDigits = s.length;
          else {
            if (c && l)
              throw new Error("We currently do not support maximum integer digits");
            if (E)
              throw new Error("We currently do not support exact integer digits");
          }
          return "";
        });
        continue;
    }
    if (ke.test(i.stem)) {
      t.minimumIntegerDigits = i.stem.length;
      continue;
    }
    if (ye.test(i.stem)) {
      if (i.options.length > 1)
        throw new RangeError("Fraction-precision stems only accept a single optional option");
      i.stem.replace(ye, function(f, u, s, c, l, E) {
        return s === "*" ? t.minimumFractionDigits = u.length : c && c[0] === "#" ? t.maximumFractionDigits = c.length : l && E ? (t.minimumFractionDigits = l.length, t.maximumFractionDigits = l.length + E.length) : (t.minimumFractionDigits = u.length, t.maximumFractionDigits = u.length), "";
      });
      var o = i.options[0];
      o === "w" ? t = b(b({}, t), { trailingZeroDisplay: "stripIfInteger" }) : o && (t = b(b({}, t), He(o)));
      continue;
    }
    if (Xe.test(i.stem)) {
      t = b(b({}, t), He(i.stem));
      continue;
    }
    var a = ze(i.stem);
    a && (t = b(b({}, t), a));
    var h = Ct(i.stem);
    h && (t = b(b({}, t), h));
  }
  return t;
}
var X = {
  "001": [
    "H",
    "h"
  ],
  AC: [
    "H",
    "h",
    "hb",
    "hB"
  ],
  AD: [
    "H",
    "hB"
  ],
  AE: [
    "h",
    "hB",
    "hb",
    "H"
  ],
  AF: [
    "H",
    "hb",
    "hB",
    "h"
  ],
  AG: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  AI: [
    "H",
    "h",
    "hb",
    "hB"
  ],
  AL: [
    "h",
    "H",
    "hB"
  ],
  AM: [
    "H",
    "hB"
  ],
  AO: [
    "H",
    "hB"
  ],
  AR: [
    "H",
    "h",
    "hB",
    "hb"
  ],
  AS: [
    "h",
    "H"
  ],
  AT: [
    "H",
    "hB"
  ],
  AU: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  AW: [
    "H",
    "hB"
  ],
  AX: [
    "H"
  ],
  AZ: [
    "H",
    "hB",
    "h"
  ],
  BA: [
    "H",
    "hB",
    "h"
  ],
  BB: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  BD: [
    "h",
    "hB",
    "H"
  ],
  BE: [
    "H",
    "hB"
  ],
  BF: [
    "H",
    "hB"
  ],
  BG: [
    "H",
    "hB",
    "h"
  ],
  BH: [
    "h",
    "hB",
    "hb",
    "H"
  ],
  BI: [
    "H",
    "h"
  ],
  BJ: [
    "H",
    "hB"
  ],
  BL: [
    "H",
    "hB"
  ],
  BM: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  BN: [
    "hb",
    "hB",
    "h",
    "H"
  ],
  BO: [
    "H",
    "hB",
    "h",
    "hb"
  ],
  BQ: [
    "H"
  ],
  BR: [
    "H",
    "hB"
  ],
  BS: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  BT: [
    "h",
    "H"
  ],
  BW: [
    "H",
    "h",
    "hb",
    "hB"
  ],
  BY: [
    "H",
    "h"
  ],
  BZ: [
    "H",
    "h",
    "hb",
    "hB"
  ],
  CA: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  CC: [
    "H",
    "h",
    "hb",
    "hB"
  ],
  CD: [
    "hB",
    "H"
  ],
  CF: [
    "H",
    "h",
    "hB"
  ],
  CG: [
    "H",
    "hB"
  ],
  CH: [
    "H",
    "hB",
    "h"
  ],
  CI: [
    "H",
    "hB"
  ],
  CK: [
    "H",
    "h",
    "hb",
    "hB"
  ],
  CL: [
    "H",
    "h",
    "hB",
    "hb"
  ],
  CM: [
    "H",
    "h",
    "hB"
  ],
  CN: [
    "H",
    "hB",
    "hb",
    "h"
  ],
  CO: [
    "h",
    "H",
    "hB",
    "hb"
  ],
  CP: [
    "H"
  ],
  CR: [
    "H",
    "h",
    "hB",
    "hb"
  ],
  CU: [
    "H",
    "h",
    "hB",
    "hb"
  ],
  CV: [
    "H",
    "hB"
  ],
  CW: [
    "H",
    "hB"
  ],
  CX: [
    "H",
    "h",
    "hb",
    "hB"
  ],
  CY: [
    "h",
    "H",
    "hb",
    "hB"
  ],
  CZ: [
    "H"
  ],
  DE: [
    "H",
    "hB"
  ],
  DG: [
    "H",
    "h",
    "hb",
    "hB"
  ],
  DJ: [
    "h",
    "H"
  ],
  DK: [
    "H"
  ],
  DM: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  DO: [
    "h",
    "H",
    "hB",
    "hb"
  ],
  DZ: [
    "h",
    "hB",
    "hb",
    "H"
  ],
  EA: [
    "H",
    "h",
    "hB",
    "hb"
  ],
  EC: [
    "H",
    "hB",
    "h",
    "hb"
  ],
  EE: [
    "H",
    "hB"
  ],
  EG: [
    "h",
    "hB",
    "hb",
    "H"
  ],
  EH: [
    "h",
    "hB",
    "hb",
    "H"
  ],
  ER: [
    "h",
    "H"
  ],
  ES: [
    "H",
    "hB",
    "h",
    "hb"
  ],
  ET: [
    "hB",
    "hb",
    "h",
    "H"
  ],
  FI: [
    "H"
  ],
  FJ: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  FK: [
    "H",
    "h",
    "hb",
    "hB"
  ],
  FM: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  FO: [
    "H",
    "h"
  ],
  FR: [
    "H",
    "hB"
  ],
  GA: [
    "H",
    "hB"
  ],
  GB: [
    "H",
    "h",
    "hb",
    "hB"
  ],
  GD: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  GE: [
    "H",
    "hB",
    "h"
  ],
  GF: [
    "H",
    "hB"
  ],
  GG: [
    "H",
    "h",
    "hb",
    "hB"
  ],
  GH: [
    "h",
    "H"
  ],
  GI: [
    "H",
    "h",
    "hb",
    "hB"
  ],
  GL: [
    "H",
    "h"
  ],
  GM: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  GN: [
    "H",
    "hB"
  ],
  GP: [
    "H",
    "hB"
  ],
  GQ: [
    "H",
    "hB",
    "h",
    "hb"
  ],
  GR: [
    "h",
    "H",
    "hb",
    "hB"
  ],
  GT: [
    "H",
    "h",
    "hB",
    "hb"
  ],
  GU: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  GW: [
    "H",
    "hB"
  ],
  GY: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  HK: [
    "h",
    "hB",
    "hb",
    "H"
  ],
  HN: [
    "H",
    "h",
    "hB",
    "hb"
  ],
  HR: [
    "H",
    "hB"
  ],
  HU: [
    "H",
    "h"
  ],
  IC: [
    "H",
    "h",
    "hB",
    "hb"
  ],
  ID: [
    "H"
  ],
  IE: [
    "H",
    "h",
    "hb",
    "hB"
  ],
  IL: [
    "H",
    "hB"
  ],
  IM: [
    "H",
    "h",
    "hb",
    "hB"
  ],
  IN: [
    "h",
    "H"
  ],
  IO: [
    "H",
    "h",
    "hb",
    "hB"
  ],
  IQ: [
    "h",
    "hB",
    "hb",
    "H"
  ],
  IR: [
    "hB",
    "H"
  ],
  IS: [
    "H"
  ],
  IT: [
    "H",
    "hB"
  ],
  JE: [
    "H",
    "h",
    "hb",
    "hB"
  ],
  JM: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  JO: [
    "h",
    "hB",
    "hb",
    "H"
  ],
  JP: [
    "H",
    "K",
    "h"
  ],
  KE: [
    "hB",
    "hb",
    "H",
    "h"
  ],
  KG: [
    "H",
    "h",
    "hB",
    "hb"
  ],
  KH: [
    "hB",
    "h",
    "H",
    "hb"
  ],
  KI: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  KM: [
    "H",
    "h",
    "hB",
    "hb"
  ],
  KN: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  KP: [
    "h",
    "H",
    "hB",
    "hb"
  ],
  KR: [
    "h",
    "H",
    "hB",
    "hb"
  ],
  KW: [
    "h",
    "hB",
    "hb",
    "H"
  ],
  KY: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  KZ: [
    "H",
    "hB"
  ],
  LA: [
    "H",
    "hb",
    "hB",
    "h"
  ],
  LB: [
    "h",
    "hB",
    "hb",
    "H"
  ],
  LC: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  LI: [
    "H",
    "hB",
    "h"
  ],
  LK: [
    "H",
    "h",
    "hB",
    "hb"
  ],
  LR: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  LS: [
    "h",
    "H"
  ],
  LT: [
    "H",
    "h",
    "hb",
    "hB"
  ],
  LU: [
    "H",
    "h",
    "hB"
  ],
  LV: [
    "H",
    "hB",
    "hb",
    "h"
  ],
  LY: [
    "h",
    "hB",
    "hb",
    "H"
  ],
  MA: [
    "H",
    "h",
    "hB",
    "hb"
  ],
  MC: [
    "H",
    "hB"
  ],
  MD: [
    "H",
    "hB"
  ],
  ME: [
    "H",
    "hB",
    "h"
  ],
  MF: [
    "H",
    "hB"
  ],
  MG: [
    "H",
    "h"
  ],
  MH: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  MK: [
    "H",
    "h",
    "hb",
    "hB"
  ],
  ML: [
    "H"
  ],
  MM: [
    "hB",
    "hb",
    "H",
    "h"
  ],
  MN: [
    "H",
    "h",
    "hb",
    "hB"
  ],
  MO: [
    "h",
    "hB",
    "hb",
    "H"
  ],
  MP: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  MQ: [
    "H",
    "hB"
  ],
  MR: [
    "h",
    "hB",
    "hb",
    "H"
  ],
  MS: [
    "H",
    "h",
    "hb",
    "hB"
  ],
  MT: [
    "H",
    "h"
  ],
  MU: [
    "H",
    "h"
  ],
  MV: [
    "H",
    "h"
  ],
  MW: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  MX: [
    "H",
    "h",
    "hB",
    "hb"
  ],
  MY: [
    "hb",
    "hB",
    "h",
    "H"
  ],
  MZ: [
    "H",
    "hB"
  ],
  NA: [
    "h",
    "H",
    "hB",
    "hb"
  ],
  NC: [
    "H",
    "hB"
  ],
  NE: [
    "H"
  ],
  NF: [
    "H",
    "h",
    "hb",
    "hB"
  ],
  NG: [
    "H",
    "h",
    "hb",
    "hB"
  ],
  NI: [
    "H",
    "h",
    "hB",
    "hb"
  ],
  NL: [
    "H",
    "hB"
  ],
  NO: [
    "H",
    "h"
  ],
  NP: [
    "H",
    "h",
    "hB"
  ],
  NR: [
    "H",
    "h",
    "hb",
    "hB"
  ],
  NU: [
    "H",
    "h",
    "hb",
    "hB"
  ],
  NZ: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  OM: [
    "h",
    "hB",
    "hb",
    "H"
  ],
  PA: [
    "h",
    "H",
    "hB",
    "hb"
  ],
  PE: [
    "H",
    "hB",
    "h",
    "hb"
  ],
  PF: [
    "H",
    "h",
    "hB"
  ],
  PG: [
    "h",
    "H"
  ],
  PH: [
    "h",
    "hB",
    "hb",
    "H"
  ],
  PK: [
    "h",
    "hB",
    "H"
  ],
  PL: [
    "H",
    "h"
  ],
  PM: [
    "H",
    "hB"
  ],
  PN: [
    "H",
    "h",
    "hb",
    "hB"
  ],
  PR: [
    "h",
    "H",
    "hB",
    "hb"
  ],
  PS: [
    "h",
    "hB",
    "hb",
    "H"
  ],
  PT: [
    "H",
    "hB"
  ],
  PW: [
    "h",
    "H"
  ],
  PY: [
    "H",
    "h",
    "hB",
    "hb"
  ],
  QA: [
    "h",
    "hB",
    "hb",
    "H"
  ],
  RE: [
    "H",
    "hB"
  ],
  RO: [
    "H",
    "hB"
  ],
  RS: [
    "H",
    "hB",
    "h"
  ],
  RU: [
    "H"
  ],
  RW: [
    "H",
    "h"
  ],
  SA: [
    "h",
    "hB",
    "hb",
    "H"
  ],
  SB: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  SC: [
    "H",
    "h",
    "hB"
  ],
  SD: [
    "h",
    "hB",
    "hb",
    "H"
  ],
  SE: [
    "H"
  ],
  SG: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  SH: [
    "H",
    "h",
    "hb",
    "hB"
  ],
  SI: [
    "H",
    "hB"
  ],
  SJ: [
    "H"
  ],
  SK: [
    "H"
  ],
  SL: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  SM: [
    "H",
    "h",
    "hB"
  ],
  SN: [
    "H",
    "h",
    "hB"
  ],
  SO: [
    "h",
    "H"
  ],
  SR: [
    "H",
    "hB"
  ],
  SS: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  ST: [
    "H",
    "hB"
  ],
  SV: [
    "H",
    "h",
    "hB",
    "hb"
  ],
  SX: [
    "H",
    "h",
    "hb",
    "hB"
  ],
  SY: [
    "h",
    "hB",
    "hb",
    "H"
  ],
  SZ: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  TA: [
    "H",
    "h",
    "hb",
    "hB"
  ],
  TC: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  TD: [
    "h",
    "H",
    "hB"
  ],
  TF: [
    "H",
    "h",
    "hB"
  ],
  TG: [
    "H",
    "hB"
  ],
  TH: [
    "H",
    "h"
  ],
  TJ: [
    "H",
    "h"
  ],
  TL: [
    "H",
    "hB",
    "hb",
    "h"
  ],
  TM: [
    "H",
    "h"
  ],
  TN: [
    "h",
    "hB",
    "hb",
    "H"
  ],
  TO: [
    "h",
    "H"
  ],
  TR: [
    "H",
    "hB"
  ],
  TT: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  TW: [
    "hB",
    "hb",
    "h",
    "H"
  ],
  TZ: [
    "hB",
    "hb",
    "H",
    "h"
  ],
  UA: [
    "H",
    "hB",
    "h"
  ],
  UG: [
    "hB",
    "hb",
    "H",
    "h"
  ],
  UM: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  US: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  UY: [
    "H",
    "h",
    "hB",
    "hb"
  ],
  UZ: [
    "H",
    "hB",
    "h"
  ],
  VA: [
    "H",
    "h",
    "hB"
  ],
  VC: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  VE: [
    "h",
    "H",
    "hB",
    "hb"
  ],
  VG: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  VI: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  VN: [
    "H",
    "h"
  ],
  VU: [
    "h",
    "H"
  ],
  WF: [
    "H",
    "hB"
  ],
  WS: [
    "h",
    "H"
  ],
  XK: [
    "H",
    "hB",
    "h"
  ],
  YE: [
    "h",
    "hB",
    "hb",
    "H"
  ],
  YT: [
    "H",
    "hB"
  ],
  ZA: [
    "H",
    "h",
    "hb",
    "hB"
  ],
  ZM: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  ZW: [
    "H",
    "h"
  ],
  "af-ZA": [
    "H",
    "h",
    "hB",
    "hb"
  ],
  "ar-001": [
    "h",
    "hB",
    "hb",
    "H"
  ],
  "ca-ES": [
    "H",
    "h",
    "hB"
  ],
  "en-001": [
    "h",
    "hb",
    "H",
    "hB"
  ],
  "es-BO": [
    "H",
    "h",
    "hB",
    "hb"
  ],
  "es-BR": [
    "H",
    "h",
    "hB",
    "hb"
  ],
  "es-EC": [
    "H",
    "h",
    "hB",
    "hb"
  ],
  "es-ES": [
    "H",
    "h",
    "hB",
    "hb"
  ],
  "es-GQ": [
    "H",
    "h",
    "hB",
    "hb"
  ],
  "es-PE": [
    "H",
    "h",
    "hB",
    "hb"
  ],
  "fr-CA": [
    "H",
    "h",
    "hB"
  ],
  "gl-ES": [
    "H",
    "h",
    "hB"
  ],
  "gu-IN": [
    "hB",
    "hb",
    "h",
    "H"
  ],
  "hi-IN": [
    "hB",
    "h",
    "H"
  ],
  "it-CH": [
    "H",
    "h",
    "hB"
  ],
  "it-IT": [
    "H",
    "h",
    "hB"
  ],
  "kn-IN": [
    "hB",
    "h",
    "H"
  ],
  "ml-IN": [
    "hB",
    "h",
    "H"
  ],
  "mr-IN": [
    "hB",
    "hb",
    "h",
    "H"
  ],
  "pa-IN": [
    "hB",
    "hb",
    "h",
    "H"
  ],
  "ta-IN": [
    "hB",
    "h",
    "hb",
    "H"
  ],
  "te-IN": [
    "hB",
    "h",
    "H"
  ],
  "zu-ZA": [
    "H",
    "hB",
    "hb",
    "h"
  ]
};
function Rt(e, t) {
  for (var r = "", n = 0; n < e.length; n++) {
    var i = e.charAt(n);
    if (i === "j") {
      for (var o = 0; n + 1 < e.length && e.charAt(n + 1) === i; )
        o++, n++;
      var a = 1 + (o & 1), h = o < 2 ? 1 : 3 + (o >> 1), f = "a", u = Ut(t);
      for ((u == "H" || u == "k") && (h = 0); h-- > 0; )
        r += f;
      for (; a-- > 0; )
        r = u + r;
    } else
      i === "J" ? r += "H" : r += i;
  }
  return r;
}
function Ut(e) {
  var t = e.hourCycle;
  if (t === void 0 && // @ts-ignore hourCycle(s) is not identified yet
  e.hourCycles && // @ts-ignore
  e.hourCycles.length && (t = e.hourCycles[0]), t)
    switch (t) {
      case "h24":
        return "k";
      case "h23":
        return "H";
      case "h12":
        return "h";
      case "h11":
        return "K";
      default:
        throw new Error("Invalid hourCycle");
    }
  var r = e.language, n;
  r !== "root" && (n = e.maximize().region);
  var i = X[n || ""] || X[r || ""] || X["".concat(r, "-001")] || X["001"];
  return i[0];
}
var ee, Gt = new RegExp("^".concat(Ve.source, "*")), Dt = new RegExp("".concat(Ve.source, "*$"));
function p(e, t) {
  return { start: e, end: t };
}
var Ft = !!String.prototype.startsWith && "_a".startsWith("a", 1), jt = !!String.fromCodePoint, Vt = !!Object.fromEntries, Xt = !!String.prototype.codePointAt, kt = !!String.prototype.trimStart, zt = !!String.prototype.trimEnd, Wt = !!Number.isSafeInteger, Zt = Wt ? Number.isSafeInteger : function(e) {
  return typeof e == "number" && isFinite(e) && Math.floor(e) === e && Math.abs(e) <= 9007199254740991;
}, he = !0;
try {
  var Qt = Ze("([^\\p{White_Space}\\p{Pattern_Syntax}]*)", "yu");
  he = ((ee = Qt.exec("a")) === null || ee === void 0 ? void 0 : ee[0]) === "a";
} catch {
  he = !1;
}
var Be = Ft ? (
  // Native
  function(t, r, n) {
    return t.startsWith(r, n);
  }
) : (
  // For IE11
  function(t, r, n) {
    return t.slice(n, n + r.length) === r;
  }
), ue = jt ? String.fromCodePoint : (
  // IE11
  function() {
    for (var t = [], r = 0; r < arguments.length; r++)
      t[r] = arguments[r];
    for (var n = "", i = t.length, o = 0, a; i > o; ) {
      if (a = t[o++], a > 1114111)
        throw RangeError(a + " is not a valid code point");
      n += a < 65536 ? String.fromCharCode(a) : String.fromCharCode(((a -= 65536) >> 10) + 55296, a % 1024 + 56320);
    }
    return n;
  }
), Se = (
  // native
  Vt ? Object.fromEntries : (
    // Ponyfill
    function(t) {
      for (var r = {}, n = 0, i = t; n < i.length; n++) {
        var o = i[n], a = o[0], h = o[1];
        r[a] = h;
      }
      return r;
    }
  )
), We = Xt ? (
  // Native
  function(t, r) {
    return t.codePointAt(r);
  }
) : (
  // IE 11
  function(t, r) {
    var n = t.length;
    if (!(r < 0 || r >= n)) {
      var i = t.charCodeAt(r), o;
      return i < 55296 || i > 56319 || r + 1 === n || (o = t.charCodeAt(r + 1)) < 56320 || o > 57343 ? i : (i - 55296 << 10) + (o - 56320) + 65536;
    }
  }
), qt = kt ? (
  // Native
  function(t) {
    return t.trimStart();
  }
) : (
  // Ponyfill
  function(t) {
    return t.replace(Gt, "");
  }
), Jt = zt ? (
  // Native
  function(t) {
    return t.trimEnd();
  }
) : (
  // Ponyfill
  function(t) {
    return t.replace(Dt, "");
  }
);
function Ze(e, t) {
  return new RegExp(e, t);
}
var le;
if (he) {
  var Ae = Ze("([^\\p{White_Space}\\p{Pattern_Syntax}]*)", "yu");
  le = function(t, r) {
    var n;
    Ae.lastIndex = r;
    var i = Ae.exec(t);
    return (n = i[1]) !== null && n !== void 0 ? n : "";
  };
} else
  le = function(t, r) {
    for (var n = []; ; ) {
      var i = We(t, r);
      if (i === void 0 || Qe(i) || er(i))
        break;
      n.push(i), r += i >= 65536 ? 2 : 1;
    }
    return ue.apply(void 0, n);
  };
var Yt = (
  /** @class */
  function() {
    function e(t, r) {
      r === void 0 && (r = {}), this.message = t, this.position = { offset: 0, line: 1, column: 1 }, this.ignoreTag = !!r.ignoreTag, this.locale = r.locale, this.requiresOtherClause = !!r.requiresOtherClause, this.shouldParseSkeletons = !!r.shouldParseSkeletons;
    }
    return e.prototype.parse = function() {
      if (this.offset() !== 0)
        throw Error("parser can only be used once");
      return this.parseMessage(0, "", !1);
    }, e.prototype.parseMessage = function(t, r, n) {
      for (var i = []; !this.isEOF(); ) {
        var o = this.char();
        if (o === 123) {
          var a = this.parseArgument(t, n);
          if (a.err)
            return a;
          i.push(a.val);
        } else {
          if (o === 125 && t > 0)
            break;
          if (o === 35 && (r === "plural" || r === "selectordinal")) {
            var h = this.clonePosition();
            this.bump(), i.push({
              type: g.pound,
              location: p(h, this.clonePosition())
            });
          } else if (o === 60 && !this.ignoreTag && this.peek() === 47) {
            if (n)
              break;
            return this.error(m.UNMATCHED_CLOSING_TAG, p(this.clonePosition(), this.clonePosition()));
          } else if (o === 60 && !this.ignoreTag && fe(this.peek() || 0)) {
            var a = this.parseTag(t, r);
            if (a.err)
              return a;
            i.push(a.val);
          } else {
            var a = this.parseLiteral(t, r);
            if (a.err)
              return a;
            i.push(a.val);
          }
        }
      }
      return { val: i, err: null };
    }, e.prototype.parseTag = function(t, r) {
      var n = this.clonePosition();
      this.bump();
      var i = this.parseTagName();
      if (this.bumpSpace(), this.bumpIf("/>"))
        return {
          val: {
            type: g.literal,
            value: "<".concat(i, "/>"),
            location: p(n, this.clonePosition())
          },
          err: null
        };
      if (this.bumpIf(">")) {
        var o = this.parseMessage(t + 1, r, !0);
        if (o.err)
          return o;
        var a = o.val, h = this.clonePosition();
        if (this.bumpIf("</")) {
          if (this.isEOF() || !fe(this.char()))
            return this.error(m.INVALID_TAG, p(h, this.clonePosition()));
          var f = this.clonePosition(), u = this.parseTagName();
          return i !== u ? this.error(m.UNMATCHED_CLOSING_TAG, p(f, this.clonePosition())) : (this.bumpSpace(), this.bumpIf(">") ? {
            val: {
              type: g.tag,
              value: i,
              children: a,
              location: p(n, this.clonePosition())
            },
            err: null
          } : this.error(m.INVALID_TAG, p(h, this.clonePosition())));
        } else
          return this.error(m.UNCLOSED_TAG, p(n, this.clonePosition()));
      } else
        return this.error(m.INVALID_TAG, p(n, this.clonePosition()));
    }, e.prototype.parseTagName = function() {
      var t = this.offset();
      for (this.bump(); !this.isEOF() && $t(this.char()); )
        this.bump();
      return this.message.slice(t, this.offset());
    }, e.prototype.parseLiteral = function(t, r) {
      for (var n = this.clonePosition(), i = ""; ; ) {
        var o = this.tryParseQuote(r);
        if (o) {
          i += o;
          continue;
        }
        var a = this.tryParseUnquoted(t, r);
        if (a) {
          i += a;
          continue;
        }
        var h = this.tryParseLeftAngleBracket();
        if (h) {
          i += h;
          continue;
        }
        break;
      }
      var f = p(n, this.clonePosition());
      return {
        val: { type: g.literal, value: i, location: f },
        err: null
      };
    }, e.prototype.tryParseLeftAngleBracket = function() {
      return !this.isEOF() && this.char() === 60 && (this.ignoreTag || // If at the opening tag or closing tag position, bail.
      !Kt(this.peek() || 0)) ? (this.bump(), "<") : null;
    }, e.prototype.tryParseQuote = function(t) {
      if (this.isEOF() || this.char() !== 39)
        return null;
      switch (this.peek()) {
        case 39:
          return this.bump(), this.bump(), "'";
        case 123:
        case 60:
        case 62:
        case 125:
          break;
        case 35:
          if (t === "plural" || t === "selectordinal")
            break;
          return null;
        default:
          return null;
      }
      this.bump();
      var r = [this.char()];
      for (this.bump(); !this.isEOF(); ) {
        var n = this.char();
        if (n === 39)
          if (this.peek() === 39)
            r.push(39), this.bump();
          else {
            this.bump();
            break;
          }
        else
          r.push(n);
        this.bump();
      }
      return ue.apply(void 0, r);
    }, e.prototype.tryParseUnquoted = function(t, r) {
      if (this.isEOF())
        return null;
      var n = this.char();
      return n === 60 || n === 123 || n === 35 && (r === "plural" || r === "selectordinal") || n === 125 && t > 0 ? null : (this.bump(), ue(n));
    }, e.prototype.parseArgument = function(t, r) {
      var n = this.clonePosition();
      if (this.bump(), this.bumpSpace(), this.isEOF())
        return this.error(m.EXPECT_ARGUMENT_CLOSING_BRACE, p(n, this.clonePosition()));
      if (this.char() === 125)
        return this.bump(), this.error(m.EMPTY_ARGUMENT, p(n, this.clonePosition()));
      var i = this.parseIdentifierIfPossible().value;
      if (!i)
        return this.error(m.MALFORMED_ARGUMENT, p(n, this.clonePosition()));
      if (this.bumpSpace(), this.isEOF())
        return this.error(m.EXPECT_ARGUMENT_CLOSING_BRACE, p(n, this.clonePosition()));
      switch (this.char()) {
        case 125:
          return this.bump(), {
            val: {
              type: g.argument,
              // value does not include the opening and closing braces.
              value: i,
              location: p(n, this.clonePosition())
            },
            err: null
          };
        case 44:
          return this.bump(), this.bumpSpace(), this.isEOF() ? this.error(m.EXPECT_ARGUMENT_CLOSING_BRACE, p(n, this.clonePosition())) : this.parseArgumentOptions(t, r, i, n);
        default:
          return this.error(m.MALFORMED_ARGUMENT, p(n, this.clonePosition()));
      }
    }, e.prototype.parseIdentifierIfPossible = function() {
      var t = this.clonePosition(), r = this.offset(), n = le(this.message, r), i = r + n.length;
      this.bumpTo(i);
      var o = this.clonePosition(), a = p(t, o);
      return { value: n, location: a };
    }, e.prototype.parseArgumentOptions = function(t, r, n, i) {
      var o, a = this.clonePosition(), h = this.parseIdentifierIfPossible().value, f = this.clonePosition();
      switch (h) {
        case "":
          return this.error(m.EXPECT_ARGUMENT_TYPE, p(a, f));
        case "number":
        case "date":
        case "time": {
          this.bumpSpace();
          var u = null;
          if (this.bumpIf(",")) {
            this.bumpSpace();
            var s = this.clonePosition(), c = this.parseSimpleArgStyleIfPossible();
            if (c.err)
              return c;
            var l = Jt(c.val);
            if (l.length === 0)
              return this.error(m.EXPECT_ARGUMENT_STYLE, p(this.clonePosition(), this.clonePosition()));
            var E = p(s, this.clonePosition());
            u = { style: l, styleLocation: E };
          }
          var x = this.tryParseArgumentClose(i);
          if (x.err)
            return x;
          var d = p(i, this.clonePosition());
          if (u && Be(u == null ? void 0 : u.style, "::", 0)) {
            var y = qt(u.style.slice(2));
            if (h === "number") {
              var c = this.parseNumberSkeletonFromString(y, u.styleLocation);
              return c.err ? c : {
                val: { type: g.number, value: n, location: d, style: c.val },
                err: null
              };
            } else {
              if (y.length === 0)
                return this.error(m.EXPECT_DATE_TIME_SKELETON, d);
              var M = y;
              this.locale && (M = Rt(y, this.locale));
              var l = {
                type: I.dateTime,
                pattern: M,
                location: u.styleLocation,
                parsedOptions: this.shouldParseSkeletons ? Nt(M) : {}
              }, S = h === "date" ? g.date : g.time;
              return {
                val: { type: S, value: n, location: d, style: l },
                err: null
              };
            }
          }
          return {
            val: {
              type: h === "number" ? g.number : h === "date" ? g.date : g.time,
              value: n,
              location: d,
              style: (o = u == null ? void 0 : u.style) !== null && o !== void 0 ? o : null
            },
            err: null
          };
        }
        case "plural":
        case "selectordinal":
        case "select": {
          var _ = this.clonePosition();
          if (this.bumpSpace(), !this.bumpIf(","))
            return this.error(m.EXPECT_SELECT_ARGUMENT_OPTIONS, p(_, b({}, _)));
          this.bumpSpace();
          var R = this.parseIdentifierIfPossible(), T = 0;
          if (h !== "select" && R.value === "offset") {
            if (!this.bumpIf(":"))
              return this.error(m.EXPECT_PLURAL_ARGUMENT_OFFSET_VALUE, p(this.clonePosition(), this.clonePosition()));
            this.bumpSpace();
            var c = this.tryParseDecimalInteger(m.EXPECT_PLURAL_ARGUMENT_OFFSET_VALUE, m.INVALID_PLURAL_ARGUMENT_OFFSET_VALUE);
            if (c.err)
              return c;
            this.bumpSpace(), R = this.parseIdentifierIfPossible(), T = c.val;
          }
          var V = this.tryParsePluralOrSelectOptions(t, h, r, R);
          if (V.err)
            return V;
          var x = this.tryParseArgumentClose(i);
          if (x.err)
            return x;
          var ve = p(i, this.clonePosition());
          return h === "select" ? {
            val: {
              type: g.select,
              value: n,
              options: Se(V.val),
              location: ve
            },
            err: null
          } : {
            val: {
              type: g.plural,
              value: n,
              options: Se(V.val),
              offset: T,
              pluralType: h === "plural" ? "cardinal" : "ordinal",
              location: ve
            },
            err: null
          };
        }
        default:
          return this.error(m.INVALID_ARGUMENT_TYPE, p(a, f));
      }
    }, e.prototype.tryParseArgumentClose = function(t) {
      return this.isEOF() || this.char() !== 125 ? this.error(m.EXPECT_ARGUMENT_CLOSING_BRACE, p(t, this.clonePosition())) : (this.bump(), { val: !0, err: null });
    }, e.prototype.parseSimpleArgStyleIfPossible = function() {
      for (var t = 0, r = this.clonePosition(); !this.isEOF(); ) {
        var n = this.char();
        switch (n) {
          case 39: {
            this.bump();
            var i = this.clonePosition();
            if (!this.bumpUntil("'"))
              return this.error(m.UNCLOSED_QUOTE_IN_ARGUMENT_STYLE, p(i, this.clonePosition()));
            this.bump();
            break;
          }
          case 123: {
            t += 1, this.bump();
            break;
          }
          case 125: {
            if (t > 0)
              t -= 1;
            else
              return {
                val: this.message.slice(r.offset, this.offset()),
                err: null
              };
            break;
          }
          default:
            this.bump();
            break;
        }
      }
      return {
        val: this.message.slice(r.offset, this.offset()),
        err: null
      };
    }, e.prototype.parseNumberSkeletonFromString = function(t, r) {
      var n = [];
      try {
        n = Ot(t);
      } catch {
        return this.error(m.INVALID_NUMBER_SKELETON, r);
      }
      return {
        val: {
          type: I.number,
          tokens: n,
          location: r,
          parsedOptions: this.shouldParseSkeletons ? Mt(n) : {}
        },
        err: null
      };
    }, e.prototype.tryParsePluralOrSelectOptions = function(t, r, n, i) {
      for (var o, a = !1, h = [], f = /* @__PURE__ */ new Set(), u = i.value, s = i.location; ; ) {
        if (u.length === 0) {
          var c = this.clonePosition();
          if (r !== "select" && this.bumpIf("=")) {
            var l = this.tryParseDecimalInteger(m.EXPECT_PLURAL_ARGUMENT_SELECTOR, m.INVALID_PLURAL_ARGUMENT_SELECTOR);
            if (l.err)
              return l;
            s = p(c, this.clonePosition()), u = this.message.slice(c.offset, this.offset());
          } else
            break;
        }
        if (f.has(u))
          return this.error(r === "select" ? m.DUPLICATE_SELECT_ARGUMENT_SELECTOR : m.DUPLICATE_PLURAL_ARGUMENT_SELECTOR, s);
        u === "other" && (a = !0), this.bumpSpace();
        var E = this.clonePosition();
        if (!this.bumpIf("{"))
          return this.error(r === "select" ? m.EXPECT_SELECT_ARGUMENT_SELECTOR_FRAGMENT : m.EXPECT_PLURAL_ARGUMENT_SELECTOR_FRAGMENT, p(this.clonePosition(), this.clonePosition()));
        var x = this.parseMessage(t + 1, r, n);
        if (x.err)
          return x;
        var d = this.tryParseArgumentClose(E);
        if (d.err)
          return d;
        h.push([
          u,
          {
            value: x.val,
            location: p(E, this.clonePosition())
          }
        ]), f.add(u), this.bumpSpace(), o = this.parseIdentifierIfPossible(), u = o.value, s = o.location;
      }
      return h.length === 0 ? this.error(r === "select" ? m.EXPECT_SELECT_ARGUMENT_SELECTOR : m.EXPECT_PLURAL_ARGUMENT_SELECTOR, p(this.clonePosition(), this.clonePosition())) : this.requiresOtherClause && !a ? this.error(m.MISSING_OTHER_CLAUSE, p(this.clonePosition(), this.clonePosition())) : { val: h, err: null };
    }, e.prototype.tryParseDecimalInteger = function(t, r) {
      var n = 1, i = this.clonePosition();
      this.bumpIf("+") || this.bumpIf("-") && (n = -1);
      for (var o = !1, a = 0; !this.isEOF(); ) {
        var h = this.char();
        if (h >= 48 && h <= 57)
          o = !0, a = a * 10 + (h - 48), this.bump();
        else
          break;
      }
      var f = p(i, this.clonePosition());
      return o ? (a *= n, Zt(a) ? { val: a, err: null } : this.error(r, f)) : this.error(t, f);
    }, e.prototype.offset = function() {
      return this.position.offset;
    }, e.prototype.isEOF = function() {
      return this.offset() === this.message.length;
    }, e.prototype.clonePosition = function() {
      return {
        offset: this.position.offset,
        line: this.position.line,
        column: this.position.column
      };
    }, e.prototype.char = function() {
      var t = this.position.offset;
      if (t >= this.message.length)
        throw Error("out of bound");
      var r = We(this.message, t);
      if (r === void 0)
        throw Error("Offset ".concat(t, " is at invalid UTF-16 code unit boundary"));
      return r;
    }, e.prototype.error = function(t, r) {
      return {
        val: null,
        err: {
          kind: t,
          message: this.message,
          location: r
        }
      };
    }, e.prototype.bump = function() {
      if (!this.isEOF()) {
        var t = this.char();
        t === 10 ? (this.position.line += 1, this.position.column = 1, this.position.offset += 1) : (this.position.column += 1, this.position.offset += t < 65536 ? 1 : 2);
      }
    }, e.prototype.bumpIf = function(t) {
      if (Be(this.message, t, this.offset())) {
        for (var r = 0; r < t.length; r++)
          this.bump();
        return !0;
      }
      return !1;
    }, e.prototype.bumpUntil = function(t) {
      var r = this.offset(), n = this.message.indexOf(t, r);
      return n >= 0 ? (this.bumpTo(n), !0) : (this.bumpTo(this.message.length), !1);
    }, e.prototype.bumpTo = function(t) {
      if (this.offset() > t)
        throw Error("targetOffset ".concat(t, " must be greater than or equal to the current offset ").concat(this.offset()));
      for (t = Math.min(t, this.message.length); ; ) {
        var r = this.offset();
        if (r === t)
          break;
        if (r > t)
          throw Error("targetOffset ".concat(t, " is at invalid UTF-16 code unit boundary"));
        if (this.bump(), this.isEOF())
          break;
      }
    }, e.prototype.bumpSpace = function() {
      for (; !this.isEOF() && Qe(this.char()); )
        this.bump();
    }, e.prototype.peek = function() {
      if (this.isEOF())
        return null;
      var t = this.char(), r = this.offset(), n = this.message.charCodeAt(r + (t >= 65536 ? 2 : 1));
      return n ?? null;
    }, e;
  }()
);
function fe(e) {
  return e >= 97 && e <= 122 || e >= 65 && e <= 90;
}
function Kt(e) {
  return fe(e) || e === 47;
}
function $t(e) {
  return e === 45 || e === 46 || e >= 48 && e <= 57 || e === 95 || e >= 97 && e <= 122 || e >= 65 && e <= 90 || e == 183 || e >= 192 && e <= 214 || e >= 216 && e <= 246 || e >= 248 && e <= 893 || e >= 895 && e <= 8191 || e >= 8204 && e <= 8205 || e >= 8255 && e <= 8256 || e >= 8304 && e <= 8591 || e >= 11264 && e <= 12271 || e >= 12289 && e <= 55295 || e >= 63744 && e <= 64975 || e >= 65008 && e <= 65533 || e >= 65536 && e <= 983039;
}
function Qe(e) {
  return e >= 9 && e <= 13 || e === 32 || e === 133 || e >= 8206 && e <= 8207 || e === 8232 || e === 8233;
}
function er(e) {
  return e >= 33 && e <= 35 || e === 36 || e >= 37 && e <= 39 || e === 40 || e === 41 || e === 42 || e === 43 || e === 44 || e === 45 || e >= 46 && e <= 47 || e >= 58 && e <= 59 || e >= 60 && e <= 62 || e >= 63 && e <= 64 || e === 91 || e === 92 || e === 93 || e === 94 || e === 96 || e === 123 || e === 124 || e === 125 || e === 126 || e === 161 || e >= 162 && e <= 165 || e === 166 || e === 167 || e === 169 || e === 171 || e === 172 || e === 174 || e === 176 || e === 177 || e === 182 || e === 187 || e === 191 || e === 215 || e === 247 || e >= 8208 && e <= 8213 || e >= 8214 && e <= 8215 || e === 8216 || e === 8217 || e === 8218 || e >= 8219 && e <= 8220 || e === 8221 || e === 8222 || e === 8223 || e >= 8224 && e <= 8231 || e >= 8240 && e <= 8248 || e === 8249 || e === 8250 || e >= 8251 && e <= 8254 || e >= 8257 && e <= 8259 || e === 8260 || e === 8261 || e === 8262 || e >= 8263 && e <= 8273 || e === 8274 || e === 8275 || e >= 8277 && e <= 8286 || e >= 8592 && e <= 8596 || e >= 8597 && e <= 8601 || e >= 8602 && e <= 8603 || e >= 8604 && e <= 8607 || e === 8608 || e >= 8609 && e <= 8610 || e === 8611 || e >= 8612 && e <= 8613 || e === 8614 || e >= 8615 && e <= 8621 || e === 8622 || e >= 8623 && e <= 8653 || e >= 8654 && e <= 8655 || e >= 8656 && e <= 8657 || e === 8658 || e === 8659 || e === 8660 || e >= 8661 && e <= 8691 || e >= 8692 && e <= 8959 || e >= 8960 && e <= 8967 || e === 8968 || e === 8969 || e === 8970 || e === 8971 || e >= 8972 && e <= 8991 || e >= 8992 && e <= 8993 || e >= 8994 && e <= 9e3 || e === 9001 || e === 9002 || e >= 9003 && e <= 9083 || e === 9084 || e >= 9085 && e <= 9114 || e >= 9115 && e <= 9139 || e >= 9140 && e <= 9179 || e >= 9180 && e <= 9185 || e >= 9186 && e <= 9254 || e >= 9255 && e <= 9279 || e >= 9280 && e <= 9290 || e >= 9291 && e <= 9311 || e >= 9472 && e <= 9654 || e === 9655 || e >= 9656 && e <= 9664 || e === 9665 || e >= 9666 && e <= 9719 || e >= 9720 && e <= 9727 || e >= 9728 && e <= 9838 || e === 9839 || e >= 9840 && e <= 10087 || e === 10088 || e === 10089 || e === 10090 || e === 10091 || e === 10092 || e === 10093 || e === 10094 || e === 10095 || e === 10096 || e === 10097 || e === 10098 || e === 10099 || e === 10100 || e === 10101 || e >= 10132 && e <= 10175 || e >= 10176 && e <= 10180 || e === 10181 || e === 10182 || e >= 10183 && e <= 10213 || e === 10214 || e === 10215 || e === 10216 || e === 10217 || e === 10218 || e === 10219 || e === 10220 || e === 10221 || e === 10222 || e === 10223 || e >= 10224 && e <= 10239 || e >= 10240 && e <= 10495 || e >= 10496 && e <= 10626 || e === 10627 || e === 10628 || e === 10629 || e === 10630 || e === 10631 || e === 10632 || e === 10633 || e === 10634 || e === 10635 || e === 10636 || e === 10637 || e === 10638 || e === 10639 || e === 10640 || e === 10641 || e === 10642 || e === 10643 || e === 10644 || e === 10645 || e === 10646 || e === 10647 || e === 10648 || e >= 10649 && e <= 10711 || e === 10712 || e === 10713 || e === 10714 || e === 10715 || e >= 10716 && e <= 10747 || e === 10748 || e === 10749 || e >= 10750 && e <= 11007 || e >= 11008 && e <= 11055 || e >= 11056 && e <= 11076 || e >= 11077 && e <= 11078 || e >= 11079 && e <= 11084 || e >= 11085 && e <= 11123 || e >= 11124 && e <= 11125 || e >= 11126 && e <= 11157 || e === 11158 || e >= 11159 && e <= 11263 || e >= 11776 && e <= 11777 || e === 11778 || e === 11779 || e === 11780 || e === 11781 || e >= 11782 && e <= 11784 || e === 11785 || e === 11786 || e === 11787 || e === 11788 || e === 11789 || e >= 11790 && e <= 11798 || e === 11799 || e >= 11800 && e <= 11801 || e === 11802 || e === 11803 || e === 11804 || e === 11805 || e >= 11806 && e <= 11807 || e === 11808 || e === 11809 || e === 11810 || e === 11811 || e === 11812 || e === 11813 || e === 11814 || e === 11815 || e === 11816 || e === 11817 || e >= 11818 && e <= 11822 || e === 11823 || e >= 11824 && e <= 11833 || e >= 11834 && e <= 11835 || e >= 11836 && e <= 11839 || e === 11840 || e === 11841 || e === 11842 || e >= 11843 && e <= 11855 || e >= 11856 && e <= 11857 || e === 11858 || e >= 11859 && e <= 11903 || e >= 12289 && e <= 12291 || e === 12296 || e === 12297 || e === 12298 || e === 12299 || e === 12300 || e === 12301 || e === 12302 || e === 12303 || e === 12304 || e === 12305 || e >= 12306 && e <= 12307 || e === 12308 || e === 12309 || e === 12310 || e === 12311 || e === 12312 || e === 12313 || e === 12314 || e === 12315 || e === 12316 || e === 12317 || e >= 12318 && e <= 12319 || e === 12320 || e === 12336 || e === 64830 || e === 64831 || e >= 65093 && e <= 65094;
}
function ce(e) {
  e.forEach(function(t) {
    if (delete t.location, Ge(t) || De(t))
      for (var r in t.options)
        delete t.options[r].location, ce(t.options[r].value);
    else
      Me(t) && je(t.style) || (Re(t) || Ue(t)) && se(t.style) ? delete t.style.location : Fe(t) && ce(t.children);
  });
}
function tr(e, t) {
  t === void 0 && (t = {}), t = b({ shouldParseSkeletons: !0, requiresOtherClause: !0 }, t);
  var r = new Yt(e, t).parse();
  if (r.err) {
    var n = SyntaxError(m[r.err.kind]);
    throw n.location = r.err.location, n.originalMessage = r.err.message, n;
  }
  return t != null && t.captureLocation || ce(r.val), r.val;
}
function te(e, t) {
  var r = t && t.cache ? t.cache : sr, n = t && t.serializer ? t.serializer : ar, i = t && t.strategy ? t.strategy : nr;
  return i(e, {
    cache: r,
    serializer: n
  });
}
function rr(e) {
  return e == null || typeof e == "number" || typeof e == "boolean";
}
function qe(e, t, r, n) {
  var i = rr(n) ? n : r(n), o = t.get(i);
  return typeof o > "u" && (o = e.call(this, n), t.set(i, o)), o;
}
function Je(e, t, r) {
  var n = Array.prototype.slice.call(arguments, 3), i = r(n), o = t.get(i);
  return typeof o > "u" && (o = e.apply(this, n), t.set(i, o)), o;
}
function be(e, t, r, n, i) {
  return r.bind(t, e, n, i);
}
function nr(e, t) {
  var r = e.length === 1 ? qe : Je;
  return be(e, this, r, t.cache.create(), t.serializer);
}
function ir(e, t) {
  return be(e, this, Je, t.cache.create(), t.serializer);
}
function or(e, t) {
  return be(e, this, qe, t.cache.create(), t.serializer);
}
var ar = function() {
  return JSON.stringify(arguments);
};
function ge() {
  this.cache = /* @__PURE__ */ Object.create(null);
}
ge.prototype.get = function(e) {
  return this.cache[e];
};
ge.prototype.set = function(e, t) {
  this.cache[e] = t;
};
var sr = {
  create: function() {
    return new ge();
  }
}, re = {
  variadic: ir,
  monadic: or
}, O;
(function(e) {
  e.MISSING_VALUE = "MISSING_VALUE", e.INVALID_VALUE = "INVALID_VALUE", e.MISSING_INTL_API = "MISSING_INTL_API";
})(O || (O = {}));
var J = (
  /** @class */
  function(e) {
    q(t, e);
    function t(r, n, i) {
      var o = e.call(this, r) || this;
      return o.code = n, o.originalMessage = i, o;
    }
    return t.prototype.toString = function() {
      return "[formatjs Error: ".concat(this.code, "] ").concat(this.message);
    }, t;
  }(Error)
), Pe = (
  /** @class */
  function(e) {
    q(t, e);
    function t(r, n, i, o) {
      return e.call(this, 'Invalid values for "'.concat(r, '": "').concat(n, '". Options are "').concat(Object.keys(i).join('", "'), '"'), O.INVALID_VALUE, o) || this;
    }
    return t;
  }(J)
), hr = (
  /** @class */
  function(e) {
    q(t, e);
    function t(r, n, i) {
      return e.call(this, 'Value for "'.concat(r, '" must be of type ').concat(n), O.INVALID_VALUE, i) || this;
    }
    return t;
  }(J)
), ur = (
  /** @class */
  function(e) {
    q(t, e);
    function t(r, n) {
      return e.call(this, 'The intl string context variable "'.concat(r, '" was not provided to the string "').concat(n, '"'), O.MISSING_VALUE, n) || this;
    }
    return t;
  }(J)
), v;
(function(e) {
  e[e.literal = 0] = "literal", e[e.object = 1] = "object";
})(v || (v = {}));
function lr(e) {
  return e.length < 2 ? e : e.reduce(function(t, r) {
    var n = t[t.length - 1];
    return !n || n.type !== v.literal || r.type !== v.literal ? t.push(r) : n.value += r.value, t;
  }, []);
}
function fr(e) {
  return typeof e == "function";
}
function k(e, t, r, n, i, o, a) {
  if (e.length === 1 && _e(e[0]))
    return [
      {
        type: v.literal,
        value: e[0].value
      }
    ];
  for (var h = [], f = 0, u = e; f < u.length; f++) {
    var s = u[f];
    if (_e(s)) {
      h.push({
        type: v.literal,
        value: s.value
      });
      continue;
    }
    if (At(s)) {
      typeof o == "number" && h.push({
        type: v.literal,
        value: r.getNumberFormat(t).format(o)
      });
      continue;
    }
    var c = s.value;
    if (!(i && c in i))
      throw new ur(c, a);
    var l = i[c];
    if (St(s)) {
      (!l || typeof l == "string" || typeof l == "number") && (l = typeof l == "string" || typeof l == "number" ? String(l) : ""), h.push({
        type: typeof l == "string" ? v.literal : v.object,
        value: l
      });
      continue;
    }
    if (Re(s)) {
      var E = typeof s.style == "string" ? n.date[s.style] : se(s.style) ? s.style.parsedOptions : void 0;
      h.push({
        type: v.literal,
        value: r.getDateTimeFormat(t, E).format(l)
      });
      continue;
    }
    if (Ue(s)) {
      var E = typeof s.style == "string" ? n.time[s.style] : se(s.style) ? s.style.parsedOptions : n.time.medium;
      h.push({
        type: v.literal,
        value: r.getDateTimeFormat(t, E).format(l)
      });
      continue;
    }
    if (Me(s)) {
      var E = typeof s.style == "string" ? n.number[s.style] : je(s.style) ? s.style.parsedOptions : void 0;
      E && E.scale && (l = l * (E.scale || 1)), h.push({
        type: v.literal,
        value: r.getNumberFormat(t, E).format(l)
      });
      continue;
    }
    if (Fe(s)) {
      var x = s.children, d = s.value, y = i[d];
      if (!fr(y))
        throw new hr(d, "function", a);
      var M = k(x, t, r, n, i, o), S = y(M.map(function(T) {
        return T.value;
      }));
      Array.isArray(S) || (S = [S]), h.push.apply(h, S.map(function(T) {
        return {
          type: typeof T == "string" ? v.literal : v.object,
          value: T
        };
      }));
    }
    if (Ge(s)) {
      var _ = s.options[l] || s.options.other;
      if (!_)
        throw new Pe(s.value, l, Object.keys(s.options), a);
      h.push.apply(h, k(_.value, t, r, n, i));
      continue;
    }
    if (De(s)) {
      var _ = s.options["=".concat(l)];
      if (!_) {
        if (!Intl.PluralRules)
          throw new J(`Intl.PluralRules is not available in this environment.
Try polyfilling it using "@formatjs/intl-pluralrules"
`, O.MISSING_INTL_API, a);
        var R = r.getPluralRules(t, { type: s.pluralType }).select(l - (s.offset || 0));
        _ = s.options[R] || s.options.other;
      }
      if (!_)
        throw new Pe(s.value, l, Object.keys(s.options), a);
      h.push.apply(h, k(_.value, t, r, n, i, l - (s.offset || 0)));
      continue;
    }
  }
  return lr(h);
}
function cr(e, t) {
  return t ? b(b(b({}, e || {}), t || {}), Object.keys(e).reduce(function(r, n) {
    return r[n] = b(b({}, e[n]), t[n] || {}), r;
  }, {})) : e;
}
function mr(e, t) {
  return t ? Object.keys(e).reduce(function(r, n) {
    return r[n] = cr(e[n], t[n]), r;
  }, b({}, e)) : e;
}
function ne(e) {
  return {
    create: function() {
      return {
        get: function(t) {
          return e[t];
        },
        set: function(t, r) {
          e[t] = r;
        }
      };
    }
  };
}
function pr(e) {
  return e === void 0 && (e = {
    number: {},
    dateTime: {},
    pluralRules: {}
  }), {
    getNumberFormat: te(function() {
      for (var t, r = [], n = 0; n < arguments.length; n++)
        r[n] = arguments[n];
      return new ((t = Intl.NumberFormat).bind.apply(t, $([void 0], r, !1)))();
    }, {
      cache: ne(e.number),
      strategy: re.variadic
    }),
    getDateTimeFormat: te(function() {
      for (var t, r = [], n = 0; n < arguments.length; n++)
        r[n] = arguments[n];
      return new ((t = Intl.DateTimeFormat).bind.apply(t, $([void 0], r, !1)))();
    }, {
      cache: ne(e.dateTime),
      strategy: re.variadic
    }),
    getPluralRules: te(function() {
      for (var t, r = [], n = 0; n < arguments.length; n++)
        r[n] = arguments[n];
      return new ((t = Intl.PluralRules).bind.apply(t, $([void 0], r, !1)))();
    }, {
      cache: ne(e.pluralRules),
      strategy: re.variadic
    })
  };
}
var br = (
  /** @class */
  function() {
    function e(t, r, n, i) {
      var o = this;
      if (r === void 0 && (r = e.defaultLocale), this.formatterCache = {
        number: {},
        dateTime: {},
        pluralRules: {}
      }, this.format = function(f) {
        var u = o.formatToParts(f);
        if (u.length === 1)
          return u[0].value;
        var s = u.reduce(function(c, l) {
          return !c.length || l.type !== v.literal || typeof c[c.length - 1] != "string" ? c.push(l.value) : c[c.length - 1] += l.value, c;
        }, []);
        return s.length <= 1 ? s[0] || "" : s;
      }, this.formatToParts = function(f) {
        return k(o.ast, o.locales, o.formatters, o.formats, f, void 0, o.message);
      }, this.resolvedOptions = function() {
        var f;
        return {
          locale: ((f = o.resolvedLocale) === null || f === void 0 ? void 0 : f.toString()) || Intl.NumberFormat.supportedLocalesOf(o.locales)[0]
        };
      }, this.getAst = function() {
        return o.ast;
      }, this.locales = r, this.resolvedLocale = e.resolveLocale(r), typeof t == "string") {
        if (this.message = t, !e.__parse)
          throw new TypeError("IntlMessageFormat.__parse must be set to process `message` of type `string`");
        var a = i || {};
        a.formatters;
        var h = Bt(a, ["formatters"]);
        this.ast = e.__parse(t, b(b({}, h), { locale: this.resolvedLocale }));
      } else
        this.ast = t;
      if (!Array.isArray(this.ast))
        throw new TypeError("A message must be provided as a String or AST.");
      this.formats = mr(e.formats, n), this.formatters = i && i.formatters || pr(this.formatterCache);
    }
    return Object.defineProperty(e, "defaultLocale", {
      get: function() {
        return e.memoizedDefaultLocale || (e.memoizedDefaultLocale = new Intl.NumberFormat().resolvedOptions().locale), e.memoizedDefaultLocale;
      },
      enumerable: !1,
      configurable: !0
    }), e.memoizedDefaultLocale = null, e.resolveLocale = function(t) {
      if (!(typeof Intl.Locale > "u")) {
        var r = Intl.NumberFormat.supportedLocalesOf(t);
        return r.length > 0 ? new Intl.Locale(r[0]) : new Intl.Locale(typeof t == "string" ? t : t[0]);
      }
    }, e.__parse = tr, e.formats = {
      number: {
        integer: {
          maximumFractionDigits: 0
        },
        currency: {
          style: "currency"
        },
        percent: {
          style: "percent"
        }
      },
      date: {
        short: {
          month: "numeric",
          day: "numeric",
          year: "2-digit"
        },
        medium: {
          month: "short",
          day: "numeric",
          year: "numeric"
        },
        long: {
          month: "long",
          day: "numeric",
          year: "numeric"
        },
        full: {
          weekday: "long",
          month: "long",
          day: "numeric",
          year: "numeric"
        }
      },
      time: {
        short: {
          hour: "numeric",
          minute: "numeric"
        },
        medium: {
          hour: "numeric",
          minute: "numeric",
          second: "numeric"
        },
        long: {
          hour: "numeric",
          minute: "numeric",
          second: "numeric",
          timeZoneName: "short"
        },
        full: {
          hour: "numeric",
          minute: "numeric",
          second: "numeric",
          timeZoneName: "short"
        }
      }
    }, e;
  }()
);
function gr(e, t) {
  if (t == null)
    return;
  if (t in e)
    return e[t];
  const r = t.split(".");
  let n = e;
  for (let i = 0; i < r.length; i++)
    if (typeof n == "object") {
      if (i > 0) {
        const o = r.slice(i, r.length).join(".");
        if (o in n) {
          n = n[o];
          break;
        }
      }
      n = n[r[i]];
    } else
      n = void 0;
  return n;
}
const H = {}, Er = (e, t, r) => r && (t in H || (H[t] = {}), e in H[t] || (H[t][e] = r), r), Ye = (e, t) => {
  if (t == null)
    return;
  if (t in H && e in H[t])
    return H[t][e];
  const r = Y(t);
  for (let n = 0; n < r.length; n++) {
    const i = r[n], o = vr(i, e);
    if (o)
      return Er(e, t, o);
  }
};
let Ee;
const F = Q({});
function xr(e) {
  return Ee[e] || null;
}
function Ke(e) {
  return e in Ee;
}
function vr(e, t) {
  if (!Ke(e))
    return null;
  const r = xr(e);
  return gr(r, t);
}
function dr(e) {
  if (e == null)
    return;
  const t = Y(e);
  for (let r = 0; r < t.length; r++) {
    const n = t[r];
    if (Ke(n))
      return n;
  }
}
function _r(e, ...t) {
  delete H[e], F.update((r) => (r[e] = Tt.all([r[e] || {}, ...t]), r));
}
L(
  [F],
  ([e]) => Object.keys(e)
);
F.subscribe((e) => Ee = e);
const z = {};
function yr(e, t) {
  z[e].delete(t), z[e].size === 0 && delete z[e];
}
function $e(e) {
  return z[e];
}
function Hr(e) {
  return Y(e).map((t) => {
    const r = $e(t);
    return [t, r ? [...r] : []];
  }).filter(([, t]) => t.length > 0);
}
function me(e) {
  return e == null ? !1 : Y(e).some(
    (t) => {
      var r;
      return (r = $e(t)) == null ? void 0 : r.size;
    }
  );
}
function Tr(e, t) {
  return Promise.all(
    t.map((n) => (yr(e, n), n().then((i) => i.default || i)))
  ).then((n) => _r(e, ...n));
}
const U = {};
function et(e) {
  if (!me(e))
    return e in U ? U[e] : Promise.resolve();
  const t = Hr(e);
  return U[e] = Promise.all(
    t.map(
      ([r, n]) => Tr(r, n)
    )
  ).then(() => {
    if (me(e))
      return et(e);
    delete U[e];
  }), U[e];
}
const Br = {
  number: {
    scientific: { notation: "scientific" },
    engineering: { notation: "engineering" },
    compactLong: { notation: "compact", compactDisplay: "long" },
    compactShort: { notation: "compact", compactDisplay: "short" }
  },
  date: {
    short: { month: "numeric", day: "numeric", year: "2-digit" },
    medium: { month: "short", day: "numeric", year: "numeric" },
    long: { month: "long", day: "numeric", year: "numeric" },
    full: { weekday: "long", month: "long", day: "numeric", year: "numeric" }
  },
  time: {
    short: { hour: "numeric", minute: "numeric" },
    medium: { hour: "numeric", minute: "numeric", second: "numeric" },
    long: {
      hour: "numeric",
      minute: "numeric",
      second: "numeric",
      timeZoneName: "short"
    },
    full: {
      hour: "numeric",
      minute: "numeric",
      second: "numeric",
      timeZoneName: "short"
    }
  }
}, Sr = {
  fallbackLocale: null,
  loadingDelay: 200,
  formats: Br,
  warnOnMissingMessages: !0,
  handleMissingMessage: void 0,
  ignoreTag: !0
}, Ar = Sr;
function w() {
  return Ar;
}
const ie = Q(!1);
var Pr = Object.defineProperty, Nr = Object.defineProperties, Ir = Object.getOwnPropertyDescriptors, Ne = Object.getOwnPropertySymbols, Or = Object.prototype.hasOwnProperty, wr = Object.prototype.propertyIsEnumerable, Ie = (e, t, r) => t in e ? Pr(e, t, { enumerable: !0, configurable: !0, writable: !0, value: r }) : e[t] = r, Lr = (e, t) => {
  for (var r in t || (t = {}))
    Or.call(t, r) && Ie(e, r, t[r]);
  if (Ne)
    for (var r of Ne(t))
      wr.call(t, r) && Ie(e, r, t[r]);
  return e;
}, Cr = (e, t) => Nr(e, Ir(t));
let pe;
const W = Q(null);
function Oe(e) {
  return e.split("-").map((t, r, n) => n.slice(0, r + 1).join("-")).reverse();
}
function Y(e, t = w().fallbackLocale) {
  const r = Oe(e);
  return t ? [.../* @__PURE__ */ new Set([...r, ...Oe(t)])] : r;
}
function B() {
  return pe ?? void 0;
}
W.subscribe((e) => {
  pe = e ?? void 0, typeof window < "u" && e != null && document.documentElement.setAttribute("lang", e);
});
const Mr = (e) => {
  if (e && dr(e) && me(e)) {
    const { loadingDelay: t } = w();
    let r;
    return typeof window < "u" && B() != null && t ? r = window.setTimeout(
      () => ie.set(!0),
      t
    ) : ie.set(!0), et(e).then(() => {
      W.set(e);
    }).finally(() => {
      clearTimeout(r), ie.set(!1);
    });
  }
  return W.set(e);
}, j = Cr(Lr({}, W), {
  set: Mr
}), Rr = () => typeof window > "u" ? null : window.navigator.language || window.navigator.languages[0], K = (e) => {
  const t = /* @__PURE__ */ Object.create(null);
  return (n) => {
    const i = JSON.stringify(n);
    return i in t ? t[i] : t[i] = e(n);
  };
};
var Ur = Object.defineProperty, Z = Object.getOwnPropertySymbols, tt = Object.prototype.hasOwnProperty, rt = Object.prototype.propertyIsEnumerable, we = (e, t, r) => t in e ? Ur(e, t, { enumerable: !0, configurable: !0, writable: !0, value: r }) : e[t] = r, xe = (e, t) => {
  for (var r in t || (t = {}))
    tt.call(t, r) && we(e, r, t[r]);
  if (Z)
    for (var r of Z(t))
      rt.call(t, r) && we(e, r, t[r]);
  return e;
}, C = (e, t) => {
  var r = {};
  for (var n in e)
    tt.call(e, n) && t.indexOf(n) < 0 && (r[n] = e[n]);
  if (e != null && Z)
    for (var n of Z(e))
      t.indexOf(n) < 0 && rt.call(e, n) && (r[n] = e[n]);
  return r;
};
const D = (e, t) => {
  const { formats: r } = w();
  if (e in r && t in r[e])
    return r[e][t];
  throw new Error(`[svelte-i18n] Unknown "${t}" ${e} format.`);
}, Gr = K(
  (e) => {
    var t = e, { locale: r, format: n } = t, i = C(t, ["locale", "format"]);
    if (r == null)
      throw new Error('[svelte-i18n] A "locale" must be set to format numbers');
    return n && (i = D("number", n)), new Intl.NumberFormat(r, i);
  }
), Dr = K(
  (e) => {
    var t = e, { locale: r, format: n } = t, i = C(t, ["locale", "format"]);
    if (r == null)
      throw new Error('[svelte-i18n] A "locale" must be set to format dates');
    return n ? i = D("date", n) : Object.keys(i).length === 0 && (i = D("date", "short")), new Intl.DateTimeFormat(r, i);
  }
), Fr = K(
  (e) => {
    var t = e, { locale: r, format: n } = t, i = C(t, ["locale", "format"]);
    if (r == null)
      throw new Error(
        '[svelte-i18n] A "locale" must be set to format time values'
      );
    return n ? i = D("time", n) : Object.keys(i).length === 0 && (i = D("time", "short")), new Intl.DateTimeFormat(r, i);
  }
), jr = (e = {}) => {
  var t = e, {
    locale: r = B()
  } = t, n = C(t, [
    "locale"
  ]);
  return Gr(xe({ locale: r }, n));
}, Vr = (e = {}) => {
  var t = e, {
    locale: r = B()
  } = t, n = C(t, [
    "locale"
  ]);
  return Dr(xe({ locale: r }, n));
}, Xr = (e = {}) => {
  var t = e, {
    locale: r = B()
  } = t, n = C(t, [
    "locale"
  ]);
  return Fr(xe({ locale: r }, n));
}, kr = K(
  // eslint-disable-next-line @typescript-eslint/no-non-null-assertion
  (e, t = B()) => new br(e, t, w().formats, {
    ignoreTag: w().ignoreTag
  })
), zr = (e, t = {}) => {
  var r, n, i, o;
  let a = t;
  typeof e == "object" && (a = e, e = a.id);
  const {
    values: h,
    locale: f = B(),
    default: u
  } = a;
  if (f == null)
    throw new Error(
      "[svelte-i18n] Cannot format a message without first setting the initial locale."
    );
  let s = Ye(e, f);
  if (!s)
    s = (o = (i = (n = (r = w()).handleMissingMessage) == null ? void 0 : n.call(r, { locale: f, id: e, defaultValue: u })) != null ? i : u) != null ? o : e;
  else if (typeof s != "string")
    return console.warn(
      `[svelte-i18n] Message with id "${e}" must be of type "string", found: "${typeof s}". Gettin its value through the "$format" method is deprecated; use the "json" method instead.`
    ), s;
  if (!h)
    return s;
  let c = s;
  try {
    c = kr(s, f).format(h);
  } catch (l) {
    l instanceof Error && console.warn(
      `[svelte-i18n] Message "${e}" has syntax error:`,
      l.message
    );
  }
  return c;
}, Wr = (e, t) => Xr(t).format(e), Zr = (e, t) => Vr(t).format(e), Qr = (e, t) => jr(t).format(e), qr = (e, t = B()) => Ye(e, t);
L([j, F], () => zr);
L([j], () => Wr);
L([j], () => Zr);
L([j], () => Qr);
L([j, F], () => qr);
const {
  SvelteComponent: Jr,
  attr: Yr,
  detach: Kr,
  element: $r,
  init: en,
  insert: tn,
  noop: oe,
  safe_not_equal: rn
} = window.__gradio__svelte__internal, { onDestroy: nn, onMount: on } = window.__gradio__svelte__internal;
function an(e) {
  let t;
  return {
    c() {
      t = $r("div"), Yr(t, "class", "lifecycle-placeholder svelte-13nmqcl");
    },
    m(r, n) {
      tn(r, t, n);
    },
    p: oe,
    i: oe,
    o: oe,
    d(r) {
      r && Kr(t);
    }
  };
}
function sn(e, t) {
  let r = null;
  return (...n) => {
    r && clearTimeout(r), r = setTimeout(() => e(...n), t);
  };
}
function Le(e, t) {
  const r = (...n) => e(...n);
  return typeof t == "number" ? sn(r, t) : r;
}
function hn(e, t, r) {
  let { value: n } = t, { gradio: i } = t, { _bind_mount_event: o = !1 } = t, { _bind_resize_event: a = !1 } = t, { _bind_unmount_event: h = !1 } = t;
  function f() {
    return {
      theme: i.theme,
      language: Rr() || "en",
      userAgent: navigator.userAgent,
      screen: {
        width: window.innerWidth,
        height: window.innerHeight,
        scrollY: window.scrollY,
        scrollX: window.scrollX
      }
    };
  }
  function u() {
    r(0, n = f()), o && i.dispatch("mount", f());
  }
  const s = Le(
    () => {
      r(0, n = f()), a && i.dispatch("resize", f());
    },
    500
  ), c = Le(() => {
    r(0, n = f()), h && i.dispatch("unmount", f());
  });
  return on(() => {
    requestAnimationFrame(() => {
      u();
    }), window.addEventListener("resize", s), window.addEventListener("beforeunload", c);
  }), nn(() => {
    window.removeEventListener("resize", s), window.removeEventListener("beforeunload", c);
  }), e.$$set = (l) => {
    "value" in l && r(0, n = l.value), "gradio" in l && r(1, i = l.gradio), "_bind_mount_event" in l && r(2, o = l._bind_mount_event), "_bind_resize_event" in l && r(3, a = l._bind_resize_event), "_bind_unmount_event" in l && r(4, h = l._bind_unmount_event);
  }, [n, i, o, a, h];
}
class un extends Jr {
  constructor(t) {
    super(), en(this, t, hn, an, rn, {
      value: 0,
      gradio: 1,
      _bind_mount_event: 2,
      _bind_resize_event: 3,
      _bind_unmount_event: 4
    });
  }
}
export {
  un as default
};
