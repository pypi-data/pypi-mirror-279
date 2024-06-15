import { Collapsible as KCollapsible } from "@kobalte/core";
import { JSXElement, splitProps } from "solid-js";
import { Icon } from "./Icon";
import "./Collapsible.styl";
import { Button } from "./Button";
import { Polymorphic } from "@src/util";

export type CollapsibleTriggerProps<T> = Polymorphic<T, KCollapsible.CollapsibleTriggerProps, { as?: T }>
export function CollapsibleTrigger<const T = typeof Button>(props: CollapsibleTriggerProps<T>) {
    let [local, remote] = splitProps(props, ["class", "children"]);
    return (
        <KCollapsible.Trigger as={Button} class={`ui-collapsible-trigger ${local.class ?? ""}`} {...remote}>
            {local.children}
        </KCollapsible.Trigger>
    )
}

export function CollapsibleTriggerIcon() {
    return (
        <Icon name="chevron-down" class="ui-collapsible-trigger-icon" />
    )
}

export function CollapsibleContent(props: KCollapsible.CollapsibleContentProps) {
    let [local, remote] = splitProps(props, ["class", "children"]);
    return (
        <div class={`ui-collapsible-content ${local.class ?? ""}`} {...remote}>
            <div class="ui-collapsible-inner">
                {local.children}
            </div>
        </div>
    )
}

export type CollapsibleProps<T> = Polymorphic<T, KCollapsible.CollapsibleRootProps, {
    as?: T
    class?: string,
    side: "right" | "left" | "bottom" | "top"
    children: JSXElement
}>
export function Collapsible<const T = "div">(props: CollapsibleProps<T>) {
    let [local, remote] = splitProps(props, ["class", "side", "children"]);
    return (
        <KCollapsible.Root {...remote} class={`ui-collapsible ${local.side} ${local.class ?? ""}`}>
            {local.children}
        </KCollapsible.Root>
    )
}
Collapsible.Trigger = CollapsibleTrigger;
Collapsible.TriggerIcon = CollapsibleTriggerIcon;
Collapsible.Content = CollapsibleContent;
