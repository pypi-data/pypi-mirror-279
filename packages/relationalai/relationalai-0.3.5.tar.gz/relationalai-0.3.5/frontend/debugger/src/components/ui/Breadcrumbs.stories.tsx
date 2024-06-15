import type {Meta, StoryObj} from "storybook-solidjs";
import {Breadcrumbs, BreadcrumbsItem} from "./Breadcrumbs";
import { For } from "solid-js";

const meta: Meta<typeof Breadcrumbs> = {
    component: Breadcrumbs,
}

export default meta;

type Story = StoryObj<typeof Breadcrumbs>;

export const Default: Story = {
    render: (args) => {
        return (
            <Breadcrumbs {...args}>
                <BreadcrumbsItem href="#/">
                    root
                </BreadcrumbsItem>
                <BreadcrumbsItem href="#/sub">
                    sub
                </BreadcrumbsItem>
                <BreadcrumbsItem href="#/sub/leaf">
                    leaf
                </BreadcrumbsItem>
            </Breadcrumbs>
        )
    },
    args: {
    }
}

