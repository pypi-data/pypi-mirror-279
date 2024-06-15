import { JSXElement, Ref, Show, children, createEffect, splitProps } from "solid-js";
import "prismjs/themes/prism.css";
import "prismjs/plugins/line-numbers/prism-line-numbers.css";
import "prismjs/plugins/line-highlight/prism-line-highlight.css";
import "prismjs/plugins/toolbar/prism-toolbar.css";
import Prism from "prismjs";
import { Button } from "./Button";
import { Icon } from "./Icon";
import "./Code.styl";
import { copy_text_to_clipboard } from "@src/util";

Prism.languages.rel = Prism.languages.python;

export interface CodeProps {
    ref?: Ref<HTMLElement>;
    class?: string,
    children: string|undefined,
    lang?: string
}
export function Code(props: CodeProps) {
    let ref!:HTMLElement;
    createEffect(() => {
        ref.textContent = props.children ?? ""; // prism doing its thing breaks solid updating the value itself.
        Prism.highlightElement(ref);
    });

    const lang_class = () => props.lang ? `language-${props.lang}` : "";
    const set_ref = (elem: HTMLElement) => {
        ref = elem;
        typeof props.ref === "function" ? props.ref(elem) : props.ref = elem;
    };

    return (
        <code ref={set_ref} class={`ui-code ${lang_class()} ${props.class || ""}`} textContent={props.children} />
    )
}


export interface CodeBlockProps extends Omit<CodeProps, "ref"> {
    ref?: Ref<HTMLPreElement>;
    no_copy?: boolean,
    dense?: boolean,
}
export function CodeBlock(props: CodeBlockProps) {
    const [local, rest] = splitProps(props, ["ref", "no_copy", "dense", "class"]);
    let code_ref!:HTMLElement;
    const has_controls = () => !local.no_copy;
    const copy = () => {
        const text = code_ref.textContent;
        if(text) {
            copy_text_to_clipboard(text);
        }
    }
    return (
        <pre ref={props.ref} class={`ui-code-block ${local.dense ? "dense" : ""} ${local.class || ""}`}>
            <Code ref={code_ref} {...rest} />
            <Show when={has_controls()}>
                <div class="code-controls">
                    <Show when={!local.no_copy}>
                        <Button class="icon" tooltip="copy to clipboard" onclick={copy}>
                            <Icon name="copy" />
                        </Button>
                    </Show>
                </div>
            </Show>
        </pre>
    )
}
