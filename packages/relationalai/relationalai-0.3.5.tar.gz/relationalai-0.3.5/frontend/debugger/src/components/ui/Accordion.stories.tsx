import type {Meta, StoryObj} from "storybook-solidjs";
import {Accordion} from "./Accordion";
import { For } from "solid-js";

const meta: Meta<typeof Accordion> = {
    component: Accordion,
}

export default meta;

type Story = StoryObj<typeof Accordion>;

export const Static: Story = {
    render: (args) => {
        return (
            <Accordion {...args}>
                <Accordion.Item value="1">
                    <Accordion.Header>item 1</Accordion.Header>
                    <Accordion.Content>
                        some content for one
                    </Accordion.Content>
                </Accordion.Item>
                <Accordion.Item value="2">
                    <Accordion.Header>item 2</Accordion.Header>
                    <Accordion.Content>
                        some content for two
                    </Accordion.Content>
                </Accordion.Item>
                <Accordion.Item value="3">
                    <Accordion.Header>item 3</Accordion.Header>
                    <Accordion.Content>
                        some content for three
                    </Accordion.Content>
                </Accordion.Item>
            </Accordion>
        )
    },
    args: {
        multiple: false,
    }
}

export const Dynamic: Story = {
    render: (args) => {
        let items = ["a", "b", "c", "d", "e"]
        return (
            <Accordion {...args}>
                <For each={items}>
                    {(item) => (
                        <Accordion.Item value={item}>
                            <Accordion.Header>
                                item {item}
                            </Accordion.Header>
                            <Accordion.Content>
                                some content for {item}
                            </Accordion.Content>
                        </Accordion.Item>
                    )}
                </For>
            </Accordion>
        )
    },
    args: {
        multiple: false
    }
}

export const InlineHeader: Story = {
    render: (args) => {
        let items = ["a", "b", "c", "d", "e"]
        return (
            <Accordion {...args}>
                <For each={items}>
                    {(item) => (
                        <Accordion.Item value={item} header={`item ${item}`}>
                            some content for {item}
                        </Accordion.Item>
                    )}
                </For>
            </Accordion>
        )
    },
    args: {
        multiple: false,
    }
}
