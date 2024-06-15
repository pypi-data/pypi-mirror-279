/* @refresh reload */
import { render } from 'solid-js/web';

import './index.css';
import App from './App';

const root = document.getElementById('root');

function detect_os() {
  const platform = navigator.platform.toLowerCase();

  if (platform.startsWith("mac")) {
    return "mac";
  } else if (platform.startsWith("win")) {
    return "windows";
  } else {
    return "other";
  }
}

const OS = detect_os();

document.body.classList.add(`os-${OS}`);

if (import.meta.env.DEV && !(root instanceof HTMLElement)) {
    throw new Error(
        'Root element not found. Did you forget to add it to your index.html? Or maybe the id attribute got misspelled?',
    );
}

render(() => <App />, root!);
