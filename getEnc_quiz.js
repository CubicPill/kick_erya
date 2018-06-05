(function anonymous() {
        function encrypt(h, g) {
            if (g == null || g.length <= 0) {
                return null
            }
            var m = "";
            for (var d = 0; d < g.length; d++) {
                m += g.charCodeAt(d).toString()
            }
            var j = Math.floor(m.length / 5);
            var c = parseInt(m.charAt(j) + m.charAt(j * 2) + m.charAt(j * 3) + m.charAt(j * 4));
            var a = Math.ceil(g.length / 2);
            var k = Math.pow(2, 31) - 1;
            if (c < 2) {
                alert("Algorithm cannot find a suitable hash. Please choose a different password. \nPossible considerations are to choose a more complex or longer password.");
                return null
            }
            var b = Math.random();
            var e = Math.round(b * 1000000000) % 100000000;
            m += e;
            if (m.length > 10) {
                m = parseInt(m.substring(0, 10)).toString()
            }
            m = (c * m + a) % k;
            var f = "";
            var l = "";
            for (var d = 0; d < h.length; d++) {
                f = parseInt(h.charCodeAt(d) ^ Math.floor((m / k) * 255));
                if (f < 16) {
                    l += "0" + f.toString(16)
                } else {
                    l += f.toString(16)
                }
                m = (c * m + a) % k
            }
            e = e.toString(16);
            while (e.length < 8) {
                e = "0" + e
            }
            l += e;
            return l + "&rd=" + b
        }

        var __e = function () {
            var g = {
                "x": -1,
                "y": -1
            };
            var c = document.getElementById("userId").value;
            var a = document.getElementById("workRelationId").value;
            var j = c + "_" + a;
            try {
                if (typeof (j) == "undefined") {
                    j = "axvP^&Sg"
                }
                var d = window.event;
                if (typeof (d) == "undefined") {
                    var k = arguments.callee.caller
                        , l = k;
                    while (k != null) {
                        l = k;
                        k = k.caller
                    }
                    d = l.arguments[0]
                }
                if (d != null) {
                    var i = document.documentElement.scrollLeft || document.body.scrollLeft;
                    var h = document.documentElement.scrollTop || document.body.scrollTop;
                    g.x = d.pageX || d.clientX + i;
                    g.y = d.pageY || d.clientY + h
                }
            } catch (f) {
                g = {
                    "x": -2,
                    "y": -2
                }
            }
            var b = "(" + Math.ceil(g.x) + "|" + Math.ceil(g.y) + ")";
            return encrypt(b, j) + "&value=" + b + "&wid=" + a
        };
        window.getEnc = function () {
            return __e()
        }
        ;
    }
)
