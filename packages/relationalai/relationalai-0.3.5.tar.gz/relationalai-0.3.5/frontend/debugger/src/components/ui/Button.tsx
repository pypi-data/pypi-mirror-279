import {Button as KButton} from "@kobalte/core";
import { type JSXElement, Match, Switch, splitProps } from "solid-js";
import {Tooltip} from "./Tooltip";
import "./Button.styl";
import { Polymorphic } from "@src/util";

export type ButtonProps<T> = Polymorphic<T, KButton.ButtonRootProps, {
    as?: T
    class?: string
    tooltip?: JSXElement
}>
export function Button<const T = "button">(props: ButtonProps<T>) {
    const [local, remote] = splitProps(props, ["class", "tooltip"]);
    return (
        <Switch>
            <Match when={local.tooltip}>
                <Tooltip content={local.tooltip}>
                    <Tooltip.Trigger as={KButton.Root} class={`ui-button ${local.class || ""}`} {...remote} />
                </Tooltip>
            </Match>
            <Match when={true}>
                <KButton.Root class={`ui-button ${local.class || ""}`} {...remote as KButton.ButtonRootProps} />
            </Match>
        </Switch>
    )
}
