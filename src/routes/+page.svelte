<script lang="ts">
  const numbers = '0123456789';
  const lower = 'abcdefghijklmnopqrstuvwxyz';
  const upper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
  const symbolsSimple = '!@#$%^&*';
  const same = '1Il0Oo';

  let length = $state(14);
  
  let cbNumbers = $state(true);
  let cbLower = $state(true);
  let cbUpper = $state(true);
  let cbSymbolsSimple = $state(true);
  let cdSame = $state(false);

  let allSymbols = $derived.by(() => {
    let symbols = (cbNumbers ? numbers : '')
    + (cbUpper ? upper : '')
    + (cbLower ? lower : '')
    + (cbSymbolsSimple ? symbolsSimple : '')

    if (!cdSame) {
      symbols = symbols.replace(new RegExp('[' + same + ']', 'g'), '');
    }

    return symbols
  });

  $inspect(allSymbols)

  let result = $derived.by(() => {
    let pass = '';

    function generatePass() {
      let pass = '';
      for (let i = 0; i < length; i++) {
        pass += allSymbols.charAt(Math.floor(Math.random() * allSymbols.length));
      }
      return pass
    };

    let needsRegeneration = true;
    while (needsRegeneration) {
      needsRegeneration = false;
      
      if (length < 4) {
        return `Length must be at least 4`;
      }
      if (length > 9999) {
        return `Length must be at most 9999`;
      }
      if (allSymbols.length === 0) {
        return `Check at least one option`;
      }

      if (cbNumbers && !numbers.split('').some(c => pass.includes(c))) {
        needsRegeneration = true;
      }
      if (cbLower && !lower.split('').some(c => pass.includes(c))) {
        needsRegeneration = true;
      }
      if (cbUpper && !upper.split('').some(c => pass.includes(c))) {
        needsRegeneration = true;
      }
      if (cbSymbolsSimple && !symbolsSimple.split('').some(c => pass.includes(c))) {
        needsRegeneration = true;
      }

      if (needsRegeneration) {
        pass = generatePass();
      }
    }
    
    return pass
  })

  let resultColor = $derived.by(() => {
    let html = '';
    for (let char of result) {
      if (numbers.includes(char)) {
        html += `<span style="color: #3C71F7;">${char}</span>`;
      } else if (symbolsSimple.includes(char)) {
        html += `<span style="color: #D93526;">${char}</span>`;
      } else {
        html += char;
      }
    }
    return html;
  })

  function copy() {
    navigator.clipboard.writeText(result);
  }
</script>

<main class="container">
  <div class="result-container">
    <span class="result-text">{@html resultColor}</span>
    <button class="secondary copy" onclick={copy}>Copy</button>
  </div>

  <input type="range" bind:value={length} min="4" max="28" class="slider-length"/>
  <div class="length-container">
    <input type="number" bind:value={length} min="4" max="9999" class="input-length">
    <small>Length</small>
  </div>
  
  <div class="options">
    <label>
      <input type="checkbox" name="numbers" bind:checked={cbNumbers} />
      0-9
    </label>
    <label>
      <input type="checkbox" name="upper" bind:checked={cbUpper} />
      A-Z
    </label>
    <label>
      <input type="checkbox" name="lower" bind:checked={cbLower} />
      a-z
    </label>
    <label>
      <input type="checkbox" name="symbols" bind:checked={cbSymbolsSimple} />
      !@#$%^&*
    </label>
    <label>
      <input type="checkbox" name="dothraki" bind:checked={cdSame} />
      1Ii0Oo
    </label>
  </div>
</main>

<style>
  .container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100vh;
    font-family: monospace;
  }
  .result-container {
    display: flex;
    align-items: center;
    margin: 20px;
    padding: 10px;
    border-radius: 5px;
    background-color: var(--pico-code-background-color);
    width: 22em;
  }
  .result-text {
    font-size: 1.4em;
    max-height: 3.7em;
    margin-right: 0.3em;
    word-break: break-word;
    overflow-y: auto;
    flex-grow: 1;
    text-align: center;
  }
  .slider-length {
    width: 150px;
  }
  .length-container {
    text-align: center;
  }
  .input-length {
    font-size: 1.5em;
  }
  button {
    padding: 3px;
    width: auto;
    flex-shrink: 0;
  }
  label {
    font-size: 1.25em;
  }
</style>
