
// ----
function Address(val) {
    this.value = val;
};

Address.prototype.to_code = function() {
    return this.value;
}

Address.prototype.kind = function() {
    return "address";
}

function address(x) { return new Address(x); }

// ----
function Indirect(register, ix) {
    this.register = register;
    this.ix = ix;
};

Indirect.prototype.to_code = function() {
    reg_code = {
	"r1": 0,
	"r2": 1,
	"r3": 2,
	"r4": 3,
	"r5": 4,
	"r6": 5,
	"st": 6,
	"sp": 7
    }[this.register];
    return reg_code + ((this.ix + 16) << 3);
}

Indirect.prototype.kind = function() {
    return "indirect";
}

function indirect(reg, ix) { return new Indirect(reg, ix); }

// ----
function Constant(val) {
    this.value = val;
};

Constant.prototype.to_code = function() {
    return this.value;
}

Constant.prototype.kind = function() {
    return "constant";
}

function constant(x) { return new Constant(x); }

// ----
function Register(name) {
    this.name = name;
};

Register.prototype.to_code = function() {
    return {
	"r1": 0,
	"r2": 1,
	"r3": 2,
	"r4": 3,
	"r5": 4,
	"r6": 5,
	"st": 6,
	"sp": 7
    }[this.name];
}

Register.prototype.kind = function() {
    return "register";
}

function register(x) { return new Register(x); }

// ----
function Constantref(name) {
    this.name = name;
    this.refkind = "constant";
};

Constantref.prototype.to_code = function() {
    return 0;
}

Constantref.prototype.kind = function() {
    return "constant";
}

function constantref(x) { return new Constantref(x); }

// ----
function Addressref(name) {
    this.name = name;
    this.refkind = "address";
};

Addressref.prototype.to_code = function() {
    return 0;
}

Addressref.prototype.kind = function() {
    return "constant";
}

function addressref(x) { return new Addressref(x); }

// ----------------------------------------------------------------------------

function Instruction(operands) {
    this.operands = operands;
}

Instruction.prototype.opcodes = [
];

Instruction.prototype.token = "UNDEFINED";

Instruction.prototype.to_code = function() {

    var signature = "";
    for (var i in this.operands) {
	signature += this.operands[i].kind() + "/";
    }

    for (var i in this.opcodes) {

	if (signature == this.opcodes[i][1]) {

	    // Found the right opcode

	    var mc = [this.opcodes[i][0]];

	    for(var j in this.operands) {

		// Assumes each operand is one byte (which it is)
		mc.push(this.operands[j].to_code());
	    }

	    return mc;

	}
    }

    throw "No matching signature for instruction."

}

// Resolve references
Instruction.prototype.resolve = function(labelmap) {

    for(var i in this.operands) {
	if (this.operands[i].refkind) {
	    var refname = this.operands[i].name;

	    if (labelmap[refname] == undefined)
		throw "Label '" + refname + "' not resolved";

	    if (this.operands[i].refkind == "constant") {
		this.operands[i] = constant(labelmap[refname]);
	    }
	    if (this.operands[i].refkind == "address") {
		this.operands[i] = address(labelmap[refname]);
	    }

	}
    }

}

// ----------------------------------------------------------------------------

function Label(label, instr) {
    this.instr = instr;
    this.label = label;
}

Label.prototype.to_code = function() {
    if (this.instr != null)
	return this.instr.to_code();
    else
	return [];
}

Label.prototype.resolve = function(labelmap) {
    if (this.instr != null)
	return this.instr.resolve(labelmap);
}

function label(label, instr) {
    return new Label(label, instr);
}

// ----------------------------------------------------------------------------

function Nop(operands) {
    Instruction.call(this, operands);
}

Nop.prototype = Object.create(Instruction.prototype);

Nop.prototype.opcodes = [
    [0x0, ""],
];

function nop() {
    return new Nop([]);
}

function basic_opcodes(base) {
    return [
	[base, "register/register/"],
	[base + 1, "register/address/"],
	[base + 2, "register/constant/"],
	[base + 3, "register/indirect/"],
    ];
}

function Move(operands) {
    Instruction.call(this, operands);
}

Move.prototype = Object.create(Instruction.prototype);

Move.prototype.opcodes = [
    [0x10, "register/register/"],
    [0x11, "register/address/"],
    [0x12, "register/constant/"],
    [0x13, "register/indirect/"],
    [0x14, "address/register/"],
    [0x15, "address/constant/"],
    [0x16, "indirect/register/"],
    [0x17, "indirect/constant/"],
];

function move(op1, op2) {
    return new Move([op1, op2]);
}

function basic_opcodes(base) {
    return [
	[base, "register/register/"],
	[base + 1, "register/address/"],
	[base + 2, "register/constant/"],
	[base + 3, "register/indirect/"],
    ];
}

// ----
function Add(operands) {
    Instruction.call(this, operands);
}

Add.prototype = Object.create(Instruction.prototype);

Add.prototype.opcodes = basic_opcodes(0x20);

function add(op1, op2) {
    return new Add([op1, op2]);
}

// ----
function Sub(operands) {
    Instruction.call(this, operands);
}

Sub.prototype = Object.create(Instruction.prototype);

Sub.prototype.opcodes = basic_opcodes(0x28);

function sub(op1, op2) {
    return new Sub([op1, op2]);
}

// ----

function Inc(operands) {
    Instruction.call(this, operands);
}

Inc.prototype = Object.create(Instruction.prototype);

Inc.prototype.opcodes = [
    [0x30, "register/"],
];

function inc(op1) {
    return new Inc([op1]);
}

// ----

function Dec(operands) {
    Instruction.call(this, operands);
}

Dec.prototype = Object.create(Instruction.prototype);

Dec.prototype.opcodes = [
    [0x31, "register/"],
];

function dec(op1) {
    return new Dec([op1]);
}

// ----
function Mul(operands) {
    Instruction.call(this, operands);
}

Mul.prototype = Object.create(Instruction.prototype);

Mul.prototype.opcodes = basic_opcodes(0x40);

function mul(op1, op2) {
    return new Mul([op1, op2]);
}

// ----
function Div(operands) {
    Instruction.call(this, operands);
}

Div.prototype = Object.create(Instruction.prototype);

Div.prototype.opcodes = basic_opcodes(0x44);

function div(op1, op2) {
    return new Div([op1, op2]);
}

// ----
function Mod(operands) {
    Instruction.call(this, operands);
}

Mod.prototype = Object.create(Instruction.prototype);

Mod.prototype.opcodes = basic_opcodes(0x48);

function mod(op1, op2) {
    return new Mod([op1, op2]);
}

// ----
function And(operands) {
    Instruction.call(this, operands);
}

And.prototype = Object.create(Instruction.prototype);

And.prototype.opcodes = basic_opcodes(0x50);

function and(op1, op2) {
    return new And([op1, op2]);
}

// ----
function Or(operands) {
    Instruction.call(this, operands);
}

Or.prototype = Object.create(Instruction.prototype);

Or.prototype.opcodes = basic_opcodes(0x54);

function or(op1, op2) {
    return new Or([op1, op2]);
}

// ----
function Xor(operands) {
    Instruction.call(this, operands);
}

Xor.prototype = Object.create(Instruction.prototype);

Xor.prototype.opcodes = basic_opcodes(0x58);

function xor(op1, op2) {
    return new Xor([op1, op2]);
}

// ----

function Not(operands) {
    Instruction.call(this, operands);
}

Not.prototype = Object.create(Instruction.prototype);

Not.prototype.opcodes = [
    [0x5c, "register/"],
];

function not(op1) {
    return new Not([op1]);
}

// ----
function Shiftl(operands) {
    Instruction.call(this, operands);
}

Shiftl.prototype = Object.create(Instruction.prototype);

Shiftl.prototype.opcodes = basic_opcodes(0x60);

function shiftl(op1, op2) {
    return new Shiftl([op1, op2]);
}

// ----
function Shiftr(operands) {
    Instruction.call(this, operands);
}

Shiftr.prototype = Object.create(Instruction.prototype);

Shiftr.prototype.opcodes = basic_opcodes(0x64);

function shiftr(op1, op2) {
    return new Shiftr([op1, op2]);
}

// ----
function Equal(operands) {
    Instruction.call(this, operands);
}

Equal.prototype = Object.create(Instruction.prototype);

Equal.prototype.opcodes = basic_opcodes(0x68);

function equal(op1, op2) {
    return new Equal([op1, op2]);
}

// ----
function Lt(operands) {
    Instruction.call(this, operands);
}

Lt.prototype = Object.create(Instruction.prototype);

Lt.prototype.opcodes = basic_opcodes(0x70);

function lt(op1, op2) {
    return new Lt([op1, op2]);
}

// ----
function Lte(operands) {
    Instruction.call(this, operands);
}

Lte.prototype = Object.create(Instruction.prototype);

Lte.prototype.opcodes = basic_opcodes(0x74);

function lte(op1, op2) {
    return new Lte([op1, op2]);
}

// ----
function Gt(operands) {
    Instruction.call(this, operands);
}

Gt.prototype = Object.create(Instruction.prototype);

Gt.prototype.opcodes = basic_opcodes(0x78);

function gt(op1, op2) {
    return new Gt([op1, op2]);
}

// ----
function Gte(operands) {
    Instruction.call(this, operands);
}

Gte.prototype = Object.create(Instruction.prototype);

Gte.prototype.opcodes = basic_opcodes(0x7c);

function gte(op1, op2) {
    return new Gte([op1, op2]);
}

// ----

function Jump(operands) {
    Instruction.call(this, operands);
}

Jump.prototype = Object.create(Instruction.prototype);

Jump.prototype.opcodes = [
    [0x80, "constant/"],
    [0x81, "indirect/"],
];

function jump(op1) {
    return new Jump([op1]);
}

// ----

function Jumpt(operands) {
    Instruction.call(this, operands);
}

Jumpt.prototype = Object.create(Instruction.prototype);

Jumpt.prototype.opcodes = [
    [0x82, "constant/"],
    [0x83, "indirect/"],
];

function jumpt(op1) {
    return new Jumpt([op1]);
}

// ----

function Jumpf(operands) {
    Instruction.call(this, operands);
}

Jumpf.prototype = Object.create(Instruction.prototype);

Jumpf.prototype.opcodes = [
    [0x86, "constant/"],
    [0x87, "indirect/"],
];

function jumpf(op1) {
    return new Jumpf([op1]);
}


// ----

function Call(operands) {
    Instruction.call(this, operands);
}

Call.prototype = Object.create(Instruction.prototype);

Call.prototype.opcodes = [
    [0x84, "constant/"],
    [0x85, "indirect/"],
];

function call(op1) {
    return new Call([op1]);
}

// ----

function Ret(operands) {
    Instruction.call(this, operands);
}

Ret.prototype = Object.create(Instruction.prototype);

Ret.prototype.opcodes = [
    [0x90, ""],
];

function ret() {
    return new Ret([]);
}

// ----
function Reti(operands) {
    Instruction.call(this, operands);
}

Reti.prototype = Object.create(Instruction.prototype);

Reti.prototype.opcodes = [
    [0x91, ""],
];

function reti() {
    return new Reti([]);
}

// ----
function Seti(operands) {
    Instruction.call(this, operands);
}

Seti.prototype = Object.create(Instruction.prototype);

Seti.prototype.opcodes = [
    [0x92, ""],
];

function seti() {
    return new Seti([]);
}

// ----
function Cleari(operands) {
    Instruction.call(this, operands);
}

Cleari.prototype = Object.create(Instruction.prototype);

Cleari.prototype.opcodes = [
    [0x93, ""],
];

function cleari() {
    return new Cleari([]);
}

// ----
function Push(operands) {
    Instruction.call(this, operands);
}

Push.prototype = Object.create(Instruction.prototype);

Push.prototype.opcodes = [
    [0x94, "register/"],
    [0x95, "address/"],
    [0x96, "constant/"],
    [0x97, "indirect/"],
];

function push(op1) {
    return new Push([op1]);
}

// ----

function Pop(operands) {
    Instruction.call(this, operands);
}

Pop.prototype = Object.create(Instruction.prototype);

Pop.prototype.opcodes = [
    [0x98, "register/"],
];

function pop(op1) {
    return new Pop([op1]);
}

// ----
function Halt(operands) {
    Instruction.call(this, operands);
}

Halt.prototype = Object.create(Instruction.prototype);

Halt.prototype.opcodes = [
    [0xb0, ""],
];

function halt() {
    return new Halt([]);
}

// ----
function Sleep(operands) {
    Instruction.call(this, operands);
}

Sleep.prototype = Object.create(Instruction.prototype);

Sleep.prototype.opcodes = [
    [0xb1, ""],
];

function sleep() {
    return new Sleep([]);
}

// ----
function Setbit(operands) {
    Instruction.call(this, operands);
}

Setbit.prototype = Object.create(Instruction.prototype);

Setbit.prototype.opcodes = [
    [0xb8, "register/register/"],
    [0xb9, "register/constant/"],
];

function setbit(op1, op2) {
    return new Setbit([op1, op2]);
}


// ----
function Setbit(operands) {
    Instruction.call(this, operands);
}

Setbit.prototype = Object.create(Instruction.prototype);

Setbit.prototype.opcodes = [
    [0xb8, "register/register/"],
    [0xb9, "register/constant/"],
];

function setbit(op1, op2) {
    return new Setbit([op1, op2]);
}

// ----
function Clearbit(operands) {
    Instruction.call(this, operands);
}

Clearbit.prototype = Object.create(Instruction.prototype);

Clearbit.prototype.opcodes = [
    [0xbc, "register/register/"],
    [0xbd, "register/constant/"],
];

function clearbit(op1, op2) {
    return new Clearbit([op1, op2]);
}

// ----
function Isset(operands) {
    Instruction.call(this, operands);
}

Isset.prototype = Object.create(Instruction.prototype);

Isset.prototype.opcodes = [
    [0xbe, "register/register/"],
    [0xbf, "register/constant/"],
];

function isset(op1, op2) {
    return new Isset([op1, op2]);
}

// ----
function Db(data) {
    this.data = data;
}

Db.prototype.to_code = function() {
    return this.data;
}

Db.prototype.resolve = function(labelmap) {
}

function db(data) {
    return new Db(data);
}

function instrs_to_code(instrs) {

    // First pass, make label to value map.
    var labels = {};
    var count = 0;

    for(var i = 0; i < instrs.length; i++) {
	if (instrs[i].label) {
	    labels[instrs[i].label] = count;
	}
	var ic = instrs[i].to_code();
	count += ic.length;
    }

    // Next, resolve all constantref/addressref to constant/address
    for(var i = 0; i < instrs.length; i++) {
	instrs[i].resolve(labels);
    }

    // Final pass, produce machine code.
    var mc = [];
    for(var i = 0; i < instrs.length; i++) {
	var ic = instrs[i].to_code();
	for (var j = 0; j < ic.length; j++) {
 	    mc.push(ic[j]);
	}
    }

    return mc;

}

function oper_obj(oper) {
    if (oper["k"] == "register") return cm.register(oper["r"]);
    if (oper["k"] == "constant") return cm.constant(oper["v"]);
    if (oper["k"] == "address") return cm.address(oper["v"]);
    if (oper["k"] == "indirect") return cm.indirect(oper["r"], oper["o"]);
    if (oper["k"] == "constantref") return cm.constantref(oper["n"]);
    if (oper["k"] == "addressref") return cm.addressref(oper["n"]);
}

function instr_obj(instr) {
    var iobj;
    if (instr.instr == "db") {
	return cm.db(instr.opers[0]);
    }
    var opers = instr.opers;
    if (opers.length == 0)
	iobj = cm[instr.instr]();
    else if (opers.length == 1)
	iobj = cm[instr.instr](oper_obj(opers[0]));
    else
	iobj = cm[instr.instr](oper_obj(opers[0]), oper_obj(opers[1]));
    return iobj;
}

function asm_to_instrs(asm) {

    var parser = new nearley.Parser(grammar, {
	keepHistory: true,
    });

    parser.feed(asm);

    var instrs = [];

    for(var i = 0; i < parser.results[0].length; i++) {
		
	var item = parser.results[0][i];

	var label = item[0];
	var instr = item[1];

	if (label == null && instr == null) continue;

	var iobj;

	iobj = null;

	if (instr != null) {
	    iobj = instr_obj(instr);
	}

	if (label != null) {
	    iobj = cm.label(label, iobj);
	}
	
	instrs.push(iobj);

    }

    return instrs;
	    
}

cm = {}
cm["Address"] = Address;
cm["address"] = address;
cm["Indirect"] = Indirect;
cm["indirect"] = indirect;
cm["Constant"] = Constant;
cm["constant"] = constant;
cm["Register"] = Register;
cm["register"] = register;
cm["Constantref"] = Constantref;
cm["constantref"] = constantref;
cm["Addressref"] = Addressref;
cm["addressref"] = addressref;
cm["Instruction"] = Instruction;
cm["Label"] = Label;
cm["label"] = label;
cm["Nop"] = Nop;
cm["nop"] = nop;
cm["Move"] = Move;
cm["move"] = move;
cm["Add"] = Add;
cm["add"] = add;
cm["Sub"] = Sub;
cm["sub"] = sub;
cm["Inc"] = Inc;
cm["inc"] = inc;
cm["Dec"] = Dec;
cm["dec"] = dec;
cm["Mul"] = Mul;
cm["mul"] = mul;
cm["Div"] = Div;
cm["div"] = div;
cm["Mod"] = Mod;
cm["mod"] = mod;
cm["And"] = And;
cm["and"] = and;
cm["Or"] = Or;
cm["or"] = or;
cm["Xor"] = Xor;
cm["xor"] = xor;
cm["Not"] = Not;
cm["not"] = not;
cm["Shiftl"] = Shiftl;
cm["shiftl"] = shiftl;
cm["Shiftr"] = Shiftr;
cm["shiftr"] = shiftr;
cm["Equal"] = Equal;
cm["equal"] = equal;
cm["Lt"] = Lt;
cm["lt"] = lt;
cm["Lte"] = Lte;
cm["lte"] = lte;
cm["Gt"] = Gt;
cm["gt"] = gt;
cm["Gte"] = Gte;
cm["gte"] = gte;
cm["Jump"] = Jump;
cm["jump"] = jump;
cm["Jumpt"] = Jumpt;
cm["jumpt"] = jumpt;
cm["Jumpf"] = Jumpf;
cm["jumpf"] = jumpf;
cm["Call"] = Call;
cm["call"] = call;
cm["Ret"] = Ret;
cm["ret"] = ret;
cm["Reti"] = Reti;
cm["reti"] = reti;
cm["Seti"] = Seti;
cm["seti"] = seti;
cm["Cleari"] = Cleari;
cm["cleari"] = cleari;
cm["Push"] = Push;
cm["push"] = push;
cm["Pop"] = Pop;
cm["pop"] = pop;
cm["Halt"] = Halt;
cm["halt"] = halt;
cm["Sleep"] = Sleep;
cm["sleep"] = sleep;
cm["Setbit"] = Setbit;
cm["setbit"] = setbit;
cm["Setbit"] = Setbit;
cm["setbit"] = setbit;
cm["Clearbit"] = Clearbit;
cm["clearbit"] = clearbit;
cm["Isset"] = Isset;
cm["isset"] = isset;
cm["Db"] = Db;
cm["db"] = db;
cm["instrs_to_code"] = instrs_to_code;
cm["asm_to_instrs"] = asm_to_instrs;

this.cm = cm;
