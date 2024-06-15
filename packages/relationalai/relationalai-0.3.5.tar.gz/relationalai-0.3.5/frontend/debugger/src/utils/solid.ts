import { TimeoutSource, createPolled } from "@solid-primitives/timer";
import { Accessor, SignalOptions, createEffect, createSignal } from "solid-js";

export function createPolledAsync<T extends P, P = T>(fn: (prev: P | Exclude<undefined, P>) => Promise<T>, timeout: TimeoutSource, value?: undefined, options?: SignalOptions<T>): Accessor<T>;
export function createPolledAsync<T extends P, I = T, P = T>(fn: (prev: P | I) => Promise<T>, timeout: TimeoutSource, value?: I, options?: SignalOptions<T>): Accessor<T> {
    const promise = createPolled<Promise<T>>(fn as any, timeout);
    const [cur, set_cur] = createSignal(value as any, options);

    createEffect(async () => set_cur(await promise() as any));

    return cur;
}

export function classy(...args: ({ [key: string]: any } | string | undefined)[]): string {
  const class_list: string[] = [];

  for (const arg of args) {
    if (typeof arg === "string") {
      class_list.push(arg);
    } else if (typeof arg === "object" && arg !== null) {
      for (const key in arg) {
        if (arg[key]) {
          class_list.push(key);
        }
      }
    }
  }

  return class_list.join(" ");
}

export const [auto_scroll_enabled, set_auto_scroll_enabled] = createSignal(false);

let prior_top = window.scrollY;
window.addEventListener("scroll", (event: Event) => {
  const scroll_top = window.scrollY;

  // Ignore spurious scroll events when document size changes
  if(prior_top === scroll_top) return;

  prior_top = scroll_top;

  if(auto_scrolling) return;

  const scrollable_height = document.documentElement.scrollHeight;
  const client_height = document.documentElement.clientHeight;

  // Check if the user is at the bottom of the page
  const scrolled_to_bottom = Math.ceil(scroll_top + client_height) >= scrollable_height - 10; // grace threshold of 10px
  set_auto_scroll_enabled(scrolled_to_bottom);
})

let auto_scroll_ix = 1;
let auto_scrolling:number|undefined;
let scheduled_rescroll = false

export function begin_auto_scroll() {
  if(auto_scrolling) {
    scheduled_rescroll = true;
    return;
  }

  auto_scrolling = auto_scroll_ix++;
  setTimeout(() => {
    window.scrollTo({
    top: document.documentElement.scrollHeight,
    behavior: "smooth",
  });
  }, 0);

  setTimeout(finish_auto_scroll, 750, auto_scrolling)
}

function finish_auto_scroll(ix: number = auto_scrolling!) {
  if(auto_scrolling !== ix) return;
  auto_scrolling = undefined;
  if(scheduled_rescroll) begin_auto_scroll();
  scheduled_rescroll = false;
}

window.addEventListener("scrollend", () => finish_auto_scroll);
