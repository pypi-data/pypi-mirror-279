import { Dialog as KDialog } from "@kobalte/core";
import { JSXElement, splitProps } from "solid-js";
import { Button } from "./Button";
import "./Modal.styl";
import { Icon } from "./Icon";
import { Polymorphic } from "@src/util";

export interface ModalProps extends KDialog.DialogRootProps {
    title?: string,
    class?: string,
    content?: JSXElement,
}
export function Modal(props: ModalProps) {
    const [local, remote] = splitProps(props, ["title", "content", "children", "class"]);
    return (
        <KDialog.Root modal {...remote}>
            {local.children}
            <KDialog.Portal>
                <div class="ui-modal">
                    <KDialog.Overlay class="ui-modal-overlay" />
                    <KDialog.Content class={`ui-modal-content ${local.class || ""}`}>
                        <header class="ui-modal-header">
                            <Modal.Title class="ui-modal-title">{local.title}</Modal.Title>
                            <Modal.CloseButton as={Button} class="ui-modal-close icon">
                                <Icon name="x" />
                            </Modal.CloseButton>
                        </header>
                        {local.content}
                    </KDialog.Content>
                </div>
            </KDialog.Portal>
        </KDialog.Root>
    )
}

export type ModalTriggerProps<T> = Polymorphic<T, KDialog.DialogTriggerProps, { as?: T }>
Modal.Trigger = <const T = "button">(props: ModalTriggerProps<T>) => KDialog.Trigger(props);
Modal.Title = KDialog.Title;
Modal.CloseButton = KDialog.CloseButton;
Modal.Description = KDialog.Description;
