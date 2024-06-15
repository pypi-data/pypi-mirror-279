import { NumberField as KNumberField, TextField as KTextField } from "@kobalte/core";
import { JSXElement, Show, splitProps } from "solid-js";
import "./Field.styl";
import { Icon } from "./Icon";
import { Button } from "./Button";

//------------------------------------------------------------------------------
// Common Formats
//------------------------------------------------------------------------------

function coerce<const T extends Record<string, Intl.NumberFormatOptions>>(v: T) {
    return v;
}

export const Format = coerce({
    "seconds": {
        style: "unit",
        unit: "second",
        unitDisplay: "long",
        minimumFractionDigits: 0,
        maximumFractionDigits: 1,
    }
})

//------------------------------------------------------------------------------
// NumberField
//------------------------------------------------------------------------------

export interface NumberFieldProps extends KNumberField.NumberFieldRootProps {
    label: JSXElement,
    placeholder?: string
}
export function NumberField(props: NumberFieldProps) {
    let [local, remote] = splitProps(props, ["label", "class", "placeholder"]);
    return (
        <KNumberField.Root {...remote} class={`ui-field number ${local.class ?? ""}`}>
            <KNumberField.Label>{local.label}</KNumberField.Label>
            <KNumberField.HiddenInput />
            <span class="ui-field-input">
                <KNumberField.Input class="ui-field-value" placeholder={local.placeholder} />
                <div class="ui-field-controls">
                    <KNumberField.IncrementTrigger as={Button} class="icon ui-field-input-increment">
                        <Icon name="chevron-up" size="0.9em" />
                    </KNumberField.IncrementTrigger>
                    <KNumberField.DecrementTrigger as={Button} class="icon ui-field-input-decrement">
                        <Icon name="chevron-down" size="0.9em" />
                    </KNumberField.DecrementTrigger>
                </div>
            </span>
        </KNumberField.Root>
    )
}

//------------------------------------------------------------------------------
// TextField
//------------------------------------------------------------------------------

export interface TextFieldProps extends KTextField.TextFieldRootProps {
    label: JSXElement,
    type?: string,
    placeholder?: string,
    multiline?: boolean,
    children?: JSXElement,
}
export function TextField(props: TextFieldProps) {
    let [local, remote] = splitProps(props, ["label", "type", "class", "placeholder", "multiline", "children"]);
    return (
        <KTextField.Root {...remote} class={`ui-field ${local.type ?? "text"} ${local.class ?? ""}`}>
            <KTextField.Label>{local.label}</KTextField.Label>
            <span class="ui-field-input">
                <Show when={!local.multiline}>
                    <KTextField.Input class="ui-field-value" placeholder={local.placeholder} />
                </Show>
                <Show when={local.multiline}>
                    <KTextField.TextArea class="ui-field-value multiline" placeholder={local.placeholder} />
                </Show>
            </span>
            {local.children}
        </KTextField.Root>
    )
}
TextField.Description = KTextField.Description;
TextField.ErrorMessage = KTextField.ErrorMessage

export namespace Field {
    export const Text = TextField;
    export const Number = NumberField;
}
