import { As, Accordion as KAccordion } from "@kobalte/core";
import { JSXElement, Show, splitProps } from "solid-js";
import "./Accordion.styl";

//------------------------------------------------------------------------------
// Subcomponents
//------------------------------------------------------------------------------

interface AccordionHeaderProps extends KAccordion.AccordionHeaderProps {}
export function AccordionHeader(props: AccordionHeaderProps) {
    let [local, remote] = splitProps(props, ["class", "children"])
    return (
        <KAccordion.Header class={`ui-accordion-header ${local.class ?? ""}`} asChild {...remote}>
            <As component={KAccordion.Trigger} as="header">
                {local.children}
            </As>
        </KAccordion.Header>
    )
}

interface AccordionContentProps extends KAccordion.AccordionContentProps {}
export function AccordionContent(props: AccordionContentProps) {
    let [local, remote] = splitProps(props, ["children", "class"])
    return (
        <KAccordion.Content class={`ui-accordion-content ${local.class ?? ""}`} {...remote}>
            {local.children}
        </KAccordion.Content>
    )
}

interface AccordionItemProps extends KAccordion.AccordionItemProps {
    header?: JSXElement
}
export function AccordionItem(props: AccordionItemProps) {
    let [local, remote] = splitProps(props, ["header", "children", "class"])
    return (
        <KAccordion.Item class={`ui-accordion-item ${local.class ?? ""}`} {...remote}>
            <Show when={local.header}>
                <AccordionHeader>{local.header}</AccordionHeader>
                <AccordionContent>{props.children}</AccordionContent>
            </Show>
            <Show when={!local.header}>
                {props.children}
            </Show>
        </KAccordion.Item>
    )
}

//------------------------------------------------------------------------------
// Accordion
//------------------------------------------------------------------------------

interface AccordionProps extends KAccordion.AccordionRootProps {}
export function Accordion(props: AccordionProps) {
    const [local, remote] = splitProps(props, ["children", "class"]);
    return (
        <KAccordion.Root class={`ui-accordion ${local.class ?? ""}`} {...remote}>
            {props.children}
        </KAccordion.Root>
    );
}
Accordion.Item = AccordionItem;
Accordion.Header = AccordionHeader;
Accordion.Content = AccordionContent;
