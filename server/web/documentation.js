const documentationContent = `
  <h2>Concepts demonstrated</h2>
  <div class="doc-grid">
    <article><h3>Syntax and semantics</h3><p>Grammar rules define valid programs, while the evaluator defines what those programs do.</p></article>
    <article><h3>Variables and data types</h3><p>Use <code>let</code> with numbers, strings, and Booleans. Values are checked at runtime.</p></article>
    <article><h3>Expressions and operators</h3><p>Arithmetic, comparisons, equality, and Boolean operators such as <code>and</code>, <code>or</code>, and <code>!</code> are supported.</p></article>
    <article><h3>Control structures</h3><p><code>if</code>/<code>else</code> selects a branch and <code>while</code> repeats a block while its condition is true.</p></article>
    <article><h3>Functions and recursion</h3><p>Functions accept parameters and return values. A function can call itself, as in factorial.</p></article>
    <article><h3>Scope and binding</h3><p>Functions retain their defining environment, so they can read variables from an enclosing scope through lexical closures.</p></article>
    <article><h3>Abstraction and modularity</h3><p>Functions hide implementation details, while the lexer, parser, AST, environment, and interpreter separate responsibilities.</p></article>
  </div>
  <h2>Common syntax</h2>
  <div class="doc-grid">
    <article><h3>Variables and output</h3><pre>let score = 5
score = score + 1
print(score)</pre></article>
    <article><h3>Branching and loops</h3><pre>if score &gt; 5:
    print("high")
else:
    print("low")
end</pre></article>
    <article><h3>Functions</h3><pre>function add(a, b):
    return a + b
end
print(add(2, 3))</pre></article>
    <article><h3>Recursion</h3><pre>function factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)
    end
end</pre></article>
  </div>
  <h2>Execution and errors</h2>
  <p>Statements run from top to bottom. The lexer creates tokens, the parser builds an abstract syntax tree, and the interpreter evaluates it using environments.</p>
  <p>Errors include illegal characters, invalid syntax, undefined variables, invalid calls, incompatible types, non-Boolean conditions, division by zero, and runaway loops. Mini does not currently include user-facing <code>try</code>/<code>catch</code> syntax.</p>
  <button class="primary" data-page="playground">Try the language in Playground</button>`;

document.querySelector('#documentation .content').insertAdjacentHTML('beforeend', documentationContent);
document.querySelector('#documentation [data-page="playground"]').onclick = () => {
    document.querySelectorAll('.page').forEach(page => page.classList.toggle('active', page.id === 'playground'));
    document.querySelectorAll('[data-page]').forEach(button => button.classList.toggle('active', button.dataset.page === 'playground'));
    location.hash = 'playground';
};
