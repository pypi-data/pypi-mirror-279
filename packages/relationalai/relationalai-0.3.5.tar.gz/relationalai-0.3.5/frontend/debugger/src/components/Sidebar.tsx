import { splitProps } from "solid-js";
import "./Sidebar.styl";
import { Collapsible, CollapsibleProps } from "./ui/Collapsible";

export interface SidebarProps extends CollapsibleProps {
}
export function Sidebar(props: SidebarProps) {
    let [local, remote] = splitProps(props, ["class", "side", "children"]);
    return (
        <Collapsible {...remote} side={props.side} class={`sidebar ${local.side} ${local.class ?? ""}`}>
            <Collapsible.Trigger class="sidebar-trigger icon">
                <Collapsible.TriggerIcon />
            </Collapsible.Trigger>
            <Collapsible.Content class="sidebar-content">
                <div class="sidebar-inner">
                    {local.children}
                </div>
            </Collapsible.Content>
        </Collapsible>
    )
}
