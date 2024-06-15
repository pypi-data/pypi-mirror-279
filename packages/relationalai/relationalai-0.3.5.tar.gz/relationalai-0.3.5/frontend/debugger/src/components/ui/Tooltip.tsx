import { Tooltip as KTooltip } from "@kobalte/core";
import { JSXElement, splitProps } from "solid-js";
import "./Tooltip.styl";

export interface TooltipProps extends KTooltip.TooltipRootProps {
    class?: string,
    content: JSXElement,
    children: JSXElement
}
export function Tooltip(props: TooltipProps) {
    const [local, remote] = splitProps(props, ["class", "content", "children"]);
    return (
        <KTooltip.Root {...remote}>
            {local.children}
            <KTooltip.Portal>
                <KTooltip.Content class={`ui-tooltip ${local.class || ""}`}>
                    <KTooltip.Arrow class="ui-tooltip-arrow" />
                    <div class="ui-tooltip-inner">
                        {local.content}
                    </div>
                </KTooltip.Content>
            </KTooltip.Portal>
        </KTooltip.Root>
    )
}

Tooltip.Trigger = KTooltip.Trigger;
