import { For, type JSXElement } from "solid-js";
import { Button } from "./ui/Button";
import "./SystemStatus.styl";
import sticky from "@src/directives/sticky";
import { Message, client } from "@src/debugger_client";
import { createPolledAsync } from "@src/utils/solid";

export interface SystemStatusProps {

}
export function SystemStatus(props: SystemStatusProps) {
    const txns = createPolledAsync(async (prev?:Message.TransactionInfo[]) => {
        // only refresh the dashboard if the debugger is visible.
        if(document.hidden) return prev;

        return (await client.send.list_transactions(20))?.transactions?.slice(0, 20)
    }, 10_000)

    return (
        <div class="system-status" use:sticky="mini">
            <SystemStatusTile label="System" status="ok" />
            <SystemStatusTile label="Schemas" status="error" />
            <SystemStatusTile label="Engines" status="ok" />
            <SystemStatusTile label="Transactions" status="ok" grow>
                <div class="transaction-dots">
                    <For each={txns()}>
                        {(txn) => <TransactionDot transaction={txn} />}
                    </For>
                </div>
            </SystemStatusTile>
        </div>
    )
}
export default SystemStatus;

export interface SystemStatusTileProps {
    label: string,
    status: string,
    class?: string,
    grow?: boolean
    children?: JSXElement
}
export function SystemStatusTile(props: SystemStatusTileProps) {
    return (
        <Button classList={{
            "system-status-tile": true,
            [`status-${props.status}`]: true,
            grow: props.grow,
            [props.class || ""]: !!props.class}}>

            <span class="tile-label">
                {props.label}
            </span>
            {props.children}
        </Button>
    )
}

export interface TransactionDotProps {
    transaction: Message.TransactionInfo
}
export function TransactionDot(props: TransactionDotProps) {
    return (
        <div class={`transaction-dot status-${props.transaction.state.toLowerCase()}`}>

        </div>
    )
}
