import type {Meta, StoryObj} from "storybook-solidjs";
import {Collapsible} from "./Collapsible";

const meta: Meta<typeof Collapsible> = {
    component: Collapsible,
    argTypes: {
        side: {
            control: { type: "select" },
            options: ["left", "top", "bottom", "right"]
        }
    }
}

export default meta;

type Story = StoryObj<typeof Collapsible>;

export const Default: Story = {
    render: (args) => {
        return (
            <Collapsible side={args.side} open={args.open || undefined}>
                <Collapsible.Trigger style="align-self: center;">
                    <Collapsible.TriggerIcon />
                    I'm the trigger
                </Collapsible.Trigger>
                <Collapsible.Content>
                    <div>I'm the content!</div>
                    <div>I'm the content!</div>
                    <div>I'm the content!</div>
                    <div>I'm the content!</div>
                </Collapsible.Content>
            </Collapsible>
        )
    },
    args: {
        open: true,
        side: "left"
    }
}
