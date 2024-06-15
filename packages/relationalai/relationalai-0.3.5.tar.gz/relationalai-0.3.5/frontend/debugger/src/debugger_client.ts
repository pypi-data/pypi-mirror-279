import { Accessor, Setter, batch, createSignal } from "solid-js";
import { SetStoreFunction, createStore, produce, unwrap } from "solid-js/store";
import * as Mech from "./types/mech";
import { create_ws } from "./ws";

//------------------------------------------------------------------------------
// Utils
//------------------------------------------------------------------------------

export function get_in(root: Span, path: number[]) {
    let cur: Subject|undefined = root;
    for(let ix of path) {
        cur = cur?.events?.[ix];
    }
    return cur;
}

export interface Placeholder {
    "event": "placeholder",
    selection_path: number[],
    span_type?: undefined,
    events?: undefined
    parent?: undefined
}
export function is_placeholder(msg: any): msg is Placeholder {
    return typeof msg === "object" && msg.event === "placeholder";
}

export type Subject = Message.Event|Span|Placeholder;

//------------------------------------------------------------------------------
// Messages
//------------------------------------------------------------------------------

export namespace Message {
    export interface Base {
        event: string,
        selection_path: number[],
        timestamp: string,
        time: Date,
        span_type?: undefined,
        events?: undefined,
        parent_id?: string,
        parent?: Span
        [key: string]: unknown
    }
    
    export interface SpanStart extends Base {
        event: "span_start";
        span: {
            type: string;
            id: string;
            parent_id: string | null;
            start_timestamp: string;
            attrs: { [key: string]: any };
        };
    }
    export interface SpanEnd extends Base {
        event: "span_end",
        id: string;
        end_timestamp: string;
        end_attrs: { [key: string]: any };
    }

    export interface Time extends Base {
        event: "time",
        type: string,
        elapsed: number,
        results?: ResultData
        code?: string
    }
    export function is_time(msg: any): msg is Message.Time {
        return msg?.event === "time";
    }
    
    export interface ProfileEvent extends Base {
        event: "profile_event",
        // TODO: fill in more properties
    }
    export function is_profile_event(span: any): span is Message.ProfileEvent {
        return span.event === "profile_event";
    }

    export interface Error extends Base {
        event: "error",
        name: string,
        message: string,
        err: any,
        content: string,
        raw_content: string,
        source: Source
    }
    export function is_error(msg: any): msg is Message.Error {
        return msg?.event === "error";
    }

    export interface Warn extends Base {
        event: "warn",
        name: string,
        source: Source
        content: string
        raw_content: string
    }

    export function is_warn(span: any): span is Message.Warn {
        return span?.event === "warn";
    }

    export interface Compilation extends Base {
        event: "compilation",
        source: Source,
        passes: Pass[],
        emitted: string,
        emit_time: number,
        mech?: Mech.Machine,
        task?: string
    }
    export function is_compilation(msg: any): msg is Message.Compilation {
        return msg?.event === "compilation";
    }

    export interface TransactionCreated extends Base {
        event: "transaction_created",
        txn_id: string
    }
    export function is_transaction_created(msg: any): msg is Message.TransactionCreated {
        return msg?.event === "transaction_created";
    }

    export type Event = Time | Error | Compilation | TransactionCreated | Warn | ProfileEvent;

    export function is_event(msg: any): msg is Message.Event {
        return "event" in msg && !("span_type" in msg) && "time" in msg;
    }

    export interface Pass {
        name: string,
        task: string,
        elapsed: number
    }

    export interface Source {
        file: string,
        line: number,
        block: string,
        source: string | undefined
    }

    export interface ResultData {
        values: Record<string, any>[],
        count: number
    }

    export interface RPCResponse {
        event: "rpc_response"
        rpc_id: number
    }

    export interface ListTransactions extends RPCResponse {
        transactions: TransactionInfo[]
    }

    export interface TransactionInfo {
        id: string,
        state: string,
        created_by: string,
        created_on: number,
        finished_at: number,

        account?: string,
        agent?: string,
        database?: string,
        engine?: string,
        query?: string,
        read_only?: boolean,
        tags?: string[]
    }
}
export type Message =
    | Message.SpanStart
    | Message.SpanEnd
    | Message.Event
    | Message.RPCResponse

//------------------------------------------------------------------------------
// Spans
//------------------------------------------------------------------------------

export namespace Span {
    export interface Base {
        event: "span",
        parent?: Span,
        span_type: string,
        start_time: Date,
        end_time?: Date,
        elapsed?: number,
        selection_path: number[],

        events: (Span | Message.Event)[],

        last_dirty_clock?: number,
        [key: string]: unknown,
    }

    export function is_span(span: any): span is Span {
        return span?.event === "span" && Array.isArray(span.events);
    }

    export interface Program extends Base {
        span_type: "program",
        main: string,
        platform?: string,
    }

    export function is_program(span: any): span is Program {
        return is_span(span) && span.span_type === "program";
    }

    export interface RuleBatch extends Base {
        span_type: "rule_batch",
    }

    export function is_rule_batch(span: any): span is RuleBatch {
        return is_span(span) && span.span_type === "rule_batch";
    }

    export interface Block extends Base {
        span_type: "rule"|"query",
        task: string,
        mech: Mech.Machine
    }

    export function is_block(span: any): span is Block {
        return is_span(span) && (span.span_type === "rule" || span.span_type === "query"); //  && span?.name !== "pyrel_base"
    }

    export interface Rule extends Block {
        span_type: "rule"
    }

    export function is_rule(span: any): span is Rule {
        return is_span(span) && span.span_type === "rule";
    }

    export interface Query extends Block {
        span_type: "query",
        results?: Message.ResultData,
        errors?: any
    }

    export function is_query(span: Span|Message.Event): span is Query {
        return is_span(span) && span.span_type === "query";
    }
}
export type Span =
    | Span.Query
    | Span.Rule
    | Span.Base;

//------------------------------------------------------------------------------
// Client
//------------------------------------------------------------------------------

export class DebuggerClient {
    connection: Connection;
    messages: Accessor<Message[]>;
    protected set_messages: Setter<Message[]>;

    root: Span;
    protected set_root: SetStoreFunction<Span>;

    spans() {
        return this.root.events;
    }

    connected: Accessor<boolean>;
    protected set_connected: Setter<boolean>;

    protected path: number[] = [];
    protected open_spans: Span[] = [];

    latest: Accessor<Span.Program|undefined>;

    constructor(ws_url: string) {
        this.connection = new Connection(ws_url);
        [this.messages, this.set_messages] = createSignal<Message[]>([], {equals: () => false});
        [this.root, this.set_root] = createStore<Span>({
            event: "span",
            span_type: "root",
            span: [],
            start_time: new Date(0),
            events: [],
            selection_path: []
        });
        [this.connected, this.set_connected] = createSignal<boolean>(false, {equals: () => false});

        this.latest = () => this.spans().findLast(Span.is_program);

        this.connection.onreceive = this.handle_message;
        this.connection.onconnect = this.set_connected;
    }

    clear() {
        batch(() => {
            this.open_spans = [];
            this.set_messages([]);
            this.set_root({event: "span", span_type: "root", span: [], start_time: new Date(0), events: [], selection_path: []});
        });
        return this.send.clear();
    }

    exportData = () => {
        const data = JSON.stringify(unwrap(this.root));
        const blob = new Blob([data], {type: "application/json"});


        const a = document.createElement("a");
        const url = URL.createObjectURL(blob);
        a.href = url;
        a.download = "debugger_data.json";

        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
    }

    importData = (data: Span) => {
        this.set_root(data);
    }

    send = {
        clear: () => this._send({type: "clear"}),
        list_transactions: (limit = 20, only_active = false) => this._send<Message.ListTransactions>({type: "list_transactions", limit, only_active})
    }
    rpc_callbacks = new Map<number, (v: any) => any>()

    _next_rpc_id = 1;
    protected _send<T = any>(msg: any): Promise<T> {
        const rpc_id = msg.rpc_id = this._next_rpc_id++;
        this.connection.send(JSON.stringify(msg));

        return new Promise<T>((resolve, reject) => {
            this.rpc_callbacks.set(rpc_id, (response) => {
                if(response.status === "error") reject(response);
                else resolve(response);
                this.rpc_callbacks.delete(rpc_id)
            })
        });
    }

    protected get_open_span(id: string|null|undefined, within: Span, pop = false) {
        if(!id) return within;
        for(let ix = this.open_spans.length - 1; ix >= 0; ix -= 1) {
            let span = this.open_spans[ix];
            if(span.id === id) {
                if(pop) this.open_spans.splice(ix, 1);
                return get_in(within, span.selection_path);
            }
        }
    }

    protected handle_span_start(msg: Message.SpanStart) {
        this.set_root(produce((root) => {
            const parent = this.get_open_span(msg.span.parent_id, root);
            if(!parent || !Span.is_span(parent)) {
                throw new Error(`Parent '${msg.span.parent_id}' not found for span '${msg.span.id}'`);
            }
            let sub: Span = {
                ...msg.span.attrs,
                id: msg.span.id,
                start_time: new Date(msg.span.start_timestamp),
                end_time: undefined,
                span_type: msg.span.type,
                event: "span",
                selection_path: [...parent.selection_path, parent.events.length],
                events: []
            };
            this.open_spans.push(sub);
            Object.defineProperty(sub, "parent", {value: unwrap(parent), enumerable: false, configurable: true, writable: true});
            parent.events.push(sub)
        }));
    }

    protected handle_span_end(msg: Message.SpanEnd) {
        this.set_root(produce((root) => {
            let start = this.get_open_span(msg.id, root, true);
            if(!start || !Span.is_span(start)) throw new Error(`Open span not found for close '${msg.id}'`);
            start.end_time = new Date(msg.end_timestamp);
            start.elapsed = (start.end_time.getTime() - start.start_time.getTime());
            
            for (let key in msg.end_attrs) {
                if (key === "span" || key === "event") continue;
                start[key] = msg[key];
            }
        }));
    }

    protected handle_event(msg: Message.Event) {
        this.set_root(produce((root) => {
            const span = this.get_open_span(msg.parent_id, root);
            if(!span || !Span.is_span(span)) {
                throw new Error(`Parent '${msg.parent_id}' not found for event '${msg.event}'`);
            }
            msg.time = new Date(msg.timestamp);
            msg.selection_path = [...span.selection_path, span.events.length];
            Object.defineProperty(msg, "parent", {value: unwrap(span), enumerable: false, configurable: true, writable: true});
            span.events.push(msg);
        }));
    }

    protected handle_rpc_response(msg: Message.RPCResponse) {
        const callback = this.rpc_callbacks.get(msg.rpc_id);
        if(!callback) throw new Error(`Got RPC response for unsent RPC: ${msg.rpc_id}`);
        callback(msg);
    }

    protected handle_single_message = (msg: Message) => {
        if(msg.event === "span_start") this.handle_span_start(msg)
        else if(msg.event === "span_end") this.handle_span_end(msg)
        else if(msg.event === "rpc_response") this.handle_rpc_response(msg)
        else this.handle_event(msg);
    }

    protected handle_message = (msgs: Message[]) => {
        batch(() => {
            for(let msg of msgs) {
                this.handle_single_message(msg)
            }

            this.set_messages((prev) => {
                for(let msg of msgs) {
                    prev.push(msg);
                }
                return prev;
            });
        });
    }
}

//------------------------------------------------------------------------------
// Connection
//------------------------------------------------------------------------------

export class Connection {
    private socket: WebSocket | null = null;
    private shouldReconnect = true;
    private active = false;

    ws_url: string;
    reconnectInterval: number;
    onreceive?: (msg: any) => void;
    onconnect?: (is_connected: boolean) => void;
    buffered_sends: any[] = [];

    constructor(ws_url: string, reconnectInterval: number = 1_000) {
        this.ws_url = ws_url;
        this.reconnectInterval = reconnectInterval;
        this.connect();
    }

    private connect(): void {
        // @NOTE: I wasted an hour trying to figure out how to suppress the default error message and then gave up.
        this.socket = create_ws(this.ws_url);

        this.socket.addEventListener("open", () => {
            this.active = true;
            this.onconnect?.(true);
            for(let msg of this.buffered_sends) {
                this.send(msg);
            }
            this.buffered_sends = [];
        });

        this.socket.addEventListener("message", (event) => {
            let msg;
            try {
                msg = JSON.parse(event.data);
            } catch (err: any) {
                console.warn("Failed to parse message:", event.data);
            }
            if(msg.event === "span_end" && msg.span?.length === 1 && msg.span[0] === "program") {
                this.active = false;
            }
            this.onreceive?.(msg);
        });

        this.socket.addEventListener("close", () => {
            this.onconnect?.(false);
            if(this.active) {
                console.warn("Disconnected unexpectedly from the WebSocket server");
                this.active = false;
            }

            if (this.shouldReconnect) {
                setTimeout(() => this.connect(), this.reconnectInterval);
            }
        });

        this.socket.addEventListener("error", (event) => {
            if (this.socket) {
                this.socket.close();
            }
        });
    }

    public send(msg: string|ArrayBufferLike|Blob|ArrayBufferView) {
        if(this.active) {
            this.socket?.send(msg);
        } else {
            this.buffered_sends.push(msg);
        }
    }

    public disconnect() {
        if (this.socket) {
            this.socket.close();
        }
    }

    public close(): void {
        this.shouldReconnect = false;
        this.disconnect();
    }
}

export const client = new DebuggerClient(`ws://${location.host}/ws/client`);

(globalThis as any).client = client;
