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
  let cbSame = $state(false);

  let allSymbols = $derived.by(() => {
    let symbols = (cbNumbers ? numbers : '')
    + (cbUpper ? upper : '')
    + (cbLower ? lower : '')
    + (cbSymbolsSimple ? symbolsSimple : '')

    if (!cbSame) {
      symbols = symbols.replace(new RegExp('[' + same + ']', 'g'), '');
    }

    return symbols
  });

  let allSymbolsLength = $derived(allSymbols.length);

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

  let difficulty = $derived.by(() => {
    let html = '';
    if (result.length >= 14) {
      html = `<svg xmlns="http://www.w3.org/2000/svg" height="2em" width="2em" viewBox="0 -960 960 960" fill="#398712"><path d="m424-408-86-86q-11-11-28-11t-28 11q-11 11-11 28t11 28l114 114q12 12 28 12t28-12l226-226q11-11 11-28t-11-28q-11-11-28-11t-28 11L424-408Zm56 328q-83 0-156-31.5T197-197q-54-54-85.5-127T80-480q0-83 31.5-156T197-763q54-54 127-85.5T480-880q83 0 156 31.5T763-763q54 54 85.5 127T880-480q0 83-31.5 156T763-197q-54 54-127 85.5T480-80Zm0-80q134 0 227-93t93-227q0-134-93-227t-227-93q-134 0-227 93t-93 227q0 134 93 227t227 93Zm0-320Z"/></svg>`;
    } else if (result.length >= 10) {
      html = `<svg xmlns="http://www.w3.org/2000/svg" height="2em" width="2em" viewBox="0 -960 960 960" fill="#FFBF00"><path d="M109-120q-11 0-20-5.5T75-140q-5-9-5.5-19.5T75-180l370-640q6-10 15.5-15t19.5-5q10 0 19.5 5t15.5 15l370 640q6 10 5.5 20.5T885-140q-5 9-14 14.5t-20 5.5H109Zm69-80h604L480-720 178-200Zm302-40q17 0 28.5-11.5T520-280q0-17-11.5-28.5T480-320q-17 0-28.5 11.5T440-280q0 17 11.5 28.5T480-240Zm0-120q17 0 28.5-11.5T520-400v-120q0-17-11.5-28.5T480-560q-17 0-28.5 11.5T440-520v120q0 17 11.5 28.5T480-360Zm0-100Z"/></svg>`;
    } else {
      html = `<svg xmlns="http://www.w3.org/2000/svg" height="2em" width="2em" viewBox="0 -960 960 960" fill="#D24317"><path d="M363-120q-16 0-30.5-6T307-143L143-307q-11-11-17-25.5t-6-30.5v-234q0-16 6-30.5t17-25.5l164-164q11-11 25.5-17t30.5-6h234q16 0 30.5 6t25.5 17l164 164q11 11 17 25.5t6 30.5v234q0 16-6 30.5T817-307L653-143q-11 11-25.5 17t-30.5 6H363Zm1-80h232l164-164v-232L596-760H364L200-596v232l164 164Zm116-224 86 86q11 11 28 11t28-11q11-11 11-28t-11-28l-86-86 86-86q11-11 11-28t-11-28q-11-11-28-11t-28 11l-86 86-86-86q-11-11-28-11t-28 11q-11 11-11 28t11 28l86 86-86 86q-11 11-11 28t11 28q11 11 28 11t28-11l86-86Zm0-56Z"/></svg>`;
    }
    return html;
  })

  function regenerate() {
    cbNumbers = !cbNumbers;
    cbNumbers = !cbNumbers;
  }

  function copy() {
    navigator.clipboard.writeText(result);
  }
</script>

<main class="container">
  <div class="result-container">
    <button aria-label="difficulty" class="difficulty" style="cursor: default">{@html difficulty}</button>
    <span class="result-text">{@html resultColor}</span>
    <button aria-label="regenerate" onclick={regenerate}>
      <svg xmlns="http://www.w3.org/2000/svg" height="2em" width="2em" viewBox="0 -960 960 960" fill="var(--pico-primary)"><path d="M480-160q-134 0-227-93t-93-227q0-134 93-227t227-93q69 0 132 28.5T720-690v-70q0-17 11.5-28.5T760-800q17 0 28.5 11.5T800-760v200q0 17-11.5 28.5T760-520H560q-17 0-28.5-11.5T520-560q0-17 11.5-28.5T560-600h128q-32-56-87.5-88T480-720q-100 0-170 70t-70 170q0 100 70 170t170 70q68 0 124.5-34.5T692-367q8-14 22.5-19.5t29.5-.5q16 5 23 21t-1 30q-41 80-117 128t-169 48Z"/></svg>
    </button>
    <button aria-label="copy" onclick={copy}>
      <svg xmlns="http://www.w3.org/2000/svg" height="2em" width="2em" viewBox="0 -960 960 960" fill="var(--pico-primary)"><path d="M360-240q-33 0-56.5-23.5T280-320v-480q0-33 23.5-56.5T360-880h360q33 0 56.5 23.5T800-800v480q0 33-23.5 56.5T720-240H360Zm0-80h360v-480H360v480ZM200-80q-33 0-56.5-23.5T120-160v-520q0-17 11.5-28.5T160-720q17 0 28.5 11.5T200-680v520h400q17 0 28.5 11.5T640-120q0 17-11.5 28.5T600-80H200Zm160-240v-480 480Z"/></svg>
    </button>
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
      <input type="checkbox" name="dothraki" bind:checked={cbSame} />
      1Ii0Oo
    </label>
  </div>
  <small>Total: <b>{allSymbolsLength}</b></small>
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
    margin-bottom: 1.2em;
    padding: 0.8em;
    border-radius: 0.5em;
    background-color: var(--pico-code-background-color);
    width: 22.5em;
  }
  .result-text {
    font-size: 1.4em;
    max-height: 3.7em;
    margin-left: 0.3em;
    margin-right: 0.3em;
    word-break: break-word;
    overflow-y: auto;
    flex-grow: 1;
    text-align: center;
  }
  .slider-length {
    width: 12em;
  }
  .length-container {
    text-align: center;
  }
  .input-length {
    font-size: 1.5em;
  }
  button {
    padding: 0;
    border-radius: 2em;
    background-color: var(--pico-code-background-color);
    border-color: var(--pico-code-background-color);
    width: auto;
    flex-shrink: 0;
  }
  label {
    font-size: 1.25em;
  }
</style>
