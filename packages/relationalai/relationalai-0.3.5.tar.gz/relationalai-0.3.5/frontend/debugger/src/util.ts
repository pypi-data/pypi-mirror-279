import type { Component, JSX } from "solid-js";

export function ends_in<T>(list: T[], one_of: T[]) {
    if(list.length === 0) return false;

    let last = list[list.length - 1];
    for(let v of one_of) {
        if(v === last) return true;
    }
    return false;
}

export function prefix_of<T>(list: T[], prefix: T[]) {
    if(list.length < prefix.length) return false;
    for(let ix = 0; ix < prefix.length; ix += 1) {
        if(list[ix] !== prefix[ix]) return false;
    }
    return true;
}

export function omit<T extends object, K extends keyof T>(v: T, ...keys: K[]): Omit<T, K> {
    const copy = {...v};
    for(const key of keys) {
        delete copy[key];
    }
    return copy;
}

function fallback_copy_text_to_clipboard(text: string): Promise<void> {
    var textArea = document.createElement('textarea');
    textArea.value = text;

    // Avoid scrolling to bottom
    textArea.style.top = '0';
    textArea.style.left = '0';
    textArea.style.position = 'fixed';

    return new Promise<void>((resolve, reject) => {
        try {
            document.body.appendChild(textArea);
            textArea.focus();
            textArea.select();

            var successful = document.execCommand('copy');
            setTimeout(() => successful ? resolve() : reject(), 1);
        } catch (err) {
            setTimeout(() => reject(err), 1);
        }
        document.body.removeChild(textArea);
    });
}

export async function copy_text_to_clipboard(text: string): Promise<void> {
    try {
        await navigator.clipboard.writeText(text);
        return;
    } catch {
        await fallback_copy_text_to_clipboard(text);
    }
}



export type PolymorphProps<T> =
    T extends Component<infer U> ?
        U : (T extends keyof JSX.HTMLElementTags ?
             JSX.HTMLElementTags[T] :
             JSX.HTMLAttributes<HTMLElement>);

export type Polymorphic<T, P, P2 = {}> = PolymorphProps<T>&P&P2
