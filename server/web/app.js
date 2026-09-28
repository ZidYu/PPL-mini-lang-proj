const $ = (selector) => document.querySelector(selector);
const $$ = (selector) => [...document.querySelectorAll(selector)];

const examples = {
  hello: {
    category: "Beginner",
    title: "Hello, Mini!",
    desc: "Print your first greeting to the console.",
    code: 'print("Hello, Mini Language!")'
  },
  variables: {
    category: "Beginner",
    title: "Variables",
    desc: "Store values and update them as your program runs.",
    code: 'let x = 5\nlet name = "Jasmin"\nprint(x)\nprint(name)'
  },
  condition: {
    category: "Beginner",
    title: "If / Else",
    desc: "Branch logic based on a true or false condition.",
    code: 'let x = 5\nif x > 3:\n    print("x is greater than 3")\nelse:\n    print("x is not greater than 3")\nend'
  },
  loop: {
    category: "Beginner",
    title: "While Loop",
    desc: "Repeat steps until a condition becomes false.",
    code: 'let x = 5\nwhile x < 8:\n    print(x)\n    x = x + 1\nend'
  },
  compare: {
    category: "Beginner",
    title: "Comparison Check",
    desc: "Use comparison operators to decide what to print.",
    code: 'let score = 88\nif score >= 90:\n    print("Pass with honors")\nelse:\n    print("Keep trying")\nend'
  },
  countdownBeginner: {
    category: "Beginner",
    title: "Countdown",
    desc: "Print numbers backward to explore loops in a simple way.",
    code: 'let n = 5\nwhile n > 0:\n    print(n)\n    n = n - 1\nend\nprint("Blast off!")'
  },
  function: {
    category: "Intermediate",
    title: "Function",
    desc: "Define a reusable routine and call it with arguments.",
    code: 'function add(a, b):\n    return a + b\nend\nlet result = add(5, 3)\nprint(result)'
  },
  calculator: {
    category: "Intermediate",
    title: "Calculator",
    desc: "Create a small calculator by combining functions and arithmetic.",
    code: 'function multiply(a, b):\n    return a * b\nend\nlet total = multiply(6, 7)\nprint(total)'
  },
  first: {
    category: "Intermediate",
    title: "First-class Function",
    desc: "Assign a function to a variable and invoke it later.",
    code: 'function add(a, b):\n    return a + b\nend\nlet operation = add\nprint(operation(2, 4))'
  },
  math: {
    category: "Intermediate",
    title: "Math Loop",
    desc: "Accumulate totals with a loop and numeric updates.",
    code: 'let total = 0\nlet n = 10\nwhile n > 0:\n    total = total + n\n    n = n - 1\nend\nprint(total)'
  },
  logic: {
    category: "Advanced",
    title: "Logic Gates",
    desc: "Use boolean logic to control flow with conditions.",
    code: 'let a = true\nlet b = false\nif a && !b:\n    print("Condition is true")\nelse:\n    print("Condition is false")\nend'
  },
  recursion: {
    category: "Advanced",
    title: "Recursion",
    desc: "Call a function from inside itself to solve a problem step by step.",
    code: 'function fact(n):\n    if n == 0:\n        return 1\n    else:\n        return n * fact(n - 1)\n    end\nend\nprint(fact(5))'
  }
};

const starter = `# Mini Language - starter program
let x = 5
let name = "Jasmin"
let passed = true

print(x)
print(name)
print(passed)

if x > 3:
    print("x is greater than 3")
else:
    print("x is not greater than 3")
end

while x < 8:
    print(x)
    x = x + 1
end

function add(a, b):
    return a + b
end
let result = add(5, 3)
print(result)`;

function setCode(value) {
  const editor = $("#editor");
  editor.value = value;
  updateLineNumbers();
  updateCursorPosition();
}

function updateLineNumbers() {
  const editor = $("#editor");
  const count = editor.value.split("\n").length;
  $("#numbers").textContent = Array.from({ length: count }, (_, i) => i + 1).join("\n");
}

function updateCursorPosition() {
  const editor = $("#editor");
  const beforeCursor = editor.value.slice(0, editor.selectionStart);
  const line = beforeCursor.split("\n").length;
  const lastNewLine = beforeCursor.lastIndexOf("\n");
  const col = lastNewLine === -1 ? beforeCursor.length + 1 : beforeCursor.length - lastNewLine;
  $("#position").textContent = `Line ${line}, Col ${col}`;
}

function setOutput(value) {
  $("#output").textContent = value;
}

function show(page) {
  $$(".page").forEach((section) => {
    section.classList.toggle("active", section.id === page);
  });

  $$('[data-page]').forEach((button) => {
    const isActive = button.dataset.page === page;
    button.classList.toggle("active", isActive);
  });

  location.hash = page;
}

const KEYWORDS = new Set([
  "let",
  "print",
  "if",
  "else",
  "while",
  "function",
  "return",
  "true",
  "false",
  "end"
]);

class MiniError extends Error {}

class Lexer {
  constructor(source) {
    this.source = source;
    this.index = 0;
    this.tokens = [];
  }

  advance() {
    this.index += 1;
  }

  peek(offset = 0) {
    return this.source[this.index + offset] ?? "";
  }

  scan() {
    while (this.index < this.source.length) {
      const ch = this.peek();

      if (/[\t\r ]/.test(ch)) {
        this.advance();
        continue;
      }

      if (ch === "\n") {
        this.tokens.push({ type: "newline", value: "\n" });
        this.advance();
        continue;
      }

      if (ch === "#") {
        while (this.index < this.source.length && this.peek() !== "\n") {
          this.advance();
        }
        continue;
      }

      if (/[0-9]/.test(ch)) {
        const start = this.index;
        while (/[0-9]/.test(this.peek())) {
          this.advance();
        }

        this.tokens.push({
          type: "number",
          value: Number(this.source.slice(start, this.index))
        });
        continue;
      }

      if (/[A-Za-z_]/.test(ch)) {
        const start = this.index;
        while (/[A-Za-z0-9_]/.test(this.peek())) {
          this.advance();
        }
        const value = this.source.slice(start, this.index);
        const type = KEYWORDS.has(value) ? "keyword" : "identifier";
        this.tokens.push({ type, value });
        continue;
      }

      if (ch === '"') {
        this.advance();
        let value = "";
        while (this.index < this.source.length && this.peek() !== '"') {
          value += this.peek();
          this.advance();
        }

        if (this.peek() !== '"') {
          throw new MiniError("Unclosed string literal.");
        }

        this.advance();
        this.tokens.push({ type: "string", value });
        continue;
      }

      const twoChar = this.source.slice(this.index, this.index + 2);
      if (["==", "!=", "<=", ">=", "&&", "||"].includes(twoChar)) {
        this.tokens.push({ type: "operator", value: twoChar });
        this.index += 2;
        continue;
      }

      if ("+-*/%(){}[],=:<>!".includes(ch)) {
        this.tokens.push({ type: "symbol", value: ch });
        this.advance();
        continue;
      }

      throw new MiniError(`Illegal character: ${ch}`);
    }

    this.tokens.push({ type: "eof", value: null });
    return this.tokens;
  }
}

class Parser {
  constructor(tokens) {
    this.tokens = tokens;
    this.index = 0;
  }

  current() {
    return this.tokens[this.index];
  }

  peek(offset = 0) {
    return this.tokens[this.index + offset] ?? { type: "eof", value: null };
  }

  advance() {
    const token = this.current();
    if (token.type !== "eof") {
      this.index += 1;
    }
    return token;
  }

  skipNewlines() {
    while (this.current().type === "newline") {
      this.advance();
    }
  }

  isStopToken(stopValues = []) {
    const token = this.current();

    if (token.type === "eof") {
      return true;
    }

    if (token.type === "keyword" && stopValues.includes(token.value)) {
      return true;
    }

    if (token.type === "symbol" && stopValues.includes(token.value)) {
      return true;
    }

    return false;
  }

  expect(type, value = null) {
    const token = this.current();

    if (token.type !== type) {
      throw new MiniError(`Expected ${type}, got ${token.type}.`);
    }

    if (value !== null && token.value !== value) {
      throw new MiniError(`Expected ${value}, got ${token.value}.`);
    }

    return this.advance();
  }

  match(type, value = null) {
    const token = this.current();

    if (token.type !== type) {
      return false;
    }

    if (value !== null && token.value !== value) {
      return false;
    }

    this.advance();
    return true;
  }

  parseProgram(stopValues = []) {
    const statements = [];
    this.skipNewlines();

    while (!this.isStopToken(stopValues)) {
      const token = this.current();
      if (token.type === "eof") {
        break;
      }

      statements.push(this.parseStatement());
      this.skipNewlines();
    }

    return statements;
  }

  parseStatement() {
    this.skipNewlines();
    const token = this.current();

    if (token.type === "keyword") {
      switch (token.value) {
        case "let":
          this.advance();
          const name = this.expect("identifier").value;
          this.expect("symbol", "=");
          return { kind: "let", name, expression: this.parseExpression() };

        case "print":
          this.advance();
          this.expect("symbol", "(");
          const printExpr = this.parseExpression();
          this.expect("symbol", ")");
          return { kind: "print", expression: printExpr };

        case "if":
          this.advance();
          const condition = this.parseExpression();
          this.expect("symbol", ":");
          const thenBlock = this.parseProgram(["else", "end"]);
          let elseBlock = [];

          if (this.current().type === "keyword" && this.current().value === "else") {
            this.advance();
            this.expect("symbol", ":");
            elseBlock = this.parseProgram(["end"]);
          }

          this.expect("keyword", "end");
          return { kind: "if", test: condition, yes: thenBlock, no: elseBlock };

        case "while":
          this.advance();
          const whileTest = this.parseExpression();
          this.expect("symbol", ":");
          const loopBody = this.parseProgram(["end"]);
          this.expect("keyword", "end");
          return { kind: "while", test: whileTest, body: loopBody };

        case "function":
          this.advance();
          const fnName = this.expect("identifier").value;
          this.expect("symbol", "(");
          const params = [];

          if (!this.match("symbol", ")")) {
            while (true) {
              params.push(this.expect("identifier").value);
              if (!this.match("symbol", ",")) {
                break;
              }
            }
            this.expect("symbol", ")");
          }

          this.expect("symbol", ":");
          const fnBody = this.parseProgram(["end"]);
          this.expect("keyword", "end");
          return { kind: "function", name: fnName, params, body: fnBody };

        case "return":
          this.advance();
          return { kind: "return", expression: this.parseExpression() };

        case "end":
          throw new MiniError("Unexpected end.");

        default:
          break;
      }
    }

    if (token.type === "identifier") {
      const name = this.advance().value;

      if (this.match("symbol", "=")) {
        return { kind: "set", name, expression: this.parseExpression() };
      }

      if (this.match("symbol", "(")) {
        const args = [];
        if (!this.match("symbol", ")")) {
          while (true) {
            args.push(this.parseExpression());
            if (!this.match("symbol", ",")) {
              break;
            }
          }
          this.expect("symbol", ")");
        }

        return { kind: "call", callee: { kind: "variable", name }, args };
      }

      return { kind: "expr", expression: { kind: "variable", name } };
    }

    if (token.type === "symbol" && token.value === "(") {
      return { kind: "expr", expression: this.parseExpression() };
    }

    return { kind: "expr", expression: this.parseExpression() };
  }

  parseExpression() {
    return this.parseComparison();
  }

  parseComparison() {
    let node = this.parseAdditive();

    while (["==", "!=", "<", ">", "<=", ">="].includes(this.current().value)) {
      const operator = this.advance().value;
      const right = this.parseAdditive();
      node = { kind: "binary", operator, left: node, right };
    }

    return node;
  }

  parseAdditive() {
    let node = this.parseMultiplicative();

    while (["+", "-"].includes(this.current().value)) {
      const operator = this.advance().value;
      const right = this.parseMultiplicative();
      node = { kind: "binary", operator, left: node, right };
    }

    return node;
  }

  parseMultiplicative() {
    let node = this.parseUnary();

    while (["*", "/", "%"].includes(this.current().value)) {
      const operator = this.advance().value;
      const right = this.parseUnary();
      node = { kind: "binary", operator, left: node, right };
    }

    return node;
  }

  parseUnary() {
    if (this.current().type === "symbol" && ["+", "-", "!"].includes(this.current().value)) {
      const operator = this.advance().value;
      return { kind: "unary", operator, expression: this.parseUnary() };
    }

    return this.parsePrimary();
  }

  parsePrimary() {
    const token = this.current();

    if (token.type === "number") {
      this.advance();
      return { kind: "literal", value: token.value };
    }

    if (token.type === "string") {
      this.advance();
      return { kind: "literal", value: token.value };
    }

    if (token.type === "keyword" && (token.value === "true" || token.value === "false")) {
      this.advance();
      return { kind: "literal", value: token.value === "true" };
    }

    if (token.type === "identifier") {
      const name = this.advance().value;
      if (this.match("symbol", "(")) {
        const args = [];
        if (!this.match("symbol", ")")) {
          while (true) {
            args.push(this.parseExpression());
            if (!this.match("symbol", ",")) {
              break;
            }
          }
          this.expect("symbol", ")");
        }
        return { kind: "call", callee: { kind: "variable", name }, args };
      }
      return { kind: "variable", name };
    }

    if (this.match("symbol", "(")) {
      const expr = this.parseExpression();
      this.expect("symbol", ")");
      return expr;
    }

    throw new MiniError(`Unexpected token: ${token.type} ${token.value ?? ""}`);
  }
}

class Environment {
  constructor(parent = null) {
    this.values = Object.create(null);
    this.parent = parent;
  }

  has(name) {
    return Object.prototype.hasOwnProperty.call(this.values, name) || (!!this.parent && this.parent.has(name));
  }

  get(name) {
    if (Object.prototype.hasOwnProperty.call(this.values, name)) {
      return this.values[name];
    }

    if (this.parent) {
      return this.parent.get(name);
    }

    throw new MiniError(`Undefined variable: ${name}`);
  }

  set(name, value) {
    if (Object.prototype.hasOwnProperty.call(this.values, name)) {
      this.values[name] = value;
      return;
    }

    if (this.parent && this.parent.has(name)) {
      this.parent.set(name, value);
      return;
    }

    this.values[name] = value;
  }

  declare(name, value) {
    this.values[name] = value;
  }
}

class FunctionValue {
  constructor(parameters, body, environment) {
    this.parameters = parameters;
    this.body = body;
    this.environment = environment;
  }
}

class ReturnSignal extends Error {
  constructor(value) {
    super();
    this.value = value;
  }
}

function execute(code) {
  const lexer = new Lexer(code);
  const tokens = lexer.scan();
  const parser = new Parser(tokens);
  const ast = parser.parseProgram();
  const env = new Environment();
  const logs = [];

  const evaluate = (node, scope) => {
    if (!node) {
      return null;
    }

    switch (node.kind) {
      case "literal":
        return node.value;

      case "variable":
        return scope.get(node.name);

      case "unary": {
        const value = evaluate(node.expression, scope);
        if (node.operator === "-") {
          if (typeof value !== "number") throw new MiniError("Unary minus requires a number.");
          return -value;
        }

        if (node.operator === "!") {
          if (typeof value !== "boolean") throw new MiniError("Logical not requires a boolean.");
          return !value;
        }

        return value;
      }

      case "binary": {
        const left = evaluate(node.left, scope);
        const right = evaluate(node.right, scope);

        if (node.operator === "+") {
          if (typeof left === "number" && typeof right === "number") return left + right;
          if (typeof left === "string" && typeof right === "string") return left + right;
          throw new MiniError("Type error: '+' requires two numbers or two strings.");
        }

        if (["-", "*", "/", "%", "<", ">", "<=", ">="].includes(node.operator)) {
          if (typeof left !== "number" || typeof right !== "number") {
            throw new MiniError("Arithmetic and comparison operators require two numbers.");
          }

          if (node.operator === "-") return left - right;
          if (node.operator === "*") return left * right;
          if (node.operator === "/") {
            if (right === 0) throw new MiniError("Division by zero.");
            return left / right;
          }
          if (node.operator === "%") {
            if (right === 0) throw new MiniError("Division by zero.");
            return left % right;
          }
          if (node.operator === "<") return left < right;
          if (node.operator === ">") return left > right;
          if (node.operator === "<=") return left <= right;
          if (node.operator === ">=") return left >= right;
        }

        if (node.operator === "==") return left === right;
        if (node.operator === "!=") return left !== right;

        if (node.operator === "&&") {
          if (typeof left !== "boolean" || typeof right !== "boolean") {
            throw new MiniError("Boolean AND requires two booleans.");
          }
          return left && right;
        }

        if (node.operator === "||") {
          if (typeof left !== "boolean" || typeof right !== "boolean") {
            throw new MiniError("Boolean OR requires two booleans.");
          }
          return left || right;
        }

        throw new MiniError(`Unsupported operator: ${node.operator}`);
      }

      case "call": {
        const callee = evaluate(node.callee, scope);

        if (!(callee instanceof FunctionValue)) {
          throw new MiniError("Type error: value is not callable.");
        }

        if (callee.parameters.length !== node.args.length) {
          throw new MiniError("Incorrect number of arguments.");
        }

        const localScope = new Environment(callee.environment);
        node.args.forEach((arg, index) => {
          localScope.declare(callee.parameters[index], evaluate(arg, scope));
        });

        try {
          runStatements(callee.body, localScope);
        } catch (error) {
          if (error instanceof ReturnSignal) {
            return error.value;
          }
          throw error;
        }

        return null;
      }

      default:
        throw new MiniError(`Unknown node kind: ${node.kind}`);
    }
  };

  const runStatements = (statements, scope) => {
    for (const statement of statements) {
      switch (statement.kind) {
        case "let": {
          scope.declare(statement.name, evaluate(statement.expression, scope));
          break;
        }

        case "set": {
          scope.set(statement.name, evaluate(statement.expression, scope));
          break;
        }

        case "print": {
          logs.push(String(evaluate(statement.expression, scope)));
          break;
        }

        case "return": {
          throw new ReturnSignal(evaluate(statement.expression, scope));
        }

        case "function": {
          scope.declare(statement.name, new FunctionValue(statement.params, statement.body, scope));
          break;
        }

        case "if": {
          const condition = evaluate(statement.test, scope);
          if (typeof condition !== "boolean") {
            throw new MiniError("If conditions must evaluate to a boolean.");
          }
          runStatements(condition ? statement.yes : statement.no, new Environment(scope));
          break;
        }

        case "while": {
          while (true) {
            const condition = evaluate(statement.test, scope);
            if (typeof condition !== "boolean") {
              throw new MiniError("While conditions must evaluate to a boolean.");
            }
            if (!condition) {
              break;
            }
            runStatements(statement.body, new Environment(scope));
          }
          break;
        }

        case "expr": {
          evaluate(statement.expression, scope);
          break;
        }

        default:
          throw new MiniError(`Unsupported statement: ${statement.kind}`);
      }
    }
  };

  runStatements(ast, env);
  return logs.join("\n");
}

function runProgram() {
  try {
    const result = execute($("#editor").value);
    const output = result ? `${result}\n\n> Execution finished.` : "(No output)\n\n> Execution finished.";
    setOutput(output);
  } catch (error) {
    setOutput(`Error: ${error.message}`);
  }
}

function renderGuide(category = "basics") {
  const guides = {
    basics: [
      ["Variable declaration", "let name = value"],
      ["Variable update", "name = value"],
      ["Print", "print(expression)"],
      ["Comments", "# comment"]
    ],
    control: [
      ["If / else", "if condition:\n    print(\"yes\")\nelse:\n    print(\"no\")\nend"],
      ["While", "while condition:\n    print(x)\n    x = x + 1\nend"],
      ["Operators", "+  -  *  /  %  ==  !=  <  >  <=  >=  &&  ||"]
    ],
    functions: [
      ["Function", "function add(a, b):\n    return a + b\nend"],
      ["Call", "let result = add(5, 3)"],
      ["First-class function", "let operation = add\nprint(operation(2, 4))"]
    ],
    ppl: [
      ["Formal grammar", "Recursive-descent parser builds an AST from grammar rules."],
      ["Lexical scoping", "Nested Environment objects resolve local and outer variables."],
      ["Runtime checks", "Type mismatches and division by zero are rejected."],
      ["Control flow", "if/else and while control execution."],
      ["Functions", "Functions are values that can be assigned and called."]
    ]
  };

  const guideElement = $("#guide");
  guideElement.innerHTML = guides[category]
    .map(([title, code]) => `
      <div class="guide-entry">
        <b>${title}</b>
        <pre>${code}</pre>
      </div>
    `)
    .join("");
}

function previewExample() {
  const value = $("#examplesSelect").value;
  $("#preview").textContent = examples[value].code;
}

function renderExampleCards() {
  const grouped = Object.entries(examples).reduce((accumulator, [key, value]) => {
    if (!accumulator[value.category]) {
      accumulator[value.category] = [];
    }
    accumulator[value.category].push([key, value]);
    return accumulator;
  }, {});

  $("#exampleCards").innerHTML = Object.entries(grouped)
    .map(([category, items]) => `
      <div class="example-group">
        <h2>
          <span>${category}</span>
          <span class="example-count">${items.length}</span>
        </h2>
        ${items
          .map(
            ([key, item]) => `
              <article class="example-card">
                <h3>${item.title}</h3>
                <p>${item.desc}</p>
                <button class="primary" data-load="${key}">Load Example</button>
              </article>
            `
          )
          .join("")}
      </div>
    `)
    .join("");

  $$('[data-load]').forEach((button) => {
    button.addEventListener("click", () => {
      const example = examples[button.dataset.load];
      setCode(example.code);
      show("playground");
      setOutput("Example loaded. Click Run Program to execute it.");
    });
  });
}

const select = $("#examplesSelect");
Object.entries(examples).forEach(([key, example]) => {
  select.add(new Option(`${example.title} (${example.category})`, key));
});

select.addEventListener("change", previewExample);
$("#load").addEventListener("click", () => {
  const example = examples[select.value];
  setCode(example.code);
  setOutput("Example loaded. Click Run Program to execute it.");
});

$("#run").addEventListener("click", runProgram);
$("#headerRun").addEventListener("click", runProgram);
$("#reset").addEventListener("click", () => {
  setCode(starter);
  setOutput("Ready to run your program.");
});
$("#clear").addEventListener("click", () => setOutput("Output cleared."));

$("#editor").addEventListener("input", () => {
  updateLineNumbers();
  updateCursorPosition();
});
$("#editor").addEventListener("keyup", updateCursorPosition);
$("#editor").addEventListener("click", updateCursorPosition);

$$('[data-page]').forEach((button) => {
  button.addEventListener("click", () => show(button.dataset.page));
});

$$('[data-guide]').forEach((button) => {
  button.addEventListener("click", () => {
    $$('[data-guide]').forEach((item) => item.classList.remove("active"));
    button.classList.add("active");
    renderGuide(button.dataset.guide);
  });
});

const themeSelect = $("#theme");
themeSelect.addEventListener("change", () => {
  const theme = themeSelect.value;
  document.documentElement.dataset.theme = theme;
  localStorage.setItem("mini-theme", theme);
});

themeSelect.value = localStorage.getItem("mini-theme") || "system";
document.documentElement.dataset.theme = themeSelect.value;

setCode(starter);
previewExample();
renderGuide();
renderExampleCards();

if (location.hash) {
  const page = location.hash.slice(1);
  if (page) {
    show(page);
  }
}