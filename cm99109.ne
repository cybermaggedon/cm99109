
program ->
    line (nl line {% d=>d[1] %}):* {% d => [d[0]].concat(d[1]) %}

line ->
     label:? _ instruction eol     {% d => ([d[0],d[2]]) %}
  |  label:? eol                   {% d => ([d[0], null]) %}

instruction ->
    "nop"                          {% d => ({ instr: d[0], opers: [] }) %}
  | "halt"                         {% d => ({ instr: d[0], opers: [] }) %}
  | "sleep"                        {% d => ({ instr: d[0], opers: [] }) %}
  | "ret"                          {% d => ({ instr: d[0], opers: [] }) %}
  | "reti"                         {% d => ({ instr: d[0], opers: [] }) %}
  | "seti"                         {% d => ({ instr: d[0], opers: [] }) %}
  | "cleari"                       {% d => ({ instr: d[0], opers: [] }) %}
  | "push" __ operand              {% d => ({ instr: d[0], opers: [d[2]] }) %}
  | "pop" __ operand               {% d => ({ instr: d[0], opers: [d[2]] }) %}
  | jumpinstr __ operand           {% d => ({ instr: d[0], opers: [d[2]] }) %}
  | "move" __ operands             {% d => ({ instr: d[0], opers: d[2] }) %}
  | cmpinstr __ operands           {% d => ({ instr: d[0], opers: d[2] }) %}
  | arithinstr __ operands         {% d => ({ instr: d[0], opers: d[2] }) %}
  | shiftinstr __ operands         {% d => ({ instr: d[0], opers: d[2] }) %}
  | "inc" __ operand               {% d => ({ instr: d[0], opers: [d[2]] }) %}
  | "dec" __ operand               {% d => ({ instr: d[0], opers: [d[2]] }) %}
  | logicinstr __ operands         {% d => ({ instr: d[0], opers: d[2] }) %}
  | bitinstr __ operands           {% d => ({ instr: d[0], opers: d[2] }) %}
  | "not" __ operand               {% d => ({ instr: d[0], opers: [d[2]] }) %}
  | "db" __ data                   {% d => ({ instr: d[0], opers: [d[2]] }) %}

jumpinstr ->
    "jump"                         {% d => d[0] %}
  | "jumpf"                        {% d => d[0] %}
  | "jumpt"                        {% d => d[0] %}
  | "call"                         {% d => d[0] %}

logicinstr ->
    "and"                          {% d => d[0] %}
  | "or"                           {% d => d[0] %}
  | "xor"                          {% d => d[0] %}

bitinstr ->
    "setbit"                       {% d => d[0] %}
  | "clearbit"                     {% d => d[0] %}
  | "isset"                        {% d => d[0] %}

arithinstr ->
    "add"                          {% d => d[0] %}
  | "sub"                          {% d => d[0] %}
  | "mul"                          {% d => d[0] %}
  | "div"                          {% d => d[0] %}
  | "mod"                          {% d => d[0] %}

shiftinstr ->
    "shiftl"                       {% d => d[0] %}
  | "shiftr"                       {% d => d[0] %}

cmpinstr ->
    "equal"                        {% d => d[0] %}
  | "lt"                           {% d => d[0] %}
  | "lte"                          {% d => d[0] %}
  | "gt"                           {% d => d[0] %}
  | "gte"                          {% d => d[0] %}

operand ->
    constant                       {% d => d[0] %}
  | register                       {% d => d[0] %}
  | address                        {% d => d[0] %}
  | indirect                       {% d => d[0] %}
  | constantref                    {% d => d[0] %}
  | addressref                     {% d => d[0] %}

operands ->
    operand _ "," _ operand        {% d => ([d[0], d[4]]) %}

constant ->
    integer                        {% d => ({k:"constant", v:d[0]}) %}
  | hexinteger                     {% d => ({k:"constant", v:d[0]}) %}

register ->
    "$" registername               {% d => ({k:"register", r: d[1][0]}) %}

registername ->
    "r1" | "r2" | "r3" | "r4" | "r5" | "r6" | "st" | "sp"

address ->
    "[" integer "]"                {% d => ({k:"address", v:d[1]}) %}

indirect ->
    "[$" registername ix:? "]"     {%
                                     d => ({
                                       k:"indirect",
                                       r:d[1][0],
                                       o: d[2] ? d[2] : 0
                                     })
                                   %}

ix ->
    "+" integer                    {% d => d[1] %}
  | "-" integer                    {% d => -d[1] %}

constantref ->
    labelname                      {% d => ({k:"constantref", n:d[0]}) %}

addressref ->
    "[" labelname "]"              {% d => ({k:"addressref", n:d[1]}) %}

data ->
    "0x" [0-9a-f]:+                {% d => (parseHexString(d[1].join(''))) %}
  | "\"" [^\"]:* "\""              {% d => (charToByteArray(d[1])) %}
  | integer

label -> _ labelname ":"           {% d => d[1] %}
labelname ->
    [_a-zA-Z] [_a-zA-Z0-9]:+       {% d => d[0] + d[1].join('') %}

eol -> _ comment:?                 {% empty %}
comment -> ";" [^\r\n]:*           {% empty %}
integer -> "-":? [0-9]:+           {%
                                     d => parseInt(
                                       d[1].join("") * (d[0] ? -1 : 1)
                                     )
                                   %}

hexinteger -> "0x" [0-9a-f]:+      {% d => parseInt(d[1].join(""), 16) %}

nl -> "\r":? "\n"                  {% empty %}
__ -> ws:+                         {% empty %}
_ -> ws:*                          {% empty %}
ws -> [ \t]                        {% empty %}

@{%

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

%}

