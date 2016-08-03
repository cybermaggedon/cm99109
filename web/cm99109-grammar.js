// Generated automatically by nearley, version 2.19.7
// http://github.com/Hardmath123/nearley
(function () {
function id(x) { return x[0]; }


    const empty = d => null;
    const notnull = d => d != null;

    function parseHexString(str) {
        var result = [];
        while (str.length >= 2) { 
            result.push(parseInt(str.substring(0, 2), 16));
            str = str.substring(2, str.length);
        }

        return result;
    }

    function charToByteArray(str) {
        var result = [];
        for(var i = 0; i < str.length; i++) {
        result.push(str[i].charCodeAt(0));
        }
        return result;
    }

var grammar = {
    Lexer: undefined,
    ParserRules: [
    {"name": "program$ebnf$1", "symbols": []},
    {"name": "program$ebnf$1$subexpression$1", "symbols": ["nl", "line"], "postprocess": d=>d[1]},
    {"name": "program$ebnf$1", "symbols": ["program$ebnf$1", "program$ebnf$1$subexpression$1"], "postprocess": function arrpush(d) {return d[0].concat([d[1]]);}},
    {"name": "program", "symbols": ["line", "program$ebnf$1"], "postprocess": d => [d[0]].concat(d[1])},
    {"name": "line$ebnf$1", "symbols": ["label"], "postprocess": id},
    {"name": "line$ebnf$1", "symbols": [], "postprocess": function(d) {return null;}},
    {"name": "line", "symbols": ["line$ebnf$1", "_", "instruction", "eol"], "postprocess": d => ([d[0],d[2]])},
    {"name": "line$ebnf$2", "symbols": ["label"], "postprocess": id},
    {"name": "line$ebnf$2", "symbols": [], "postprocess": function(d) {return null;}},
    {"name": "line", "symbols": ["line$ebnf$2", "eol"], "postprocess": d => ([d[0], null])},
    {"name": "instruction$string$1", "symbols": [{"literal":"n"}, {"literal":"o"}, {"literal":"p"}], "postprocess": function joiner(d) {return d.join('');}},
    {"name": "instruction", "symbols": ["instruction$string$1"], "postprocess": d => ({ instr: d[0], opers: [] })},
    {"name": "instruction$string$2", "symbols": [{"literal":"h"}, {"literal":"a"}, {"literal":"l"}, {"literal":"t"}], "postprocess": function joiner(d) {return d.join('');}},
    {"name": "instruction", "symbols": ["instruction$string$2"], "postprocess": d => ({ instr: d[0], opers: [] })},
    {"name": "instruction$string$3", "symbols": [{"literal":"s"}, {"literal":"l"}, {"literal":"e"}, {"literal":"e"}, {"literal":"p"}], "postprocess": function joiner(d) {return d.join('');}},
    {"name": "instruction", "symbols": ["instruction$string$3"], "postprocess": d => ({ instr: d[0], opers: [] })},
    {"name": "instruction$string$4", "symbols": [{"literal":"r"}, {"literal":"e"}, {"literal":"t"}], "postprocess": function joiner(d) {return d.join('');}},
    {"name": "instruction", "symbols": ["instruction$string$4"], "postprocess": d => ({ instr: d[0], opers: [] })},
    {"name": "instruction$string$5", "symbols": [{"literal":"r"}, {"literal":"e"}, {"literal":"t"}, {"literal":"i"}], "postprocess": function joiner(d) {return d.join('');}},
    {"name": "instruction", "symbols": ["instruction$string$5"], "postprocess": d => ({ instr: d[0], opers: [] })},
    {"name": "instruction$string$6", "symbols": [{"literal":"s"}, {"literal":"e"}, {"literal":"t"}, {"literal":"i"}], "postprocess": function joiner(d) {return d.join('');}},
    {"name": "instruction", "symbols": ["instruction$string$6"], "postprocess": d => ({ instr: d[0], opers: [] })},
    {"name": "instruction$string$7", "symbols": [{"literal":"c"}, {"literal":"l"}, {"literal":"e"}, {"literal":"a"}, {"literal":"r"}, {"literal":"i"}], "postprocess": function joiner(d) {return d.join('');}},
    {"name": "instruction", "symbols": ["instruction$string$7"], "postprocess": d => ({ instr: d[0], opers: [] })},
    {"name": "instruction$string$8", "symbols": [{"literal":"p"}, {"literal":"u"}, {"literal":"s"}, {"literal":"h"}], "postprocess": function joiner(d) {return d.join('');}},
    {"name": "instruction", "symbols": ["instruction$string$8", "__", "operand"], "postprocess": d => ({ instr: d[0], opers: [d[2]] })},
    {"name": "instruction$string$9", "symbols": [{"literal":"p"}, {"literal":"o"}, {"literal":"p"}], "postprocess": function joiner(d) {return d.join('');}},
    {"name": "instruction", "symbols": ["instruction$string$9", "__", "operand"], "postprocess": d => ({ instr: d[0], opers: [d[2]] })},
    {"name": "instruction", "symbols": ["jumpinstr", "__", "operand"], "postprocess": d => ({ instr: d[0], opers: [d[2]] })},
    {"name": "instruction$string$10", "symbols": [{"literal":"m"}, {"literal":"o"}, {"literal":"v"}, {"literal":"e"}], "postprocess": function joiner(d) {return d.join('');}},
    {"name": "instruction", "symbols": ["instruction$string$10", "__", "operands"], "postprocess": d => ({ instr: d[0], opers: d[2] })},
    {"name": "instruction", "symbols": ["cmpinstr", "__", "operands"], "postprocess": d => ({ instr: d[0], opers: d[2] })},
    {"name": "instruction", "symbols": ["arithinstr", "__", "operands"], "postprocess": d => ({ instr: d[0], opers: d[2] })},
    {"name": "instruction", "symbols": ["shiftinstr", "__", "operands"], "postprocess": d => ({ instr: d[0], opers: d[2] })},
    {"name": "instruction$string$11", "symbols": [{"literal":"i"}, {"literal":"n"}, {"literal":"c"}], "postprocess": function joiner(d) {return d.join('');}},
    {"name": "instruction", "symbols": ["instruction$string$11", "__", "operand"], "postprocess": d => ({ instr: d[0], opers: [d[2]] })},
    {"name": "instruction$string$12", "symbols": [{"literal":"d"}, {"literal":"e"}, {"literal":"c"}], "postprocess": function joiner(d) {return d.join('');}},
    {"name": "instruction", "symbols": ["instruction$string$12", "__", "operand"], "postprocess": d => ({ instr: d[0], opers: [d[2]] })},
    {"name": "instruction", "symbols": ["logicinstr", "__", "operands"], "postprocess": d => ({ instr: d[0], opers: d[2] })},
    {"name": "instruction", "symbols": ["bitinstr", "__", "operands"], "postprocess": d => ({ instr: d[0], opers: d[2] })},
    {"name": "instruction$string$13", "symbols": [{"literal":"n"}, {"literal":"o"}, {"literal":"t"}], "postprocess": function joiner(d) {return d.join('');}},
    {"name": "instruction", "symbols": ["instruction$string$13", "__", "operand"], "postprocess": d => ({ instr: d[0], opers: [d[2]] })},
    {"name": "instruction$string$14", "symbols": [{"literal":"d"}, {"literal":"b"}], "postprocess": function joiner(d) {return d.join('');}},
    {"name": "instruction", "symbols": ["instruction$string$14", "__", "data"], "postprocess": d => ({ instr: d[0], opers: [d[2]] })},
    {"name": "jumpinstr$string$1", "symbols": [{"literal":"j"}, {"literal":"u"}, {"literal":"m"}, {"literal":"p"}], "postprocess": function joiner(d) {return d.join('');}},
    {"name": "jumpinstr", "symbols": ["jumpinstr$string$1"], "postprocess": d => d[0]},
    {"name": "jumpinstr$string$2", "symbols": [{"literal":"j"}, {"literal":"u"}, {"literal":"m"}, {"literal":"p"}, {"literal":"f"}], "postprocess": function joiner(d) {return d.join('');}},
    {"name": "jumpinstr", "symbols": ["jumpinstr$string$2"], "postprocess": d => d[0]},
    {"name": "jumpinstr$string$3", "symbols": [{"literal":"j"}, {"literal":"u"}, {"literal":"m"}, {"literal":"p"}, {"literal":"t"}], "postprocess": function joiner(d) {return d.join('');}},
    {"name": "jumpinstr", "symbols": ["jumpinstr$string$3"], "postprocess": d => d[0]},
    {"name": "jumpinstr$string$4", "symbols": [{"literal":"c"}, {"literal":"a"}, {"literal":"l"}, {"literal":"l"}], "postprocess": function joiner(d) {return d.join('');}},
    {"name": "jumpinstr", "symbols": ["jumpinstr$string$4"], "postprocess": d => d[0]},
    {"name": "logicinstr$string$1", "symbols": [{"literal":"a"}, {"literal":"n"}, {"literal":"d"}], "postprocess": function joiner(d) {return d.join('');}},
    {"name": "logicinstr", "symbols": ["logicinstr$string$1"], "postprocess": d => d[0]},
    {"name": "logicinstr$string$2", "symbols": [{"literal":"o"}, {"literal":"r"}], "postprocess": function joiner(d) {return d.join('');}},
    {"name": "logicinstr", "symbols": ["logicinstr$string$2"], "postprocess": d => d[0]},
    {"name": "logicinstr$string$3", "symbols": [{"literal":"x"}, {"literal":"o"}, {"literal":"r"}], "postprocess": function joiner(d) {return d.join('');}},
    {"name": "logicinstr", "symbols": ["logicinstr$string$3"], "postprocess": d => d[0]},
    {"name": "bitinstr$string$1", "symbols": [{"literal":"s"}, {"literal":"e"}, {"literal":"t"}, {"literal":"b"}, {"literal":"i"}, {"literal":"t"}], "postprocess": function joiner(d) {return d.join('');}},
    {"name": "bitinstr", "symbols": ["bitinstr$string$1"], "postprocess": d => d[0]},
    {"name": "bitinstr$string$2", "symbols": [{"literal":"c"}, {"literal":"l"}, {"literal":"e"}, {"literal":"a"}, {"literal":"r"}, {"literal":"b"}, {"literal":"i"}, {"literal":"t"}], "postprocess": function joiner(d) {return d.join('');}},
    {"name": "bitinstr", "symbols": ["bitinstr$string$2"], "postprocess": d => d[0]},
    {"name": "bitinstr$string$3", "symbols": [{"literal":"i"}, {"literal":"s"}, {"literal":"s"}, {"literal":"e"}, {"literal":"t"}], "postprocess": function joiner(d) {return d.join('');}},
    {"name": "bitinstr", "symbols": ["bitinstr$string$3"], "postprocess": d => d[0]},
    {"name": "arithinstr$string$1", "symbols": [{"literal":"a"}, {"literal":"d"}, {"literal":"d"}], "postprocess": function joiner(d) {return d.join('');}},
    {"name": "arithinstr", "symbols": ["arithinstr$string$1"], "postprocess": d => d[0]},
    {"name": "arithinstr$string$2", "symbols": [{"literal":"s"}, {"literal":"u"}, {"literal":"b"}], "postprocess": function joiner(d) {return d.join('');}},
    {"name": "arithinstr", "symbols": ["arithinstr$string$2"], "postprocess": d => d[0]},
    {"name": "arithinstr$string$3", "symbols": [{"literal":"m"}, {"literal":"u"}, {"literal":"l"}], "postprocess": function joiner(d) {return d.join('');}},
    {"name": "arithinstr", "symbols": ["arithinstr$string$3"], "postprocess": d => d[0]},
    {"name": "arithinstr$string$4", "symbols": [{"literal":"d"}, {"literal":"i"}, {"literal":"v"}], "postprocess": function joiner(d) {return d.join('');}},
    {"name": "arithinstr", "symbols": ["arithinstr$string$4"], "postprocess": d => d[0]},
    {"name": "arithinstr$string$5", "symbols": [{"literal":"m"}, {"literal":"o"}, {"literal":"d"}], "postprocess": function joiner(d) {return d.join('');}},
    {"name": "arithinstr", "symbols": ["arithinstr$string$5"], "postprocess": d => d[0]},
    {"name": "shiftinstr$string$1", "symbols": [{"literal":"s"}, {"literal":"h"}, {"literal":"i"}, {"literal":"f"}, {"literal":"t"}, {"literal":"l"}], "postprocess": function joiner(d) {return d.join('');}},
    {"name": "shiftinstr", "symbols": ["shiftinstr$string$1"], "postprocess": d => d[0]},
    {"name": "shiftinstr$string$2", "symbols": [{"literal":"s"}, {"literal":"h"}, {"literal":"i"}, {"literal":"f"}, {"literal":"t"}, {"literal":"r"}], "postprocess": function joiner(d) {return d.join('');}},
    {"name": "shiftinstr", "symbols": ["shiftinstr$string$2"], "postprocess": d => d[0]},
    {"name": "cmpinstr$string$1", "symbols": [{"literal":"e"}, {"literal":"q"}, {"literal":"u"}, {"literal":"a"}, {"literal":"l"}], "postprocess": function joiner(d) {return d.join('');}},
    {"name": "cmpinstr", "symbols": ["cmpinstr$string$1"], "postprocess": d => d[0]},
    {"name": "cmpinstr$string$2", "symbols": [{"literal":"l"}, {"literal":"t"}], "postprocess": function joiner(d) {return d.join('');}},
    {"name": "cmpinstr", "symbols": ["cmpinstr$string$2"], "postprocess": d => d[0]},
    {"name": "cmpinstr$string$3", "symbols": [{"literal":"l"}, {"literal":"t"}, {"literal":"e"}], "postprocess": function joiner(d) {return d.join('');}},
    {"name": "cmpinstr", "symbols": ["cmpinstr$string$3"], "postprocess": d => d[0]},
    {"name": "cmpinstr$string$4", "symbols": [{"literal":"g"}, {"literal":"t"}], "postprocess": function joiner(d) {return d.join('');}},
    {"name": "cmpinstr", "symbols": ["cmpinstr$string$4"], "postprocess": d => d[0]},
    {"name": "cmpinstr$string$5", "symbols": [{"literal":"g"}, {"literal":"t"}, {"literal":"e"}], "postprocess": function joiner(d) {return d.join('');}},
    {"name": "cmpinstr", "symbols": ["cmpinstr$string$5"], "postprocess": d => d[0]},
    {"name": "operand", "symbols": ["constant"], "postprocess": d => d[0]},
    {"name": "operand", "symbols": ["register"], "postprocess": d => d[0]},
    {"name": "operand", "symbols": ["address"], "postprocess": d => d[0]},
    {"name": "operand", "symbols": ["indirect"], "postprocess": d => d[0]},
    {"name": "operand", "symbols": ["constantref"], "postprocess": d => d[0]},
    {"name": "operand", "symbols": ["addressref"], "postprocess": d => d[0]},
    {"name": "operands", "symbols": ["operand", "_", {"literal":","}, "_", "operand"], "postprocess": d => ([d[0], d[4]])},
    {"name": "constant", "symbols": ["integer"], "postprocess": d => ({k:"constant", v:d[0]})},
    {"name": "constant", "symbols": ["hexinteger"], "postprocess": d => ({k:"constant", v:d[0]})},
    {"name": "register", "symbols": [{"literal":"$"}, "registername"], "postprocess": d => ({k:"register", r: d[1][0]})},
    {"name": "registername$string$1", "symbols": [{"literal":"r"}, {"literal":"1"}], "postprocess": function joiner(d) {return d.join('');}},
    {"name": "registername", "symbols": ["registername$string$1"]},
    {"name": "registername$string$2", "symbols": [{"literal":"r"}, {"literal":"2"}], "postprocess": function joiner(d) {return d.join('');}},
    {"name": "registername", "symbols": ["registername$string$2"]},
    {"name": "registername$string$3", "symbols": [{"literal":"r"}, {"literal":"3"}], "postprocess": function joiner(d) {return d.join('');}},
    {"name": "registername", "symbols": ["registername$string$3"]},
    {"name": "registername$string$4", "symbols": [{"literal":"r"}, {"literal":"4"}], "postprocess": function joiner(d) {return d.join('');}},
    {"name": "registername", "symbols": ["registername$string$4"]},
    {"name": "registername$string$5", "symbols": [{"literal":"r"}, {"literal":"5"}], "postprocess": function joiner(d) {return d.join('');}},
    {"name": "registername", "symbols": ["registername$string$5"]},
    {"name": "registername$string$6", "symbols": [{"literal":"r"}, {"literal":"6"}], "postprocess": function joiner(d) {return d.join('');}},
    {"name": "registername", "symbols": ["registername$string$6"]},
    {"name": "registername$string$7", "symbols": [{"literal":"s"}, {"literal":"t"}], "postprocess": function joiner(d) {return d.join('');}},
    {"name": "registername", "symbols": ["registername$string$7"]},
    {"name": "registername$string$8", "symbols": [{"literal":"s"}, {"literal":"p"}], "postprocess": function joiner(d) {return d.join('');}},
    {"name": "registername", "symbols": ["registername$string$8"]},
    {"name": "address", "symbols": [{"literal":"["}, "integer", {"literal":"]"}], "postprocess": d => ({k:"address", v:d[1]})},
    {"name": "indirect$string$1", "symbols": [{"literal":"["}, {"literal":"$"}], "postprocess": function joiner(d) {return d.join('');}},
    {"name": "indirect$ebnf$1", "symbols": ["ix"], "postprocess": id},
    {"name": "indirect$ebnf$1", "symbols": [], "postprocess": function(d) {return null;}},
    {"name": "indirect", "symbols": ["indirect$string$1", "registername", "indirect$ebnf$1", {"literal":"]"}], "postprocess": 
        d => ({
          k:"indirect",
          r:d[1][0],
          o: d[2] ? d[2] : 0
        })
                                           },
    {"name": "ix", "symbols": [{"literal":"+"}, "integer"], "postprocess": d => d[1]},
    {"name": "ix", "symbols": [{"literal":"-"}, "integer"], "postprocess": d => -d[1]},
    {"name": "constantref", "symbols": ["labelname"], "postprocess": d => ({k:"constantref", n:d[0]})},
    {"name": "addressref", "symbols": [{"literal":"["}, "labelname", {"literal":"]"}], "postprocess": d => ({k:"addressref", n:d[1]})},
    {"name": "data$string$1", "symbols": [{"literal":"0"}, {"literal":"x"}], "postprocess": function joiner(d) {return d.join('');}},
    {"name": "data$ebnf$1", "symbols": [/[0-9a-f]/]},
    {"name": "data$ebnf$1", "symbols": ["data$ebnf$1", /[0-9a-f]/], "postprocess": function arrpush(d) {return d[0].concat([d[1]]);}},
    {"name": "data", "symbols": ["data$string$1", "data$ebnf$1"], "postprocess": d => (parseHexString(d[1].join('')))},
    {"name": "data$ebnf$2", "symbols": []},
    {"name": "data$ebnf$2", "symbols": ["data$ebnf$2", /[^\"]/], "postprocess": function arrpush(d) {return d[0].concat([d[1]]);}},
    {"name": "data", "symbols": [{"literal":"\""}, "data$ebnf$2", {"literal":"\""}], "postprocess": d => (charToByteArray(d[1]))},
    {"name": "data", "symbols": ["integer"]},
    {"name": "label", "symbols": ["_", "labelname", {"literal":":"}], "postprocess": d => d[1]},
    {"name": "labelname$ebnf$1", "symbols": [/[_a-zA-Z0-9]/]},
    {"name": "labelname$ebnf$1", "symbols": ["labelname$ebnf$1", /[_a-zA-Z0-9]/], "postprocess": function arrpush(d) {return d[0].concat([d[1]]);}},
    {"name": "labelname", "symbols": [/[_a-zA-Z]/, "labelname$ebnf$1"], "postprocess": d => d[0] + d[1].join('')},
    {"name": "eol$ebnf$1", "symbols": ["comment"], "postprocess": id},
    {"name": "eol$ebnf$1", "symbols": [], "postprocess": function(d) {return null;}},
    {"name": "eol", "symbols": ["_", "eol$ebnf$1"], "postprocess": empty},
    {"name": "comment$ebnf$1", "symbols": []},
    {"name": "comment$ebnf$1", "symbols": ["comment$ebnf$1", /[^\r\n]/], "postprocess": function arrpush(d) {return d[0].concat([d[1]]);}},
    {"name": "comment", "symbols": [{"literal":";"}, "comment$ebnf$1"], "postprocess": empty},
    {"name": "integer$ebnf$1", "symbols": [{"literal":"-"}], "postprocess": id},
    {"name": "integer$ebnf$1", "symbols": [], "postprocess": function(d) {return null;}},
    {"name": "integer$ebnf$2", "symbols": [/[0-9]/]},
    {"name": "integer$ebnf$2", "symbols": ["integer$ebnf$2", /[0-9]/], "postprocess": function arrpush(d) {return d[0].concat([d[1]]);}},
    {"name": "integer", "symbols": ["integer$ebnf$1", "integer$ebnf$2"], "postprocess": 
        d => parseInt(
          d[1].join("") * (d[0] ? -1 : 1)
        )
                                           },
    {"name": "hexinteger$string$1", "symbols": [{"literal":"0"}, {"literal":"x"}], "postprocess": function joiner(d) {return d.join('');}},
    {"name": "hexinteger$ebnf$1", "symbols": [/[0-9a-f]/]},
    {"name": "hexinteger$ebnf$1", "symbols": ["hexinteger$ebnf$1", /[0-9a-f]/], "postprocess": function arrpush(d) {return d[0].concat([d[1]]);}},
    {"name": "hexinteger", "symbols": ["hexinteger$string$1", "hexinteger$ebnf$1"], "postprocess": d => parseInt(d[1].join(""), 16)},
    {"name": "nl$ebnf$1", "symbols": [{"literal":"\r"}], "postprocess": id},
    {"name": "nl$ebnf$1", "symbols": [], "postprocess": function(d) {return null;}},
    {"name": "nl", "symbols": ["nl$ebnf$1", {"literal":"\n"}], "postprocess": empty},
    {"name": "__$ebnf$1", "symbols": ["ws"]},
    {"name": "__$ebnf$1", "symbols": ["__$ebnf$1", "ws"], "postprocess": function arrpush(d) {return d[0].concat([d[1]]);}},
    {"name": "__", "symbols": ["__$ebnf$1"], "postprocess": empty},
    {"name": "_$ebnf$1", "symbols": []},
    {"name": "_$ebnf$1", "symbols": ["_$ebnf$1", "ws"], "postprocess": function arrpush(d) {return d[0].concat([d[1]]);}},
    {"name": "_", "symbols": ["_$ebnf$1"], "postprocess": empty},
    {"name": "ws", "symbols": [/[ \t]/], "postprocess": empty}
]
  , ParserStart: "program"
}
if (typeof module !== 'undefined'&& typeof module.exports !== 'undefined') {
   module.exports = grammar;
} else {
   window.grammar = grammar;
}
})();
