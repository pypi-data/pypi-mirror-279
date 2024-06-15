import { Show, createEffect, createSignal, untrack } from "solid-js";
import { EventListSelection, Selection } from "./Selection";
import { EventList } from "./components/EventList";
import { Button } from "./components/ui/Button";
import { Field, Format } from "./components/ui/Field";
import { Icon } from "./components/ui/Icon";
import { Modal } from "./components/ui/Modal";
import { Tooltip } from "./components/ui/Tooltip";
import { FileDropZone } from "./components/FileDropZone";
import { client, get_in, is_placeholder, type Subject } from "./debugger_client";
import "./App.styl";
import { SystemStatus } from "./components/SystemStatus";
import Logo from "./logo.svg";
import { begin_auto_scroll, set_auto_scroll_enabled, auto_scroll_enabled } from "./utils/solid";

function App() {
    const event_list_selection = new Selection<Subject>("EventList");

    const clear = () => {
        event_list_selection.clear()
        client.clear();
    };

    const exportData = () => {
        client.exportData();
	};

    const handleFileDrop = (jsonObjects: any[]) => {
        clear();
        client.importData(jsonObjects[0]);
    }

    const program_running = () => client.latest() && !client.latest()?.end_time;

    const [pinned, set_pinned] = createSignal<boolean>(true);

    // If we're pinned when a new program starts:
    // replace the current selections with placeholders for their equivalents in the new program
    createEffect((prev_run_count: number|undefined) => {
        const cur_run_count = client.spans().length;
        if (!pinned() || cur_run_count === prev_run_count) return cur_run_count;

        for (let selected of untrack(() => event_list_selection.selected())) {
            if (is_placeholder(selected)) continue;
            event_list_selection.remove(selected);
            event_list_selection.add({ event: "placeholder", selection_path: [cur_run_count - 1, ...selected.selection_path.slice(1)] })
        }
        return cur_run_count;
    });

    // When a new message comes in:
    // Replace any selected placeholders with the actual event if possible
    createEffect((prev_message_count: number|undefined) => {
        const cur_message_count = client.messages().length;
        if(cur_message_count === prev_message_count) return cur_message_count;

        for (let selected of untrack(() => event_list_selection.selected())) {
            if (!is_placeholder(selected)) continue;

            let available = get_in(client.root, selected.selection_path);
            if(available) {
                event_list_selection.remove(selected);
                event_list_selection.add(available);
            }
        }

        return cur_message_count
    });

    // If auto scroll is enabled when a new message comes in:
    // Attempt to scroll to the bottom to keep it in view
    createEffect((prev_message_count: number | undefined) => {
        const cur_message_count = client.messages().length;
        if (cur_message_count === prev_message_count) return cur_message_count;

        if (auto_scroll_enabled()) {
            begin_auto_scroll()
        }
        return cur_message_count
    })

    // If we open/close a group while auto scroll is enabled:
    // disable auto scrolling until the user re-docks to bottom
    createEffect(() => {
        event_list_selection.selected();
        set_auto_scroll_enabled(false);
    });

    return (
        <EventListSelection.Provider value={event_list_selection}>
            <FileDropZone onFileDrop={handleFileDrop}>
                <div class="app">
                    <header>
                        <Logo />
                        <span style="flex: 1" />
                        <div class="hidden-controls">
                            <Button class="icon" onclick={clear} tooltip={program_running() ? "cannot clear events while program is running" : "clear events"} disabled={program_running()}>
                                <Icon name="ban" />
                            </Button>
                            <Button class="icon" tooltip="Follow last run" onclick={() => set_pinned(v => !v)}>
                                <Icon name="pin" type={pinned() ? "filled" : "outline"} />
                            </Button>


                            <Button class="icon" tooltip="Export events" onclick={exportData}>
                                <Icon name="download" />
                            </Button>

                            <Modal title="Settings" content={<Settings />}>
                                <Modal.Trigger as={Button} class="icon" tooltip="settings">
                                    <Icon name="settings" />
                                </Modal.Trigger>
                            </Modal>
                        </div>

                        <Status />
                    </header>
                    <SystemStatus />
                    <EventList events={client.spans()} />

                </div>
            </FileDropZone>
        </EventListSelection.Provider>
    );
};

export default App;

function Status() {
    return (
        <Tooltip content={client.connected() ? "Connected to program" : "Disconnected from program"}>
            <Tooltip.Trigger as="status-icon">
                <Show when={client.connected()} fallback={<Icon name="antenna-bars-off" />}>
                    <Icon name="antenna-bars-5" />
                </Show>
            </Tooltip.Trigger>
        </Tooltip>
    )
}


function Settings() {
    return (
        <>
            <section>
                <h3>Connection</h3>
                <Field.Number label="Polling Interval" formatOptions={Format.seconds} minValue={1}
                    defaultValue={client.connection.reconnectInterval / 1000}
                    onRawValueChange={(v) => client.connection.reconnectInterval = v * 1000} />
                <Field.Text label={"Debug URL"} placeholder={"ws://localhost:1234"}
                    defaultValue={client.connection.ws_url} onChange={(v) => {
                        client.connection.ws_url = v
                        client.connection.disconnect();
                    }} />
            </section>

        </>
    )
}

