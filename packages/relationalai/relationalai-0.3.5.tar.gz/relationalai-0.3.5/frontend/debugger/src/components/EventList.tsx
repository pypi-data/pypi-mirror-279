import { Message, Span, client, type Subject } from "@src/debugger_client"
import { Component, For, Show, createEffect, createMemo, createSignal, untrack, useContext, type JSXElement } from "solid-js"
import { Collapsible } from "./ui/Collapsible";
import { EventListSelection } from "@src/Selection";
import { Dynamic } from "solid-js/web";
import { CodeBlock } from "./ui/Code";
import "./EventList.styl";
import { prefix_of } from "@src/util";
import { Icon } from "./ui/Icon";
import * as format from "@src/utils/format";
import { createTimeDifferenceFromNow } from "@solid-primitives/date";
import {GradientPath} from "gradient-path";
import { Button } from "./ui/Button";
import { Alert } from "./Alert";
import { classy } from "@src/utils/solid";


function create_elapsed(subject: Subject) {
    if (Span.is_span(subject)) {
        if (subject.elapsed) {
            return () => subject.elapsed!;
        } else {
            const [time_since_start] = createTimeDifferenceFromNow(subject.start_time, 100);
            return () => subject.elapsed ?? -time_since_start();
        }
    }
    return () => undefined;
}

//------------------------------------------------------------------------------
// EventList
//------------------------------------------------------------------------------

export interface EventListProps {
    events: (Message.Event | Span)[],
    depth?: number
}
export function EventList(props: EventListProps) {
    return (
        <div class={`event-list ${props.depth ? "sub" : ""}`}>
            <Show when={!props.depth}>
                <EventListSVGDefs />
            </Show>
            <For each={props.events}>
                {(event) => <EventListItem event={event} depth={props.depth ?? 0} />}
            </For>
        </div>
    )
}

// Interface all event items adhere to
export interface EventItemProps<T extends Subject = Subject> {
    event: T,
    depth: number
}

// Dynamically dispatch events to the appropriate component for rendering them
export function EventListItem(props: EventItemProps) {
    const component = (() => {
        const event = props.event;
        if (Span.is_program(event)) return EventItemProgram;
        if (Span.is_block(event)) return EventItemBlock;
        if (Span.is_rule_batch(event)) return EventItemRuleBatch;
        if (Span.is_span(event) && event.span_type === "transaction") return EventItemTransaction;
        if (Span.is_span(event) && event.span_type === "install_batch") return EventItemInstall;
        if (Message.is_error(event) || Message.is_warn(event)) return EventItemAlert;
        if (Message.is_time(event) && event.results) return EventItemResults;
        if (Span.is_span(event)) return EventItemUnknownSpan;

    }) as () => Component<EventItemProps>;
    return (
        <Dynamic component={component()} event={props.event} depth={props.depth} />
    )
}

function EventItemUnknownSpan(props: EventItemProps<Span>) {
    return (
        <For each={props.event.events}>
            {(child) => <EventListItem event={child} depth={props.depth} />}
        </For>
    )
}

//------------------------------------------------------------------------------
// Icons
//------------------------------------------------------------------------------

interface EventNodeIconProps {
    radius: number
    running?: boolean
    multi?: number
}
function EventNodeIcon(props: EventNodeIconProps) {
    let progress_group!: SVGGElement;
    let p3!: SVGCircleElement;
    const viewbox = () => {
        const r = props.radius;
        const d = r * 2;
        return `-${r} -${r} ${d} ${d}`;
    }
    const multi = () => props.multi || 0;

    createEffect((prev: any) => {
        if (props.running && p3 && !prev) {
            const style = getComputedStyle(p3);
            const stops = [
                style.getPropertyValue("--stop-1"),
                style.getPropertyValue("--stop-2"),
                style.getPropertyValue("--stop-3"),
            ];
            const gp = new GradientPath({
                path: p3,
                segments: 36,
                samples: 12,
            });
            let res = gp.render({
                type: "path",
                stroke: [
                    { color: stops[0], pos: 0 },
                    { color: stops[1], pos: 0.5 },
                    { color: stops[2], pos: 1 }
                ],
                strokeWidth: 1
            });
            res.group.classList.add("spinner");
            progress_group.appendChild(res.group);
            return res;
        }
        return prev;
    })
    return (
        <svg class={`event-icon ${props.running ? "running" : ""}`} style={`--base-radius: ${props.radius}px`} viewBox={viewbox()} vector-effect="non-scaling-stroke">
            <Show when={multi() > 1}>
                <g class="multi">
                    <Show when={multi() > 1}><circle /></Show>
                    <Show when={multi() > 2}><circle /></Show>
                    <Show when={multi() > 3}><circle /></Show>
                </g>
            </Show>

            <circle class="node" />

            <Show when={props.running}>
                <g ref={progress_group} class="in-progress">
                    <circle class="reflection" />
                    <circle ref={p3} class="spinner" />
                </g>
            </Show>
        </svg>
    )
}

//------------------------------------------------------------------------------
// Group Items
//------------------------------------------------------------------------------

// base component used by other groups to implement shared behavior.
interface EventGroupProps<T extends Span = Span> extends EventItemProps<T> {
    class?: string;
    children?: JSXElement;
    open?: boolean;
    multi?: number;
}
export function EventGroup<T extends Span>(props: EventGroupProps<T>) {
    const selection = useContext(EventListSelection);
    const is_selected = () => selection.is_selected(props.event);
    const contains_selection = () => !!selection.selected().find(item => prefix_of(item.selection_path, props.event.selection_path));
    const running = () => !props.event.end_time;
    const elapsed = create_elapsed(props.event);

    const radius = () => Math.max(20 - props.depth * 4, 8);

    const [open, set_open] = createSignal(contains_selection() || props.open);
    const onclick = (v: boolean) => {
        selection?.toggle(props.event, v);
        set_open(v);
    }

    createEffect(() => {
        let should_be_open = contains_selection();
        if (untrack(() => open()) !== should_be_open && untrack(() => selection.selected().length)) {
            set_open(should_be_open);
        }
    });

    const klass = () => classy("event-list-item", props.event.event, props.event.span_type, props.class, { running: running(), selected: is_selected() });
    const style = () => {
        return {
            "--node-height": `${2 * radius()}px`
        }
    }

    return (
        <Collapsible side="top" open={open()} onOpenChange={onclick} class={klass()} style={style()} data-depth={props.depth}>
            <Collapsible.Trigger as="header">
                <div class="event-before">
                    <div class="event-time">
                        {format.time(props.event.start_time)}
                    </div>
                    <div class="event-duration">
                        {format.duration(elapsed()!)}
                    </div>
                </div>
                <EventNodeIcon radius={radius()} running={running()} multi={props.multi} />
                {props.children}
            </Collapsible.Trigger>
            <Collapsible.Content>
                <EventList events={props.event.events} depth={props.depth + 1} />
            </Collapsible.Content>
        </Collapsible>
    );
}

export function EventItemProgram(props: EventItemProps<Span.Program>) {
    const rule_count = () => props.event.events.filter(Span.is_rule_batch).reduce((sum: number, batch) => sum + batch.events.filter(Span.is_rule).filter((e) => e.name !== "pyrel_base").length, 0);
    const query_count = () => props.event.events.filter(Span.is_query).length;

    return (
        <EventGroup {...props} open={props.event === client.latest()}>
            <span class="event-after">
                <span class="event-detail">
                    <span class="event-label">
                        {props.event.main}
                    </span>
                    <Value value={rule_count()} unit="rule" />
                    <span class="sep">/</span>
                    <Value value={query_count()} unit="query" />
                </span>
            </span>
        </EventGroup>
    )
}

export function EventItemBlock(props: EventItemProps<Span.Block>) {
    if(props.event.name === "pyrel_base") return;
    const compilation = () => props.event.events.find(Message.is_compilation);

    return (
        <EventGroup {...props} class="block">
            <div class="event-after">
                <Show when={compilation()}>
                    <BlockSourceInfo event={compilation()} />
                </Show>
            </div>
        </EventGroup>
    )
}

export function EventItemRuleBatch(props: EventItemProps<Span>) {
    const rule_count = () => props.event.events.filter(Span.is_rule).filter((e) => e.name !== "pyrel_base").length;

    return (
        <EventGroup {...props} multi={rule_count()}>
            <div class="event-after">
                <span class="event-detail">
                    <Value value={rule_count()} unit="rule" />
                </span>
            </div>
        </EventGroup>
    )
}

//------------------------------------------------------------------------------
// Leaf Items
//------------------------------------------------------------------------------

// Base component used by other leaf events to implement shared behavior.
interface EventLeafProps<T extends Subject = Subject> extends EventItemProps<T> {
    class?: string;
    children?: JSXElement;
}
export function EventLeaf(props: EventLeafProps<Subject>) {
    const selection = useContext(EventListSelection);
    const is_selected = () => selection.is_selected(props.event);

    const time = () => {
        const event = props.event;
        if(Span.is_span(event)) return event.start_time;
        if(Message.is_event(event)) return event.time;
    }
    const running = () => Span.is_span(props.event) && !props.event.end_time;
    const elapsed = create_elapsed(props.event);
    const radius = () => Math.max(20 - props.depth * 4, 8)

    const klass = () =>
		classy(
			"event-list-item leaf",
			props.event.event,
			props.event.span_type,
			props.class,
			{ running: running(), selected: is_selected() }
		);

    const style = () => {
        return {
            "--node-height": `${2 * radius()}px`
        }
    }

    const collectImportantEvents = (span: Span): (Message.Error | Message.Warn)[] => {
        const importantEvents: (Message.Error | Message.Warn)[] = [];
        
        const walkEvents = (events: (Span | Message.Event)[]) => {
            for (const event of events) {
                if (Span.is_span(event)) {
                    walkEvents(event.events);
                } else if (Message.is_error(event) || Message.is_warn(event)) {
                    importantEvents.push(event);
                }
            }
        };

        walkEvents(span.events);
        return importantEvents;
    };

    const importantEvents = createMemo(() => {
        if (Span.is_span(props.event)) {
            return collectImportantEvents(props.event);
        }
        return [];
    });

    const hasImportantEvents = importantEvents().length > 0;

    return (
        <>
            <div  class={classy(klass(), { 'has-important-events': hasImportantEvents })}  style={style()}>
                <div class="event-before">
                    <Show when={time()}>
                        <div class="event-time">
                            {format.time(time()!)}
                        </div>
                    </Show>
                    <Show when={elapsed()}>
                        <div class="event-duration">
                            {format.duration(elapsed()!)}
                        </div>
                    </Show>
                </div>
                <EventNodeIcon radius={radius()} />
                {props.children}
            </div >
            <For each={importantEvents()}>
                {(event) =>
                    <EventListItem event={event} depth={props.depth} />
                }
            </For>
        </>
    );
}


export function EventItemAlert(props: EventItemProps<Message.Warn | Message.Error>) {
	return (
		<EventLeaf {...props}>
			<div class="event-after">
				<span class="event-detail">
					<Alert {...props.event} />
				</span>
			</div>
		</EventLeaf>
	);
}

export function EventItemResults(props: EventItemProps<Message.Time>) {
    const results = () => props.event.results!;
    return (
        <EventLeaf {...props} class="query_results">
            <div class="event-after">
                <h3>Results ({results()?.values.length} / {results()?.count})</h3>
                <table>
                    <thead>
                        <tr>
                            <For each={Object.keys(results()?.values[0] ?? {})}>
                                {(key) => <td>{key}</td>}
                            </For>
                        </tr>
                    </thead>
                    <tbody>
                        <For each={results()?.values}>
                            {(row) => (
                                <tr>
                                    <For each={Object.entries(row)}>
                                        {([key, value]) => <td>{value}</td>}
                                    </For>
                                </tr>
                            )}
                        </For>
                    </tbody>
                </table>
            </div>
        </EventLeaf>
    )
}

export function EventItemTransaction(props: EventItemProps<Span>) {
    const txn_id = () => props.event.events.find(Message.is_transaction_created)?.txn_id;

    return (
        <Show when={txn_id()}>
            <EventLeaf {...props} class="transaction"> {/* @FIXME: is this class still needed? */}
                <div class="event-after">
                    <span class="event-detail">
                        <TransactionInfo event={props.event} />
                    </span>
                </div>
            </EventLeaf>
        </Show>
    )
}

export function EventItemInstall(props: EventItemProps<Span>) {
    const txn = () => props.event.events.find((event) => event.span_type === "transaction") as Span|undefined

    return (
        <EventLeaf {...props}>
            <div class="event-after">
                <div>installing new rules</div>
                <div class="event-detail">
                    <TransactionInfo event={txn()!} />
                </div>
            </div>
        </EventLeaf>
    )
}

//------------------------------------------------------------------------------
// Info components embedded in other nodes
//------------------------------------------------------------------------------

export interface InfoProps<T extends Subject> {
    event?: T
}

export function TransactionInfo(props: InfoProps<Span>) {
    const txn_id = () => props.event?.events.find(Message.is_transaction_created)?.txn_id;
    // @TODO: program should probably just be in a context above all this
    const program = () => {
        let cur = props.event?.parent;
        while (cur && !Span.is_program(cur)) {
            cur = cur.parent;
        }
        return cur;
    }
    const logs_url = () => `https://app.datadoghq.com/logs?query=%40rai.transaction_id%3A${txn_id()}&from_ts=${program()?.start_time.getTime()}&live=false`;
    return (
        <Show when={props.event}>
            <label>Transaction</label> <span class="subtle">{txn_id()}</span>
            <Show when={logs_url()}>
                <Button class="icon" as="a" href={logs_url()} target="_blank">
                    <Icon name="external-link" />
                </Button>
            </Show>
        </Show>
    )
}

export function BlockSourceInfo(props: InfoProps<Message.Compilation>) {
    let source = () => props.event?.source;

    return (
        <Show when={source()?.block}>
            <div class="compilation">
                <header>
                    <Show when={source()?.file}>
                        <span class="event-detail">
                            # {source()?.file}:{source()?.line}
                        </span>
                    </Show>
                </header>
                <CodeBlock lang="python" dense no_copy>
                    {source()?.block}
                </CodeBlock>
            </div>
        </Show>
    )
}

export interface ValueProps {
    value: number,
    unit: string,
    fmt?: (v: number) => string
}
export function Value(props: ValueProps) {
    const formatted = () => props.fmt ? props.fmt(props.value) : props.value;
    const pluralized_unit = () => props.value === 1 ? props.unit : plural(props.unit);
    return (<>
        <span class="value">
            {formatted()}
        </span>
        <span class="unit">
            {pluralized_unit()}
        </span>
    </>)
}

function plural(word: string) {
    if(word.endsWith("y")) return word.slice(0, -1) + "ies";
    return word + "s";
}

//------------------------------------------------------------------------------
// SVG Defs
//------------------------------------------------------------------------------

export function EventListSVGDefs() {
    return (
        <svg id="event-list-svg-defs">
            <linearGradient id="node-default" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" />
                <stop offset="100%" />
            </linearGradient>
            <linearGradient id="node-error" x1="0%" y1="0%" x2="75%" y2="75%">
                <stop offset="0%" />
                <stop offset="100%" />
            </linearGradient>
            <linearGradient id="node-warn" x1="0%" y1="0%" x2="75%" y2="100%">
                <stop offset="0%" />
                <stop offset="100%" />
            </linearGradient>
            <radialGradient id="node-reflection" cx="80%" cy="50%" r="33%">
                <stop offset="0%" />
                <stop offset="15%" />
                <stop offset="45%" />
                <stop offset="100%" />
            </radialGradient>
        </svg>
    )
}
