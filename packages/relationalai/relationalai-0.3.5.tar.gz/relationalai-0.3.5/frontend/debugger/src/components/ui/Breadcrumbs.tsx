import {Breadcrumbs as KBreadcrumbs} from "@kobalte/core";
import { splitProps } from "solid-js";
import "./Breadcrumbs.styl";
import { Icon } from "./Icon";

export interface BreadcrumbsItemProps extends KBreadcrumbs.BreadcrumbsLinkProps {
    onClick?: (event: MouseEvent) => any
}
export function BreadcrumbsItem(props: BreadcrumbsItemProps) {
    let [local, rest] = splitProps(props, ["children", "class", "onClick"]);
    return (
        <li class={`ui-breadcrumbs-item ${local.class ?? ""}`} onClick={local.onClick}>
            <KBreadcrumbs.Link class="ui-breadcrumbs-item-link" {...rest}>
                {local.children}
            </KBreadcrumbs.Link>
            <KBreadcrumbs.Separator class="ui-breadcrumbs-item-sep" />
        </li>
    );
}

export interface BreadcrumbsProps extends KBreadcrumbs.BreadcrumbsRootProps {
}
export function Breadcrumbs(props: BreadcrumbsProps) {
    let [local, rest] = splitProps(props, ["children", "class"]);
    return (
        <KBreadcrumbs.Root class={`ui-breadcrumbs ${local.class ?? ""}`} separator={<Icon name="chevron-right" />} {...rest}>
            <ol>
                {local.children}
            </ol>
        </KBreadcrumbs.Root>
    );
}

Breadcrumbs.Item = BreadcrumbsItem;
