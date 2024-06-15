import { Component, JSXElement, createEffect, lazy, splitProps, type JSX } from "solid-js";
type SVGAttributes = Partial<JSX.SvgSVGAttributes<SVGSVGElement>>
import "./Icon.styl";
import { Dynamic } from "solid-js/web";

const icons = {
    outline: import.meta.glob<{ default: Component<SVGAttributes> }>("/node_modules/@tabler/icons/icons/outline/*.svg", { query: "?component-solid" }),
    filled:  import.meta.glob<{ default: Component<SVGAttributes> }>("/node_modules/@tabler/icons/icons/filled/*.svg", { query: "?component-solid" })
} as const;

export interface IconProps extends SVGAttributes {
    name: string,
    type?: "outline" | "filled",
    size?: number|string,
    children?: JSXElement
}
export function Icon(props: IconProps) {
    const [local, rest] = splitProps(props, ["name", "type", "style", "class", "color", "size", "children"]);

    const Svg = () => {
        const type = local.type ?? "outline";
        const name = `/node_modules/@tabler/icons/icons/${type}/${local.name}.svg`;
        return lazy(() => icons[type][name]());
    };

    const klass = () => `ui-icon tabler-icon ${local.type ?? "outline"} tabler-icon-${local.name} ${local.class ?? ""}`;
    const style = () => {
        let parts = [];
        if (local.size) parts.push(`--icon-size: ${local.size}`);
        if (local.color) parts.push(`--icon-color: ${local.color}`);
        return parts.join("; ");
    }

    return (
        <Dynamic component={Svg()} xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class={klass()} style={style()} {...rest}>
            {local.children}
        </Dynamic>
    )
}
